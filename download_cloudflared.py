import urllib.request
import os

url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
target = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\cloudflared.exe"

print("Downloading cloudflared.exe...")
try:
    urllib.request.urlretrieve(url, target)
    print("Downloaded cloudflared.exe successfully!")
except Exception as e:
    print(f"Failed to download cloudflared: {e}")
