import SwiftUI

struct ContentView: View {
    private let columns = Array(repeating: GridItem(.flexible(), spacing: 12), count: 4)
    private let player = AnimalSoundPlayer()

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Animal Sound Pad")
                .font(.largeTitle.bold())

            Text("Premi un tasto per ascoltare il verso dell'animale.")
                .font(.headline)
                .foregroundStyle(.secondary)

            LazyVGrid(columns: columns, spacing: 12) {
                ForEach(animalSounds, id: \.name) { animal in
                    Button {
                        player.play(animal)
                    } label: {
                        VStack(spacing: 6) {
                            Text(animal.emoji)
                                .font(.system(size: 32))
                            Text(animal.name)
                                .font(.headline)
                                .foregroundStyle(.primary)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 12))
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .padding(20)
        .frame(minWidth: 760, minHeight: 560)
    }
}
