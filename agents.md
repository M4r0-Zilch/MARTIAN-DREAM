# agents.md — Onboarding & Handoff

> Read this first. It is written so an AI agent (or human) who has never seen the
> project can run, verify, edit, and extend it without rediscovering old bugs.

## 1. What this project is

A single Ren'Py 8.5.3 visual novel, **MARTIAN DREAM V3**, fully in English.
The player is Suhail, a boy who dreams he is running a Mars colony. The game has:

1. A classroom intro, followed by Suhail's late-night Mars research and sleep.
2. A spaceship intro, then two minigames:
   - **Solar Flare** (dodge radiation, stay in the green safe zone, use shield).
   - **Dust Storm** (sweep dust, repair the antenna, quiz, certificate).
3. A final Nout/Suhail ending that reveals everything was a dream (Suhail wakes in
   his bedroom, then answers his teacher in class).
4. A **Dictionary** screen on the main menu with space/Mars terms for ages 7–11+
   (still interesting for older readers).

Game is complete and stable: `lint` and `compile` pass and the smoke-test suites
pass. The repository is prepared for GitHub (README, `.gitignore`, no generated
artifacts staged).

## 2. Environment & commands

- Ren'Py SDK root: `/mnt/Y-Disk/Ren'Py/renpy-8.5.3-sdk`
- Project folder: `/mnt/Y-Disk/Ren'Py/renpy-8.5.3-sdk/RockPaperScissors/MARTIAN DREAM V3`
- Ren'Py: `8.5.3.26051504`; virtual resolution **1280×720**.
- Run everything from the SDK root:

```sh
cd /mnt/Y-Disk/Ren'Py/renpy-8.5.3-sdk

# Validate script (must print statistics and no errors)
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" lint

# Compile .rpy -> .rpyc (no output means success)
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" compile

# Play/test manually
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3"
```

Do not edit generated `*.rpyc`, `game/cache/`, `game/saves/`, or `game/tl/None/`.
`.bak` files in `game/` are manual backups, not loaded by Ren'Py, and are ignored.

## 3. File map

| File | Purpose |
|---|---|
| `game/script.rpy` | Characters, image definitions, `label start`, `label mars_landing`, final ending. |
| `game/solar_flare.rpy` | First minigame. `label solar_flare_story` (entry), `solar_flare_start` (game loop). |
| `game/dust_storm.rpy` | Second minigame, quiz, certificate, all Dust Storm endings. `label dust_storm_story` (entry). |
| `game/screens.rpy` | All screens. Custom `screen dictionary()` at ~line 356; `screen say`; menus; quick menu disabled. |
| `game/gui.rpy` | GUI constants, incl. `gui.language = "unicode"` and font settings. |
| `game/options.rpy` | Project config (`config.name`, version 1.0, About text, `config.window = "auto"`, `has_voice = False`). |
| `game/images/`, `game/audio/`, `game/fonts/` | Merged assets. Font: Vazirmatn. |
| `README.md` | Public overview, controls, setup, structure, credits, license note. |
| `Progress.md` | Changelog + current status. Update after every meaningful change. |
| `agents.md` | This handoff/architecture/pitfalls document. |

## 4. Story flow (do not reorder)

```
label start
  → classroom intro
  → late-night Mars research scene (bg research)
  → falls asleep at desk (bg sleepy)
  → label mars_landing
        window hide
        call solar_flare_story      # first minigame
        window hide
        call dust_storm_story       # second minigame (quiz + certificate + outro)
        window auto
        → Nout farewell
        → white flash
        → scene bg bedroom → Suhail wakes
        → scene bg classroom → Suhail answers the teacher
        → return
```

Key labels:

- `script.rpy`: `start` (line ~60), `mars_landing` (~176).
- `solar_flare.rpy`: `solar_flare_story` (~534), `solar_flare_start` (~546).
- `dust_storm.rpy`: `dust_storm_story` (~1039), `dust_storm_start` (~1046),
  `ds_intro`, `ds_sol1..6`, `ds_ending_*`, `ds_outro`, `ds_quiz`, `ds_certificate`.

### Character aliases (intentionally inconsistent legacy)

| Variable | Display name |
|---|---|
| `suhail`, `s` | Suhail (orange) |
| `nut`, `n`, `nout` | Nout (blue) |
| `teacher` | Teacher (white) |
| `ship_sys` | Ship System |

Keep these speaker colors consistent: Suhail orange, Nout blue, and Teacher
white. Use Suhail and Nout sprites in the spaceship, Dust Storm, and ending
scenes. Do not overlay Suhail's school uniform sprite on the classroom
background, which already shows him.

`suhail` is defined **only** in `game/script.rpy`. Do not redefine it in
`dust_storm.rpy` (that caused duplicate-definition problems before).

## 5. Hard-won Ren'Py rules (do not regress)

1. **Hiding the dialogue box:** use `window hide` / `window auto`.
   A bare `hide screen say` leaves the textbox background visible and previously
   produced `TypeError: missing a required argument: 'who'` when paired with
   `show screen say`. Never use `show/hide screen say` directly.
2. **Screens inside `renpy.pause(..., hard=True)`** (minigame end, certificate)
   must end with `Function(renpy.end_interaction, True/False)`. A bare `Return()`
   does not dismiss a hard pause and caused the infinite hang at the end of the
   Dust Storm. Certificate button is at `dust_storm.rpy` ~line 1023.
3. **Antenna repair hang (fixed):** the tick timer checks `ds_antenna_bolts >= 3`
   *before* the done-guard and calls `renpy.end_interaction(True)`. Keep that
   ordering; otherwise the third bolt can be registered but never end the pause.
4. **Dictionary layout:** keep English reading order — term on the left,
   definition on the right, both left-aligned. The panel must fit inside
   1280×720 (currently 1120×660 with a 1040×430 viewport).
   Do **not** add `reading_order "rtl"` as a child of `text`: in Ren'Py 8.5.3 it
   is a style property, not a valid `text` statement argument (`lint` rejects it).
5. **Solid scenes:** write `scene expression Solid("#ffffff")`; plain
   `scene Solid(...)` fails lint in this version.
6. **Escape `%`** in dialogue (`%%`) and never name a variable `sys`; it is a
   Python built-in (use `ship_sys`).
7. **Keep UTF-8** for all text. Preserve the existing file line endings
   (most `.rpy` are LF; `game/gui.rpy` is CRLF). When rewriting a file from
   Python, pass `newline=""` and avoid normalizing the whole file.
8. The quick menu is intentionally disabled (`default quick_menu = False`). It
   previously covered gameplay at the bottom of the screen; do not re-enable it.
9. `screen resource_hud()` and the `*_level` stats in `script.rpy` are legacy /
   unused. Leave them unless you intentionally build a HUD feature.
10. `solar_flare.rpy` imports pygame with a portable fallback:
    `try: import pygame` / `except ImportError: import renpy.pygame as pygame`.
    Never add a machine-specific `sys.path` entry.

## 6. Dictionary screen (`game/screens.rpy`)

`screen dictionary()` is opened from the main menu (`Dictionary` button) and
returns with `Return()`. It must stay:

- scrollable (`viewport` with vertical scrollbar, mousewheel, draggable);
- space-calm: `gui.main_menu_background` + `images/vignette.png` + small Mars;
- fully inside 1280×720: panel 1120×660, viewport 1040×430;
- readable for 7–11 and still engaging for older players: large title, section
  headers, one card per term, emoji + English term (left) + English definition
  (right).

Each entry is `("English term", "English definition")` inside a
`for section, entries in [...]` list. To add a word, add a tuple to the right
section; keep the column widths (1020 card, 290 term, 680 definition) so the
single-line layout fits. Children must remain able to scroll with the mouse wheel
and drag. The Back button returns to the main menu.

## 7. Testing workflow (Ren'Py built-in test framework)

Do **not** ship test `.rpy` files inside the real project. Test in a disposable
copy:

```sh
SDK=/mnt/Y-Disk/Ren'Py/renpy-8.5.3-sdk
SRC="$SDK/RockPaperScissors/MARTIAN DREAM V3"
T=/tmp/opencode/vntest

rm -rf "$T" && mkdir -p "$T"
cp -a "$SRC/." "$T/"
rm -rf "$T/game/saves" "$T/game/cache" "$T/game/"*.rpyc
```

Create test files under `$T/game/`. A trailing `exit` makes the test process
terminate cleanly (verified exit code 0) instead of lingering:

```renpy
testsuite ui:
    testcase screens:
        pause until screen "main_menu" timeout 10
        click "Dictionary" until screen "dictionary" timeout 10
        pause 0.8
        screenshot "ui_dictionary.png"
        click "Back to Main Menu" until screen "main_menu" timeout 10
        exit
```

Run a single case (IDs use `::`):

```sh
cd "$SDK"
timeout -k 5 60 ./renpy.sh "$T" test 'ui::screens'
```

Notes:

- Screenshots land in `$T/tests/screenshots/`.
- **Delete `$T/tests/screenshots/` before each run.** Otherwise Ren'Py compares
  the new screenshot with the old one and fails with
  `RenpyTestScreenshotError: ... pixel difference`.
- The runner can stay alive after printing `PASSED` if the case has no `exit`.
  Kill leftovers with `pkill -f "/tmp/opencode/vntest"` if needed.
- Suites used for regression testing:
  - `ui::screens` — Dictionary, Preferences, About, Help, Load.
  - `scenes::solar_flare`, `scenes::sweep`, `scenes::antenna`,
    `scenes::certificate`.
  - `more::start_intro`, `more::dust_intro`, `more::ending_gold`,
    `more::ending_silver`, `more::ending_brave`, `more::ending_dark`.
  - `ending::full_ending` (requires temporarily patching the test copy to skip
    both minigames; jumps to `mars_landing` and clicks through the farewell,
    bedroom, classroom, and main menu).
- After any edit, always run `lint` then `compile` from the SDK root.

## 8. Noise / stale files

- `errors.txt`, `log.txt`, `traceback.txt`, `runerr*.txt`, and `runout*.txt` are
  historical run artifacts and are ignored by git. They are safe to delete.
- `game/*.rpy.bak` are pre-edit backups and are ignored. Do not load or edit them
  accidentally.
- `codes.txt` is a generated source export and is ignored.
- `game/tl/None/` is generated by Ren'Py and is ignored.

## 9. Current status & sensible next steps

Done and verified:

- Full English story from start → solar flare → dust storm → ending.
- Dialogue box correctly hidden during both minigames and restored for the ending.
- Certificate and antenna hangs fixed.
- Nout/Suhail ending wired (with character sprites, white flash → bedroom →
  classroom → main menu).
- Green pulsing safe zone in Solar Flare (no longer looks like a textbox).
- Dictionary recreated: scrollable, child-friendly, English term/definition
  columns, fits 1280×720.
- About text filled; `config.has_voice = False`.
- Portable pygame import in `solar_flare.rpy`; all Arabic comments translated.
- `.gitignore` covers generated saves, cache, compiled files, logs, translation
  output, and local editor clutter.
- `lint`, `compile`, and all UI/scene/story/ending smoke tests pass.

Optional next work:

1. Add a persistent, opt-in regression test suite (e.g. `game/tests.rpy` gated by
   `config.developer`) so testing does not depend on `/tmp`.
2. Choose and add a `LICENSE` file if the project will be distributed publicly.
3. Add a gameplay screenshot or GIF to `README.md` for presentation.
4. Delete stale root artifacts (`errors.txt`, `traceback.txt`, old `run*.txt`)
   once they are no longer useful.

## 10. Documentation policy

- After every meaningful change, add a dated bullet to `Progress.md` with what
  changed, why, and how it was verified.
- Update this `agents.md` whenever the flow, file map, commands, or a Ren'Py
  gotcha changes. The goal is that a fresh model can continue from these two
  files alone.
