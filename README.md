# MARTIAN DREAM V3

A short, family-friendly Ren'Py visual novel about Suhail, a boy who dreams of running a Mars colony — and wakes up with a better understanding of the real science behind space weather.

The game is fully in English and is designed to be readable by ages 7–11 and enjoyable for older players too.

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
2. Place the project folder inside the SDK's `RockPaperScissors` directory (or open it directly from the Ren'Py launcher).
3. Launch the project from the Ren'Py launcher, or run:

```sh
# From the Ren'Py SDK root
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3"
```

On Windows, run `renpy.exe` and select the project from the launcher.

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
└── project.json            # Ren'Py project metadata
```

Generated files (`saves/`, `cache/`, `*.rpyc`, logs, and translations for the default language) are excluded by `.gitignore`.

## Development and verification

From the Ren'Py SDK root:

```sh
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" lint
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" compile
```

Current lint baseline:

```text
160 dialogue blocks, 2,255 words, 12,349 characters
11 menus, 37 images, 32 screens
```

The UI, both minigames, all four endings, and the certificate flow have been smoke-tested with Ren'Py's built-in test framework. See `Progress.md` for the test log and `agents.md` for architecture details and common pitfalls.

## Credits

- **Engine:** [Ren'Py](https://www.renpy.org/) 8.5.3.
- **Story, code, and game design:** the MARTIAN DREAM V3 project author.
- **Font:** Vazirmatn, bundled under the SIL Open Font License.
- **Art and audio:** created for this project unless otherwise noted.

## License

No public license has been chosen for this repository yet. The source and original assets are shared for viewing and educational purposes; please contact the author before redistributing or reusing them commercially. Ren'Py itself remains under its own license.
