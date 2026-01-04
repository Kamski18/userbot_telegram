import aiohttp
from datetime import date, datetime
import pytz

async def remind(message):
    lat, lon = 2.1627822, 102.3349452
    api_url = f"https://api.waktusolat.app/v2/solat/gps/{lat}/{lon}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return "❌ **Error:** Could not connect to WaktuSolat.app"

                data = await response.json()
                malaysia = pytz.timezone("Asia/Kuala_Lumpur")
                utc = pytz.utc
                now_malaysia = datetime.now(malaysia)
                today_date = now_malaysia.date()
                today_day = today_date.day

                today_data = next(
                    (item for item in data["prayers"] if item["day"] == today_day),
                    None
                )

                if not today_data:
                    return "❌ **Error:** Could not find today's data."

                zone = data.get("zone", "Unknown Zone")
                msg = [f"🕌 **Prayer Times (Zone {zone})**"]
                msg.append(f"📅 `{date.today().strftime('%d %B %Y')}`\n")

                prayer_map = {
                    "Fajr": "fajr",
                    "Syuruk": "syuruk",
                    "Dhuhr": "dhuhr",
                    "Asr": "asr",
                    "Maghrib": "maghrib",
                    "Isha": "isha"
                }

                for label, key in prayer_map.items():
                    raw_time = today_data.get(key, "N/A")

                    if isinstance(raw_time, int):
                        time_str = datetime.fromtimestamp(raw_time, tz=utc).astimezone(malaysia).strftime("%H:%M")
                    else:
                        time_str = str(raw_time)[:5]

                    msg.append(f"**{label}:** `{time_str}`")

                msg.append("\n_Source: WaktuSolat.app (JAKIM)_")
                return "\n".join(msg)

    except Exception as e:
        return f"⚠️ **Error:** `{str(e)}`"
