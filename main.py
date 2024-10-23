from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import yt_dlp

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

cur_dir = os.getcwd()

class DownloadRequest(BaseModel):
    link: str

@app.post("/download")
def download_video(request: DownloadRequest):
    youtube_di_options = {
        "format": 'best',
        "outtmpl": os.path.join(cur_dir, f"video-{request.link[-20:]}.mp4"),  # Use the last 11 characters of the link for uniqueness
    }

    try:
        with yt_dlp.YoutubeDL(youtube_di_options) as ydl:
            ydl.download([request.link])
        return {"message": "Download completed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
