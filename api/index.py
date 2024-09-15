from flask import Flask, request, jsonify
import yt_dlp
import logging
import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for specific domains, methods, and headers
CORS(app, resources={r"/download": {"origins": "http://localhost:3000"}},
     methods=['POST', 'OPTIONS'],
     allow_headers=['Content-Type'])

logging.basicConfig(level=logging.INFO)

DOWNLOAD_DIR = 'danceteacher/frontend/src/assets/media'


def download_video(url):
    ydl_opts = {
        'verbose': True,  
        'restrictfilenames': True, 
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s-%(id)s.%(ext)s'),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info['title']
    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Download error: {e}")
        return None


@app.route('/download', methods=['POST'])
def download_and_host_video():
    url = request.json['url']
    video_title = download_video(url)
    
    if video_title:
        return jsonify({'message': f'Video "{video_title}" downloaded successfully'})
    else:
        return jsonify({'error': 'Failed to download video'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    app.run(debug=True)
