import subprocess
import time
import os
import sys
import re
import shutil

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
os.chdir(app_dir)

# 1. Clear __pycache__ to prevent stale imports
pycache_dir = os.path.join(app_dir, "__pycache__")
if os.path.exists(pycache_dir):
    try:
        shutil.rmtree(pycache_dir)
    except Exception:
        pass

python_exe = sys.executable

# 2. Kill old instances
subprocess.run("taskkill /f /im cloudflared.exe", shell=True, capture_output=True)

# 3. Start Streamlit server
streamlit_cmd = [
    python_exe, "-m", "streamlit", "run",
    os.path.join(app_dir, "app.py"),
    "--server.headless", "true",
    "--server.address", "0.0.0.0",
    "--server.port", "8501"
]

st_log = os.path.join(app_dir, "streamlit.log")
with open(st_log, "w", encoding="utf-8") as f_st:
    st_proc = subprocess.Popen(
        streamlit_cmd,
        stdout=f_st,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
        cwd=app_dir
    )

time.sleep(4)

# 4. Start Cloudflare Tunnel
cloudflared_exe = os.path.join(app_dir, "cloudflared.exe")
cf_cmd = [cloudflared_exe, "tunnel", "--url", "http://127.0.0.1:8501"]

cf_log = os.path.join(app_dir, "tunnel.log")
with open(cf_log, "w", encoding="utf-8") as f_cf:
    cf_proc = subprocess.Popen(
        cf_cmd,
        stdout=f_cf,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
        cwd=app_dir
    )

print("Started Streamlit and Cloudflared successfully.")
