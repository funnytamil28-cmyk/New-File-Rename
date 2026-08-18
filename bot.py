import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db
from plugins.stream_tools import get_media_streams, process_stream_removal
from plugins.rename import apply_text_transforms
from plugins.progress import progress_for_pyrogram  # Import Progress Helper

app = Client(
    "rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

if not os.path.exists(Config.DOWNLOAD_DIR):
    os.makedirs(Config.DOWNLOAD_DIR)

user_files = {}

@app.on_message(filters.document | filters.video)
async def handle_file(client, message):
    msg = await message.reply_text("📥 **Starting Download...**")
    start_time = time.time()
    
    # Progress Bar Added in Download!
    file_path = await message.download(
        file_name=Config.DOWNLOAD_DIR + "/",
        progress=progress_for_pyrogram,
        progress_args=("📥 **Downloading File...**", msg, start_time)
    )
    
    user_files[message.from_user.id] = file_path
    streams = get_media_streams(file_path)
    
    buttons = [
        [InlineKeyboardButton("🔇 Remove All Audio Tracks", callback_data="rem_audio")],
        [InlineKeyboardButton("💬 Remove All Subtitles", callback_data="rem_subs")],
        [InlineKeyboardButton("🚫 Remove Audio + Subtitles", callback_data="rem_both")],
        [InlineKeyboardButton("⏩ Skip & Process File", callback_data="process_no_stream")]
    ]
    
    await msg.edit_text(
        f"🎬 **File Downloaded!**\n\n📁 **File:** `{os.path.basename(file_path)}`\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data
    
    if user_id not in user_files:
        return await query.answer("⚠️ Session expired!", show_alert=True)
        
    input_path = user_files[user_id]
    output_path = os.path.join(Config.DOWNLOAD_DIR, "processed_" + os.path.basename(input_path))
    
    await query.message.edit_text("⚡ **Processing Streams with FFmpeg...**")
    
    try:
        if data == "rem_audio":
            process_stream_removal(input_path, output_path, remove_audio=True)
        elif data == "rem_subs":
            process_stream_removal(input_path, output_path, remove_subtitles=True)
        elif data == "rem_both":
            process_stream_removal(input_path, output_path, remove_audio=True, remove_subtitles=True)
        else:
            output_path = input_path

        final_filename = f"[AnimeHub]_{os.path.basename(input_path)}"
        final_path = os.path.join(Config.DOWNLOAD_DIR, final_filename)
        
        if os.path.exists(output_path) and output_path != input_path:
            os.rename(output_path, final_path)
        else:
            os.rename(input_path, final_path)

        # Upload Status Message & Timer
        upload_msg = await query.message.edit_text("📤 **Starting Upload...**")
        start_time = time.time()
        
        # Progress Bar Added in Upload!
        await client.send_document(
            chat_id=query.message.chat.id,
            document=final_path,
            caption=f"✅ **Done!**\n\n📁 `{final_filename}`",
            progress=progress_for_pyrogram,
            progress_args=("📤 **Uploading File...**", upload_msg, start_time)
        )
        
        # Cleanup Files
        for p in [input_path, output_path, final_path]:
            if os.path.exists(p):
                try: os.remove(p)
                except: pass
        del user_files[user_id]
        
        await upload_msg.delete()
        
    except Exception as e:
        await query.message.edit_text(f"❌ **Error:** `{str(e)}`")

if __name__ == "__main__":
    app.run()
  
