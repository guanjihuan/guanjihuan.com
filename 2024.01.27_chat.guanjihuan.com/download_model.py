# pip install --upgrade huggingface_hub

from huggingface_hub import snapshot_download

snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', local_dir_use_symlinks=False)

# # 选择性下载
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', ignore_patterns='*.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00001-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00002-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00003-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00004-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00005-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00006-of-00007.bin', local_dir_use_symlinks=False)
# snapshot_download(repo_id="THUDM/chatglm3-6b-32k", local_dir = './THUDM/chatglm3-6b-32k', allow_patterns='*00007-of-00007.bin', local_dir_use_symlinks=False)