import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Masukkan YouTube API Key Anda di sini
YOUTUBE_API_KEY = 'AIzaSyALf2pvwRBXqgBMJdYDUaYujv6-FSc-Km4'

def search_youtube(query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}'
    headers = {
        'User-Agent': 'YourBotName/1.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Akan memunculkan exception untuk status HTTP 4xx/5xx
        data = response.json()
        if data.get('items'):
            video_id = data['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        return "Maaf, tidak ada hasil yang ditemukan."
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan saat mencari video: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.startswith('/yt'):
        query = incoming_msg.replace('/yt', '').strip()  # Ekstraksi kata kunci
        video_url = search_youtube(query)
        msg.body(f"Berikut adalah hasil pencarian untuk '{query}': {video_url}")
    else:
        msg.body("Maaf, saya tidak mengerti permintaan Anda. Gunakan format '/yt [pencarian]' untuk mencari musik.")

    return str(resp)

if __name__ == "__main__":
    # Jalankan server Flask di host 0.0.0.0 agar dapat diakses dari luar localhost
    app.run(host='0.0.0.0', port=5000, debug=True)
