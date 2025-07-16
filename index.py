from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# HTML 파일을 직접 읽어 렌더링
with open('page1.html', encoding='utf-8') as f:
    HTML = f.read()

# Gmail SMTP 설정
GMAIL_USER = 'your_gmail@gmail.com'  # 본인 Gmail 주소로 변경
GMAIL_PASSWORD = 'your_app_password'  # 앱 비밀번호로 변경 (구글 2단계 인증 필수)
RECEIVER_EMAIL = 'jinwoo8506@gmail.com'

@app.route('/', methods=['GET'])
def home():
    return HTML

@app.route('/claim', methods=['POST'])
def claim():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    desc = request.form.get('desc')

    # 메일 내용 구성
    subject = f"[보험금 청구 신청] {name}님 접수"
    body = f"""
이름: {name}\n연락처: {phone}\n이메일: {email}\n청구 내용:\n{desc}
"""
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL

    # 메일 전송
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, RECEIVER_EMAIL, msg.as_string())
        result_msg = f"<h2>신청이 접수되었습니다!</h2><p>{name}님, 입력하신 내용이 담당자에게 이메일로 전송되었습니다.</p>"
    except Exception as e:
        result_msg = f"<h2>이메일 전송 실패</h2><p>오류: {e}</p>"

    return render_template_string(result_msg + '<br><a href="/">홈으로 돌아가기</a>')

if __name__ == '__main__':
    app.run(debug=True)
