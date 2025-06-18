import pandas as pd
import os
import glob


# === A) Wczytywanie i łączenie danych Bluesky ===

def read_all_csv_from_folder(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    dfs = []
    # Lista nazw plików, które mają być ignorowane podczas wczytywania
    # Dodajemy zarówno CSV, jak i XLSX, aby uniknąć problemów
    files_to_ignore = ["przefiltrowany_bluesky.csv", "przefiltrowany_bluesky.xlsx"]

    for file_path in all_files:
        file_name = os.path.basename(file_path)  # Pobieramy tylko nazwę pliku
        if file_name not in files_to_ignore:
            dfs.append(pd.read_csv(file_path, encoding='utf-8'))

    if not dfs:  # Sprawdzamy, czy lista dfs nie jest pusta
        print(
            f"Brak oryginalnych plików CSV do wczytania w folderze: {folder_path}. Sprawdź, czy są tam pliki inne niż 'przefiltrowany_bluesky.csv'/'przefiltrowany_bluesky.xlsx'.")
        return pd.DataFrame()  # Zwracamy pustą ramkę danych

    return pd.concat(dfs, ignore_index=True)


bluesky_df = read_all_csv_from_folder("bluesky")

# Sprawdzenie, czy w ogóle coś wczytano
if bluesky_df.empty:
    print("Brak danych do przetworzenia po wczytaniu. Skrypt zakończy działanie.")
    exit()  # Zakończ działanie skryptu, jeśli nie ma danych

# === B) Wykrywanie podejrzanych autorów ===

# Zliczamy liczbę postów dla każdego autora
author_counts = bluesky_df["Autor"].value_counts()

# Uznajemy za podejrzanych tych, którzy mają np. >50 postów
threshold = 40
suspected_bots = author_counts[author_counts > threshold].index

# Filtrowanie – usuwamy posty od podejrzanych autorów
# TUTAJ UPEWNIAMY SIĘ, ŻE FILTRUJEMY ORYGINALNĄ RAMKĘ DANYCH (bluesky_df)
filtered_bluesky_df = bluesky_df[~bluesky_df["Autor"].isin(suspected_bots)]

# === C) Zapisujemy nowy przefiltrowany plik CSV i XLSX ===

# Upewnij się, że folder "bluesky" istnieje
if not os.path.exists("bluesky"):
    os.makedirs("bluesky")

# Zapis do CSV
filtered_csv_path = os.path.join("bluesky", "przefiltrowany_bluesky.csv")
filtered_bluesky_df.to_csv(filtered_csv_path, index=False)

# Zapis do XLSX
filtered_xlsx_path = os.path.join("bluesky", "przefiltrowany_bluesky.xlsx")
filtered_bluesky_df.to_excel(filtered_xlsx_path, index=False)

# Opcjonalnie – komunikaty pomocnicze
print(f"🧹 Usunięto {len(suspected_bots)} podejrzanych autorów (z więcej niż {threshold} postami).")
print(f"✅ Pozostało {len(filtered_bluesky_df)} postów po filtracji.")
print(f"Plik CSV został zapisany pod ścieżką: {filtered_csv_path}")
print(f"Plik XLSX został zapisany pod ścieżką: {filtered_xlsx_path}")