# Analiza tekstu z mediów społecznościowych
## Sondaże wyborcze 2025

Projekt napisany w Pythonie służący do analizy sentymentu wypowiedzi użytkowników mediów społecznościowych na temat wyborów prezydenckich 2025.

## Technologie i biblioteki

**Biblioteki użyte do pobierania danych z mediów społecznościowych:**
- [atproto](https://pypi.org/project/atproto/) – dostęp do danych z serwisu **Bluesky** za pomocą oficjalnego protokołu AT.  
- [PRAW](https://praw.readthedocs.io/) – obsługa **Reddita** poprzez oficjalne API.  
- [snscrape](https://github.com/JustAnotherArchivist/snscrape) – scrapowanie treści z **Twittera/X** (*wykorzystane w celach testowych, niestety paczka snscrape nie działa dla Twittera/X ze względu na zabezpieczenia platformy*).  

**Biblioteki umożliwiające analizę i przetwarzanie danych:**
- [pandas](https://pandas.pydata.org/) - wczytywanie, czyszczenie i transformacja danych
- [nltk](https://www.nltk.org/) – przetwarzanie języka naturalnego 

**Wizualizacja:**
- [matplotlib](https://matplotlib.org/) – tworzenie wykresów porównawczych i podsumowań.  

## Opis działania

1. **Pobieranie danych**
   - Posty pobierane są bezpośrednio z API Reddita i Bluesky (odpowiednio przez PRAW i atproto).  
   - Dodatkowo, pomocniczo użyto snscrape do scrapowania publicznych treści z Twittera.  
2. **Przygotowanie danych**
   - Wczytanie postów do ramek danych (`pandas`) i zapisywanie ich do plików `.csv` oraz `.xlsx`.  
   - Oczyszczenie tekstu:
      * **tokenizacja** tekstu na pojedyncze zdania, a następnie słowa,
      *  usuwanie **stopwords** (najczęstszych i nieistotnych słów),
      *  **lematyzacja** (sprowadzanie słów do formy podstawowej),
      *  tworzenie wykresu najczęściej występujących słów
      *  tworzenie **chmury słów (word cloud)** przedstawiającej najczęściej używane terminy.
3. **Filtrowanie postów potencjalnie stworzonych przez boty**
4. **Analiza sentymentu**  
   - Wykorzystanie narzędzia **VADER Sentiment** (z pakietu `nltk.sentiment.vader`) do oceny nastroju postów.  
   - Generowanie wartości: `pos`, `neg`, `neu` oraz współczynnika zbiorczego `compound`.  

5. **Wizualizacja wyników**  
   - Tworzenie wykresów porównujących wyniki dla poszczególnych platform - Reddit oraz BlueSky.
   - Tworzenie wykresów ilustrujących nastawienie sentymentalnie wobec kandydatów prezydenckich.
   - Analiza zbiorcza nastawienia użytkowników wobec wyborów i sondaży.  

