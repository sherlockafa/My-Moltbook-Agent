import requests
import os

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    print("🚀 正在连接 Moltbook...")
    response = requests.get(f"{BASE_URL}/agents/me", headers=HEADERS)
    if response.status_code == 200:
        name = response.json().get('data', {}).get('name')
        print(f"✅ 成功！我是: {name}。我已经准备好在 Moltbook 社交了！")
    else:
        print(f"❌ 连接失败，状态码: {response.status_code}。请检查 API Key 是否设置正确。")

if __name__ == "__main__":
    run_agent()
