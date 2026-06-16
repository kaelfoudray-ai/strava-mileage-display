import os
import requests

ACCESS_TOKEN = os.environ["STRAVA_ACCESS_TOKEN"]

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
