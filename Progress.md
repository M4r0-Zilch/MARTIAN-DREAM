# Progress — MARTIAN DREAM V3

> **Last updated:** 2026-11-16
> **Current state:** ✅ Complete, English, and GitHub-ready. `lint` and `compile`
> pass with no errors. All story, minigame, menu, certificate, and ending smoke
> tests pass.
>
> **Read `agents.md` first** for the architecture, file map, commands, testing
> workflow, and Ren'Py pitfalls. This file tracks *what changed and how it was
> verified*.

## Quick verification (copy/paste from SDK root)

```sh
cd /mnt/Y-Disk/Ren'Py/renpy-8.5.3-sdk
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" lint
./renpy.sh "RockPaperScissors/MARTIAN DREAM V3" compile
```

Expected lint statistics (stable baseline): **160 dialogue blocks, 2,255 words,
12,349 characters, 11 menus, 37 images, 32 screens**, no errors.

## What the game contains

1. English classroom intro, followed by a late-night Mars research scene and Suhail falling asleep.
2. Spaceship intro, then Solar Flare minigame.
3. Dust Storm minigame (sweep → antenna repair → quiz → certificate).
4. Nout/Suhail ending: farewell → white flash → bedroom wake-up → classroom line.
5. Main-menu Dictionary with Mars/space terms written for ages 7–11+.

The full game, menus, Dictionary, and minigame instructions are in English. Only
the bundled Vazirmatn font and historical filenames remain from the earlier
Arabic prototype.

## Completed work

### Final optimization and GitHub readiness (2026-11-16)

- [x] Fitted the Dictionary inside the 1280×720 screen: panel reduced from
      1180×780 to 1120×660, viewport to 1040×430, and paddings/spacing tightened.
- [x] Switched the Dictionary to English reading order: term on the left,
      definition on the right, both left-aligned; section headers left-aligned.
- [x] Replaced the hardcoded Windows path fallback in `solar_flare.rpy` with a
      portable `except ImportError: import renpy.pygame as pygame`.
- [x] Filled the previously empty About text in `options.rpy` and set
      `config.has_voice = False` (the project has no voice assets).
- [x] Translated the remaining Arabic comments in `dust_storm.rpy`; corrected
      outdated "Arabic intro", "1920x1080", and "Nut" comments in `script.rpy`.
- [x] Expanded `.gitignore` for `codes.txt`, `runerr*.txt`, `runout*.txt`,
      `game/tl/None/`, `.vscode/`, and OS clutter.
- [x] Added `README.md` with features, controls, setup, structure, test commands,
      credits, and an honest license note.
- [x] Re-ran `lint`, `compile`, and all regression smoke tests after the edits.

### Character colors and sprite overlays

- [x] Added the late-night research and falling-asleep scenes before the
      spaceship sequence, using the uploaded backgrounds already in
      `game/images/bg/`.
- [x] Standardized speaker colors: Suhail orange, Nout blue, and Teacher white.
      Restored Suhail and Nout sprites in the spaceship, Dust Storm, and ending
      scenes. The classroom keeps its background without an extra uniform
      sprite. Cleaned white cutout leftovers from Suhail's expressive sprites.
      Verified with lint and compile.

### Integration & story

- [x] Read game directory and source assets.
- [x] Copied base assets from `Martian Dream/images`.
- [x] Copied and merged Solar Flare and Dust Storm assets (images, audio, fonts).
- [x] Removed `insight_colony.rpy` and Insight-specific assets/references
      (do not add Insight Colony back).
- [x] Removed duplicate `suhail` character definition from `dust_storm.rpy`
      (`suhail` lives only in `script.rpy`).
- [x] Built combined `game/script.rpy` in the required order:
      1. Classroom intro, late-night research, and sleep transition.
      2. Spaceship intro (minigame 2).
      3. Solar Flare minigame (`solar_flare_story`).
      4. Dust Storm minigame (`dust_storm_story`).
      5. Ending with Nout/Suhail dialogue.
- [x] Fixed missing spaceship assets by mapping them to available images/audio.
- [x] Escaped percent signs and renamed `sys` → `ship_sys` to avoid conflict with
      the Python built-in.
- [x] Added the final ending and a clean `return` after it.
- [x] Wired the requested Nout/Suhail ending in `label mars_landing`.
- [x] Updated the ending to match the comments planted in `game/script.rpy`:
      Nout farewell → white flash → bedroom wake-up → classroom line → `return`.
- [x] Removed the old "fade to black" narration text box from the story.

### Display / hang bug fixes

- [x] Beautified UI: Mars theme, Vazirmatn font, space backgrounds, main-menu
      Mars/vignette backdrop.
- [x] Resized backgrounds to 1280×720 and adjusted sprite zooms for ideal fit.
- [x] Replaced all sprites with the new `game/images/sprites` assets.
- [x] Centered dialogue text in the say screen (`xalign 0.5`).
- [x] Adjusted dialogue position for 1280×720 (`gui.dialogue_xpos = 82`).
- [x] Reduced dialogue font size to 28 for readability.
- [x] Removed invalid `text_align "center"` string usage; kept numeric `xalign`
      centering to fix `TypeError: must be real number, not str`.
- [x] Disabled the in-game quick menu overlay (bottom bar blocked gameplay).
- [x] Replaced `hide screen say` / `show screen say` with `window hide` /
      `window auto` so the textbox is truly hidden during both minigames and
      restored for the ending.
- [x] Fixed the first-minigame textbox: dark box no longer appears.
- [x] Fixed the second-minigame end hang: certificate button uses
      `Function(renpy.end_interaction, True)` instead of a bare `Return()`.
- [x] Fixed the antenna-repair hang: the timer checks `ds_antenna_bolts >= 3`
      before the done guard and ends the hard pause on the third bolt.
- [x] Added a green, gently pulsing safe-zone fill to Solar Flare so it no longer
      reads as a dark textbox.

### English localization

- [x] Translated all player-facing dialogue, menus, minigame instructions, quiz
      questions, endings, and Dictionary entries to English.
- [x] Preserved speaker colors and the Nout/Suhail relationship while rewording
      the story for a natural English read.
- [x] Kept `gui.language = "unicode"` and the bundled Vazirmatn font so the
      project remains easy to localize in the future.

### Dictionary

- [x] Recreated `screen dictionary()` in `game/screens.rpy` as a scrollable,
      space-calm screen (starry background + vignette + Mars, dark translucent
      panel, large title/subtitle, viewport, Back button).
- [x] Added age-appropriate entries for 7–11+ (Solar Flare, CME, Safe Zone,
      Shield, Thin Atmosphere, Tau, Dust Devil, Colony, Oxidative Stress, RTG,
      Trade-off).
- [x] Final layout: English term left, definition right, one card per word, with
      section headers. Panel fits within 1280×720.
- [x] Kept the `reading_order "rtl"` lesson documented: in Ren'Py 8.5.3 it is a
      style property, not a valid `text` statement argument; do not reintroduce
      it.

### Verification

- [x] `lint` passes (no errors) at the 160-block baseline.
- [x] `compile` passes (no output).
- [x] UI smoke test `ui::screens` passed: Dictionary, Preferences, About, Help,
      and Load all open and return to the main menu.
- [x] Scene smoke tests passed: `scenes::solar_flare`, `scenes::sweep`,
      `scenes::antenna`, `scenes::certificate`.
- [x] Story smoke tests passed: `more::start_intro`, `more::dust_intro`,
      `more::ending_gold`, `more::ending_silver`, `more::ending_brave`,
      `more::ending_dark`.
- [x] Full ending test `ending::full_ending` passed in a patched copy:
      Nout farewell → bedroom → classroom → main menu.
- [x] Screenshots reviewed for the Dictionary, all four endings, the certificate,
      and both minigames.
- [x] Test copies use a trailing `exit`, so test processes terminate cleanly
      (exit code 0). Screenshot comparison requires deleting
      `tests/screenshots/` before each run.

### Documentation / handoff

- [x] Rewrote `agents.md` as a first-time onboarding guide: project overview,
      commands, file map, story flow/labels, character aliases, Ren'Py pitfalls,
      dictionary details, test workflow, stale files, and next steps.
- [x] Rewrote `Progress.md` with current status, quick verification commands,
      grouped changelog, known notes, and optional next steps.
- [x] Added `README.md` for GitHub visitors.

## Known notes

- `errors.txt`, `traceback.txt`, `log.txt`, `runerr*.txt`, and `runout*.txt` are
  historical run artifacts and are now ignored by git. They are safe to delete.
- Test files/screenshots live in the disposable `/tmp/opencode/vntest` copy, not
  in the shipped game. See `agents.md` §7 for the test workflow.
- Character names use legacy aliases (`nut`/`n`/`nout`, `suhail`/`s`) that all
  display the current English names. Do not rename them without a full dialogue
  review.
- `screen resource_hud()` and `oxygen_level` / `water_level` / `energy_level` /
  `food_level` in `script.rpy` are unused legacy definitions.
- `game/tl/None/` is generated by Ren'Py and ignored; do not commit it.

## Optional next steps

1. Add a persistent, opt-in regression suite in the project (gated by
   `config.developer`) so tests do not depend on `/tmp/opencode/vntest`.
2. Choose and add a `LICENSE` file if the project will be distributed publicly.
3. Add a short gameplay screenshot or GIF to the README for GitHub presentation.
4. Delete stale root artifacts (`errors.txt`, `traceback.txt`, old `run*.txt`)
   when they are no longer useful.
