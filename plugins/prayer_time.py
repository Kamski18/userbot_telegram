from time import strftime
from adhan import adhan
from datetime import date

async def remind(message):
    lat, lon = 2.1627822, 102.3349452
    params = {
        'fajr_angle' : 20.0,
        'isha_angle' : 18.0
    }
    today = date.today()

    try:
        result = [f"Prayer time for **{today}**\n\n"]
        times = adhan(day=today, location=(lat, lon), parameters=params)

        for name, p_time in times.items():
            formatted_time = p_time.strftime("%H : %M")
            result.append(f"**{name.capitalize()}** : {formatted_time}")
        return "\n".join(result)
    except Exception as e:
        return str(e) # remember to 'stringtify' the e!