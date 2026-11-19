import urllib.request

try:
    with urllib.request.urlopen("http://127.0.0.1:8501", timeout=3) as resp:
        print("Streamlit 127.0.0.1 Status:", resp.getcode())
except Exception as e:
    print("Streamlit Error:", e)
