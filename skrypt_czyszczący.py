import pandas as pd
from sqlalchemy import create_engine
from thefuzz import process
import re
import requests

DB_URL = "postgresql+psycopg2://postgres:Zautomatyzowany@db.qdipiatvpvnhanwpzqhy.supabase.co:5432/postgres"
engine = create_engine(DB_URL)

KATALOG_PRODUKTOW = ["Laptop", "Myszka bezprzewodowa", "Monitor 4K", "Klawiatura mechaniczna", "Słuchawki"]


def dopasuj_produkt(brudna_nazwa):
    if pd.isna(brudna_nazwa) or str(brudna_nazwa).strip() == "":
        return "Brak nazwy"
    najlepszy_wynik, pewnosc = process.extractOne(str(brudna_nazwa), KATALOG_PRODUKTOW)
    if pewnosc >= 70:
        return najlepszy_wynik
    else:
        return "Wymaga weryfikacji"


print("KROK 1: Wczytywanie brudnych danych z Excela...")
df = pd.read_excel("C:\\Users\\karol\\PycharmProjects\\Zautomatyzowany-system-raportowania\\surowe_dane.xlsx",sheet_name=0, header=0)

print("KROK 2: Rozpoczynam inteligentne czyszczenie danych...")
df.dropna(subset=['ID'], inplace=True)
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
df.dropna(subset=['Data'], inplace=True)
df['Data'] = df['Data'].dt.date
df['Produkt'] = df['Produkt'].apply(dopasuj_produkt)
df['Kwota'] = df['Kwota'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['Kwota'] = pd.to_numeric(df['Kwota'], errors='coerce').fillna(0)

print("KROK 3: Zapisywanie wyczyszczonych danych do bazy PostgreSQL...")
df.to_sql('raporty_sprzedazowe', engine, if_exists='replace', index=False)

print("SUKCES! Skrypt naprawił błędy i wysłał dane do bazy.")

WEBHOOK_URL = "http://localhost:5678/webhook/e08af71d-c3d1-4f22-b060-bf88c9e606e7"

dane_do_wyslania = {
    "status": "sukces",
    "wiadomosc": "Dane naprawione i załadowane",
    "ilosc_wierszy": len(df)
}

try:
    response = requests.post(WEBHOOK_URL, json=dane_do_wyslania)
    if response.status_code == 200:
        print("KROK 4: Powiadomienie do n8n wysłane pomyślnie! Sprawdź maila.")
    else:
        print(f"KROK 4: Problem z n8n. Status: {response.status_code}")
except Exception as e:
    print(f"KROK 4: Błąd połączenia z n8n: {e}")