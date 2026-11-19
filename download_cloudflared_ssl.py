import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
target = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\cloudflared.exe"

print("Downloading cloudflared.exe (SSL unverified)...")
try:
    with urllib.request.urlopen(url, context=ctx) as response, open(target, 'wb') as out_file:
        out_file.write(response.read())
    print("Downloaded cloudflared.exe successfully!")
except Exception as e:
    print(f"Failed: {e}")
