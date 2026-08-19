from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.ffmpeg import remove_selected_streams

# User stream selections store panna temporary dict
USER_STREAM_SETTINGS = {}

@Client.on_callback_query(filters.regex("^stream_setting"))
async def stream_settings_handler(bot, query):
    user_id = query.from_user.id
    
    # Default settings
    if user_id not in USER_STREAM_SETTINGS:
        USER_STREAM_SETTINGS[user_id] = {"remove_audio": [], "remove_subs": False}
        
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"Audio 2 Removal: {'✅ ON' if 1 in USER_STREAM_SETTINGS[user_id]['remove_audio'] else '❌ OFF'}", 
                callback_data="toggle_audio_1"
            )
        ],
        [
            InlineKeyboardButton(
                f"Remove All Subtitles: {'✅ ON' if USER_STREAM_SETTINGS[user_id]['remove_subs'] else '❌ OFF'}", 
                callback_data="toggle_subs"
            )
        ],
        [
            InlineKeyboardButton("🚀 Start Renaming Process", callback_data="start_ffmpeg_process")
        ]
    ])
    
    await query.message.edit_text("⚙️ **Select Streams to Remove:**", reply_markup=buttons)

# Button click actions toggle panna logic
@Client.on_callback_query(filters.regex("^(toggle_audio_1|toggle_subs)$"))
async def toggle_settings(bot, query):
    user_id = query.from_user.id
    data = query.data
    
    if user_id not in USER_STREAM_SETTINGS:
        USER_STREAM_SETTINGS[user_id] = {"remove_audio": [], "remove_subs": False}
        
    if data == "toggle_audio_1":
        if 1 in USER_STREAM_SETTINGS[user_id]["remove_audio"]:
            USER_STREAM_SETTINGS[user_id]["remove_audio"].remove(1)
        else:
            USER_STREAM_SETTINGS[user_id]["remove_audio"].append(1)
            
    elif data == "toggle_subs":
        USER_STREAM_SETTINGS[user_id]["remove_subs"] = not USER_STREAM_SETTINGS[user_id]["remove_subs"]
        
    # Re-render keyboard with updated status
    await stream_settings_handler(bot, query)


# Main Renaming Function kulla Call panna vendiya logic
async def process_rename_with_ffmpeg(input_filepath, output_filepath, user_id):
    settings = USER_STREAM_SETTINGS.get(user_id, {"remove_audio": [], "remove_subs": False})
    
    # Stream Removal FFmpeg execution
    result = await remove_selected_streams(
        input_file=input_filepath,
        output_file=output_filepath,
        remove_audios=settings["remove_audio"],
        remove_subs=settings["remove_subs"]
    )
    
    return result
  
