from time import strftime
from adhan import adhan
from adhan.methods import ISNA
from datetime import date

async def remind(message):
    coordinate = (2.1627822, 102.3349452)
    params = {"method" : 'ISNA'}
    today = date.today()

    times = adhan(day=today, location=coordinate, parameters=params)

    try:
        result = [f"Prayer time for **{today}**\n\n"]

        for name, time in times.items():
            formatted_time = strftime("%H : %M")
            result.append(f"**{name.capitalize}** : {formatted_time}")
        return "\n".join(result)
    except Exception as e:
        return e