import os
import glob
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import requests

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# === A) Wczytywanie i łączenie danych z folderów ===

def read_all_csv_from_folder(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    dfs = [pd.read_csv(file, encoding='utf-8') for file in all_files]
    return pd.concat(dfs, ignore_index=True)

reddit_df = read_all_csv_from_folder("reddit")
bluesky_df = pd.read_csv(os.path.join("bluesky", "przefiltrowany_bluesky.csv"), encoding='utf-8')
merged_df = pd.concat([reddit_df, bluesky_df], ignore_index=True)

# === B) Wyodrębnienie kolumny Treść i połączenie tekstów ===
texts = merged_df["Treść"].dropna().astype(str).str.lower()
full_text = " ".join(texts)

# === C) Tokenizacja ===
sentences = sent_tokenize(full_text, language='english')
print(f"Liczba zdań: {len(sentences)}")

word_lists = [word_tokenize(sentence, language='english') for sentence in sentences]
tokens = [token for sentence in word_lists for token in sentence]
print(f"Liczba tokenów: {len(tokens)}")

# === D) Usunięcie stopwords ===

# Funkcja pobierająca polskie stopwords z GitHuba
def load_polish_stopwords():
    stopwords_path = "stopwords-pl.txt"
    if not os.path.isfile(stopwords_path):
        print("Pobieram listę polskich stopwords z GitHub...")
        url = "https://raw.githubusercontent.com/stopwords-iso/stopwords-pl/master/stopwords-pl.txt"
        r = requests.get(url)
        if r.status_code == 200:
            with open(stopwords_path, "w", encoding="utf-8") as f:
                f.write(r.text)
        else:
            print("Nie udało się pobrać pliku stopwords z GitHub.")
            return set()
    with open(stopwords_path, encoding="utf-8") as f:
        words = set(line.strip() for line in f if line.strip() and not line.startswith("#"))
    return words

stop_words = set(stopwords.words("english"))
polish_stopwords = load_polish_stopwords()
stop_words.update(polish_stopwords)

# dodatkowe znaki do usunięcia
extra_stop = ["'s", "n't", "'ve", "'re", "http", "de", "pi", "–", ".", ",", ":", ";", "''", "’", "\"\"", "``", "`", "(", ")", "[", "]", "{", "}",
              "\\", "/", "?", "!", "-", "--", "'", "%", "#", "@", "$", "*", "...", "się", "że", "bo", "no", "już", "też", "czy", "by", "z", "a",
              "na", "do", "od", "i", "w", "o", "u", "jest", "był", "była", "są", "nie", "tak", "ale", "dla", "ten",
              "to", "tam", "tu", "tutaj", "wszyscy", "mnie", "ciebie", "go", "jej", "ich", "nam", "was", "mi", "ci",
              "niech", "bardzo", "bardziej", "mógł", "mogła", "może", "muszę", "musisz", "trzeba", "więc", "dlatego",
              "dlaczego", "żeby"]

stop_words.update(extra_stop)

tokens_no_stop = [t for t in tokens if t not in stop_words]

tokens_cleaned = [t for t in tokens_no_stop if t not in extra_stop]
print(f"Liczba tokenów po usunięciu stopwords: {len(tokens_cleaned)}")

# === E) Lematyzacja ===
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(t) for t in tokens_cleaned]
print(f"Liczba tokenów po lematyzacji: {len(lemmatized_tokens)}")

# === F) Częstość występowania słów ===
word_freq = Counter(lemmatized_tokens)
top_words = word_freq.most_common(10)
print("10 najczęściej występujących słów:")
for word, count in top_words:
    print(f"{word}: {count}")

# === G) Wykres słupkowy 10 najczęściej występujących słów===
plt.figure(figsize=(10, 5))
words, counts = zip(*top_words)
plt.bar(words, counts, color='skyblue')
plt.xlabel("Słowa")
plt.ylabel("Liczba wystąpień")
plt.title("10 najczęstszych słów")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("word_frequency.png")
plt.show()

# === H) Word Cloud ===
def generate_wordcloud(tokens):
    cloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(tokens))
    plt.figure(figsize=(12, 6))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("word_cloud.png")
    plt.show()

generate_wordcloud(lemmatized_tokens)
