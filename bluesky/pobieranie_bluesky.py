from atproto import Client
import pandas as pd
from datetime import datetime, timezone
import os
import time
from dateutil.parser import parse  # import parsera do konwersji stringów na datetime
from dotenv import load_dotenv
load_dotenv()

# Dane logowania
USERNAME = os.getenv("BLUESKY_USERNAME")
APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

# Parametry wyszukiwania
SEARCH_TERM = "wybory2025"
OUTPUT_DIR = "."
MAX_POSTS = 5000
START_DATE = datetime(2025, 5, 1, tzinfo=timezone.utc)

# Logowanie do Bluesky
client = Client()
try:
    client.login(USERNAME, APP_PASSWORD)
    print("✅ Zalogowano do Bluesky.")
except Exception as e:
    print(f"❌ Błąd logowania: {e}")
    exit(1)

# Pobieranie postów
all_posts = []
cursor = None

print(f"\n🔍 Szukam postów zawierających '{SEARCH_TERM}' od {START_DATE.date()}...\n")

while len(all_posts) < MAX_POSTS:
    try:
        response = client.app.bsky.feed.search_posts({
            "q": SEARCH_TERM,
            "limit": 100,
            "cursor": cursor
        })

        new_posts = []
        for item in response["posts"]:
            record = item["record"]

            # Konwersja created_at ze stringa na datetime
            created_at_str = record.created_at
            created_at = parse(created_at_str)

            if created_at >= START_DATE:
                new_posts.append([
                    created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    item["author"]["handle"],
                    getattr(record, "text", "").replace("\n", " ").strip(),
                    item["uri"]
                ])

        if not new_posts:
            print("ℹ️ Brak nowych pasujących postów lub koniec danych.")
            break

        all_posts.extend(new_posts)
        print(f"📥 Pobrano {len(all_posts)} postów do tej pory...")
        cursor = response["cursor"]  # tu zostawiamy oryginalnie

        if not cursor:
            print("🔚 Brak dalszego kursora – koniec wyników.")
            break

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Błąd podczas pobierania danych: {e}")
        break

# Zapis danych
if all_posts:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame(all_posts, columns=["Data", "Autor", "Treść", "Link"])
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values(by="Data", ascending=False)

    # Zapis do CSV i Excel
    csv_path = os.path.join(OUTPUT_DIR, f"bluesky_{SEARCH_TERM}.csv")
    xlsx_path = os.path.join(OUTPUT_DIR, f"bluesky_{SEARCH_TERM}.xlsx")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    df.to_excel(xlsx_path, index=False)

    print(f"\n✅ Zapisano {len(df)} postów do pliku:\n- CSV: {csv_path}\n- Excel: {xlsx_path}")
else:
    print("❗ Nie pobrano żadnych postów – nic nie zapisano.")
