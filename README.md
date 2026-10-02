# 🚀 AV FILE TO LINK PRO

<p align="center">
  <img src="https://files.catbox.moe/wnh9aa.jpg" alt="AV FILE TO LINK PRO" width="720">
</p>

<p align="center">
  <b>Telegram Files → Secure Web Links → Fast Streaming</b><br>
  A production-ready Telegram File-to-Link bot built around <b>Pyrogram</b>, <b>aiohttp</b> and <b>MongoDB</b>.
</p>

<p align="center">
  <a href="https://t.me/AV_F2L_BOT"><img src="https://img.shields.io/badge/🤖_Demo_Bot-Start-red?style=for-the-badge&logo=telegram"></a>
  <a href="https://t.me/AV_SUPPORT_GROUP"><img src="https://img.shields.io/badge/💬_Support-Join-black?style=for-the-badge&logo=telegram"></a>
  <a href="https://github.com/Botsthe/AV-FILE-TO-LINK-PRO/blob/AV-BOTz-V4.26.8460/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=github"></a>
</p>

> **AV-BOTz-V4.26.8460** — the current development branch.

---

## ✨ What is AV FILE TO LINK PRO?

AV FILE TO LINK PRO turns Telegram media into shareable web links.

```text
📤 Telegram File
      ↓
🤖 AV FILE TO LINK PRO
      ↓
📦 Telegram Bin Channel
      ↓
🌐 Secure Web Route
      ↓
▶️ Stream / ⬇️ Download
```

The project combines a Telegram bot, database-backed user system and asynchronous web server so files can be served through browser-friendly links.

## ⚡ Core Stack

| Layer | Technology |
|---|---|
| Bot | Pyrogram |
| Web Server | aiohttp |
| Database | MongoDB / Motor |
| Media Source | Telegram |
| Streaming | Async HTTP + Range requests |
| Deployment | Koyeb / Render / Heroku / VPS |
| Configuration | Environment variables |

---

## 🔥 Feature Matrix

### 👤 User Experience
- 🚀 Direct stream and download links
- 🎬 Browser-friendly media playback
- 🔐 Password-protected links
- 📂 File listing and management
- 📦 Batch file processing
- 📱 Responsive web experience
- 📢 Force-subscription support
- 💎 Premium user system
- 🔗 Optional verification / shortlink flow

### 🛠️ Admin & System
- 📊 User and file statistics
- 🚫 Ban / unban controls
- 📢 Broadcast tools
- 💎 Premium expiry management
- 🔑 Password management
- 🗑️ User file cleanup
- 🔄 Restart / maintenance controls
- 🧩 Multi-client Telegram support
- 🌐 Koyeb-friendly web service

> Feature availability depends on the configuration and enabled environment variables.

---

## 🧠 Architecture

```text
                    ┌──────────────────┐
                    │      USER        │
                    └────────┬─────────┘
                             │
                       Telegram / Web
                             │
              ┌──────────────▼──────────────┐
              │     AV FILE TO LINK PRO     │
              │                              │
              │  Pyrogram  +  aiohttp       │
              └───────┬──────────┬───────────┘
                      │          │
               ┌──────▼─────┐ ┌──▼─────────┐
               │  MongoDB   │ │ Bin Channel│
               │ Users/Data │ │   Media    │
               └────────────┘ └────┬───────┘
                                    │
                              ┌─────▼─────┐
                              │ Web Stream│
                              │ / Download│
                              └───────────┘
```

---

## 🛡️ Security & Reliability

- 🔒 Credentials are configured through environment variables.
- 🔐 Protected links can require a password.
- 🧾 Stream routes validate link/hash information before serving media.
- 📡 HTTP Range requests are handled for browser-friendly seeking/downloads.
- ⚡ Async streaming avoids loading the complete media file into server memory.
- 🧩 Additional Telegram clients can be used for media workload distribution.
- 🚦 Maintenance and access controls can be enabled through configuration.

**Never commit your real Bot Token, API credentials or MongoDB URI to GitHub.**

---

# ⚙️ Environment Variables

<details>
<summary><b>📌 Required</b></summary>

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
ADMINS=123456789
OWNER_USERNAME=YOUR_USERNAME
DATABASE_URI=mongodb+srv://USERNAME:PASSWORD@HOST/DATABASE
BIN_CHANNEL=-100XXXXXXXXXX
LOG_CHANNEL=-100XXXXXXXXXX
URL=https://your-domain.example/
```

Get Telegram API credentials from [my.telegram.org](https://my.telegram.org) and your bot token from [@BotFather](https://t.me/BotFather).

</details>

<details>
<summary><b>🔗 Verification / Shortlink</b></summary>

```env
IS_VERIFY=False
IS_SECOND_VERIFY=False
IS_SHORTLINK=False
SHORTLINK_URL=
SHORTLINK_API=
SHORTENER_WEBSITE2=
SHORTENER_API2=
TUTORIAL_LINK_1=
TUTORIAL_LINK_2=
```

</details>

<details>
<summary><b>🌐 Server / Access</b></summary>

```env
PORT=8080
WORKERS=4
FSUB=False
ENABLE_LIMIT=False
MAINTENANCE_MODE=False
AUTH_CHANNEL=
CHANNEL=
SUPPORT=
```

</details>

---

# 🤖 Commands

<details>
<summary><b>📋 User Commands</b></summary>

```text
/start       Check bot status
/help        Show help
/about       About the bot
/files       List uploaded files
/del_files   Delete uploaded files
/plan        Show premium plans
/myplan      Show current plan
/batch       Batch mode
/link        Support link
/password    Set link password
```

</details>

<details>
<summary><b>👑 Admin Commands</b></summary>

```text
/ban
/unban
/broadcast
/pin_broadcast
/restart
/stats
/blocked
/add_premium
/remove_premium
/premium_user
/add_point
/remove_point
/check_pass
/delete_pass
/file_stats
/delfile
```

</details>

---

# 🚀 Deployment

## ☁️ Koyeb

The current project branch is:

```text
AV-BOTz-V4.26.8460
```

Recommended flow:

```text
GitHub Repository
      ↓
Select AV-BOTz-V4.26.8460
      ↓
Deploy as Web Service
      ↓
Set Environment Variables
      ↓
Expose PORT=8080
      ↓
Deploy 🚀
```

<a href="https://app.koyeb.com/deploy?type=git&repository=github.com/Botsthe/AV-FILE-TO-LINK-PRO&branch=AV-BOTz-V4.26.8460&name=AV-FILE-TO-LINK-PRO">
<img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy on Koyeb">
</a>

## 🖥️ VPS

```bash
git clone https://github.com/Botsthe/AV-FILE-TO-LINK-PRO.git
cd AV-FILE-TO-LINK-PRO
git checkout AV-BOTz-V4.26.8460

pip3 install -U -r requirements.txt

# Add your environment variables
nano .env

python3 bot.py
```

## ☁️ Render / Heroku

The repository can also be deployed through platforms supporting Python/Docker-style web services. Configure the same environment variables before starting the service.

---

# 📁 Project Structure

```text
AV-FILE-TO-LINK-PRO/
│
├── bot.py                  # Application entry point
├── info.py                 # Configuration & defaults
├── koyeb.yaml              # Koyeb service configuration
│
├── plugins/                # Telegram bot features
├── database/               # MongoDB operations
├── route/                  # Bot/web route modules
├── web/                    # aiohttp web layer
│   ├── bot/
│   └── stream_routes.py
│
├── requirements.txt
├── Dockerfile
├── LICENSE
└── README.md
```

---

# 🧪 Current Branch Focus

**AV-BOTz-V4.26.8460** includes reliability-focused work around:

- ✅ Async media streaming with `StreamResponse`
- ✅ HTTP Range handling
- ✅ Safer stream route processing
- ✅ Improved additional-client handling
- ✅ Environment-based configuration
- ✅ Protected link/hash validation
- ✅ Koyeb web-service compatibility

---

# 💎 AV BOTZ

<p align="center">
  <b>Built with Python • Telegram • AsyncIO • MongoDB</b><br>
  <i>Simple for users. Powerful for operators.</i>
</p>

<p align="center">
  <a href="https://github.com/Botsthe">GitHub</a> •
  <a href="https://t.me/BOT_OWNER26">Developer</a> •
  <a href="https://t.me/AV_SUPPORT_GROUP">Support</a> •
  <a href="https://av-botz.vercel.app/">Website</a>
</p>

<p align="center">
  <b>👑 AV BOTZ — Aman Vishwakarma</b>
</p>

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0**.

See [LICENSE](LICENSE) for the applicable license terms.

<p align="center">
  <b>🚀 AV FILE TO LINK PRO</b><br>
  <sub>Telegram Files → Web Links</sub>
</p>
