from flask import Flask, request, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__)

def download_media(link, media_type):
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)

        if media_type == "1":
            ydl_opts = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return f"Video downloaded: {info['title']}"
        elif media_type == "2":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return f"Audio downloaded: {info['title']}"
        else:
            return "Invalid choice. Please choose 1 for Video or 2 for Audio."

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    media_type = request.form['media_type']

    if not link or not media_type:
        return jsonify({'status': 'error', 'message': 'Missing parameters'})

    result = download_media(link, media_type)
    return jsonify({'status': 'success', 'message': result})

if __name__ == "__main__":
    app.run(debug=True)
