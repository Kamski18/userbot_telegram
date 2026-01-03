import aiohttp
from datetime import date

async def remind(message):
    # Ayer Molek Coordinates
    lat, lon = 2.1627822, 102.3349452
    
    # We use the 'v2/solat/gps' endpoint which detects your zone automatically
    api_url = f"https://api.waktusolat.app/v2/solat/gps/{lat}/{lon}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return "❌ **Error:** Could not connect to WaktuSolat.app"
                
                data = await response.json()
                
                # 1. Get today's day number (e.g., 5 for the 5th of the month)
                today_day = date.today().day
                
                # 2. Find the entry for TODAY in the list of prayers
                # The API returns a list called "prayers" for the whole month
                today_data = next((item for item in data['prayers'] if item['day'] == today_day), None)

                if not today_data:
                    return "❌ **Error:** Could not find today's data."

                # 3. Format the message
                zone = data.get('zone', 'Unknown Zone')
                msg = [f"🕌 **Prayer Times (Zone {zone})**"]
                msg.append(f"📅 `{date.today().strftime('%d %B %Y')}`\n")
                
                # WaktuSolat.app uses lowercase keys: 'fajr', 'dhuhr', etc.
                # Timestamps are in UNIX format, but this API returns formatted strings like "06:05:00"
                prayer_map = {
                    'Fajr': 'fajr',
                    'Syuruk': 'syuruk', # Good to have for Dhuha/Ishraq limit
                    'Dhuhr': 'dhuhr',
                    'Asr': 'asr',
                    'Maghrib': 'maghrib',
                    'Isha': 'isha'
                }

                for label, key in prayer_map.items():
                    # The time comes as "13:20:00", we slice [:5] to get "13:20"
                    time_str = today_data.get(key, "N/A")[:5] 
                    
                    # Convert to AM/PM (Optional, but looks nicer)
                    # Simple trick: If strict 24h is fine, just remove this part
                    msg.append(f"**{label}:** `{time_str}`")

                msg.append("\n_Source: WaktuSolat.app (JAKIM)_")
                return "\n".join(msg)

    except Exception as e:
        return f"⚠️ **Error:** `{str(e)}`"