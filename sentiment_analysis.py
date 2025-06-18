import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import glob
import os
import seaborn as sns

sns.set(style="whitegrid")
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    if not isinstance(text, str):
        return None
    return sentiment_analyzer.polarity_scores(text)

def classify_sentiment(compound):
    if compound >= 0.05:
        return 'pozytywny'
    elif compound <= -0.05:
        return 'negatywny'
    else:
        return 'neutralny'


def print_summary(df, label):
    combined_text = ' '.join(df['Treść'].dropna().astype(str))
    summary_scores = sentiment_analyzer.polarity_scores(combined_text)
    sentiment_counts = df['sentiment'].value_counts().reindex(['pozytywny', 'neutralny', 'negatywny'], fill_value=0)

    print(f"\n=== {label.upper()} ===")
    print("Liczba postów wg klasyfikacji sentymentu (analiza każdego posta osobno):")
    print(sentiment_counts)
    print(f"Średni compound_score (średnia z każdego posta): {df['compound'].mean():.3f}")

    print("\nZagregowane wyniki sentymentu (cały tekst jako jedna wypowiedź):")
    print(f"Pozytywny (pos): {summary_scores['pos']:.3f}")
    print(f"Negatywny (neg): {summary_scores['neg']:.3f}")
    print(f"Neutralny (neu): {summary_scores['neu']:.3f}")
    print(f"Zagregowany wynik (compound): {summary_scores['compound']:.3f}")


def analyze_and_prepare(df):
    df = df.copy()
    df['scores'] = df['Treść'].apply(analyze_sentiment)
    df['compound'] = df['scores'].apply(lambda s: s['compound'] if s else None)
    df['sentiment'] = df['compound'].apply(classify_sentiment)
    return df.drop(columns=['scores'])

def plot_sentiment_comparison(df, candidates, platforms, filename):
    plt.figure(figsize=(10,6))
    df_filtered = df[(df['kandydat'].isin(candidates)) & (df['zrodlo'].isin(platforms))]
    sns.countplot(data=df_filtered, x='sentiment', hue='kandydat', palette='Set2', order=['pozytywny', 'neutralny', 'negatywny'])
    plt.title(f"Porównanie sentymentu kandydatów na platformach: {', '.join(platforms)}")
    plt.xlabel('Sentyment')
    plt.ylabel('Liczba postów')
    plt.legend(title='Kandydat')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_platform_comparison(df, candidate, platforms, filename):
    plt.figure(figsize=(10,6))
    df_filtered = df[(df['kandydat'] == candidate) & (df['zrodlo'].isin(platforms))]
    sns.countplot(data=df_filtered, x='sentiment', hue='zrodlo', palette='pastel', order=['pozytywny', 'neutralny', 'negatywny'])
    plt.title(f"Porównanie platform dla {candidate}")
    plt.xlabel('Sentyment')
    plt.ylabel('Liczba postów')
    plt.legend(title='Platforma')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_total_sentiment_across_platforms(df, filename):
    plt.figure(figsize=(10,6))
    sns.countplot(data=df, x='sentiment', hue='zrodlo', order=['pozytywny', 'neutralny', 'negatywny'], palette='Set3')
    plt.title("Ogólny rozkład sentymentu na platformach")
    plt.xlabel("Sentyment")
    plt.ylabel("Liczba postów")
    plt.legend(title='Platforma')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_overall_sentiment_distribution(df, filename):
    plt.figure(figsize=(8, 6))
    sentiment_counts = df['sentiment'].value_counts().reindex(['pozytywny', 'neutralny', 'negatywny'], fill_value=0)
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values,
                hue=sentiment_counts.index, palette='Set3', legend=False)
    plt.title('Ogólne nastawienie społeczne do wyborów')
    plt.ylabel('Liczba postów')
    plt.xlabel('Sentyment')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def main():
    reddit_files = glob.glob('reddit/reddit_*.csv')
    reddit_dfs = []
    for file in reddit_files:
        name = os.path.basename(file).replace('.csv', '').replace('reddit_', '')
        df = pd.read_csv(file, encoding='utf-8')
        df['kandydat'] = name.capitalize()
        df['zrodlo'] = 'Reddit'
        df = analyze_and_prepare(df)
        df['platform_kandydat'] = df['zrodlo'] + '_' + df['kandydat']
        print_summary(df, f"{name} (Reddit)")
        reddit_dfs.append(df)

    try:
        df_bluesky = pd.read_csv('bluesky/przefiltrowany_bluesky.csv', encoding='utf-8')
        bluesky_dfs = []
        for candidate in ['trzaskowski', 'nawrocki']:
            df_filtered = df_bluesky[df_bluesky['Treść'].str.contains(candidate, case=False, na=False)].copy()
            if df_filtered.empty:
                print(f"Brak danych dla {candidate} (Bluesky)")
                continue
            df_filtered['kandydat'] = candidate.capitalize()
            df_filtered['zrodlo'] = 'Bluesky'
            df_filtered = analyze_and_prepare(df_filtered)
            df_filtered['platform_kandydat'] = df_filtered['zrodlo'] + '_' + df_filtered['kandydat']
            print_summary(df_filtered, f"{candidate} (Bluesky)")
            bluesky_dfs.append(df_filtered)
    except FileNotFoundError:
        print("Brak pliku przefiltrowany_bluesky.csv")
        bluesky_dfs = []

    df_all = pd.concat(reddit_dfs + bluesky_dfs, ignore_index=True)

    plot_sentiment_comparison(df_all, candidates=['Trzaskowski', 'Nawrocki'], platforms=['Reddit', 'Bluesky'], filename='porownanie_kandydatow_platformy.png')
    plot_platform_comparison(df_all, candidate='Trzaskowski', platforms=['Reddit', 'Bluesky'], filename='porownanie_platform_trzaskowski.png')
    plot_platform_comparison(df_all, candidate='Nawrocki', platforms=['Reddit', 'Bluesky'], filename='porownanie_platform_nawrocki.png')

    plot_overall_sentiment_distribution(df_all, filename='ogolny_sentyment_wyborczy.png')

if __name__ == '__main__':
    main()
