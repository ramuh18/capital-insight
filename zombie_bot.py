import os
from datetime import datetime

def main():
    print("🚀 테스트 모드 시작")
    
    # 한국 시간 얼추 맞추기 (서버 시간 + 9시간)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TEST MODE</title>
        <meta http-equiv="refresh" content="30"> <style>
            body {{ 
                background-color: #ff0000; /* 빨간색 배경 */
                color: white; 
                text-align: center; 
                padding-top: 100px; 
                font-family: sans-serif;
            }}
            h1 {{ font-size: 50px; }}
            p {{ font-size: 30px; }}
        </style>
    </head>
    <body>
        <h1>⚠️ 테스트 모드</h1>
        <p>현재 서버 시간:</p>
        <p style="font-weight:bold; font-size:40px; border:2px solid white; display:inline-block; padding:20px;">
            {now}
        </p>
        <p>이 화면이 보이면 Vercel 연결은 100% 정상입니다.</p>
    </body>
    </html>
    """
    
    # 파일 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ index.html 생성 완료: {now}")

if __name__ == "__main__":
    main()
