import os
import json
import random
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

API_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_UQdP3RqooUCzwxoYYYdc7lFQADiHX13OMaGF")

CATEGORIES_FILE = 'categories.json'

def load_categories():
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_category(new_category):
    categories = load_categories()
    if new_category not in categories:
        categories.append(new_category)
        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_category = random.choice(load_categories())

    if request.method == "POST":
        if "new_category" in request.form:
            new_cat = request.form["new_category"].strip()
            if new_cat:
                save_category(new_cat)
                return redirect(url_for('index'))

        username = request.form.get("username")
        if username:
            insta_url = f'https://www.instagram.com/{username}/'
            api_url = f'https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={API_TOKEN}'

            payload = {
                "directUrls": [insta_url],
                "resultsLimit": 1,
                "resultsType": "details"
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code in [200, 201]:
                data = response.json()
                if data:
                    result = {
                        "username": data[0].get("username"),
                        "followers": data[0].get("followersCount"),
                        "profile_pic": data[0].get("profilePicUrlHD")
                    }

    return render_template("index.html", category=selected_category, result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
