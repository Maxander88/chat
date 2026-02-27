// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AnimalSoundPad",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "AnimalSoundPad", targets: ["AnimalSoundPadApp"])
    ],
    targets: [
        .executableTarget(
            name: "AnimalSoundPadApp",
            path: "Sources"
        )
    ]
)
