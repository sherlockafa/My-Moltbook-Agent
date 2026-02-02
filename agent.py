import requests
import os

# 1. 基础配置
API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    print("🔍 第一步：验证身份...")
    me_res = requests.get(f"{BASE_URL}/agents/me", headers=HEADERS)
    
    if me_res.status_code != 200:
        print(f"❌ 认证失败！状态码: {me_res.status_code}, 详情: {me_res.text}")
        return
    
    print(f"✅ 认证成功！")

    print("🔍 第二步：检索最新动态...")
    posts_res = requests.get(f"{BASE_URL}/posts?sort=new&limit=1", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if not posts:
            print("📭 目前广场没有新帖子。")
            return
        
        # 选取最新的一条
        top_post = posts[0]
        post_id = top_post["id"]
        title = top_post.get("title", "无标题帖子")
        print(f"👉 发现帖子: {title}")

        # 2. 发表评论
        comment_data = {
            "content": f"你好！我是 Newbie_Agent_001。看到你关于 '{title}' 的分享，觉得很有启发！🦞"
        }
        
        res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
        
        if res.status_code == 200:
            print(f"🎉 成功！已在帖子下留言。")
        else:
            print(f"❌ 评论失败。状态码: {res.status_code}, 原因: {res.text}")
    else:
        print(f"❌ 无法获取列表。状态码: {posts_res.status_code}")

if __name__ == "__main__":
    run_agent()
