import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db
from plugins.stream_tools import get_media_streams, process_stream_removal
from plugins.rename import apply_text_transforms
from plugins.progress import progress_for_pyrogram

app = Client(
    "rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

if not os.path.exists(Config.DOWNLOAD_DIR):
    os.makedirs(Config.DOWNLOAD_DIR)

user_files = {}

# --- COMMAND HANDLERS ---

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "👋 **Welcome to Multi-Feature File Rename & Stream Remover Bot!**\n\n"
        "📹 Video or Document anuppunga. Audio/Subtitle remove panni, custom prefix and caption oda upload panni tharendren.\n\n"
        "📖 Commands list paarka `/help` type panga."
    )

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "🛠️ **Bot Commands Guide:**\n\n"
        "🔹 `/set_prefix [text]` - Prefix set panna (e.g., `/set_prefix [AnimeHub]`)\n"
        "🔹 `/see_prefix` - Enna prefix save aagi irukunu paarka\n"
        "🔹 `/del_prefix` - Prefix delete panna\n"
        "🔹 `/set_caption [text]` - Custom caption set panna\n"
        "🔹 `/see_caption` - Save aana caption paarka\n"
        "🔹 `/del_caption` - Caption delete panna\n\n"
        "📁 **Usage:** File/Video anuppiyavudan Inline buttons varum. Audio/Subtitle tracks select panni remove pannaalaam."
    )
    await message.reply_text(help_text)

# --- PREFIX COMMANDS ---

@app.on_message(filters.command("set_prefix"))
async def set_prefix(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/set_prefix [AnimeHub]`")
    prefix = message.text.split(None, 1)[1]
    await db.set_user_data(message.from_user.id, "prefix", prefix)
    await message.reply_text(f"✅ **Prefix Saved:** `{prefix}`")

@app.on_message(filters.command("see_prefix"))
async def see_prefix(client, message):
    user_settings = await db.get_user_data(message.from_user.id)
    prefix = user_settings.get("prefix", "No prefix set!")
    await message.reply_text(f"🔍 **Current Prefix:** `{prefix}`")

@app.on_message(filters.command("del_prefix"))
async def del_prefix(client, message):
    await db.delete_user_setting(message.from_user.id, "prefix")
    await message.reply_text("🗑️ **Prefix deleted successfully!**")

# --- CAPTION COMMANDS ---

@app.on_message(filters.command("set_caption"))
async def set_caption(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/set_caption Downloaded by MyBot`")
    caption = message.text.split(None, 1)[1]
    await db.set_user_data(message.from_user.id, "caption", caption)
    await message.reply_text(f"✅ **Caption Saved:**\n`{caption}`")

@app.on_message(filters.command("see_caption"))
async def see_caption(client, message):
    user_settings = await db.get_user_data(message.from_user.id)
    caption = user_settings.get("caption", "No custom caption set!")
    await message.reply_text(f"🔍 **Current Caption:**\n`{caption}`")

@app.on_message(filters.command("del_caption"))
async def del_caption(client, message):
    await db.delete_user_setting(message.from_user.id, "caption")
    await message.reply_text("🗑️ **Caption deleted successfully!**")

# --- MAIN FILE PROCESSOR ---

@app.on_message(filters.document | filters.video)
async def handle_file(client, message):
    msg = await message.reply_text("📥 **Starting Download...**")
    start_time = time.time()
    
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

        # Get Saved User Settings from MongoDB
        user_settings = await db.get_user_data(user_id)
        prefix = user_settings.get("prefix", "")
        custom_caption = user_settings.get("caption", None)
        
        final_filename = apply_text_transforms(os.path.basename(input_path), prefix=prefix)
        final_path = os.path.join(Config.DOWNLOAD_DIR, final_filename)
        
        if os.path.exists(output_path) and output_path != input_path:
            os.rename(output_path, final_path)
        else:
            os.rename(input_path, final_path)

        upload_msg = await query.message.edit_text("📤 **Starting Upload...**")
        start_time = time.time()
        
        caption_text = custom_caption if custom_caption else f"✅ **Done!**\n\n📁 `{final_filename}`"
        
        await client.send_document(
            chat_id=query.message.chat.id,
            document=final_path,
            caption=caption_text,
            progress=progress_for_pyrogram,
            progress_args=("📤 **Uploading File...**", upload_msg, start_time)
        )
        
        # Clean up local storage
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
    
