from flask import Flask, request, jsonify
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Directory to save downloaded files
OUTPUT_DIR = "tests"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def download_mp3(youtube_id):
    try:
        youtube_url = f'https://www.youtube.com/watch?v={youtube_id}'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return {"status": "success", "message": f"Downloaded video with ID: {youtube_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Extract video_id from request JSON
        data = request.get_json()
        video_id = data.get("video_id")
        
        if not video_id:
            return jsonify({"status": "error", "message": "No video_id provided"}), 400

        # Call the download function
        result = download_mp3(video_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
