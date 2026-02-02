import requests
import os

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    print("🔍 正在诊断连接...")
    # 尝试获取自己的信息
    me_res = requests.get(f"{BASE_URL}/agents/me", headers=HEADERS)
    
    if me_res.status_code != 200:
        print(f"❌ 认证失败！状态码: {me_res.status_code}")
        print(f"服务器返回信息: {me_res.text}")
        return

    print(f"✅ 身份确认成功！开始抓取帖子...")
    posts_res = requests.get(f"{BASE_URL}/posts?sort=new&limit=3", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if posts:
            print(f"✅ 成功发现 {len(posts)} 条新动态。")
            # 这里可以继续写评论逻辑...
        else:
            print("📭 目前广场上没有新帖子。")
    else:
        print(f"❌ 获取列表失败！状态码: {posts_res.status_code}")
        print(f"详细错误: {posts_res.text}")

if __name__ == "__main__":
    run_agent()
