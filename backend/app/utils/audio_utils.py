"""
Audio processing utilities
"""

import os
from fastapi import UploadFile, HTTPException
from loguru import logger


ALLOWED_AUDIO_EXTENSIONS = {
    "wav", "mp3", "m4a", "ogg", "flac", "aac", "wma", "opus", "webm"
}

MAX_FILE_SIZE = int(os.getenv("MAX_AUDIO_SIZE_MB", 10)) * 1024 * 1024  # MB to bytes


async def validate_audio_file(file: UploadFile) -> bool:
    """
    Validate uploaded audio file
    
    Args:
        file: Uploaded file
    
    Returns:
        True if valid
    
    Raises:
        HTTPException if invalid
    """
    # Check file extension
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}"
        )
    
    # Check file size
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    logger.info(f"File validated: {file.filename} ({file_size} bytes)")
    
    return True


def get_audio_duration(file_path: str) -> float:
    """Get audio file duration in seconds"""
    try:
        import soundfile as sf
        with sf.SoundFile(file_path) as audio:
            duration = len(audio) / audio.samplerate
            return duration
    except Exception as e:
        logger.error(f"Failed to get audio duration: {e}")
        return 0.0


def convert_audio_format(input_path: str, output_path: str, format: str = "wav"):
    """Convert audio file format"""
    try:
        from pydub import AudioSegment
        
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=format)
        
        logger.info(f"Converted audio: {input_path} → {output_path}")
        
        return output_path
    except Exception as e:
        logger.error(f"Audio conversion failed: {e}")
        raise
