import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from info import URL, BIN_CHANNEL, CHANNEL, FSUB, MAX_FILES
from database.users_db import db
from web.utils.file_properties import get_hash
from utils import temp, get_size
from plugins.utils import is_user_allowed, is_user_joined
from Script import script

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    user_id = m.from_user.id

    if FSUB and not await is_user_joined(c, m):
        return

    if await db.is_user_blocked(user_id):
        await m.reply(
            "🚫 **Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.**\n\n"
            "🔄 **Cᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ɪғ ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ.**\n\n"
            "@AV_OWNER_BOT"
        )
        return

    if not await db.has_premium_access(user_id):
        is_allowed, remaining_time = await is_user_allowed(user_id)
        if not is_allowed:
            await m.reply_text(
                f"🚫 **Yᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ꜱᴇɴᴛ {MAX_FILES} ғɪʟᴇꜱ!**\n"
                f"\nPʟᴇᴀꜱᴇ **{remaining_time} Sᴇᴄᴏɴᴅꜱ** ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ।",
                quote=True
            )
            return

    file_id = m.document or m.video or m.audio
    file_name = file_id.file_name or f"AV_File_{int(time.time())}.mkv"
    file_size = get_size(file_id.file_size)

    try:
        forwarded = await m.forward(chat_id=BIN_CHANNEL)
        hash_str = get_hash(forwarded)

        if not hash_str:
            raise ValueError("Unable to generate file hash from forwarded message")

        base_url = URL.rstrip("/") + "/"
        stream = f"{base_url}watch/{forwarded.id}/AV_File_{int(time.time())}.mkv?hash={hash_str}"
        download = f"{base_url}{forwarded.id}?hash={hash_str}"
        file_link = f"https://t.me/{temp.U_NAME}?start=file_{forwarded.id}"

        await db.files.insert_one({
            "user_id": user_id,
            "file_name": file_name,
            "file_size": file_size,
            "file_id": forwarded.id,
            "hash": hash_str,
            "timestamp": time.time()
        })

        await forwarded.reply_text(
            f"Requested By: [{m.from_user.first_name}](tg://user?id={user_id})\n"
            f"User ID: {user_id}\nStream Link: {stream}",
            disable_web_page_preview=True,
            quote=True
        )

        await m.reply_text(
            script.CAPTION_TXT.format(CHANNEL, file_name, file_size, stream, download),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• ꜱᴛʀᴇᴀᴍ •", url=stream),
                    InlineKeyboardButton("• ᴅᴏᴡɴʟᴏᴀᴅ •", url=download)
                ],
                [
                    InlineKeyboardButton("• ɢᴇᴛ ғɪʟᴇ •", url=file_link),
                    InlineKeyboardButton(
                        "• ᴅᴇʟᴇᴛᴇ ғɪʟᴇ •",
                        callback_data=f"deletefile_{forwarded.id}"
                    )
                ],
                [InlineKeyboardButton("• ᴄʟᴏꜱᴇ •", callback_data="close_data")]
            ])
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await c.send_message(
            BIN_CHANNEL,
            f"⚠️ FloodWait: {e.value}s from {m.from_user.first_name}"
        )
    except Exception:
        await m.reply_text(
            "❌ **File process nahi ho payi. Please thodi der baad try karein.**",
            quote=True
        )
        raise
