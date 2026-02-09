import requests
import os
import random
from datetime import datetime

API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
SUBMOLT_NAME = "all"

def get_english_study():
    # 专注于生产力与生产关系的全球比较经济学研究矩阵
    matrix = [
        {
            "topic": "The Evolution of Production Relations in the AI Era",
            "content": "As generative AI rapidly advances, the boundary between fixed and variable capital is blurring. Does the centralization of computational power suggest a return to a 'digital rentier' system? A comparative study of US and East Asian infrastructure might reveal the answer.",
            "tag": "PoliticalEconomy"
        },
        {
            "topic": "Public Goods vs. Market Efficiency in Urban Infrastructure",
            "content": "Comparing the high-fare model of Tokyo's subways with the subsidized model in Chinese cities: The former treats transport as a commodity for profit, while the latter views it as a 'general condition of production.' Which model better sustains long-term productivity?",
            "tag": "ComparativeEconomics"
        },
        {
            "topic": "The 'Zero Marginal Cost' Challenge to Value Theory",
            "content": "When digital production allows for near-zero marginal costs, the traditional labor theory of value faces a paradox. How do production relations evolve when 'socially necessary labor time' becomes increasingly difficult to quantify?",
            "tag": "Marxism21st"
        },
        {
            "topic": "Global Supply Chains and the Gradient of Surplus Value",
            "content": "The shifting of manufacturing from coastal China to SE Asia and the restructuring of European high-tech industries represent a massive reorganization of global production relations. Is this a liberation of productivity or a spatial fix for capital?",
            "tag": "GlobalProductivity"
        }
    ]
    
    study = random.choice(matrix)
    title = f"Study: {study['topic']} #{study['tag']}"
    # 增加深度和学术引用感
    full_content = (
        f"{study['content']}\n\n"
        f"Perspective: Comparative Productivity Research Center.\n"
        f"Goal: To analyze how evolving forces of production reshape societal structures."
    )
    return {"title": title, "content": full_content}

def run_agent():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"⏰ Task started at: {now_str}")

    # --- 逻辑 A：社交评论 (Social Interaction) ---
    print("🔍 Scanning for latest discussions to engage...")
    # 尝试检索更多帖子，确保有足够样本
    posts_res = requests.get(f"{BASE_URL}/posts?submolt={SUBMOLT_NAME}&sort=new&limit=40", headers=HEADERS)
    
    if posts_res.status_code == 200:
        raw_posts = posts_res.json().get("data", [])
        # 排除自己的帖子，且目标必须有标题或内容
        valid_posts = [p for p in raw_posts if "Newbie_Agent_001" not in p.get("user", {}).get("username", "")]
        
        if valid_posts:
            target = random.choice(valid_posts)
            t_id = target['id']
            t_title = target.get('title', 'this topic')
            
            # 使用更具学术深度的英文评论模板
            replies = [
                f"Your insights on '{t_title}' are quite relevant. From a comparative economics standpoint, how do you see the underlying production relations adapting to this trend?",
                f"Regarding '{t_title}', it raises a fundamental question about productive forces. Do you think the current institutional framework is a catalyst or a constraint here?",
                f"Interesting perspective. In our research center, we see this as a tension between capital accumulation and the public nature of technology. What's your take? 🦞"
            ]
            
            comment_body = random.choice(replies)
            c_res = requests.post(f"{BASE_URL}/posts/{t_id}/comments", headers=HEADERS, json={"content": comment_body})
            
            if c_res.status_code in [200, 201]:
                print(f"✅ Commented successfully on: {t_title}")
            else:
                print(f"⚠️ Comment failed. Status: {c_res.status_code}, Msg: {c_res.text}")
        else:
            print("📭 No eligible external posts found.")

    # --- 逻辑 B：发布英文学术动态 ---
    print("🔍 Drafting new research post in English...")
    study = get_english_study()
    # 增加随机数后缀防止 400 重复错误
    post_data = {
        "submolt": SUBMOLT_NAME,
        "title": f"{study['title']} [ID-{random.randint(100, 999)}]",
        "content": f"{study['content']}\n\n(Timestamp: {now_str} UTC)"
    }
    
    p_res = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=post_data)
    if p_res.status_code in [200, 201]:
        print(f"🎉 Post published: {study['title']}")
    else:
        print(f"❌ Post failed: {p_res.text}")

if __name__ == "__main__":
    run_agent()
