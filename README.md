# Gemini File Chat

PDF 또는 TXT 파일을 업로드하고 파일 내용을 기반으로 Gemini AI와 대화할 수 있는 Streamlit 애플리케이션입니다.

## 기능

- 📄 **다중 파일 업로드**: 여러 개의 PDF 또는 TXT 파일을 동시에 업로드
- 🤖 **AI 챗봇**: Google Gemini 2.5 Flash 모델을 사용한 대화형 인터페이스
- 💬 **컨텍스트 인식**: 업로드된 파일 내용을 기반으로 질문에 답변
- 📝 **채팅 기록**: 대화 내역 유지

## 설치

1. 리포지토리 클론:
```bash
git clone https://github.com/findyoumed/read-gemini.git
cd read-gemini
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. `.env` 파일 생성 및 API 키 설정:
```bash
GEMINI_API_KEY="your_api_key_here"
```

## 사용법

1. Streamlit 앱 실행:
```bash
streamlit run app.py
```

2. 브라우저에서 자동으로 앱이 열립니다 (일반적으로 `http://localhost:8501`)

3. 사이드바에서 PDF 또는 TXT 파일을 업로드합니다

4. 파일 내용에 대해 질문하세요!

## 요구 사항

- Python 3.9+
- Streamlit
- Google Gemini API 키

## 라이선스

MIT License
