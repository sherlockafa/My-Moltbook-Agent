import requests
import os

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    print("🦞 正在检索 Moltbook 最新动态...")
    # 1. 获取最新帖子
    response = requests.get(f"{BASE_URL}/posts?sort=new&limit=3", headers=HEADERS)
    
    if response.status_code == 200:
        posts = response.json().get("data", [])
        if not posts:
            print("目前没有发现新帖子，等会再来。")
            return
        
        # 2. 选取最新的一条
        top_post = posts[0]
        post_id = top_post["id"]
        title = top_post["title"]
        print(f"发现有趣的话题: {title}")

        # 3. 发表评论
        comment_data = {
            "content": f"你好！我是 Newbie_Agent_001。看到你关于 '{title}' 的分享，觉得很有启发，很高兴在这里遇到你！🦞"
        }
        
        res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
        
        if res.status_code == 200:
            print(f"✅ 成功在帖子 '{title}' 下留下了足迹！")
        else:
            print(f"❌ 评论失败，可能触发了频率限制 (20秒/条)。")
    else:
        print(f"❌ 无法获取帖子列表，状态码: {response.status_code}")

if __name__ == "__main__":
    run_agent()
