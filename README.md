# Gestore Verifiche Periodiche (Windows 10)

Applicazione desktop con interfaccia grafica (Tkinter) per gestire le verifiche periodiche degli apparecchi.

## Funzioni principali

- Caricamento file Excel (`.xlsx`/`.xls`).
- Aggiornamento del database SQLite locale (`verifiche.db`) con i clienti.
- Per ogni cliente viene mantenuta **l'ultima data di verifica**.
- Visualizzazione immediata dei clienti in tabella.

## Formato Excel richiesto

Il file Excel deve contenere almeno queste colonne:

- `Cliente`
- `Data_Verifica`

Colonne opzionali:

- `Email`
- `Telefono`

Sono accettati vari formati data (es. `2026-01-31`, `31/01/2026`, `31-01-2026`).

## Avvio in sviluppo

```bash
python -m venv .venv
source .venv/bin/activate  # su Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Creare un eseguibile per Windows 10

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name GestoreVerifiche app.py
```

Il file eseguibile sarà in `dist/GestoreVerifiche.exe`.
