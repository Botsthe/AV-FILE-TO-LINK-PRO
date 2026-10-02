import re
import os
import logging
from os import environ, getenv
from Script import script

# --- Helper Functions ---
def required_env(name):
    value = environ.get(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value.strip()

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "on"]:
        return True
    elif value.lower() in ["false", "no", "0", "off"]:
        return False
    return default

# =========================================================
# 🤖 BOT INFO & CREDENTIALS
# =========================================================
SESSION = environ.get('SESSION', 'Webavbot')
API_ID = int(required_env('API_ID'))
API_HASH = required_env('API_HASH')
BOT_TOKEN = required_env('BOT_TOKEN')

# Admin Settings
ADMINS = [int(x) for x in environ.get('ADMINS', '5977931010').split()]
OWNER_USERNAME = environ.get("OWNER_USERNAME", 'BOT_OWNER26')

# =========================================================
# 🗄️ DATABASE CONNECTION
# =========================================================
DB_URL = required_env('DATABASE_URI')
DB_NAME = environ.get('DATABASE_NAME', 'testing').strip() or 'testing'

# =========================================================
# 📢 CHANNELS & LOGS
# =========================================================
# Mandatory Channels
BIN_CHANNEL = int(environ.get("BIN_CHANNEL", '-1002114619001'))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1002114619001'))

# Feature Specific Logs
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", '-1002114619001'))
VERIFIED_LOG = int(environ.get('VERIFIED_LOG', '-1002114619001'))
SUPPORT_GROUP = int(environ.get("SUPPORT_GROUP", "-1002114619001"))

# Auth Channels (Safe Parsing)
auth_channel_str = environ.get("AUTH_CHANNEL", "-1002114619001")
AUTH_CHANNEL = [int(x) for x in auth_channel_str.split()] if auth_channel_str else []

# =========================================================
# 🔗 LINKS & URLS
# =========================================================
CHANNEL = environ.get('CHANNEL', 'https://t.me/AV_BOTz_UPDATE')
SUPPORT = environ.get('SUPPORT', 'https://t.me/AV_SUPPORT_GROUP')
TUTORIAL_LINK_1 = environ.get('TUTORIAL_LINK_1', 'https://t.me/1')
TUTORIAL_LINK_2 = environ.get('TUTORIAL_LINK_2', 'https://t.me/2')

# =========================================================
# 🔐 VERIFICATION & SHORTENER
# =========================================================
IS_VERIFY = is_enabled(environ.get("IS_VERIFY", "True"), True)
IS_SECOND_VERIFY = is_enabled(environ.get("IS_SECOND_VERIFY", "True"), True)
IS_SHORTLINK = is_enabled(environ.get('IS_SHORTLINK', "False"), False)

# Verification Config
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 60)) # In Minutes/Hours based on logic
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'mdiskshortner.link')
SHORTLINK_API = environ.get('SHORTLINK_API', '').strip()

# Second Verification Config
SHORTLINK_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "mdiskshortner.link")
SHORTLINK_API2 = environ.get("SHORTENER_API2", '').strip()

# =========================================================
# ⚙️ SETTINGS & LIMITS
# =========================================================
FSUB = is_enabled(environ.get("FSUB", "True"), True)
ENABLE_LIMIT = is_enabled(environ.get("ENABLE_LIMIT", "True"), True)
MAINTENANCE_MODE = is_enabled(environ.get("MAINTENANCE_MODE", "False"), False)

# Time & Rate Limits
TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
RATE_LIMIT_TIMEOUT = int(environ.get("RATE_LIMIT_TIMEOUT", "600"))

# File Limits
MAX_FILES = int(environ.get("MAX_FILES", "5"))
BATCH_LIMIT = int(environ.get('BATCH_LIMIT', 60))

# =========================================================
# 🖼️ MEDIA & CAPTIONS
# =========================================================
QR_CODE = environ.get('QR_CODE', 'https://graph.org/file/6afb4093d5ec5c4176979.jpg')
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/1669ab9af68eaa62c3ca4.jpg")
AUTH_PICS = environ.get('AUTH_PICS', 'https://envs.sh/AwV.jpg')
PICS = environ.get('PICS', 'https://ibb.co/VpTJNNCN')
FILE_PIC = environ.get('FILE_PIC', 'https://i.ibb.co/bj4My0bW/photo-2025-07-21-02-15-21-7529360175656861700.jpg')

FILE_CAPTION = environ.get('FILE_CAPTION', script.CAPTION)

# =========================================================
# 🌐 SERVER & APP CONFIG
# =========================================================
WORKERS = int(getenv('WORKERS', '4'))
MULTI_CLIENT = False
name = str(environ.get('name', 'avbotz'))

# Heroku & Port Config
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False
    APP_NAME = None

PORT = int(getenv('PORT', '2626'))
NO_PORT = is_enabled(getenv("NO_PORT", "False"), False)
HAS_SSL = is_enabled(getenv("HAS_SSL", "False"), False)
BIND_ADDRESS = getenv("WEB_SERVER_BIND_ADDRESS", "127.0.0.1")

# URL Generation
# Always prefer an explicit public URL on Koyeb/Cloudflare.
custom_url = environ.get("URL", "").strip()

if custom_url:
    URL = custom_url.rstrip("/") + "/"
else:
    FQDN = getenv("FQDN", "").strip()
    if FQDN:
        PROTOCOL = "https" if HAS_SSL else "http"
        PORT_SEGMENT = "" if NO_PORT else f":{PORT}"
        URL = f"{PROTOCOL}://{FQDN}{PORT_SEGMENT}/"
    else:
        # Never silently generate public links to 127.0.0.1.
        URL = ""
        logging.warning(
            "URL is not configured. Set URL to the public HTTPS address of this deployment."
        )
