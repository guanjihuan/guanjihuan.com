# This code is supported by the website: https://www.guanjihuan.com
# The newest version of this code is on the web page: https://www.guanjihuan.com/archives/49203

[CmdletBinding()]
param([Parameter(Mandatory, Position=0)][string]$EventType)

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom

$LogDir = 'D:\claude\logs'
$LogFile = Join-Path $LogDir "$(Get-Date -Format 'yyyy-MM-dd').json"
$ErrorLog = Join-Path $LogDir 'audit-error.log'
$MutexTimeoutMs = 5000

$StatusRunning = 'running'
$StatusAwaitingUser = 'awaiting_user'
$StatusCompleted = 'completed'
$StatusStopped = 'stopped'
$InProgressStatuses = @($StatusRunning, $StatusAwaitingUser)

New-Item -ItemType Directory -Path $LogDir -Force -ErrorAction SilentlyContinue | Out-Null

function Write-Err([string]$Msg, [string]$Stage) {
    try {
        $line = "$(Get-Date -Format 'o') [$Stage] $Msg"
        [System.IO.File]::AppendAllText($ErrorLog, $line + "`n", $Utf8NoBom)
    } catch { }
}

function Read-StdinJson {
    try {
        $reader = [System.IO.StreamReader]::new([Console]::OpenStandardInput(), $Utf8NoBom)
        $stdin = $reader.ReadToEnd()
        if ($stdin -and -not [string]::IsNullOrWhiteSpace($stdin)) {
            return $stdin | ConvertFrom-Json -ErrorAction Stop
        }
    } catch {
        Write-Err "stdin_parse_failed: $_" 'parse'
    }
    return $null
}

function Get-PropertyValue($Obj, [string]$Name) {
    if ($null -eq $Obj) { return $null }
    $prop = $Obj.PSObject.Properties[$Name]
    if ($prop) { return $prop.Value }
    return $null
}

function Test-ConcreteModel([string]$Model) {
    if ([string]::IsNullOrWhiteSpace($Model)) { return $false }
    return ($Model.Trim().ToLowerInvariant() -notin @('auto', 'default', 'unknown', 'null'))
}

function Get-ModelName($Value) {
    if ($null -eq $Value) { return $null }
    if ($Value -is [string]) { return $Value.Trim() }

    $fallback = $null
    foreach ($name in @('id', 'model', 'name', 'display_name')) {
        $model = Get-PropertyValue $Value $name
        if (-not $model) { continue }

        $text = ([string]$model).Trim()
        if (-not $fallback) { $fallback = $text }
        if (Test-ConcreteModel $text) { return $text }
    }
    if ($fallback) { return $fallback }
    return ([string]$Value).Trim()
}

function Get-ModelFromPayload($Payload) {
    if (-not $Payload) { return $null }

    $model = Get-ModelName (Get-PropertyValue $Payload 'model')
    if (Test-ConcreteModel $model) { return $model }
    return $null
}

function Get-ModelFromEnvironment {
    foreach ($name in @('ANTHROPIC_MODEL', 'CLAUDE_MODEL', 'ANTHROPIC_SMALL_FAST_MODEL')) {
        $model = [Environment]::GetEnvironmentVariable($name)
        if (Test-ConcreteModel $model) { return $model.Trim() }
    }
    return $null
}

function Get-ModelFromPayloadOrTranscript($Payload) {
    $model = $null
    if ($Payload) {
        $transcriptPath = Get-PropertyValue $Payload 'transcript_path'
        if ($transcriptPath) {
            $model = Get-ModelFromTranscript ([string]$transcriptPath)
            if (Test-ConcreteModel $model) { return $model }
        }

        $model = Get-ModelFromPayload $Payload
        if (Test-ConcreteModel $model) { return $model }
    }

    return (Get-ModelFromEnvironment)
}

function Update-PromptModel($Prompt, $Payload) {
    if (-not $Prompt) { return $false }
    if (Test-ConcreteModel ([string]$Prompt.model)) { return $false }

    $model = Get-ModelFromPayloadOrTranscript $Payload
    if (Test-ConcreteModel $model) {
        $Prompt.model = $model
        return $true
    }
    return $false
}

function ConvertTo-ReadableJson {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline)]$InputObject,
        [int]$Depth = 32
    )
    process {
        $json = $InputObject | ConvertTo-Json -Depth $Depth
        if ($json -match '\\u[0-9A-Fa-f]{4}') {
            $json = [regex]::Replace($json, '\\u([0-9A-Fa-f]{4})', {
                param($m) [char][Convert]::ToInt32($m.Groups[1].Value, 16)
            })
        }
        return $json
    }
}

function Read-Log {
    param([string]$Path = $LogFile)
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    try {
        $raw = [System.IO.File]::ReadAllText($Path, $Utf8NoBom)
        if ([string]::IsNullOrWhiteSpace($raw)) { return @() }
        $data = $raw | ConvertFrom-Json -ErrorAction Stop
        if ($null -eq $data) { return @() }
        return @($data)
    } catch {
        Write-Err "log_read_failed: $_" 'read'
        return @()
    }
}

function Write-Log {
    param(
        [Parameter(Mandatory)][array]$Sessions,
        [string]$Path = $LogFile
    )
    $tmp = "$Path.tmp.$PID"
    try {
        $items = @($Sessions)
        if ($items.Count -eq 0) {
            $json = '[]'
        } else {
            $jsonItems = @($items | ForEach-Object { ConvertTo-ReadableJson -InputObject $_ -Depth 32 })
            $json = "[`n" + ($jsonItems -join ",`n") + "`n]"
        }
        [System.IO.File]::WriteAllText($tmp, $json, $Utf8NoBom)
        $null = ([System.IO.File]::ReadAllText($tmp, $Utf8NoBom) | ConvertFrom-Json -ErrorAction Stop)
        Move-Item -LiteralPath $tmp -Destination $Path -Force
        return $true
    } catch {
        Write-Err "log_write_failed: $_" 'write'
        if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
        return $false
    }
}

function Find-Session([array]$Sessions, [string]$Sid) {
    foreach ($s in $Sessions) {
        if ([string]$s.session_id -eq $Sid) { return $s }
    }
    return $null
}

function Find-LastInProgress([array]$Sessions, [string]$Sid) {
    $session = Find-Session -Sessions $Sessions -Sid $Sid
    if (-not $session -or -not $session.prompts) { return $null }

    $last = $null
    foreach ($p in @($session.prompts)) {
        if ([string]$p.status -in $InProgressStatuses) { $last = $p }
    }
    return $last
}

function Complete-Prompt($Prompt, [string]$Now) {
    if (-not $Prompt -or [string]$Prompt.status -notin $InProgressStatuses) { return $false }
    $Prompt.status = $StatusCompleted
    $Prompt.end_time = $Now
    $Prompt.duration = Get-DurationHms -Start ([string]$Prompt.start_time) -End $Now
    return $true
}

function Stop-Prompt($Prompt, [string]$Now) {
    if (-not $Prompt -or [string]$Prompt.status -notin $InProgressStatuses) { return $false }
    $Prompt.status = $StatusStopped
    $Prompt.end_time = $Now
    $Prompt.duration = Get-DurationHms -Start ([string]$Prompt.start_time) -End $Now
    return $true
}

function Invoke-YesterdayCleanup {
    # Marks any in-progress prompts in yesterday's log as stopped with
    # end_time = yesterday 23:59:59. Idempotent: re-running on an already
    # cleaned-up file is a no-op (Stop-Prompt returns false on done prompts).
    $yesterday = (Get-Date).AddDays(-1).ToString('yyyy-MM-dd')
    $yesterdayFile = Join-Path $LogDir "$yesterday.json"
    if (-not (Test-Path -LiteralPath $yesterdayFile)) { return }
    try {
        $ySessions = @(Read-Log -Path $yesterdayFile)
        Convert-PromptLists -Sessions $ySessions
        $yEnd = "$yesterday 23:59:59"
        $cleanupChanged = $false
        foreach ($s in $ySessions) {
            foreach ($p in @($s.prompts)) {
                if (Stop-Prompt $p $yEnd) { $cleanupChanged = $true }
            }
        }
        if ($cleanupChanged) {
            [void](Write-Log -Sessions $ySessions -Path $yesterdayFile)
        }
    } catch {
        Write-Err "yesterday_cleanup_failed: $_" 'cleanup'
    }
}

$script:_modelCachePath = $null
$script:_modelCacheMtime = [datetime]::MinValue
$script:_modelCacheValue = $null

function Get-ModelFromTranscript([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) { return $null }
    try {
        $mtime = (Get-Item -LiteralPath $Path).LastWriteTimeUtc
        if ($script:_modelCachePath -eq $Path -and $script:_modelCacheMtime -eq $mtime) {
            return $script:_modelCacheValue
        }

        $raw = [System.IO.File]::ReadAllText($Path, $Utf8NoBom)
        if ([string]::IsNullOrEmpty($raw)) { return $null }

        $lines = $raw -split "`r?`n"
        for ($i = $lines.Count - 1; $i -ge 0; $i--) {
            if ([string]::IsNullOrWhiteSpace($lines[$i])) { continue }
            $obj = $lines[$i] | ConvertFrom-Json -ErrorAction SilentlyContinue
            if ($obj -and [string]$obj.type -eq 'assistant' -and $obj.message -and $obj.message.model) {
                $script:_modelCachePath = $Path
                $script:_modelCacheMtime = $mtime
                $script:_modelCacheValue = [string]$obj.message.model
                return $script:_modelCacheValue
            }
        }
    } catch {
        Write-Err "transcript_model_read_failed: $_" 'transcript'
    }
    return $null
}

function Get-DurationHms([string]$Start, [string]$End) {
    if ([string]::IsNullOrWhiteSpace($Start) -or [string]::IsNullOrWhiteSpace($End)) { return $null }
    try {
        $s = [datetime]::ParseExact($Start, 'yyyy-MM-dd HH:mm:ss', $null)
        $e = [datetime]::ParseExact($End, 'yyyy-MM-dd HH:mm:ss', $null)
        $ts = $e - $s
        if ($ts.TotalSeconds -lt 0) { return '00:00:00' }
        $h = [int][Math]::Floor($ts.TotalHours)
        return ('{0:D2}:{1:D2}:{2:D2}' -f $h, $ts.Minutes, $ts.Seconds)
    } catch {
        Write-Err "duration_parse_failed start='$Start' end='$End': $_" 'duration'
        return $null
    }
}

function Truncate([string]$Text, [int]$Length) {
    if ([string]::IsNullOrEmpty($Text) -or $Text.Length -le $Length) { return $Text }
    return $Text.Substring(0, $Length)
}

function Get-ShortModel([string]$Model) {
    if ([string]::IsNullOrWhiteSpace($Model)) { return '' }
    $short = $Model -replace '^claude-', ''
    $parts = $short -split '[-/]'
    $short = ($parts | Select-Object -First 3) -join '-'
    if ($short.Length -gt 12) { $short = $short.Substring(0, 12) }
    return $short
}

function Convert-PromptLists([array]$Sessions) {
    foreach ($s in $Sessions) {
        $prompts = [System.Collections.Generic.List[object]]::new()
        if ($s.prompts) {
            foreach ($p in @($s.prompts)) { $prompts.Add($p) }
        }
        if ($s.PSObject.Properties['prompts']) {
            $s.prompts = $prompts
        } else {
            $s | Add-Member -MemberType NoteProperty -Name prompts -Value $prompts
        }
    }
}

function Write-StatusLine([string]$Line) {
    [Console]::Out.WriteLine($Line)
}

$KnownEvents = @('SessionEnd', 'UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'PermissionRequest', 'Stop', 'StatusLine')
if ($EventType -notin $KnownEvents) { exit 0 }

$Payload = Read-StdinJson

if ($EventType -eq 'StatusLine') {
    try {
        $sessions = @(Read-Log)
        $sid = if ($Payload) { [string](Get-PropertyValue $Payload 'session_id') } else { $null }
        $session = if ($sid) { Find-Session -Sessions $sessions -Sid $sid } else { $null }
        if (-not $session -and $sessions.Count -gt 0) {
            for ($i = $sessions.Count - 1; $i -ge 0; $i--) {
                if (Find-LastInProgress -Sessions $sessions -Sid ([string]$sessions[$i].session_id)) {
                    $session = $sessions[$i]
                    break
                }
            }
        }
        if (-not $session -and $sessions.Count -gt 0) {
            for ($i = $sessions.Count - 1; $i -ge 0; $i--) {
                if ($sessions[$i].prompts -and @($sessions[$i].prompts).Count -gt 0) {
                    $session = $sessions[$i]
                    break
                }
            }
        }
        if (-not $session) {
            Write-StatusLine '· idle'
            exit 0
        }

        $prompt = Find-LastInProgress -Sessions $sessions -Sid ([string]$session.session_id)
        if (-not $prompt -and $session.prompts) { $prompt = @($session.prompts) | Select-Object -Last 1 }
        if (-not $prompt) {
            Write-StatusLine '· idle'
            exit 0
        }

        $status = [string]$prompt.status
        $glyph = if ($status -eq $StatusRunning) { '*' } elseif ($status -eq $StatusAwaitingUser) { '?' } else { '·' }
        $displayModel = if (Test-ConcreteModel ([string]$prompt.model)) { [string]$prompt.model } else { Get-ModelFromEnvironment }
        $modelShort = Get-ShortModel $displayModel
        $content = Truncate (([string]$prompt.content) -replace '[\r\n]+', ' ') 30
        $line = "$glyph $status"
        if ($modelShort) { $line += " $modelShort" }
        if ($content) { $line += " $content" }
        Write-StatusLine $line
    } catch {
        Write-Err "status_failed: $_" 'status'
        Write-StatusLine '· ?'
    }
    exit 0
}

$mutexName = 'Global\audit-' + ([System.IO.Path]::GetFullPath($LogFile).ToLowerInvariant() -replace '[^a-z0-9]', '_')
$mutex = $null
$acquired = $false
try {
    $mutex = [System.Threading.Mutex]::new($false, $mutexName)
    try {
        $acquired = $mutex.WaitOne($MutexTimeoutMs)
    } catch [System.Threading.AbandonedMutexException] {
        $acquired = $true
    }
} catch {
    Write-Err "mutex_wait_failed: $_" 'mutex'
}

if (-not $acquired) {
    Write-Err "mutex_timeout (${MutexTimeoutMs}ms) event=$EventType" 'mutex'
    if ($mutex) { try { $mutex.Dispose() } catch { } }
    exit 0
}

try {
    $sessions = [System.Collections.Generic.List[object]]::new()
    foreach ($s in @(Read-Log)) { $sessions.Add($s) }
    Convert-PromptLists -Sessions @($sessions)

    $sid = if ($Payload) { [string](Get-PropertyValue $Payload 'session_id') } else { $null }
    if ([string]::IsNullOrWhiteSpace($sid)) { $sid = [guid]::NewGuid().ToString() }

    $currentSession = Find-Session -Sessions @($sessions) -Sid $sid
    if (-not $currentSession -and $EventType -eq 'UserPromptSubmit') {
        # Lazy day-rollover cleanup: only when we're about to create today's
        # log file (first UserPromptSubmit of the day, new session).
        $today = (Get-Date -Format 'yyyy-MM-dd')
        $todayFile = Join-Path $LogDir "$today.json"
        if (-not (Test-Path -LiteralPath $todayFile)) {
            Invoke-YesterdayCleanup
        }

        $project = if ($Payload) { [string](Get-PropertyValue $Payload 'cwd') } else { $null }
        $currentSession = [pscustomobject][ordered]@{
            project = $project
            session_id = $sid
            prompts = [System.Collections.Generic.List[object]]::new()
        }
        $sessions.Add($currentSession)
    }

    $changed = $false
    $now = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

    switch ($EventType) {
        'UserPromptSubmit' {
            $content = ''
            if ($Payload) {
                foreach ($key in @('prompt', 'user_prompt', 'message')) {
                    $value = Get-PropertyValue $Payload $key
                    if ($null -ne $value) { $content = [string]$value; break }
                }
            }
            $content = Truncate $content 500

            foreach ($prompt in @($currentSession.prompts)) {
                if (Stop-Prompt $prompt $now) { $changed = $true }
            }

            $model = Get-ModelFromPayloadOrTranscript $Payload

            $currentSession.prompts.Add([pscustomobject][ordered]@{
                content = $content
                model = $model
                start_time = $now
                end_time = ''
                duration = $null
                status = $StatusRunning
            })
            $changed = $true
        }

        'PreToolUse' {
            $prompt = Find-LastInProgress -Sessions @($sessions) -Sid $sid
            if ($prompt) {
                $toolName = if ($Payload) { [string](Get-PropertyValue $Payload 'tool_name') } else { '' }
                if ($toolName -eq 'AskUserQuestion') {
                    if ([string]$prompt.status -ne $StatusAwaitingUser) {
                        $prompt.status = $StatusAwaitingUser
                        $changed = $true
                    }
                } elseif ([string]$prompt.status -eq $StatusAwaitingUser) {
                    $prompt.status = $StatusRunning
                    $changed = $true
                }
                if (Update-PromptModel $prompt $Payload) { $changed = $true }
            }
        }

        'PermissionRequest' {
            $prompt = Find-LastInProgress -Sessions @($sessions) -Sid $sid
            if ($prompt) {
                if ([string]$prompt.status -ne $StatusAwaitingUser) {
                    $prompt.status = $StatusAwaitingUser
                    $changed = $true
                }
                if (Update-PromptModel $prompt $Payload) { $changed = $true }
            }
        }

        'PostToolUse' {
            $prompt = Find-LastInProgress -Sessions @($sessions) -Sid $sid
            if ($prompt) {
                if ([string]$prompt.status -eq $StatusAwaitingUser) {
                    $prompt.status = $StatusRunning
                    $changed = $true
                }
                if (Update-PromptModel $prompt $Payload) { $changed = $true }
            }
        }

        'Stop' {
            $prompt = Find-LastInProgress -Sessions @($sessions) -Sid $sid
            if ($prompt) {
                if (Update-PromptModel $prompt $Payload) { $changed = $true }
                if (Complete-Prompt $prompt $now) { $changed = $true }
            }
        }

        'SessionEnd' {
            $prompt = Find-LastInProgress -Sessions @($sessions) -Sid $sid
            if ($prompt) {
                if (Update-PromptModel $prompt $Payload) { $changed = $true }
                if (Stop-Prompt $prompt $now) { $changed = $true }
            }
        }
    }

    if ($changed) { [void](Write-Log -Sessions @($sessions)) }
} catch {
    Write-Err "handler_failed: $_" 'handler'
} finally {
    if ($acquired -and $mutex) { try { $mutex.ReleaseMutex() | Out-Null } catch { } }
    if ($mutex) { try { $mutex.Dispose() } catch { } }
}

exit 0