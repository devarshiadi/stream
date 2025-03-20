from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

def get_m4a_url(video_url: str) -> str:
    """
    Extracts the best m4a audio stream URL from a YouTube video using yt_dlp.
    """
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/best',
        'quiet': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Try to find an m4a format URL
            for fmt in info.get('formats', []):
                if fmt.get('ext') == 'm4a' and fmt.get('url'):
                    return fmt.get('url')
            
            # Fallback to best audio URL if m4a is not found
            return info.get('url') if info.get('url') else None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract audio: {str(e)}")


@app.get("/{video_id}")
def get_audio_url(video_id: str):
    """
    FastAPI endpoint to return the m4a audio stream URL in JSON format.
    """
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    m4a_url = get_m4a_url(youtube_url)

    if not m4a_url:
        raise HTTPException(status_code=404, detail="m4a audio stream not found")

    return JSONResponse(content={"m4a_url": m4a_url})
