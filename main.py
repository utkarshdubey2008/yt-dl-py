from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return "Please provide a YouTube video URL.", 400

    try:
        # Setup yt-dlp options
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'video.%(ext)s',
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Send the downloaded video
        return send_file('video.mp4', as_attachment=True, download_name='video.mp4')

    except Exception as e:
        return f"Error downloading video: {str(e)}", 500

    finally:
        # Clean up the downloaded file after sending
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")


if __name__ == "__main__":
    app.run(debug=True)
