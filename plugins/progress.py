import time
import math

def Humanbytes(size):
    if not size:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def Time_formatter(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((f"{days}d, " if days else "") +
           (f"{hours}h, " if hours else "") +
           (f"{minutes}m, " if minutes else "") +
           (f"{seconds}s" if seconds else ""))
    return tmp if tmp else "0s"

async def progress_for_pyrogram(current, total, ud_type, message, start_time):
    now = time.time()
    diff = now - start_time
    
    # Refresh message every 4 seconds to avoid Telegram API FloodWait
    if round(diff % 4.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = Time_formatter(math.ceil((total - current) / speed))
        
        # Design Progress Bar [■■■■□□□□□□]
        filled_blocks = math.floor(percentage / 10)
        progress_bar = "■" * filled_blocks + "□" * (10 - filled_blocks)
        
        tmp = (
            f"**{ud_type}**\n\n"
            f"[{progress_bar}] `{percentage:.1f}%`\n\n"
            f"🚀 **Speed:** `{Humanbytes(speed)}/s`\n"
            f"📦 **Done:** `{Humanbytes(current)}` / `{Humanbytes(total)}`\n"
            f"⏱️ **ETA:** `{time_to_completion}`"
        )
        
        try:
            await message.edit_text(text=tmp)
        except Exception:
            pass
          
