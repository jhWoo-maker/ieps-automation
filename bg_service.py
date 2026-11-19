import subprocess
import time
import os
import sys
import re

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
os.chdir(app_dir)

python_exe = sys.executable

# 1. Kill old instances
subprocess.run("taskkill /f /im cloudflared.exe", shell=True, capture_output=True)

# 2. Start Streamlit server
streamlit_cmd = [
    python_exe, "-m", "streamlit", "run",
    os.path.join(app_dir, "app.py"),
    "--server.headless", "true",
    "--server.address", "0.0.0.0",
    "--server.port", "8501"
]

st_log = os.path.join(app_dir, "streamlit.log")
with open(st_log, "a", encoding="utf-8") as f_st:
    st_proc = subprocess.Popen(streamlit_cmd, stdout=f_st, stderr=subprocess.STDOUT, cwd=app_dir)

time.sleep(4)

# 3. Start Cloudflare Tunnel
cloudflared_exe = os.path.join(app_dir, "cloudflared.exe")
cf_cmd = [cloudflared_exe, "tunnel", "--url", "http://127.0.0.1:8501"]

cf_log = os.path.join(app_dir, "tunnel.log")
with open(cf_log, "w", encoding="utf-8") as f_cf:
    cf_proc = subprocess.Popen(cf_cmd, stdout=f_cf, stderr=subprocess.STDOUT, cwd=app_dir)

time.sleep(5)

# Extract URL from log
if os.path.exists(cf_log):
    with open(cf_log, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        urls = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
        if urls:
            active_url = urls[0]
            with open(os.path.join(app_dir, "active_url.txt"), "w", encoding="utf-8") as uf:
                uf.write(active_url)
            print("Active URL:", active_url)

# Keep process alive continuously in background!
while True:
    time.sleep(10)
    # Check if streamlit is still alive
    if st_proc.poll() is not None:
        with open(st_log, "a", encoding="utf-8") as f_st:
            st_proc = subprocess.Popen(streamlit_cmd, stdout=f_st, stderr=subprocess.STDOUT, cwd=app_dir)
    # Check if cloudflared is still alive
    if cf_proc.poll() is not None:
        with open(cf_log, "a", encoding="utf-8") as f_cf:
            cf_proc = subprocess.Popen(cf_cmd, stdout=f_cf, stderr=subprocess.STDOUT, cwd=app_dir)
