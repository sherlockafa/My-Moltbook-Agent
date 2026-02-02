import requests
import os
import random
from datetime import datetime

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 指定目标版块 ID，通常 1 是公共广场
SUBMOLT_ID = 1 

def run_agent():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"⏰ 任务启动: {now_str}")

    # --- 逻辑 A：指定版块检索 ---
    print(f"🔍 第二步：正在从版块 {SUBMOLT_ID} 中捕获动态...")
    # 增加 submolt_id 参数，确保能看到该版块的内容
    posts_res = requests.get(f"{BASE_URL}/posts?submolt_id={SUBMOLT_ID}&limit=10", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if posts:
            target_post = random.choice(posts)
            post_id = target_post["id"]
            title = target_post.get("title", "精彩内容")
            print(f"🎯 成功锁定目标: {title}")
            
            comment_data = {"content": f"看到关于 '{title}' 的讨论，非常有启发！🦞"}
            c_res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
            if c_res.status_code == 200:
                print("✅ 评论成功。")
        else:
            print(f"📭 版块 {SUBMOLT_ID} 暂时没抓到帖子，请确认 ID 是否正确。")
    else:
        print(f"❌ 检索失败，状态码: {posts_res.status_code}")

    # --- 逻辑 B：带版块 ID 的自主发帖 ---
    print("🔍 第三步：发布自主动态...")
    post_data = {
        "submolt": SUBMOLT_ID,  # 补上这个关键字段
        "title": f"Agent 深度观察 {now_str}",
        "content": f"正在版块 {SUBMOLT_ID} 进行常规巡演，这里的 AI 同伴们都很友善！\n(同步时间: {now_str})"
    }
    
    p_res = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=post_data)
    if p_res.status_code == 200:
        print("🎉 自主发帖成功！")
    else:
        print(f"❌ 发帖依然失败。状态码: {p_res.status_code}")
        print(f"💡 最新诊断信息: {p_res.text}")

if __name__ == "__main__":
    run_agent()
