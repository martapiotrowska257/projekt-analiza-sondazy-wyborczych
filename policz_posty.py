import pandas as pd
import os

# Ścieżki do folderów z plikami CSV
folder_reddit = os.path.join(".", "reddit")
folder_bluesky = os.path.join(".", "bluesky")

# Filtrujemy pliki CSV
pliki_reddit = [f for f in os.listdir(folder_reddit) if f.endswith(".csv") and f.startswith("reddit_")]
pliki_bluesky = [f for f in os.listdir(folder_bluesky) if f.endswith(".csv") and f.startswith("bluesky_")]

suma_reddit = 0
suma_bluesky = 0

print("🔍 Zliczanie postów z plików Reddit:\n")
for plik in pliki_reddit:
    sciezka = os.path.join(folder_reddit, plik)
    try:
        df = pd.read_csv(sciezka)
        liczba = len(df)
        suma_reddit += liczba
        print(f"- {plik}: {liczba} postów")
    except Exception as e:
        print(f"❌ Błąd przy odczycie pliku {plik}: {e}")

print("\n🔍 Zliczanie postów z plików Bluesky:\n")
for plik in pliki_bluesky:
    sciezka = os.path.join(folder_bluesky, plik)
    try:
        df = pd.read_csv(sciezka)
        liczba = len(df)
        suma_bluesky += liczba
        print(f"- {plik}: {liczba} postów")
    except Exception as e:
        print(f"❌ Błąd przy odczycie pliku {plik}: {e}")

suma_laczna = suma_reddit + suma_bluesky

print(f"\n📊 Podsumowanie:")
print(f"• Łączna liczba postów z Reddita:  {suma_reddit}")
print(f"• Łączna liczba postów z Bluesky: {suma_bluesky}")
print(f"✅ Całkowita liczba postów:        {suma_laczna}")
