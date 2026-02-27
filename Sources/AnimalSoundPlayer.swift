import AVFoundation

struct AnimalSound {
    let name: String
    let emoji: String
    let onomatopoeia: String
}

@MainActor
final class AnimalSoundPlayer {
    private let synthesizer = AVSpeechSynthesizer()

    func play(_ sound: AnimalSound) {
        let utterance = AVSpeechUtterance(string: sound.onomatopoeia)
        utterance.voice = AVSpeechSynthesisVoice(language: "it-IT")
        utterance.rate = 0.42
        utterance.pitchMultiplier = 1.25
        utterance.volume = 1.0

        synthesizer.stopSpeaking(at: .immediate)
        synthesizer.speak(utterance)
    }
}

let animalSounds: [AnimalSound] = [
    AnimalSound(name: "Cane", emoji: "🐶", onomatopoeia: "Bau bau!"),
    AnimalSound(name: "Gatto", emoji: "🐱", onomatopoeia: "Miao miao!"),
    AnimalSound(name: "Mucca", emoji: "🐮", onomatopoeia: "Muuu!"),
    AnimalSound(name: "Pecora", emoji: "🐑", onomatopoeia: "Beee!"),
    AnimalSound(name: "Cavallo", emoji: "🐴", onomatopoeia: "Ih ih!"),
    AnimalSound(name: "Gallina", emoji: "🐔", onomatopoeia: "Coccodè!"),
    AnimalSound(name: "Gallo", emoji: "🐓", onomatopoeia: "Chicchirichì!"),
    AnimalSound(name: "Maiale", emoji: "🐷", onomatopoeia: "Oink oink!"),
    AnimalSound(name: "Anatra", emoji: "🦆", onomatopoeia: "Qua qua!"),
    AnimalSound(name: "Asino", emoji: "🫏", onomatopoeia: "Ii-aa!"),
    AnimalSound(name: "Leone", emoji: "🦁", onomatopoeia: "Roooar!"),
    AnimalSound(name: "Tigre", emoji: "🐯", onomatopoeia: "Grrr!"),
    AnimalSound(name: "Elefante", emoji: "🐘", onomatopoeia: "Prrr!"),
    AnimalSound(name: "Scimmia", emoji: "🐵", onomatopoeia: "Uu uu aa aa!"),
    AnimalSound(name: "Gufo", emoji: "🦉", onomatopoeia: "Uh uh!"),
    AnimalSound(name: "Lupo", emoji: "🐺", onomatopoeia: "Auuuu!"),
    AnimalSound(name: "Rana", emoji: "🐸", onomatopoeia: "Cra cra!"),
    AnimalSound(name: "Ape", emoji: "🐝", onomatopoeia: "Bzzz!"),
    AnimalSound(name: "Serpente", emoji: "🐍", onomatopoeia: "Ssssss!"),
    AnimalSound(name: "Delfino", emoji: "🐬", onomatopoeia: "Iiii-iii!"),
]
