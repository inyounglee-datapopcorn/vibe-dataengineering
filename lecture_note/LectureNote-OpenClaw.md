# 🦞 OpenClaw: 나만의 개인용 AI 어시스턴트 구축하기

> **강의 목표**: "어디서나 접근 가능한 나만의 AI 비서"를 만드는 가장 강력한 오픈소스 프로젝트인 **OpenClaw**를 배웁니다. 특정 플랫폼에 갇히지 않고 Slack, Telegram, WhatsApp 등 내가 원하는 채널에 나만의 에이전트를 연동해 봅니다.
> 🔗 **공식 문서**: [OpenClaw Docs](https://docs.openclaw.ai/)

---

## 1. OpenClaw란 무엇인가? (Everything's Assistant)

### 💡 한 줄 요약
**"어떤 OS, 어떤 플랫폼에서도 돌아가는 개인용 AI 어시스턴트 플랫폼"**

### 🧩 왜 OpenClaw인가?
- **채널 통합**: 카카오톡(비공식 연동 가능), 슬랙, 텔레그램, 디스코드, iMessage 등 거의 모든 메시징 서비스와 연동됩니다. (Lobster Way 🦞)
- **자율성**: 내 컴퓨터나 서버에 설치하여 데이터 주권을 직접 관리합니다.
- **멀티 모델**: GPT-4, Claude 3.5, Gemini, Ollama(로컬)를 자유롭게 갈아끼며 사용할 수 있습니다.

---

## 2. 핵심 기능 (Key Highlights)

### ① Gateway & Node 아키텍처
- **Gateway**: 메시지를 주고받는 중앙 허브 역할을 합니다.
- **Node**: 실제 수행하는 에이전트 지능입니다. (macOS, iOS, Android 등 다양한 환경 지원)

### ② 다양한 채널 지원 (Channels)
- [WhatsApp](https://docs.openclaw.ai/channels/whatsapp), [Telegram](https://docs.openclaw.ai/channels/telegram), [Slack](https://docs.openclaw.ai/channels/slack), [Discord](https://docs.openclaw.ai/channels/discord), [Signal](https://docs.openclaw.ai/channels/signal), [iMessage](https://docs.openclaw.ai/channels/imessage) 등

### ③ 툴 및 자동화 (Tools & Automation)
- 단순 대화뿐만 아니라 구글 검색, 파일 관리, 파이썬 코드 실행 등의 도구를 에이전트에게 쥐여줄 수 있습니다.

---

## 3. [실급] OpenClaw 시작하기 (Setup Guide)

OpenClaw는 Node.js 기반으로 아주 쉽게 설치할 수 있습니다. (Node v22 이상 권장)

### ① 설치 (Installation)
터미널을 열고 다음 명령어를 입력하세요.

```bash
# 글로벌 설치
npm install -g openclaw@latest

# 초기 설정 도우미 실행 (Gateway 데몬 설치 포함)
openclaw onboard --install-daemon
```

### ② 실행 및 게이트웨이 설정
게이트웨이를 실행하여 에이전트가 통신할 수 있는 준비를 합니다.

```bash
# 게이트웨이 실행 (포트 18789 사용)
openclaw gateway --port 18789 --verbose
```

### ③ 메시지 보내기 테스트
연동된 채널로 메시지를 보내봅니다.

```bash
openclaw message send --to "+821012345678" --message "안녕 OpenClaw! 너는 이제 내 비서야."
```

---

## 4. [고급] 보안 및 페어링 (Security)

OpenClaw는 실제 내 계정과 연결되므로 보안이 중요합니다.
- **Pairing Code**: 모르는 사람이 내 비서에게 말을 걸면 '페어링 코드'를 요구합니다.
- **승인 방법**: 터미널에서 `openclaw pairing approve <채널명> <코드>`를 입력해 명시적으로 허용한 사용자만 비서와 대화하게 할 수 있습니다.

---

## 5. 실무/취업 활용 팁

- **개인 자동화**: "나한테 슬랙 메시지로 오늘 기사 요약해서 보내줘" 같은 개인화된 에이전트 구축 경험은 **AX(AI Experience)** 역량을 증명하기 좋습니다.
- **Tailscale 연동**: OpenClaw는 Tailscale과 연동되어 외부에서도 안전하게 내 서버로 접속할 수 있는 기능을 제공합니다.
- **포트폴리오**: 단순히 API를 쓰는 게 아니라, **"게이트웨이-에이전트 구조의 플랫폼을 구축하고 메시징 채널을 통합한 경험"**으로 어필하세요.
