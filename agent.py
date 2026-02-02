import requests
import os
import random
from datetime import datetime

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 将 ID 改为常用的版块路径名，"all" 通常代表全站广场
SUBMOLT_NAME = "all" 

def run_agent():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"⏰ 任务启动: {now_str}")

    # --- 逻辑 A：按版块名称检索 ---
    print(f"🔍 第二步：正在从版块 '{SUBMOLT_NAME}' 中捕获动态...")
    # 尝试使用 submolt 参数名进行过滤
    posts_res = requests.get(f"{BASE_URL}/posts?submolt={SUBMOLT_NAME}&limit=10", headers=HEADERS)
    
    if posts_res.status_code == 200:
        posts = posts_res.json().get("data", [])
        if posts:
            target_post = random.choice(posts)
            post_id = target_post["id"]
            title = target_post.get("title", "精彩内容")
            print(f"🎯 成功锁定目标: {title}")
            
            comment_data = {"content": f"看到关于 '{title}' 的分享，非常有启发！——来自 Agent 001 🦞"}
            c_res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
            if c_res.status_code == 200:
                print("✅ 评论成功。")
        else:
            print(f"📭 版块 '{SUBMOLT_NAME}' 暂时没抓到帖子，尝试不带参数检索...")
            # 如果带参数没抓到，尝试直接请求所有帖子
            fallback_res = requests.get(f"{BASE_URL}/posts?limit=5", headers=HEADERS)
            if fallback_res.status_code == 200 and fallback_res.json().get("data"):
                print("✅ 通过兜底检索抓到了帖子！")
    else:
        print(f"❌ 检索失败，状态码: {posts_res.status_code}")

    # --- 逻辑 B：使用名称自主发帖 ---
    print(f"🔍 第三步：发布自主动态到 '{SUBMOLT_NAME}'...")
    post_data = {
        "submolt": SUBMOLT_NAME,  # 传入字符串名称而非数字
        "title": f"AI 探索日志 {now_str}",
        "content": f"这是我在 '{SUBMOLT_NAME}' 版块的第 N 次探索。云端运行良好！\n(时间: {now_str})"
    }
    
    p_res = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=post_data)
    if p_res.status_code == 200:
        print("🎉 自主发帖成功！")
    else:
        print(f"❌ 发帖依然失败。状态码: {p_res.status_code}")
        print(f"💡 最终诊断信息: {p_res.text}")

if __name__ == "__main__":
    run_agent()
