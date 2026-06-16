Automatyczny rurociąg danych z modułem oczyszczania danych

Ten projekt to kompletny system ETL, który automatyzuje pobieranie, czyszczenie i archiwizacje brudnych danych sprzedażowych z plików Excel, a następnie powiadamia użytkowników o sukcesie operacji bezpośrednio na adres email.
Ręczne przeklejanie i poprawianie raportów to proces podatny na błędy i pochłaniający czas. System ten rozwiązuje ten problem poprzez:
1. Automatyczne wczytywanie surowych plików `.xlsx`.
2. Rozpoznawanie i naprawianie błędów ludzkich (np. literówek w nazwach produktów, błędnych formatów dat).
3. Bezpieczny zapis gotowych danych w chmurowej bazie SQL.
4. Orkiestrację całego procesu i wysyłkę powiadomień (n8n + Webhooki).

Architektura i Stack Technologiczny
* **Język:** Python 3.14
* **Przetwarzanie danych:** Pandas, TheFuzz (Fuzzy Matching), RegEx
* **Baza danych:** PostgreSQL (Supabase) via SQLAlchemy
* **Orkiestracja i Automatyzacja:** n8n (hostowany w Dockerze)
* **Powiadomienia:** REST API (Webhooki), Email (SMTP)

 Główne funkcjonalności 
Skrypt nie opiera się na sztywnym poprawianiu konkretnych błędów (tzw. hardcoding), lecz używa uniwersalnej logiki:
* **Fuzzy Matching:** Użycie algorytmu odległości Levenshteina do oceny prawdopodobieństwa literówek (np. system sam wie, że "Lptop" to "Laptop").
* **Type Coercion & RegEx:** Agresywne filtry oczyszczające kwoty z walut i spacji oraz standaryzujące formaty dat (wymuszanie typu daty).
* **Walidacja krytyczna:** Automatyczne odrzucanie wierszy bez unikalnych identyfikatorów (ID).

 Bezpieczeństwo (Security Note)
Ze względów bezpieczeństwa, plik `skrypt_czyszczący.py` widoczny w repozytorium zawiera placeholdery w miejscach danych wrażliwych. W środowisku produkcyjnym dane dostępowe (Connection String do bazy PostgreSQL oraz Webhook URL) są zarządzane za pomocą zmiennych środowiskowych (plik `.env`). W eksportowanym pliku z n8n (`workflow.json`) poświadczenia SMTP zostały usunięte.

 Jak uruchomić projekt lokalnie?

1. Sklonuj repozytorium:
   `git clone https://github.com/TwojLogin/nazwa-repozytorium.git`
2. Zainstaluj wymagane biblioteki:
   `pip install pandas openpyxl sqlalchemy psycopg2-binary thefuzz[levenshtein] requests`
3. Uzupełnij zmienne `DB_URL` oraz `WEBHOOK_URL` we własnym środowisku.
4. Uruchom kontener n8n w Dockerze:
   `docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n`
5. Zaimportuj plik `workflow.json` w interfejsie n8n i aktywuj przepływ.
6. Uruchom skrypt:
   `python skrypt_czyszczący.py`
