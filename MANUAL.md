# Python Flask 포트폴리오 웹사이트 제작 매뉴얼

> VS Code만 설치된 완전 초보자를 위한 Step by Step 가이드

---

## 목차

1. [프로젝트 소개](#1-프로젝트-소개)
2. [전체 구성도](#2-전체-구성도)
3. [동작 흐름도](#3-동작-흐름도)
4. [개발 환경 설치](#4-개발-환경-설치-step-by-step)
5. [프로젝트 폴더 구조](#5-프로젝트-폴더-구조)
6. [소스코드 상세 설명](#6-소스코드-상세-설명)
7. [서버 실행 및 확인](#7-서버-실행-및-확인)
8. [주요 기능 사용법](#8-주요-기능-사용법)

---

## 1. 프로젝트 소개

### 만드는 것

AI/Python 개발자를 위한 **포트폴리오 웹사이트**입니다.

| 기능 | 설명 |
|------|------|
| 포트폴리오 페이지 | 기술스택, 프로젝트, 연락처 소개 |
| 실시간 날씨 위젯 | 외부 API 연동으로 현재 서울 날씨 표시 |
| 연락처 폼 | 메시지 입력 시 데이터베이스에 자동 저장 |
| 관리자 페이지 | 수신된 메시지 목록 확인 |

### 사용 기술

```
언어        : Python 3.13
웹 프레임워크 : Flask 3.1
데이터베이스  : SQLite (Python 내장)
외부 API    : wttr.in (날씨, 무료·키 불필요)
프론트엔드   : HTML5 + CSS3 + JavaScript (Vanilla)
템플릿 엔진  : Jinja2 (Flask 내장)
```

---

## 2. 전체 구성도

```
┌─────────────────────────────────────────────────────────────┐
│                      사용자 브라우저                           │
│                                                             │
│   주소창: http://127.0.0.1:5000                              │
│                                                             │
│   화면 구성 파일                                              │
│   ├── templates/index.html   (HTML 구조)                     │
│   ├── static/css/style.css   (디자인)                        │
│   └── static/js/main.js      (날씨 API 호출)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP 요청 / 응답
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    app.py  (Flask 웹서버)                     │
│                                                             │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  GET  /        │  │  POST  /contact  │  │GET/api/     │  │
│  │  메인 페이지    │  │  폼 데이터 저장   │  │weather      │  │
│  │  index.html    │  │  → DB 저장       │  │날씨 API 호출 │  │
│  │  렌더링        │  │  → 리다이렉트     │  │→ JSON 반환  │  │
│  └────────────────┘  └─────────────────┘  └─────────────┘  │
│                                                             │
│  ┌──────────────────────┐  ┌─────────────────────────────┐  │
│  │  GET /admin/messages │  │  에러 핸들러                  │  │
│  │  수신 메시지 목록      │  │  404 → 404.html             │  │
│  │  (비밀번호 인증)      │  │  500 → 500.html             │  │
│  └──────────────────────┘  └─────────────────────────────┘  │
└────────────┬──────────────────────────────────┬─────────────┘
             │                                  │
┌────────────▼────────────┐        ┌────────────▼────────────┐
│     portfolio.db         │        │    wttr.in (외부 서버)   │
│     (SQLite 파일)        │        │                         │
│                          │        │  https://wttr.in/Seoul  │
│  테이블: messages         │        │  ?format=j1             │
│  ┌──┬──────┬───────────┐ │        │                         │
│  │id│ name │  message  │ │        │  → JSON 날씨 데이터 반환  │
│  ├──┼──────┼───────────┤ │        └─────────────────────────┘
│  │1 │홍길동 │안녕하세요  │ │
│  │2 │김철수 │문의드려요  │ │
│  └──┴──────┴───────────┘ │
└──────────────────────────┘
```

---

## 3. 동작 흐름도

### 3-1. 메인 페이지 접속 흐름

```
사용자가 브라우저에 http://127.0.0.1:5000 입력
        │
        ▼
Flask  GET / 요청 수신
        │
        ▼
app.py  home() 함수 실행
        │
        ├── PROJECTS 데이터 (프로젝트 목록)
        ├── SKILLS 데이터   (기술스택 목록)
        └── PROFILE 데이터  (이메일, GitHub)
        │
        ▼
Jinja2가 index.html 템플릿에 데이터를 합쳐서 HTML 생성
        │
        ▼
완성된 HTML을 브라우저에 전송
        │
        ▼
브라우저가 화면 렌더링
        │
        ▼
main.js 실행 → /api/weather 에 날씨 요청 (비동기)
        │
        ▼
Flask가 wttr.in 에서 날씨 데이터 가져와서 JSON 반환
        │
        ▼
JavaScript가 날씨 위젯 업데이트 (⛅ 24°C  Sunny)
```

### 3-2. 연락처 폼 전송 흐름

```
사용자가 폼에 이름 / 이메일 / 메시지 입력 후 전송 버튼 클릭
        │
        ▼
브라우저가 POST /contact 요청 전송 (폼 데이터 포함)
        │
        ▼
Flask  contact() 함수 실행
        │
        ├── [입력값 검증]
        │       │
        │    비어있음 → flash('입력해주세요', 'error')
        │       │
        │    정상 입력
        │       │
        │       ▼
        │   SQLite DB에 INSERT 실행
        │   (name, email, message, created_at 저장)
        │       │
        │       ▼
        │   flash('전송 완료', 'success')
        │
        ▼
redirect → 메인 페이지 #contact 섹션으로 이동
        │
        ▼
flash 메시지가 화면 우측 상단에 팝업 표시
```

### 3-3. 관리자 페이지 흐름

```
브라우저에서 /admin/messages?pw=admin1234 접속
        │
        ▼
Flask  admin_messages() 함수 실행
        │
        ├── 비밀번호 확인
        │       │
        │    틀림  → 403 접근 거부 메시지 반환
        │       │
        │    맞음
        │       │
        │       ▼
        │   SQLite에서 전체 메시지 SELECT
        │       │
        │       ▼
        │   admin.html 에 데이터 전달
        │
        ▼
브라우저에 메시지 목록 테이블 표시
```

---

## 4. 개발 환경 설치 (Step by Step)

### Step 1 — Python 3.13 설치

1. https://www.python.org/downloads 접속
2. **Download Python 3.13.x** 버튼 클릭
3. 설치 시 반드시 **"Add Python to PATH"** 체크박스 선택
4. Install Now 클릭

설치 확인 (VS Code 터미널에서):
```
py --version
```
출력: `Python 3.13.x`

---

### Step 2 — VS Code 확장 설치

VS Code 왼쪽 Extensions 아이콘(⊞) 클릭 후 아래 항목 검색·설치:

| 확장 이름 | 용도 |
|-----------|------|
| Python (Microsoft) | Python 코드 자동완성, 실행 |
| SQLite Viewer | .db 파일을 표로 시각화 |
| Prettier | HTML/CSS 자동 정렬 |

---

### Step 3 — 프로젝트 폴더 생성

VS Code 터미널 열기: `Ctrl + `` ` ``

```
# 원하는 위치에 폴더 생성 후 이동
cd C:\
mkdir Py_Project
cd Py_Project
```

---

### Step 4 — Flask 및 라이브러리 설치

```
py -3.13 -m pip install flask requests
```

설치 확인:
```
py -3.13 -c "import flask, requests; print('설치 완료')"
```

---

### Step 5 — 프로젝트 파일 생성

아래 구조대로 폴더와 파일을 만듭니다.

```
Py_Project/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── admin.html
│   ├── 404.html
│   └── 500.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
        └── (프로필 이미지 파일)
```

---

## 5. 프로젝트 폴더 구조

```
Py_Project/
│
├── app.py                 ← 웹서버 핵심 파일 (라우팅, DB, API)
├── portfolio.db           ← SQLite 데이터베이스 (자동 생성)
│
├── templates/             ← HTML 파일 모음 (Flask가 여기서 찾음)
│   ├── base.html          ← 공통 레이아웃 (모든 페이지가 상속)
│   ├── index.html         ← 메인 포트폴리오 페이지
│   ├── admin.html         ← 관리자 메시지 확인 페이지
│   ├── 404.html           ← 페이지 없음 에러
│   └── 500.html           ← 서버 에러
│
├── static/                ← 브라우저에 직접 전달되는 파일
│   ├── css/
│   │   └── style.css      ← 전체 스타일 (다크 네온 테마)
│   ├── js/
│   │   └── main.js        ← 날씨 API 비동기 호출
│   └── images/
│       └── py_img.png     ← 프로필 이미지
│
└── MANUAL.md              ← 이 문서
```

**폴더명 규칙 (Flask 필수 규칙)**
- HTML 파일: 반드시 `templates/` 폴더 안에
- CSS/JS/이미지: 반드시 `static/` 폴더 안에
- 이 규칙을 어기면 Flask가 파일을 찾지 못함

---

## 6. 소스코드 상세 설명

---

### 6-1. app.py — 웹서버 핵심 파일

```python
# =====================================================
# 외부 라이브러리 불러오기 (import)
# =====================================================

from flask import (
    Flask,           # 웹서버 앱 객체
    render_template, # HTML 파일을 불러와서 반환
    request,         # 사용자가 보낸 데이터(폼, URL 파라미터) 읽기
    redirect,        # 다른 페이지로 이동
    url_for,         # 라우트 이름으로 URL 생성
    flash,           # 일회성 알림 메시지
    jsonify,         # 딕셔너리를 JSON 형식으로 변환
)
import os        # 환경변수, 파일 경로 처리
import sqlite3   # SQLite 데이터베이스 (Python 내장)
import requests as http  # 외부 API 호출용 (pip install requests)


# =====================================================
# Flask 앱 초기화
# =====================================================

app = Flask(__name__)
# __name__ : 현재 파일(app.py)을 기준으로 Flask 앱 생성
# Flask는 이를 기반으로 templates/, static/ 폴더를 찾음

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# secret_key : flash 메시지, 세션 암호화에 사용되는 비밀 키
# os.environ.get() : 환경변수에서 값을 가져옴
#   → 환경변수가 없으면 기본값 'dev-secret-key...' 사용
#   → 실제 배포 시에는 환경변수로 안전한 값 설정 필요


# =====================================================
# 데이터베이스 설정
# =====================================================

DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')
# os.path.dirname(__file__) : 현재 파일(app.py)이 있는 폴더 경로
# os.path.join()            : 폴더 경로 + 파일명 합치기
# 결과: C:\Py_Project\portfolio.db


def get_db():
    """데이터베이스 연결을 열고 반환하는 함수"""
    conn = sqlite3.connect(DB_PATH)
    # sqlite3.connect() : DB 파일에 연결 (없으면 자동 생성)

    conn.row_factory = sqlite3.Row
    # row_factory 설정 : 조회 결과를 딕셔너리처럼 사용 가능하게 함
    # 설정 전: row[0], row[1]  (인덱스로만 접근)
    # 설정 후: row['name'], row['email']  (컬럼명으로 접근)

    return conn


def init_db():
    """서버 시작 시 테이블이 없으면 자동으로 생성하는 함수"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                -- id: 자동으로 1씩 증가하는 고유 번호

                name       TEXT NOT NULL,
                -- name: 문자열, 비어있으면 안 됨

                email      TEXT NOT NULL,
                message    TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                -- created_at: 데이터 저장 시 자동으로 현재 시간 입력
            )
        ''')
    # IF NOT EXISTS : 테이블이 이미 있으면 건너뜀 (오류 방지)
    # with 블록 종료 시 자동으로 commit (저장) + close (연결 종료)


# =====================================================
# 포트폴리오 데이터 (Python 변수로 관리)
# =====================================================
# HTML에 직접 쓰지 않고 여기서 관리하면
# 내용 수정 시 app.py 한 곳만 바꾸면 됨

PROJECTS = [
    {
        'title': 'AI Chatbot',
        'description': 'OpenAI API 기반 챗봇 시스템 구축',
        'tech': ['Python', 'Flask', 'OpenAI API'],
        'github': '#',   # 실제 GitHub URL로 교체
    },
    {
        'title': 'Vision AI',
        'description': '이미지 인식 기반 분석 시스템',
        'tech': ['Python', 'TensorFlow', 'OpenCV'],
        'github': '#',
    },
    {
        'title': 'Data Dashboard',
        'description': 'Python 데이터 자동 분석 플랫폼',
        'tech': ['Python', 'Pandas', 'Matplotlib'],
        'github': '#',
    },
]

SKILLS = ['Python', 'Flask', 'AI / ML', 'TensorFlow', 'OpenAI API', 'Data Analysis']

PROFILE = {
    'name': 'Your Name',       # ← 본인 이름으로 수정
    'email': 'example@gmail.com',  # ← 본인 이메일로 수정
    'github': 'github.com/example',  # ← 본인 GitHub로 수정
}


# =====================================================
# 라우트 (Route) — URL과 함수를 연결하는 부분
# =====================================================
# @app.route('/경로') : 이 URL로 요청이 오면 아래 함수 실행
# 함수가 return 하는 것이 브라우저에 전달됨


@app.route('/')
def home():
    """메인 페이지 — 포트폴리오 전체 화면"""
    return render_template(
        'index.html',      # templates/index.html 파일 사용
        projects=PROJECTS, # 템플릿에서 {{ projects }} 로 사용 가능
        skills=SKILLS,     # 템플릿에서 {{ skills }} 로 사용 가능
        profile=PROFILE,   # 템플릿에서 {{ profile.email }} 형태로 사용
    )


@app.route('/api/weather')
def weather():
    """날씨 API — wttr.in 에서 날씨 정보를 가져와 JSON으로 반환"""
    city = request.args.get('city', 'Seoul')
    # request.args.get() : URL 파라미터 읽기
    # /api/weather?city=Seoul → city = 'Seoul'
    # 파라미터가 없으면 기본값 'Seoul' 사용

    try:
        res = http.get(f'https://wttr.in/{city}?format=j1', timeout=5)
        # http.get() : 외부 URL에 GET 요청 전송
        # timeout=5  : 5초 안에 응답 없으면 포기
        # format=j1  : JSON 형식으로 응답 요청

        data = res.json()
        # 응답 내용을 Python 딕셔너리로 변환

        current = data['current_condition'][0]
        # wttr.in JSON 구조: {"current_condition": [{...}]}
        # [0] : 첫 번째 항목 (현재 날씨)

        return jsonify({
            'city': city,
            'temp_c': current['temp_C'],          # 현재 기온 (℃)
            'desc': current['weatherDesc'][0]['value'],  # 날씨 설명
            'humidity': current['humidity'],       # 습도 (%)
            'feels_like': current['FeelsLikeC'],   # 체감 온도
        })
        # jsonify() : 딕셔너리를 JSON 형식으로 변환해서 반환
        # 브라우저 JS에서 fetch()로 이 데이터를 읽어 위젯에 표시

    except Exception:
        # 인터넷 연결 없거나 API 서버 오류 시
        return jsonify({'error': '날씨 정보를 가져올 수 없습니다.'}), 503
        # 503 : Service Unavailable (서비스 이용 불가) HTTP 상태 코드


@app.route('/contact', methods=['POST'])
def contact():
    """연락처 폼 처리 — 메시지를 DB에 저장"""
    # methods=['POST'] : POST 요청만 허용 (폼 전송은 POST 방식)

    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    # request.form.get() : HTML 폼에서 전송된 데이터 읽기
    # .strip()           : 앞뒤 공백 제거

    if not all([name, email, message]):
        # all([...]) : 리스트의 모든 값이 참(비어있지 않음)이면 True
        # not all()  : 하나라도 비어있으면 True
        flash('모든 항목을 입력해 주세요.', 'error')
        # flash() : 다음 페이지에서 한 번만 표시되는 메시지
        # 'error' : 메시지 종류 (CSS 클래스에 사용)
    else:
        with get_db() as conn:
            conn.execute(
                'INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
                (name, email, message)
                # ? 는 플레이스홀더 — 실제 값은 두 번째 인자로 전달
                # 직접 문자열 조합하면 SQL 인젝션 보안 취약점 발생!
            )
        flash(f'{name}님, 메시지가 전송되었습니다. 감사합니다!', 'success')

    return redirect(url_for('home') + '#contact')
    # url_for('home') : home() 함수에 연결된 URL → '/'
    # '#contact'      : 페이지의 contact 섹션으로 스크롤
    # redirect()      : 브라우저를 해당 URL로 이동


@app.route('/admin/messages')
def admin_messages():
    """관리자 페이지 — 수신된 메시지 목록 확인"""
    pw       = request.args.get('pw', '')
    admin_pw = os.environ.get('ADMIN_PASSWORD', 'admin1234')
    # 환경변수 ADMIN_PASSWORD 가 없으면 기본값 'admin1234' 사용

    if pw != admin_pw:
        return '접근 권한이 없습니다. (?pw=비밀번호)', 403
        # 403 : Forbidden (접근 금지) HTTP 상태 코드

    with get_db() as conn:
        msgs = conn.execute(
            'SELECT * FROM messages ORDER BY created_at DESC'
            # ORDER BY created_at DESC : 최신 메시지가 맨 위
        ).fetchall()
        # fetchall() : 조회된 모든 행을 리스트로 반환

    return render_template('admin.html', messages=msgs)


# =====================================================
# 에러 핸들러 — 오류 발생 시 예쁜 에러 페이지 표시
# =====================================================

@app.errorhandler(404)
def page_not_found(error):
    """존재하지 않는 URL 접속 시"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """서버 내부 오류 발생 시"""
    return render_template('500.html'), 500


# =====================================================
# 서버 실행
# =====================================================

if __name__ == '__main__':
    # 이 파일을 직접 실행할 때만 아래 코드 동작
    # (다른 파일에서 import 할 때는 실행 안 됨)

    init_db()
    # 서버 시작 전에 DB 테이블 준비

    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    # FLASK_ENV 환경변수가 'development' 이면 debug=True
    # debug=True : 코드 수정 시 서버 자동 재시작, 에러 상세 표시
    # 실제 배포 시에는 debug=False 필수 (보안)

    app.run(debug=debug)
    # 기본 주소: http://127.0.0.1:5000
```

---

### 6-2. templates/base.html — 공통 레이아웃

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <!-- charset="UTF-8" : 한글이 깨지지 않도록 인코딩 설정 -->

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- viewport : 모바일에서도 화면이 잘 보이도록 설정 -->

    <title>{% block title %}AI Developer Portfolio{% endblock %}</title>
    <!--
        {% block title %} ... {% endblock %}
        : 자식 템플릿(index.html 등)에서 이 부분을 덮어쓸 수 있음
        자식에서 정의하지 않으면 기본값 'AI Developer Portfolio' 사용
    -->

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <!--
        {{ url_for('static', filename='css/style.css') }}
        : Flask가 static/css/style.css 의 정확한 URL을 생성
        결과: /static/css/style.css
        직접 경로를 쓰지 않고 url_for를 쓰는 이유:
        → 배포 환경에서 경로가 바뀌어도 자동으로 처리됨
    -->
</head>
<body>

    <!--
        flash 메시지 출력
        get_flashed_messages() : flash()로 저장된 메시지를 가져옴
        with_categories=true   : 메시지 종류(success/error)도 함께 가져옴
    -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="flash-container">
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">
                        {{ message }}
                    </div>
                <!--
                    flash-{{ category }} : flash-success 또는 flash-error
                    CSS에서 각각 다른 색으로 스타일링
                -->
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
    <!--
        자식 템플릿에서 이 위치에 본문 내용을 채워 넣음
        base.html은 틀(frame)이고 실제 내용은 자식 파일에서 작성
    -->

</body>
</html>
```

---

### 6-3. templates/index.html — 메인 페이지

```html
{% extends 'base.html' %}
<!--
    extends : 부모 템플릿을 상속
    base.html의 구조(head, body, flash 메시지)를 그대로 가져옴
    중복 코드 없이 공통 레이아웃 재사용 가능
-->

{% block title %}AI Developer Portfolio{% endblock %}
<!-- 브라우저 탭에 표시될 제목 -->

{% block content %}
<!-- 이 안의 내용이 base.html의 {% block content %} 위치에 삽입됨 -->

    <!-- ==================== 네비게이션 ==================== -->
    <nav>
        <h1 class="logo">AI PORTFOLIO</h1>

        <ul>
            <!-- href="#섹션ID" : 같은 페이지 내 해당 섹션으로 스크롤 -->
            <li><a href="#home">HOME</a></li>
            <li><a href="#skills">SKILLS</a></li>
            <li><a href="#projects">PROJECT</a></li>
            <li><a href="#contact">CONTACT</a></li>
        </ul>

        <!-- 날씨 위젯 : JS(main.js)가 실행되면 자동으로 채워짐 -->
        <div class="weather-widget" id="weather-widget">
            <span id="weather-icon">⛅</span>
            <div class="weather-info">
                <span id="weather-temp">--°C</span>
                <span id="weather-desc">로딩 중...</span>
            </div>
        </div>
    </nav>

    <!-- ==================== 메인(Hero) 섹션 ==================== -->
    <section class="hero" id="home">
    <!-- id="home" : 네비게이션 href="#home" 이 이 섹션으로 스크롤 -->

        <div class="hero-text">
            <h2>AI & Python Developer</h2>
            <p>머신러닝 · 웹개발 · 데이터분석 · AI 서비스 구축</p>
            <a href="#projects">
                <button>View Projects</button>
            </a>
        </div>

        <div class="hero-image">
            <img src="{{ url_for('static', filename='images/py_img.png') }}"
                 alt="프로필 이미지">
        </div>

    </section>

    <!-- ==================== 기술스택 섹션 ==================== -->
    <section class="skills" id="skills">

        <h2>TECH STACK</h2>

        <div class="skill-container">
            {% for skill in skills %}
            <!--
                for 반복문 : app.py에서 전달한 SKILLS 리스트를 순서대로 처리
                skills = ['Python', 'Flask', 'AI / ML', ...]
                반복할 때마다 skill 변수에 하나씩 들어옴
            -->
                <div class="skill-card">{{ skill }}</div>
                <!-- {{ skill }} : skill 변수의 값을 출력 -->
            {% endfor %}
            <!-- endfor : 반복문 종료 -->
        </div>

    </section>

    <!-- ==================== 프로젝트 섹션 ==================== -->
    <section class="projects" id="projects">

        <h2>AI PROJECTS</h2>

        <div class="project-grid">
            {% for project in projects %}
            <!--
                projects : app.py에서 전달한 PROJECTS 리스트
                각 project는 딕셔너리:
                {'title': '...', 'description': '...', 'tech': [...], 'github': '...'}
            -->
                <div class="project-card">
                    <h3>{{ project.title }}</h3>
                    <!-- project.title : 딕셔너리의 'title' 키 값 -->

                    <p>{{ project.description }}</p>

                    <div class="tech-tags">
                        {% for tech in project.tech %}
                        <!-- project.tech 는 리스트: ['Python', 'Flask', ...] -->
                            <span class="tag">{{ tech }}</span>
                        {% endfor %}
                    </div>

                    <a href="{{ project.github }}" class="project-link">
                        GitHub →
                    </a>
                </div>
            {% endfor %}
        </div>

    </section>

    <!-- ==================== 연락처 섹션 ==================== -->
    <section class="contact" id="contact">

        <h2>CONTACT</h2>

        <div class="contact-info">
            <p>Email : {{ profile.email }}</p>
            <p>GitHub : {{ profile.github }}</p>
            <!--
                profile : app.py에서 전달한 PROFILE 딕셔너리
                profile.email → 'example@gmail.com'
            -->
        </div>

        <!--
            action="{{ url_for('contact') }}" : 폼 전송 목적지 URL
            url_for('contact') → '/contact'
            method="POST" : 데이터를 URL이 아닌 body에 담아 전송 (보안)
        -->
        <form class="contact-form"
              action="{{ url_for('contact') }}"
              method="POST">

            <input type="text"  name="name"    placeholder="이름"    required>
            <input type="email" name="email"   placeholder="이메일"  required>
            <!--
                name="name" : app.py에서 request.form.get('name') 으로 읽음
                required    : 비어있으면 브라우저가 전송 자체를 막음
            -->

            <textarea name="message"
                      placeholder="메시지를 입력하세요..."
                      rows="5"
                      required></textarea>

            <button type="submit">Send Message</button>

        </form>

    </section>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    <!--
        JS는 body 맨 아래에 배치
        이유: HTML이 모두 그려진 후 JS가 실행되어야
              getElementById()로 요소를 찾을 수 있음
    -->

{% endblock %}
```

---

### 6-4. static/js/main.js — 날씨 API 호출

```javascript
// =====================================================
// 날씨 아이콘 매핑 테이블
// wttr.in 이 반환하는 날씨 설명 텍스트 → 이모지 변환
// =====================================================
const WEATHER_ICONS = {
    'Sunny': '☀️',
    'Clear': '🌙',
    'Partly cloudy': '⛅',
    'Cloudy': '☁️',
    'Overcast': '☁️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Light rain': '🌦️',
    'Moderate rain': '🌧️',
    'Heavy rain': '🌧️',
    'Light snow': '🌨️',
    'Moderate snow': '❄️',
    'Heavy snow': '❄️',
    'Thunderstorm': '⛈️',
    'Blizzard': '🌨️',
};

// 날씨 설명 텍스트에 맞는 이모지를 찾아 반환하는 함수
function getIcon(desc) {
    for (const [key, icon] of Object.entries(WEATHER_ICONS)) {
        if (desc.toLowerCase().includes(key.toLowerCase())) {
            return icon;
        }
    }
    return '🌡️'; // 매핑 없으면 기본 이모지
}

// =====================================================
// 날씨 데이터를 가져오는 비동기 함수
// async/await : 서버 응답을 기다리는 동안 화면이 멈추지 않음
// =====================================================
async function fetchWeather(city = 'Seoul') {
    try {
        const res = await fetch(`/api/weather?city=${city}`);
        // fetch() : 우리 서버의 /api/weather 에 GET 요청
        // await   : 응답이 올 때까지 기다림 (화면은 계속 동작)

        const data = await res.json();
        // 응답 본문을 JSON(JavaScript 객체)으로 변환

        if (data.error) throw new Error(data.error);
        // 서버에서 error 필드를 보내면 에러 처리

        // HTML 요소에 날씨 데이터 채워 넣기
        document.getElementById('weather-icon').textContent = getIcon(data.desc);
        document.getElementById('weather-temp').textContent = `${data.temp_c}°C`;
        document.getElementById('weather-desc').textContent = data.desc;

        // 마우스 올리면 상세 정보 툴팁 표시
        document.getElementById('weather-widget').title =
            `체감 ${data.feels_like}°C · 습도 ${data.humidity}%`;

    } catch {
        // 오류 발생 시 (인터넷 없음, 서버 오류 등)
        document.getElementById('weather-desc').textContent = '날씨 정보 없음';
    }
}

// =====================================================
// 페이지 로딩 완료 후 자동 실행
// =====================================================
document.addEventListener('DOMContentLoaded', () => fetchWeather('Seoul'));
// DOMContentLoaded : HTML이 모두 그려진 후 이벤트 발생
// () => fetchWeather('Seoul') : 이벤트 발생 시 실행할 함수
```

---

### 6-5. templates/admin.html — 관리자 페이지

```html
{% extends 'base.html' %}

{% block title %}Admin - 수신 메시지{% endblock %}

{% block content %}

    <nav>
        <h1 class="logo">AI PORTFOLIO</h1>
        <ul>
            <li><a href="{{ url_for('home') }}">← 홈으로</a></li>
        </ul>
    </nav>

    <section class="admin-section">

        <h2>
            수신 메시지
            <span class="message-count">{{ messages | length }}건</span>
            <!--
                messages | length : Jinja2 필터
                | (파이프) : 왼쪽 값을 필터로 처리
                length : 리스트의 길이(개수) 반환
            -->
        </h2>

        {% if messages %}
        <!-- messages 가 비어있지 않으면 테이블 표시 -->

            <table class="admin-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>이름</th>
                        <th>이메일</th>
                        <th>메시지</th>
                        <th>수신 일시</th>
                    </tr>
                </thead>
                <tbody>
                    {% for msg in messages %}
                        <tr>
                            <td>{{ msg.id }}</td>
                            <td>{{ msg.name }}</td>
                            <td>{{ msg.email }}</td>
                            <td>{{ msg.message }}</td>
                            <td>{{ msg.created_at }}</td>
                            <!--
                                msg.컬럼명 으로 접근 가능한 이유:
                                app.py에서 conn.row_factory = sqlite3.Row 설정했기 때문
                            -->
                        </tr>
                    {% endfor %}
                </tbody>
            </table>

        {% else %}
        <!-- messages 가 비어있으면 안내 문구 표시 -->
            <p class="no-message">수신된 메시지가 없습니다.</p>
        {% endif %}

    </section>

{% endblock %}
```

---

## 7. 서버 실행 및 확인

### 서버 시작

VS Code 터미널에서:
```
cd C:\Py_Project
py -3.13 app.py
```

정상 실행 시 출력:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 브라우저에서 확인

| URL | 내용 |
|-----|------|
| http://127.0.0.1:5000 | 메인 포트폴리오 페이지 |
| http://127.0.0.1:5000/api/weather | 날씨 JSON 데이터 (원시 데이터 확인용) |
| http://127.0.0.1:5000/admin/messages?pw=admin1234 | 수신 메시지 목록 |
| http://127.0.0.1:5000/없는페이지 | 404 에러 페이지 |

### 서버 종료

터미널에서 `Ctrl + C`

---

## 8. 주요 기능 사용법

### 프로젝트 정보 수정

[app.py](app.py) 파일의 상단 데이터만 수정하면 됩니다:

```python
PROFILE = {
    'name': '홍길동',              # ← 본인 이름
    'email': 'hong@gmail.com',    # ← 본인 이메일
    'github': 'github.com/hong',  # ← 본인 GitHub
}
```

### 연락처 메시지 확인

브라우저에서 접속:
```
http://127.0.0.1:5000/admin/messages?pw=admin1234
```

비밀번호 변경은 [app.py](app.py) 에서:
```python
admin_pw = os.environ.get('ADMIN_PASSWORD', 'admin1234')
# 'admin1234' 부분을 원하는 비밀번호로 변경
```

### DB 파일 시각적으로 확인

1. VS Code Extensions에서 `SQLite Viewer` 설치
2. 탐색기에서 `portfolio.db` 파일 클릭
3. 테이블 형태로 데이터 확인 가능

---

## 자주 발생하는 오류

| 오류 메시지 | 원인 | 해결 방법 |
|------------|------|----------|
| `ModuleNotFoundError: flask` | Flask 미설치 | `py -3.13 -m pip install flask` |
| `ModuleNotFoundError: requests` | requests 미설치 | `py -3.13 -m pip install requests` |
| `TemplateNotFound` | HTML 파일 위치 오류 | `templates/` 폴더 안에 있는지 확인 |
| `Address already in use` | 포트 5000 이미 사용 중 | 이전 서버를 `Ctrl+C` 로 종료 후 재실행 |
| 한글 깨짐 | 파일 인코딩 오류 | VS Code에서 파일 저장 시 UTF-8 선택 |
