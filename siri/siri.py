from pyrogram import Client, filters

import youtube_dl # youtube_dl is shit
from youtube_search import YoutubeSearch
import requests

import os
import time
import asyncio
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    m=await message.reply_text("▰▱▱▱")
    n=await m.edit("▰▰▱▱")
    s=await n.edit("▰▰▰▱")
    o=await s.edit("▰▰▰▰")
    await o.edit(text=Config.START_MSG.format(message.from_user.mention),
         disable_web_page_preview=True,
         reply_markup = InlineKeyboardMarkup(
           [[
             InlineKeyboardButton("🎧 ᴍᴜsɪᴄ.ᴘᴀɴᴅᴀ", url="telegram.dog/musicspanda")
           ],[
             InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Gxneo"),
             InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
           ]]))
                 
    
@Client.on_message(
    (
        filters.command(["song"]) |
        filters.regex("https://youtube.com/")
    ) &
    filters.group
)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply_text('**🔍 𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖳𝗁𝖾 𝖲𝗈𝗇𝗀...**')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 7000:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"εzяα" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**👎 ɴᴏᴛʜɪɴɢ ᴛᴏ ꜰᴏᴜɴᴅ 🥺 ᴛʀʏ ᴡɪᴛʜ ᴀɴᴏᴛʜᴇʀ**')
            return
    except Exception as e:
        m.edit(
            "**ᴇɴᴛᴇʀ sᴏɴɢ ɴᴀᴍᴇ ᴡɪᴛʜ /song ᴄᴏᴍᴍᴀɴᴅ**"
        )
        print(str(e))
        return
    m.edit("**⏫ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀...**")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'<b>❍ Title: <i>{title}</i>\n❍ Duration:</b> <b>{duration}</b>\n<b>❍ Link:</b> <b><a href={link}>Click Here</a></b>\n<b>❍ Requested By: {message.from_user.mention}</b>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML', title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('**ᴀɴ ɪɴᴛᴇʀɴᴀʟ ᴇʀʀᴏʀ ᴏᴄᴄᴇᴜʀᴇᴅ; ʀᴇᴘᴏʀᴛ ᴛʜɪs @GxNeo!!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

@Client.on_callback_query(filters.regex("close"))
async def close_dta(bot, query):
   await query.message.delete()
  
@Client.on_callback_query(filters.regex("gxneo"))
async def neo(bot, query):
   await query.answer(url="https://t.me/GXNeo")
