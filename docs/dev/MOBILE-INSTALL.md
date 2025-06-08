---

## ✅ 전체 구성 요약

| 구성 요소          | 설명                                        |
| -------------- | ----------------------------------------- |
| Termux         | 안드로이드 리눅스 CLI 환경                          |
| code-server    | 브라우저에서 쓰는 VSCode                          |
| Python/Node.js | FastAPI + React/Vue 개발용                   |
| 외부 접속 (선택)     | localhost 대신 접속 URL 설정 가능 (클라우드 expose 시) |

---

## 📦 1단계: Termux 설치 및 초기 설정

1. **Termux 설치**

   * Play Store 버전은 오래됐으니 [F-Droid](https://f-droid.org/)에서 설치 권장

2. **업데이트**

   ```bash
   pkg update && pkg upgrade
   ```

3. **개발 도구 설치**

   ```bash
   pkg install git python nodejs
   ```

4. **Python 가상환경**

   ```bash
   pip install virtualenv
   virtualenv venv
   source venv/bin/activate
   ```

---

## 🧠 2단계: code-server 설치 (VSCode Web)

1. **code-server 설치 스크립트 실행**

   ```bash
   curl -fsSL https://code-server.dev/install.sh | sh
   ```

2. **기본 실행 테스트**

   ```bash
   code-server
   ```

3. **처음 실행 시 안내되는 주소 확인**

   * 보통: `http://localhost:8080`
   * 비밀번호는 `~/.config/code-server/config.yaml`에 있음

---

## 🛠 3단계: code-server 자동 설정

### 비밀번호 없애고 로그인 없이 접속하기 (로컬 한정)

```bash
vim ~/.config/code-server/config.yaml
```

```yaml
bind-addr: 127.0.0.1:8080
auth: none
```

---

## 🌐 4단계: 브라우저에서 접속하기

1. **Termux에서 code-server 실행 중**

2. **갤럭시 폴드 브라우저에서 아래 주소 접속**

   ```
   http://localhost:8080
   ```

3. Chrome 브라우저 추천 + 홈화면에 바로가기 추가하면 앱처럼 사용 가능

---

## 💡 개발용 추가 설정

### FastAPI 설치

```bash
pip install fastapi uvicorn
```

### React/Vue 프로젝트 생성

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

---

## 🔐 외부 접속 하고 싶다면?

Termux는 외부에서 직접 접근 불가이므로 **[ngrok](https://ngrok.com/)** 같은 터널링 도구를 사용해야 해:

```bash
pkg install wget unzip
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
./ngrok http 8080
```

→ `https://xxxxx.ngrok.io` 주소로 code-server 접속 가능

---

## ✅ 요약

* `Termux + code-server`로 갤럭시 폴드에서 VSCode Web 개발 가능
* Python, Node.js 등 필요한 스택도 설치 가능
* 내부에서만 쓸 거면 `localhost:8080`, 외부 접속은 `ngrok`으로 처리

