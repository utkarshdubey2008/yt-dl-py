import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

# Options to bypass bot detection using a custom User-Agent
ydl_opts = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'format': 'best',  # Best video format
}

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Use yt-dlp to extract video info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            download_url = info_dict['url']  # Direct download URL

        return jsonify({"download_url": download_url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app when this script is executed
if __name__ == '__main__':
    app.run(debug=True)
