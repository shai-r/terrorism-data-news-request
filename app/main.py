import time

from app.services.data_service import process_and_save_articles

TIME_SLEEP = 120


def main():
    page = 1
    while True:
        print(f"Processing page {page}...")
        has_articles = process_and_save_articles(page)

        if not has_articles:
            print("No more articles found. Stopping...")

        print(f"Waiting for {TIME_SLEEP} seconds before fetching the next page...")
        time.sleep(TIME_SLEEP)
        page += 1

if __name__ == "__main__":
    main()
