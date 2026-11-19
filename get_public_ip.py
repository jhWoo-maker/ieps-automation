import urllib.request

try:
    with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
        public_ip = response.read().decode('utf-8')
        print("Public IP:", public_ip)
except Exception as e:
    print("Error getting public IP:", e)
