import asyncio
import logging

logger = logging.getLogger(__name__)

async def remove_selected_streams(input_file: str, output_file: str, remove_audios: list = [], remove_subs: bool = False):
    """
    FFmpeg command to remove selected audio tracks or subtitles using negative mapping
    """
    # Base command: input file-a read panni ella streams-um select panrom
    cmd = ["ffmpeg", "-y", "-i", input_file, "-map", "0"]
    
    # Specific audio stream index remove panna (-0:a:1, -0:a:2, etc.)
    if remove_audios:
        for audio_idx in remove_audios:
            cmd.extend(["-map", f"-0:a:{audio_idx}"])
            
    # Subtitles poorama remove panna (-0:s)
    if remove_subs:
        cmd.extend(["-map", "-0:s"])
        
    # Quality loss illama super fast-a finish panna Stream Copy (-c copy)
    cmd.extend(["-c", "copy", output_file])
    
    logger.info(f"Executing FFmpeg Command: {' '.join(cmd)}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FFmpeg Error: {stderr.decode()}")
            return False
            
        return output_file
    except Exception as e:
        logger.error(f"Execution Error: {e}")
        return False
      
