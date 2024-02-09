# Standard Library
import datetime
from datetime import timedelta

# Third Party Library
import pytz
from dateutil.relativedelta import relativedelta

# Project Library
from project.core.utils.exceptions import ImageProcessingError


def add_days_to_date(days=7):
    """
    This function will add the days to current date and returns the current date, expected date
    """
    utc_datetime = datetime.datetime.utcnow()
    current_date = utc_datetime.strftime("%Y-%m-%d")
    t_delta_days = timedelta(days=days)
    date_from_iso = datetime.date.fromisoformat(current_date)
    expected_date = date_from_iso - t_delta_days
    return current_date, expected_date


def add_months_to_date(start_date, months=12):
    """
    This function will add the months to current date and returns the expected date
    """
    utc_start_date = start_date.strftime("%Y-%m-%d")
    hours = start_date.strftime("%H:%M:%S.%f")
    relative_delta = relativedelta(months=months)
    purchased_date = datetime.date.fromisoformat(utc_start_date)
    warranty_date = purchased_date + relative_delta
    utc_date = warranty_date.strftime("%Y-%m-%d")
    warranty_date_time = utc_date + " " + hours
    return warranty_date_time


async def get_local_time(utc_time):
    if "." in str(utc_time):
        dtime_array = str(utc_time).split(".")
        utc_time = dtime_array[0]
    dtime = datetime.datetime.strptime(str(utc_time), "%Y-%m-%d %H:%M:%S")
    local_tz = pytz.timezone("Asia/Kolkata")
    local_time = dtime.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time


async def get_schedule(schedule_data):
    li_array = []
    for data in schedule_data:
        name = data["name"]
        start_date = data["startDate"]
        end_date = data["endDate"]
        start_date_time = await get_local_time(start_date)
        end_date_time = await get_local_time(end_date)
        if not data["recurring"]["enabled"]:
            li_array.append(
                {
                    "scheduleName": name,
                    "scheduleCategory": "Single",
                    "englishDateTime": f"{start_date_time.strftime('%I:%M %p')} to {end_date_time.strftime('%I:%M %p')}, From {start_date_time.strftime('%d %b %Y')} to {end_date_time.strftime('%d %b %Y')}.",
                }
            )
        elif data["recurring"]["enabled"]:
            if data["recurring"]["repeat"] == "daily":
                li_array.append(
                    {
                        "scheduleName": name,
                        "scheduleCategory": "Daily",
                        "englishDateTime": f"{start_date_time.strftime('%I:%M %p')} to {end_date_time.strftime('%I:%M %p')}, From {start_date_time.strftime('%d %b %Y')} to {end_date_time.strftime('%d %b %Y')}.",
                    }
                )
            elif data["recurring"]["repeat"] == "weekly":
                li_array.append(
                    {
                        "scheduleName": name,
                        "scheduleCategory": "Weekly",
                        "englishDateTime": f"{start_date_time.strftime('%I:%M %p')} to {end_date_time.strftime('%I:%M %p')}, From {start_date_time.strftime('%d %b %Y')} to {end_date_time.strftime('%d %b %Y')}, Occurs {list_of_days(data['recurring']['weekDays'])}",
                    }
                )
    return li_array


def list_of_days(schedule):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_days = [day for day in days_of_week if schedule.get(day.lower())]
    if len(selected_days) == 7:
        return "everyday."
    return f'every {", ".join(selected_days)}.'


def generate_date():
    """Generates the current date in the format '%Y/%m/%d'."""
    try:
        return datetime.datetime.now().strftime("%d/%m/%Y")
    except Exception as e:
        raise ImageProcessingError(f"Error generating date: {e}")
