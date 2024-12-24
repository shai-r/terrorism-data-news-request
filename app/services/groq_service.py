import os
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq

load_dotenv(verbose=True)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def send_request_to_model(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                    Analyze the following event and determine:
                    1. Whether it happened in the past, 
                        is happening today, or is planned for the future. 
                        Respond with one of the following 4 words only: 
                        Today, in the Past, in the Future, or Unknown.
                    2. The exact location of the event: 
                        include the word "City:" before the city name 
                        and "Country:" before the country name. 
                        If not available, return "City: Unknown" and "Country: Unknown."
                    3. The approximate date of the event (if possible) in "YYYY-MM-DD" format.
                        If not available, return the nearest date.
                        include the word "Date:" before

                    Event: {text}
                """,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.to_dict()["choices"][0]["message"]["content"]


def extract_category(content):
    if "past" in content.lower():
        return "past"
    elif "today" in content.lower() or "now" in content.lower():
        return "today"
    elif "future" in content.lower():
        return "future"
    else:
        return "unknown"


def extract_location(content):
    city = "Unknown"
    country = "Unknown"

    for line in content.split("\n"):
        line = line.strip()
        if "City:" in line:
            city = line.split("City:")[1].strip().title()
        if "Country:" in line:
            country = line.split("Country:")[1].strip().title()

    return city, country


def extract_date(content):
    for line in content.split("\n"):
        line = line.strip()
        if "Date:" in line:
            potential_date = line.split("Date:")[1].strip()
            try:
                datetime.strptime(potential_date, "%Y-%m-%d")
                return potential_date
            except ValueError:
                return "Unknown"


def classify_article(text):
    content = send_request_to_model(text)
    category = extract_category(content)
    city, country = extract_location(content)
    date = extract_date(content)

    return {
        "category": category,
        "city": city,
        "country": country,
        "date": date,
    }
