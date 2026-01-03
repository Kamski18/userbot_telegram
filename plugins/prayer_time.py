# plugins/prayer_time.py
import aiohttp
from datetime import date

async def remind(message):
    # Ayer Molek Coordinates
    lat, lon = 2.1627822, 102.3349452
    

    api_url = f"http://api.aladhan.com/v1/timings/{date.today()}?latitude={lat}&longitude={lon}&method=17"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                return "❌ Error fetching prayer times."
            
            data = await response.json()
            timings = data['data']['timings']

            # Create the list of prayers we want to show
            # We filter out "Sunset" and "Imsak" usually
            prayer_list = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
            
            msg = ["🕌 **Prayer Times (JAKIM)**"]
            msg.append(f"📅 `{date.today()}`\n")
            
            for prayer in prayer_list:
                time = timings.get(prayer)
                msg.append(f"**{prayer}:** `{time}`")
            
            return "\n".join(msg)