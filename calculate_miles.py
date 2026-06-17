import os
import requests

CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]

token_response = requests.post(
    "https://www.strava.com/oauth/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
)

token_data = token_response.json()

print(token_response.status_code)
print(token_data)

ACCESS_TOKEN = token_data["access_token"]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

page = 1
per_page = 200

total_meters = 0

while True:
    url = f"https://www.strava.com/api/v3/athlete/activities?page={page}&per_page={per_page}"
    r = requests.get(url, headers=headers)
    activities = r.json()
    print(r.status_code)
    print(r.text)

    if not activities:
        break

    for a in activities:
        if a["type"] != "Run":
            continue

        if a["start_date"][:4] != "2026":
            continue

        total_meters += a["distance"]

    page += 1

miles = total_meters / 1609.34

print("Miles:", miles)

with open("miles.json", "w") as f:
    f.write(f'{{"miles": {miles}}}')
