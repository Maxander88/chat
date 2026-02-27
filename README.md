# Animal Sound Pad (macOS)

Piccola app grafica per macOS con **20 tasti**, dove ogni tasto riproduce il verso di un animale.

## Requisiti

- macOS 13 o superiore
- Xcode 15 o superiore

## Avvio rapido

1. Apri il progetto come Swift Package in Xcode (`File > Open...` e seleziona la cartella del repo).
2. Scegli un target macOS locale.
3. Premi **Run**.

## Funzionalità

- Interfaccia a griglia con 20 pulsanti.
- Ogni pulsante mostra emoji + nome animale.
- Riproduzione del verso con sintesi vocale italiana.

## Personalizzazione

L'elenco dei suoni è in `Sources/AnimalSoundPlayer.swift` nella costante `animalSounds`.
Puoi cambiare testo, animali o onomatopee in modo semplice.
