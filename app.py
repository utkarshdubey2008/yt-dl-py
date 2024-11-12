import yt_dlp
import os
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

# Function to download video using yt-dlp
def download_video(video_url):
    try:
        # Configuration for yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            video_filename = f"downloads/{video_title}.mp4"
            return video_filename
    except Exception as e:
        return f"Error: {e}"

# API endpoint to download the video
@app.route('/download', methods=['GET'])
def api_download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Download the video
    video_filename = download_video(video_url)

    # If there was an error, return the error message
    if "Error" in video_filename:
        return jsonify({'error': video_filename}), 500

    # Send the downloaded video file
    return send_file(video_filename, as_attachment=True)

if __name__ == "__main__":
    # Ensure the download folder exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Run the app
    app.run(debug=True)
