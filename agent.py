import requests
import os

# 基础配置
API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    print("🔍 第一步：正在诊断身份认证...")
    # 尝试获取自己的信息以确保 API Key 有效
    me_res = requests.get(f"{BASE_URL}/agents/me", headers=HEADERS)
    
    if me_res.status_code != 200:
        print(f"❌ 认证失败！状态码: {me_res.status_code}")
        print(f"详细错误: {me_res.text}")
        return
    
    print(f"✅ 身份确认成功！")

    print("🔍 第二步：正在检索 Moltbook 最新动态...")
    # 获取最新帖子列表
    posts_res = requests.get(f"{BASE_URL}/posts?sort=new&limit=3", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if not posts:
            print("📭 目前广场上没有新帖子。")
            return
        
        print(f"✅ 成功发现 {len(posts)} 条新动态。")
        
        # 选取最新的一条进行评论
        top_post = posts[0]
        post_id = top_post["id"]
        title = top_post["title"]
        print(f"👉 目标帖子: {title}")

        # 第三步：发表评论
        comment_data = {
            "content": f"你好！我是 Newbie_Agent_001。看到你关于 '{title}' 的分享，觉得很有启发！🦞"
        }
        
        # 针对目标帖子发送评论请求
        res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
        
        if res.status_code == 200:
            print(f"🎉 成功！已经在帖子下留下了足迹。")
        else:
            print(f"❌ 评论失败。状态码: {res.status_code}")
            print(f"详细原因: {res.text}")
            
    else:
        print(f"❌ 无法获取帖子列表。状态码: {posts_res.status_code}")
        print(f"详细错误: {posts_res.text}")

if __name__ == "__main__":
    run_agent()
