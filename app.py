from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os

app = Flask(__name__)

# Function to download a single video
def download_video(link):
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download()
        return file_path, yt.title
    except Exception as e:
        return str(e), None

# Function to download a playlist
def download_playlist(link):
    try:
        p = Playlist(link)
        file_paths = []
        titles = []
        for video in p.videos:
            stream = video.streams.get_highest_resolution()
            file_path = stream.download()
            file_paths.append(file_path)
            titles.append(video.title)
        return file_paths, titles
    except Exception as e:
        return str(e), None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    download_type = request.form['download_type']

    if not link or not download_type:
        return jsonify({'status': 'error', 'message': 'Missing parameters'})

    if download_type == 'video':
        file_path, title = download_video(link)
        if title:
            return jsonify({'status': 'success', 'file': file_path, 'title': title})
        else:
            return jsonify({'status': 'error', 'message': file_path})
    elif download_type == 'playlist':
        file_paths, titles = download_playlist(link)
        if titles:
            return jsonify({'status': 'success', 'files': file_paths, 'titles': titles})
        else:
            return jsonify({'status': 'error', 'message': file_paths})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid download type'})

if __name__ == "__main__":
    app.run(debug=True)
