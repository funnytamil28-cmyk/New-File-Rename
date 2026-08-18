import subprocess
import json

def get_media_streams(input_file):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "stream=index,codec_type,codec_name:stream_tags=language,title",
        "-of", "json",
        input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        return data.get("streams", [])
    except Exception as e:
        print("FFprobe Error:", e)
        return []

def process_stream_removal(input_file, output_file, remove_audio=False, remove_subtitles=False, remove_stream_index=None):
    cmd = ["ffmpeg", "-y", "-i", input_file]
    
    if remove_stream_index is not None:
        cmd.extend(["-map", "0", "-map", f"-0:{remove_stream_index}", "-c", "copy"])
    else:
        cmd.extend(["-map", "0:v"])
        if not remove_audio:
            cmd.extend(["-map", "0:a?"])
        if not remove_subtitles:
            cmd.extend(["-map", "0:s?"])
        cmd.extend(["-c", "copy"])

    cmd.append(output_file)
    subprocess.run(cmd, check=True)
    return output_file
  
