from urllib.parse import quote

def generate_reminder(task):

    text = quote(task)

    link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={text}"

    return link