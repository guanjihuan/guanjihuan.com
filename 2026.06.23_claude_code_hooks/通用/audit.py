# This code is supported by the website: https://www.guanjihuan.com
# The newest version of this code is on the web page: https://www.guanjihuan.com/archives/49203

#!/usr/bin/env python3
"""Audit hook for Claude Code — Linux port of audit.ps1.

Reads an event name as argv[1] and a JSON payload on stdin, then mutates a
daily JSON log under $CLAUDE_AUDIT_LOG_DIR (default ~/claude/logs). Cross-process
safety is provided by an fcntl flock on a per-log-dir lock file (replaces the
Windows named mutex in the original). All event handlers and the StatusLine
behaviour are kept 1:1 with the PowerShell source.
"""

import fcntl
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path


# --- Config ---

LOG_DIR = Path(os.environ.get(
    'CLAUDE_AUDIT_LOG_DIR',
    os.path.expanduser('~/claude/logs'),
))
LOG_FILE = LOG_DIR / f"{datetime.now():%Y-%m-%d}.json"
ERROR_LOG = LOG_DIR / 'audit-error.log'
MUTEX_TIMEOUT_MS = 5000

STATUS_RUNNING = 'running'
STATUS_AWAITING_USER = 'awaiting_user'
STATUS_COMPLETED = 'completed'
STATUS_STOPPED = 'stopped'
IN_PROGRESS_STATUSES = (STATUS_RUNNING, STATUS_AWAITING_USER)

KNOWN_EVENTS = (
    'SessionEnd', 'UserPromptSubmit', 'PreToolUse',
    'PostToolUse', 'PermissionRequest', 'Stop', 'StatusLine',
)

# Per-invocation cache for transcript model lookup.
_model_cache_path = None
_model_cache_mtime = None
_model_cache_value = None


# --- Error / IO helpers ---


def write_err(msg, stage):
    """Append a timestamped line to the error log; never raise."""
    try:
        line = f"{datetime.now().isoformat()} [{stage}] {msg}"
        with open(ERROR_LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass


def read_stdin_json():
    """Read and parse JSON from stdin. Returns None on empty/invalid input."""
    try:
        raw = sys.stdin.read()
        if raw and raw.strip():
            return json.loads(raw)
    except Exception as e:
        write_err(f'stdin_parse_failed: {e}', 'parse')
    return None


def get_property(obj, name):
    """dict.get() / getattr() shim matching the PSObject property accessor."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def write_status_line(line):
    sys.stdout.write(line + '\n')
    sys.stdout.flush()


# --- Model helpers ---


def test_concrete_model(model):
    """A model name is 'concrete' if it's a non-empty string not in the
    placeholder set (auto/default/unknown/null)."""
    if not model or not isinstance(model, str) or not model.strip():
        return False
    return model.strip().lower() not in ('auto', 'default', 'unknown', 'null')


def get_model_name(value):
    """Pull a model identifier out of either a string or an object with one
    of the well-known field names. Returns the first concrete match, falling
    back to the first non-empty text or str(value)."""
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()

    fallback = None
    if isinstance(value, dict):
        for name in ('id', 'model', 'name', 'display_name'):
            model = get_property(value, name)
            if not model:
                continue
            text = str(model).strip()
            if not fallback:
                fallback = text
            if test_concrete_model(text):
                return text
    if fallback:
        return fallback
    return str(value).strip()


def get_model_from_payload(payload):
    if not payload:
        return None
    model = get_model_name(get_property(payload, 'model'))
    if test_concrete_model(model):
        return model
    return None


def get_model_from_environment():
    for name in ('ANTHROPIC_MODEL', 'CLAUDE_MODEL', 'ANTHROPIC_SMALL_FAST_MODEL'):
        model = os.environ.get(name)
        if test_concrete_model(model):
            return model.strip()
    return None


def get_model_from_transcript(path):
    """Walk a Claude Code transcript JSONL file backwards to find the most
    recent assistant message that carries a concrete model name. Cached by
    (path, mtime) for the lifetime of this invocation."""
    global _model_cache_path, _model_cache_mtime, _model_cache_value
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        mtime = p.stat().st_mtime
        if _model_cache_path == str(p) and _model_cache_mtime == mtime:
            return _model_cache_value

        with open(p, 'r', encoding='utf-8') as f:
            raw = f.read()
        if not raw.strip():
            return None

        for line in reversed(raw.splitlines()):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            if obj.get('type') != 'assistant':
                continue
            msg = obj.get('message')
            if isinstance(msg, dict) and msg.get('model'):
                _model_cache_path = str(p)
                _model_cache_mtime = mtime
                _model_cache_value = msg['model']
                return _model_cache_value
    except Exception as e:
        write_err(f'transcript_model_read_failed: {e}', 'transcript')
    return None


def get_model_from_payload_or_transcript(payload):
    if payload:
        transcript_path = get_property(payload, 'transcript_path')
        if transcript_path:
            model = get_model_from_transcript(str(transcript_path))
            if test_concrete_model(model):
                return model

        model = get_model_from_payload(payload)
        if test_concrete_model(model):
            return model

    return get_model_from_environment()


def update_prompt_model(prompt, payload):
    """If the prompt has no concrete model, fill it in from payload/transcript/
    env. Mutates prompt in place. Returns True iff it changed."""
    if not prompt:
        return False
    if test_concrete_model(str(prompt.get('model'))):
        return False
    model = get_model_from_payload_or_transcript(payload)
    if test_concrete_model(model):
        prompt['model'] = model
        return True
    return False


# --- Log IO ---


def read_log(path=None):
    """Read the log file and return its sessions as a list of dicts."""
    p = Path(path) if path else LOG_FILE
    if not p.exists():
        return []
    try:
        with open(p, 'r', encoding='utf-8') as f:
            raw = f.read()
        if not raw.strip():
            return []
        data = json.loads(raw)
        if data is None:
            return []
        if isinstance(data, list):
            return data
        return [data]
    except Exception as e:
        write_err(f'log_read_failed: {e}', 'read')
        return []


def write_log(sessions, path=None):
    """Atomically write the sessions array as pretty JSON. Validates the
    output by re-parsing before swapping the temp file into place."""
    p = Path(path) if path else LOG_FILE
    tmp = p.with_name(f'{p.name}.tmp.{os.getpid()}')
    try:
        items = list(sessions) if sessions else []
        if not items:
            json_text = '[]'
        else:
            json_items = [json.dumps(s, ensure_ascii=False, indent=2) for s in items]
            json_text = '[\n' + ',\n'.join(json_items) + '\n]'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(json_text)
        with open(tmp, 'r', encoding='utf-8') as f:
            json.loads(f.read())
        os.replace(tmp, p)
        return True
    except Exception as e:
        write_err(f'log_write_failed: {e}', 'write')
        try:
            tmp.unlink()
        except Exception:
            pass
        return False


# --- Session / prompt state ---


def find_session(sessions, sid):
    if not sid:
        return None
    for s in sessions:
        if str(s.get('session_id')) == sid:
            return s
    return None


def find_last_in_progress(sessions, sid):
    """Last prompt (by list order) whose status is still running or
    awaiting_user. Mirrors the original's 'keep overwriting $last' loop."""
    session = find_session(sessions, sid)
    if not session or not session.get('prompts'):
        return None

    last = None
    for p in session['prompts']:
        if str(p.get('status')) in IN_PROGRESS_STATUSES:
            last = p
    return last


def complete_prompt(prompt, now):
    if not prompt or str(prompt.get('status')) not in IN_PROGRESS_STATUSES:
        return False
    prompt['status'] = STATUS_COMPLETED
    prompt['end_time'] = now
    prompt['duration'] = get_duration_hms(str(prompt.get('start_time')), now)
    return True


def stop_prompt(prompt, now):
    if not prompt or str(prompt.get('status')) not in IN_PROGRESS_STATUSES:
        return False
    prompt['status'] = STATUS_STOPPED
    prompt['end_time'] = now
    prompt['duration'] = get_duration_hms(str(prompt.get('start_time')), now)
    return True


def invoke_yesterday_cleanup():
    """Mark any in-progress prompts in yesterday's log as stopped with
    end_time = 23:59:59. Idempotent: stop_prompt returns False on done prompts."""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_file = LOG_DIR / f'{yesterday}.json'
    if not yesterday_file.exists():
        return
    try:
        y_sessions = read_log(yesterday_file)
        convert_prompt_lists(y_sessions)
        y_end = f'{yesterday} 23:59:59'
        cleanup_changed = False
        for s in y_sessions:
            for p in s.get('prompts') or []:
                if stop_prompt(p, y_end):
                    cleanup_changed = True
        if cleanup_changed:
            write_log(y_sessions, yesterday_file)
    except Exception as e:
        write_err(f'yesterday_cleanup_failed: {e}', 'cleanup')


def get_duration_hms(start, end):
    """Format a duration as HH:MM:SS, floor-zero on negative deltas."""
    if not start or not end:
        return None
    try:
        fmt = '%Y-%m-%d %H:%M:%S'
        s = datetime.strptime(start, fmt)
        e = datetime.strptime(end, fmt)
        delta = e - s
        if delta.total_seconds() < 0:
            return '00:00:00'
        total_seconds = int(delta.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        sec = total_seconds % 60
        return f'{h:02d}:{m:02d}:{sec:02d}'
    except Exception as e:
        write_err(f"duration_parse_failed start='{start}' end='{end}': {e}", 'duration')
        return None


def truncate(text, length):
    if not text or len(text) <= length:
        return text
    return text[:length]


def get_short_model(model):
    """Compact model label: strip 'claude-' prefix, join first 3 dash/slash
    parts, cap at 12 chars."""
    if not model or not isinstance(model, str) or not model.strip():
        return ''
    short = re.sub(r'^claude-', '', model.strip())
    parts = re.split(r'[-/]', short)
    short = '-'.join(parts[:3])
    if len(short) > 12:
        short = short[:12]
    return short


def convert_prompt_lists(sessions):
    """Ensure each session has a real list at .prompts (always true for
    json.loads output, but kept for parity with the PS version)."""
    for s in sessions:
        if not isinstance(s, dict):
            continue
        prompts = []
        if s.get('prompts'):
            for p in s['prompts']:
                prompts.append(p)
        s['prompts'] = prompts


# --- Main ---


def acquire_lock(lock_path, timeout_ms):
    """Try to acquire an exclusive flock within timeout_ms. Returns
    (fd, acquired). fd is left open on success so the lock stays held."""
    fd = open(lock_path, 'w')
    deadline = time.monotonic() + timeout_ms / 1000.0
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd, True
        except (BlockingIOError, OSError):
            if time.monotonic() >= deadline:
                return fd, False
            time.sleep(0.05)


def release_lock(fd):
    if fd is None:
        return
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        fd.close()
    except Exception:
        pass


def handle_status_line(payload):
    try:
        sessions = read_log()
        sid = str(get_property(payload, 'session_id')) if payload else None
        session = find_session(sessions, sid) if sid else None

        if not session and sessions:
            for i in range(len(sessions) - 1, -1, -1):
                if find_last_in_progress(sessions, str(sessions[i].get('session_id'))):
                    session = sessions[i]
                    break

        if not session and sessions:
            for i in range(len(sessions) - 1, -1, -1):
                if sessions[i].get('prompts'):
                    session = sessions[i]
                    break

        if not session:
            write_status_line('· idle')
            return

        prompt = find_last_in_progress(sessions, str(session.get('session_id')))
        if not prompt and session.get('prompts'):
            prompt = session['prompts'][-1]

        if not prompt:
            write_status_line('· idle')
            return

        status = str(prompt.get('status'))
        if status == STATUS_RUNNING:
            glyph = '*'
        elif status == STATUS_AWAITING_USER:
            glyph = '?'
        else:
            glyph = '·'

        prompt_model = str(prompt.get('model'))
        display_model = prompt_model if test_concrete_model(prompt_model) else get_model_from_environment()
        model_short = get_short_model(display_model)
        content = truncate(re.sub(r'[\r\n]+', ' ', str(prompt.get('content', ''))), 30)
        line = f"{glyph} {status}"
        if model_short:
            line += f" {model_short}"
        if content:
            line += f" {content}"
        write_status_line(line)
    except Exception as e:
        write_err(f'status_failed: {e}', 'status')
        write_status_line('· ?')


def handle_event(event_type, payload):
    sessions = read_log()
    convert_prompt_lists(sessions)

    sid = str(get_property(payload, 'session_id')) if payload else None
    if not sid or not sid.strip():
        sid = str(uuid.uuid4())

    current_session = find_session(sessions, sid)
    if not current_session and event_type == 'UserPromptSubmit':
        # Lazy day-rollover cleanup: only when we're about to create today's
        # log file (first UserPromptSubmit of the day, new session).
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = LOG_DIR / f'{today}.json'
        if not today_file.exists():
            invoke_yesterday_cleanup()

        project = str(get_property(payload, 'cwd')) if payload else None
        current_session = {
            'project': project,
            'session_id': sid,
            'prompts': [],
        }
        sessions.append(current_session)

    changed = False
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if event_type == 'UserPromptSubmit':
        content = ''
        if payload:
            for key in ('prompt', 'user_prompt', 'message'):
                value = get_property(payload, key)
                if value is not None:
                    content = str(value)
                    break
        content = truncate(content, 500)

        for prompt in current_session.get('prompts') or []:
            if stop_prompt(prompt, now):
                changed = True

        model = get_model_from_payload_or_transcript(payload)
        current_session['prompts'].append({
            'content': content,
            'model': model,
            'start_time': now,
            'end_time': '',
            'duration': None,
            'status': STATUS_RUNNING,
        })
        changed = True

    elif event_type == 'PreToolUse':
        prompt = find_last_in_progress(sessions, sid)
        if prompt:
            tool_name = str(get_property(payload, 'tool_name')) if payload else ''
            if tool_name == 'AskUserQuestion':
                if str(prompt.get('status')) != STATUS_AWAITING_USER:
                    prompt['status'] = STATUS_AWAITING_USER
                    changed = True
            elif str(prompt.get('status')) == STATUS_AWAITING_USER:
                prompt['status'] = STATUS_RUNNING
                changed = True
            if update_prompt_model(prompt, payload):
                changed = True

    elif event_type == 'PermissionRequest':
        prompt = find_last_in_progress(sessions, sid)
        if prompt:
            if str(prompt.get('status')) != STATUS_AWAITING_USER:
                prompt['status'] = STATUS_AWAITING_USER
                changed = True
            if update_prompt_model(prompt, payload):
                changed = True

    elif event_type == 'PostToolUse':
        prompt = find_last_in_progress(sessions, sid)
        if prompt:
            if str(prompt.get('status')) == STATUS_AWAITING_USER:
                prompt['status'] = STATUS_RUNNING
                changed = True
            if update_prompt_model(prompt, payload):
                changed = True

    elif event_type == 'Stop':
        prompt = find_last_in_progress(sessions, sid)
        if prompt:
            if update_prompt_model(prompt, payload):
                changed = True
            if complete_prompt(prompt, now):
                changed = True

    elif event_type == 'SessionEnd':
        prompt = find_last_in_progress(sessions, sid)
        if prompt:
            if update_prompt_model(prompt, payload):
                changed = True
            if stop_prompt(prompt, now):
                changed = True

    if changed:
        write_log(sessions)


def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    event_type = sys.argv[1]

    if event_type not in KNOWN_EVENTS:
        sys.exit(0)

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        write_err(f'logdir_create_failed: {e}', 'init')

    payload = read_stdin_json()

    if event_type == 'StatusLine':
        handle_status_line(payload)
        sys.exit(0)

    lock_fd, acquired = None, False
    try:
        lock_fd, acquired = acquire_lock(LOG_DIR / '.audit.lock', MUTEX_TIMEOUT_MS)
    except Exception as e:
        write_err(f'mutex_wait_failed: {e}', 'mutex')

    if not acquired:
        write_err(f'mutex_timeout ({MUTEX_TIMEOUT_MS}ms) event={event_type}', 'mutex')
        release_lock(lock_fd)
        sys.exit(0)

    try:
        handle_event(event_type, payload)
    except Exception as e:
        write_err(f'handler_failed: {e}', 'handler')
    finally:
        release_lock(lock_fd)

    sys.exit(0)


if __name__ == '__main__':
    main()
