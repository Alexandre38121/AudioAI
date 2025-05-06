from flask import Flask, request, jsonify
import yt_dlp
import requests
import os

app = Flask(__name__)

@app.route("/extract-audio", methods=["POST"])
def extract_audio():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    output_filename = "audio.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    with open(output_filename, 'rb') as f:
        res = requests.post("https://api.gofile.io/uploadFile", files={"file": f})
        if res.status_code != 200:
            return jsonify({"error": "Upload failed"}), 500
        audio_url = res.json()['data']['downloadPage']

    os.remove(output_filename)

    return jsonify({"audio_url": audio_url})
