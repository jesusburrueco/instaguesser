from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_TOKEN = 'apify_api_UQdP3RqooUCzwxoYYYdc7lFQADiHX13OMaGF'  # Sustituye por tu token real

@app.route('/', methods=['GET', 'POST'])
def index():
    followers = None
    profile_pic = None
    username = None
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            url = f'https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={API_TOKEN}'
            payload = {
                "directUrls": [f'https://www.instagram.com/{username}/'],
                "resultsLimit": 1,
                "resultsType": "details"
            }
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code in [200, 201]:
                data = response.json()
                if data:
                    followers = data[0].get('followersCount')
                    profile_pic = data[0].get('profilePicUrlHD')
                else:
                    error = "No se encontraron datos para este usuario."
            else:
                error = f"Error al obtener los datos: {response.status_code}"

    return render_template('index.html',
                           followers=followers,
                           profile_pic=profile_pic,
                           username=username,
                           error=error)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
