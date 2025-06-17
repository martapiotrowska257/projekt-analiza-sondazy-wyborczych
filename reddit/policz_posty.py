import pandas as pd
import os

# Ścieżka do folderu, w którym są Twoje pliki CSV
folder_path = "."

# Lista plików, które chcesz zliczyć (można dać filtr .startswith)
plik_csv = [f for f in os.listdir(folder_path) if f.endswith(".csv") and f.startswith("reddit_")]

suma = 0

print("Zliczanie postów w plikach:\n")

for plik in plik_csv:
    sciezka = os.path.join(folder_path, plik)
    try:
        df = pd.read_csv(sciezka)
        liczba = len(df)
        suma += liczba
        print(f"- {plik}: {liczba} postów")
    except Exception as e:
        print(f"! Błąd przy odczycie pliku {plik}: {e}")

print(f"\n✅ Łączna liczba postów we wszystkich plikach: {suma}")
