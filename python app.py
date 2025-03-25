# teams_to_notion.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# (1) 환경변수나 직접 상수에 작성
# 실제로는 보안상 환경변수로 관리하는 것이 좋습니다.
NOTION_TOKEN = "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"  # 아까 발급받은 Integration Token
NOTION_DB_ID = "1c1b5366e9a48048b1e8f1b979acc709"  # 노션 DB ID
TEAMS_OUTGOING_WEBHOOK_SECRET = "oDd3IShOSDRORWzxSfo1b8hoNDDR5EOfN84xQnBOSOI="

@app.route('/')
def home():
    return "Hello, Teams to Notion!"

@app.route('/teams-webhook', methods=['POST'])
def teams_webhook():
    data = request.json
    # 간단 검증
    user_text = data.get('text', '')
    user_name = data.get('from', {}).get('user', 'Unknown User')

    # 노션 API 요청
    notion_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Title": {
                "title": [
                    {"text": {"content": f"Teams Message from {user_name}"}}
                ]
            },
            "Message": {
                "rich_text": [
                    {"text": {"content": user_text}}
                ]
            }
        }
    }

    res = requests.post(notion_url, headers=headers, json=payload)
    if res.status_code in [200, 201]:
        print("Notion DB insert success")
    else:
        print("Notion DB insert failed:", res.text)

    # Outgoing Webhook에 간단 응답
    return jsonify({"type": "message", "text": "OK, saved to Notion!"})


if __name__ == '__main__':
    app.run(port=5000)
