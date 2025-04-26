from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User
from pyrogram.errors import FloodWait
from pyromod import listen
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
from config import api_id, api_hash, bot_token, auth_users, sudo_users
import sys
import re
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_health_server():
    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@bot.on_message(filters.command(["stop"]))
async def cancel_command(bot: Client, m: Message):
    user_id = m.from_user.id if m.from_user else None
    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply("**You Are Not Subscribed To This Bot\nContact - @Mahagoraxyz**", quote=True)
        return
    await m.reply_text("**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    user_id = m.from_user.id if m.from_user else None
    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply("**You Are Not Subscribed To This Bot\nContact - @HKOWNER0**", quote=True)
        return

    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt file**")
    input: Message = await bot.listen(editable.chat.id)

    if input.document:
        x = await input.download()
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"

        try:
            with open(x, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            links = []
            for line in lines:
                line = line.strip()
                if "://" in line:
                    title, url_part = line.split("://", 1)
                    url = "https://" + url_part.strip()

                    if not title.strip():
                        title = "Untitled"

                    title = re.sub(r'[^A-Za-z0-9\s]', '', title).strip()
                    if not title:
                        title = "Untitled"

                    links.append((title, url))
            os.remove(x)
        except Exception as e:
            await m.reply_text(f"Invalid file input. 🥲 Error: {e}")
            os.remove(x)
            return
    else:
        lines = input.text.splitlines()
        links = []
        for line in lines:
            line = line.strip()
            if "://" in line:
                title, url_part = line.split("://", 1)
                url = "https://" + url_part.strip()

                if not title.strip():
                    title = "Untitled"

                title = re.sub(r'[^A-Za-z0-9\s]', '', title).strip()
                if not title:
                    title = "Untitled"

                links.append((title, url))

    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    b_name = file_name if raw_text0 == 'd' else raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    res_map = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }
    res = res_map.get(raw_text2, "UN")

    await editable.edit("**Enter Your Name or send `de` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    CR = credit if raw_text3 == 'de' else raw_text3

    await editable.edit("**Enter Your PW Working Token\n\nOtherwise Send No**")
    input4: Message = await bot.listen(editable.chat.id)
    pw_token = input4.text
    await input4.delete(True)

    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send No")
    input6 = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "No"

    count = 1 if len(links) == 1 else int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'classplusapp' in url or "testbook.com" in url or "classplusapp.com/drm" in url or "media-cdn.classplusapp.com/drm" in url:
                headers = {
                    'host': 'api.classplusapp.com',
                    'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9',
                    'accept-language': 'EN',
                    'api-version': '18',
                    'app-version': '1.4.73.2',
                    'build-number': '35',
                    'connection': 'Keep-Alive',
                    'content-type': 'application/json',
                    'device-details': 'Xiaomi_Redmi 7_SDK-32',
                    'device-id': 'c28d3cb16bbdac01',
                    'region': 'IN',
                    'user-agent': 'Mobile-Android',
                    'accept-encoding': 'gzip'
                }
                url = url.replace('https://tencdn.classplusapp.com/', 'https://media-cdn.classplusapp.com/tencent/')
                params = {"url": f"{url}"}
                res = requests.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", params=params, headers=headers).json()

                if "testbook.com" in url or "classplusapp.com/drm" in url or "media-cdn.classplusapp.com/drm" in url:
                    url = res['drmUrls']['manifestUrl']
                else:
                    url = res["url"]

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                url_id = url.split("/")[-2]
                url = f"https://as-multiverse-b0b2769da88f.herokuapp.com/{url_id}/master.m3u8?token={pw_token}"

            name1 = links[i][0][:60]
            name = f'{str(count).zfill(3)}) {name1}'

            ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]" if "youtu" in url else f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'** {str(count).zfill(3)}.** {name1}\n**Batch Name :** {b_name}\n\n**Downloaded by : {CR}**'
                if "drive" in url:
                    ka = await helper.download(url, name)
                    await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc)
                    count += 1
                    os.remove(ka)
                    time.sleep(1)
                elif ".pdf" in url:
                    os.system(f'{cmd} -R 25 --fragment-retries 25')
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc)
                    count += 1
                    os.remove(f'{name}.pdf')
                else:
                    prog = await m.reply_text(f"**Downloading:** `{name}`\n**Quality:** {raw_text2}")
                    res_file = await helper.download_video(url, cmd, name)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, res_file, thumb, name)
                    count += 1
            except FloodWait as e:
                await m.reply_text(str(e))
                time.sleep(e.x)
                continue
            except Exception as e:
                await m.reply_text(f"**Failed File:** `{name}`\n**Link:** `{url}`\n\n**Reason:** {e}")
                count += 1
                continue
    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("🔰Done Boss🔰")

bot.run()
