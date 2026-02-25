# Orologio analogico trasparente (300x300)

Programma grafico in Python (Tkinter) che mostra un **orologio analogico** sempre a video, con **dimensione 300x300 px**, **sfondo trasparente** e **lancette che cambiano colore ogni secondo**.

## Requisiti

- Python 3.10+
- Windows (la trasparenza con `-transparentcolor` è pensata per Windows)

## Avvio rapido

```bash
python analog_clock_transparent.py
```

## Creazione EXE

Da prompt Windows:

```bat
build_exe.bat
```

Output previsto:

- `dist\OrologioAnalogico.exe`

## Note

- Lo sfondo trasparente usa una chiave colore (`#00ff00`) tramite `wm_attributes("-transparentcolor", ...)`.
- La finestra è `topmost` per restare visibile.
