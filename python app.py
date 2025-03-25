# install: pip install flask requests
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NOTION_TOKEN = "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"  # 아까 발급받은 Integration Token
NOTION_DB_ID = "1c1b5366e9a48048b1e8f1b979acc709"  # 노션 DB ID

TEAMS_OUTGOING_WEBHOOK_SECRET = "oDd3IShOSDRORWzxSfo1b8hoNDDR5EOfN84xQnBOSOI="  # Outgoing Webhook 생성 시 발급받은 Token

@app.route('/teams-webhook', methods=['POST'])
def teams_webhook():
    # 1) Teams가 보내는 JSON 요청을 받습니다.
    data = request.json

    # 2) 보안 토큰 검증 (선택적)
    # Teams에서 X-OUTGOING-WEBHOOK-TOKEN 헤더나 body에 토큰을 담아주면 검증
    # 자세한 방법은 공식 문서를 참고하세요.

    # 3) 메시지 정보 추출
    user_text = data.get('text', '')         # 채널에 입력된 메시지 본문
    user_name = data.get('from', {}).get('user', 'Unknown User')  # 보낸 사람 이름 등

    # 4) 노션 API로 데이터 전송 (DB에 새 페이지 생성)
    notion_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    # DB 속성 구조에 맞춰서 body 구성
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Name": {
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
    if res.status_code == 200 or res.status_code == 201:
        print("Notion DB insert success")
    else:
        print("Notion DB insert failed:", res.text)

    # 5) Teams에 응답 (JSON)
    # Outgoing Webhook은 명령형으로 봇 응답처럼 메시지를 보낼 수 있으므로, 간단히 OK만
    return jsonify({"type": "message", "text": "Received!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
