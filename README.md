# Duck Clock (Windows 10)

Piccola applicazione desktop (400x200) che funziona come:
- Orologio digitale
- Sveglia (orario HH:MM)
- Avviso/prompt tra N minuti
- Suono "papera" automatico ogni 5 minuti

## Requisiti
- Windows 10
- Python 3.10+

## Avvio
```bash
python duck_clock.py
```

## Note
Su Windows il suono usa `winsound.Beep`; su altri sistemi stampa solo `Quack!` in console.
