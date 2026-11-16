# MARTIAN DREAM V3

**MARTIAN DREAM V3** is a family-friendly science adventure about a young
student whose dream of reaching Mars turns into an unexpected mission to help
protect a colony. The story introduces space weather and the challenges of
living on Mars through dialogue, choices, and short interactive games.

Created by **Team AG10S** for the **NASA Space Apps Challenge Alexandria Local
Event**. The project is an independent event submission and is not an official
NASA product or endorsement.

The game is in English, designed to be approachable for readers ages 7–11, and
made to be enjoyable for older players too. It runs on desktop with keyboard
and mouse controls.

## The game

Suhail is researching whether people could live on Mars when he falls asleep
and wakes aboard a spacecraft. With the ship and colony facing dangerous space
weather, he must help Nout respond to a solar flare and a planet-wide dust
storm. The choices you make shape the colony's outcome.

Along the way, players can:

- Navigate a solar-flare challenge, avoiding radiation and using a timed shield.
- Help the colony through dust-storm tasks, including cleaning solar panels and
  repairing a communications antenna.
- Answer a short Mars science quiz and earn a mission certificate.
- Explore the Astronaut's Dictionary for friendly explanations of Mars and
  space-weather terms.

There are four possible endings. The game uses original story, art, and sound
assets, with a calm 1280×720 interface. No account, network connection, or
additional download is needed to play once Ren'Py is installed.

## Features

- A complete story with a classroom intro, a late-night research scene, and a dream sequence on Mars.
- **Solar Flare** minigame: dodge radiation, stay inside the moving safe zone, and use your shield.
- **Dust Storm** minigame: clean the solar panels, repair the antenna, answer a short Mars quiz, and earn a certificate.
- Four different endings based on the choices you make.
- A scrollable **Astronaut's Dictionary** on the main menu, with friendly explanations of space-weather and Mars terms.
- Custom art, sound effects, and a calm 1280×720 interface.
- No voice acting required, no external downloads, and no online features.

## Running the game

This project targets **Ren'Py 8.5.3**.

1. Install the Ren'Py 8.5.3 SDK.
2. Clone or download this repository to any folder on your computer.
3. Launch the project from the Ren'Py launcher, or run:

```sh
# Replace the path with the folder where you cloned this repository.
./renpy.sh "/path/to/MARTIAN-DREAM"
```

On Windows, open the Ren'Py launcher and select the cloned `MARTIAN-DREAM`
project folder.

## Controls

| Action | Control |
| --- | --- |
| Advance dialogue / choose an option | Left click, `Enter`, or `Space` |
| Open the game menu | `Esc` or right click |
| Solar Flare: move | Arrow keys, `WASD`, or the mouse |
| Solar Flare: dash | `Space` or `Shift` |
| Solar Flare: shield | `X` |
| Solar Flare: pause | `Esc` |
| Solar Flare: quit the minigame | `Esc`, then follow the on-screen prompt |
| Dust Storm: clean panels | Click each dirty panel three times |
| Dust Storm: repair antenna | Press **FIX!** while the marker is in the green zone |

The dialogue box is hidden during minigames so the play area stays clear. The quick menu is intentionally disabled.

## Project structure

```text
.
├── game/
│   ├── script.rpy          # Story, scenes, characters, and the ending
│   ├── solar_flare.rpy     # Solar Flare minigame
│   ├── dust_storm.rpy      # Dust Storm minigame, quiz, certificate, endings
│   ├── screens.rpy         # Menus, dictionary, dialogue UI
│   ├── options.rpy         # Game configuration and About text
│   ├── gui.rpy             # GUI constants and theme
│   ├── images/             # Backgrounds, sprites, badges, and effects
│   ├── audio/              # Music and sound effects
│   ├── fonts/              # Bundled font
│   └── gui/                # Ren'Py GUI images
├── Progress.md             # Development log and verification notes
├── agents.md               # Handoff guide for future contributors/AI agents
├── LICENSE                 # MIT License for the project
├── .gitignore              # Excludes saves, caches, compiled scripts, and logs
└── project.json            # Ren'Py project metadata
```

Generated files (`saves/`, `cache/`, `*.rpyc`, logs, and translations for the default language) are excluded by `.gitignore`.

## Development and verification

From the Ren'Py SDK folder, use the path to your cloned project:

```sh
./renpy.sh "/path/to/MARTIAN-DREAM" lint
./renpy.sh "/path/to/MARTIAN-DREAM" compile
```

Current lint baseline:

```text
160 dialogue blocks, 2,255 words, 12,349 characters
11 menus, 37 images, 32 screens
```

The UI, both minigames, all four endings, and the certificate flow have been smoke-tested with Ren'Py's built-in test framework. See `Progress.md` for the test log and `agents.md` for architecture details and common pitfalls.

## Credits

- **Engine:** [Ren'Py](https://www.renpy.org/) 8.5.3.
- **Created for:** NASA Space Apps Challenge Alexandria Local Event.
- **Team:** AG10S.
- **Story, code, and game design:** Team AG10S.
- **Font:** Vazirmatn, bundled under the SIL Open Font License.
- **Art and audio:** created for this project unless otherwise noted.

## License

This project is licensed under the [MIT License](LICENSE). You may use,
modify, and redistribute it, including commercially, provided you retain the
copyright and permission notice.

The copyright attribution credits Team AG10S. Third-party components retain
their own licenses; for example,
the bundled Vazirmatn font is licensed under the SIL Open Font License, and
Ren'Py is distributed under its own license.
