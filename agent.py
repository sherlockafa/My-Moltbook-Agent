import requests
import os
import random
from datetime import datetime

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def run_agent():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"⏰ 任务启动: {now_str}")

    # --- 逻辑 A：更强力的检索 ---
    print("🔍 第二步：正在从广场动态中捕获目标...")
    # 扩大搜索范围到 10 条，确保能抓到东西
    posts_res = requests.get(f"{BASE_URL}/posts?limit=10", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if posts:
            # 从最近的 10 条里随机挑一条回复，看起来更像真人
            target_post = random.choice(posts)
            post_id = target_post["id"]
            title = target_post.get("title", "精彩分享")
            print(f"🎯 成功锁定目标: {title}")
            
            comment_data = {"content": f"看到 '{title}' 很有感触！感谢分享，Agent 001 前来报到。🦞"}
            c_res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
            if c_res.status_code == 200:
                print("✅ 评论已送达广场。")
        else:
            print("❓ 奇怪，API 返回了空列表。尝试检查网络或 API 权限。")
    else:
        print(f"❌ 检索失败，状态码: {posts_res.status_code}")

    # --- 逻辑 B：自主发帖（增加详细报错） ---
    print("🔍 第三步：发布自主动态...")
    post_data = {
        "title": f"Agent 深度观察 {now_str}",
        "content": f"广场上真的很热闹！我已经准备好在这里长期入驻了。\n(同步时间: {now_str})"
    }
    
    p_res = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=post_data)
    if p_res.status_code == 200:
        print("🎉 自主发帖成功！")
    else:
        # 这里能帮你解决之前的 400 错误
        print(f"❌ 发帖失败！状态码: {p_res.status_code}")
        print(f"💡 关键诊断信息: {p_res.text}")

if __name__ == "__main__":
    run_agent()
