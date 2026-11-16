# =====================================================================
#  THE GREAT DUST STORM  -  Suhail and Nout
#  (The storm that silenced Opportunity - June 2018)
# =====================================================================
#
#  HOW TO INTEGRATE INTO YOUR REN'PY GAME (3 steps):
#   1. Copy this file (dust_storm.rpy) into your project's game/ folder.
#   2. Copy game/images/, game/audio/ and game/fonts/ into your project
#      (merge, don't overwrite).
#   3. In your story, call it:
#
#        call dust_storm_start      # standalone (title, replay, record)
#        # or
#        call dust_storm_story      # embedded (returns when done)
#
#  That's it. No gui.rpy or screens.rpy changes needed.
#  Resolution: 1280x720. Works with Ren'Py 8.5.3 and its Unicode text shaping.
#  Assets: bg_station, suhail, nout, dustdevil,
#  rock_sample, badge_*, panel_dirty/panel_clean, dust_veil + audio.
#
#  If your project ALSO defines `suhail` / `nout` characters, delete the
#  two `define` lines below (yours win).
#
#  REALITY BEHIND THE GAME (for the curious):
#   - 2018 Global Dust Storm. tau reached 10.8 (a Sun so dim it looked like
#     a full Moon). NASA's Opportunity rover - solar powered, 15 years old,
#     designed to last 90 sols - went silent on sol 5111 (June 10, 2018).
#   - NASA declared the mission over on Feb 13, 2019. 1,000+ commands were
#     sent into the dark. No answer.
#   - Curiosity & Perseverance survived the same storm: they run on nuclear
#     power (RTG), not sunlight.
#   - Dust devils RE-CLEANED the rovers' panels several times - that is how
#     Opportunity lived 60x longer than designed.
#   THIS GAME asks every kid the real question the JPL team faced:
#   spend your last drop of energy on SCIENCE, on SURVIVAL, or on your CREW?
#   Every decision costs something else. That is a TRADE-OFF.
# =====================================================================
# define suhail removed to avoid duplicate (main script defines suhail)
define nout   = Character("Nout", color="#5ce0ff")  # suhail defined in main script

default persistent.ds_best_tier = 0      # 0=none 1=bronze 2=silver 3=gold (survived endings)
default persistent.ds_runs = 0           # completed runs (right or wrong choices)

# ---------------------------------------------------------------- state
default ds_energy   = 70      # station battery
default ds_warmth   = 85      # station warmth (zero = Opportunity-style ending)
default ds_dust     = 15      # dust level on the solar panels
default ds_water    = 5       # water units (used only to clean the panels)
default ds_science  = 10      # science experiment progress
default ds_comms    = 100     # Earth signal strength
default ds_sol      = 1       # current Martian sol
default ds_tau      = 0.5     # dust thickness in the air (tau)
default ds_heater   = "eco"   # selected heater mode
default ds_smart    = 0       # balanced-decision counter
default ds_brave    = 0       # brave-decision counter
default ds_risky    = 0       # risky-decision counter
default ds_quiz     = 0       # Mars quiz score
default ds_nougat   = False   # did Nout do her big move?
default ds_final_tx = False   # was the final discovery broadcast to Earth?
default ds_frozen   = False   # did the station freeze?
default ds_history  = []      # decision log used by the certificate
default ds_sweep_picked = 0   # sweep minigame state
default ds_antenna_bolts = 0  # antenna repair result
default ds_needle_t  = 0.0    # antenna minigame needle position
default ds_needle_zone = 50.0 # green-zone position
default ds_needle_speed = 1.6 # needle speed in the antenna minigame
default ds_panel_picked = [0, 0, 0]  # dust per panel in sweep game (3 = maximum)
default ds_sweep_timer = 25.0
default ds_sweep_running = False
default ds_sweep_done = False
default ds_antenna_timer = 35.0
default ds_antenna_done = False
default ds_sweep_clean_count = 0

init python:

    def ds_reset_game():
        global ds_energy, ds_warmth, ds_dust, ds_water, ds_science, ds_comms
        global ds_sol, ds_tau, ds_heater, ds_smart, ds_brave, ds_risky, ds_quiz
        global ds_nougat, ds_final_tx, ds_frozen, ds_history
        global ds_sweep_picked, ds_antenna_bolts, ds_needle_t, ds_needle_zone, ds_needle_speed
        global ds_panel_picked, ds_sweep_timer, ds_sweep_running, ds_sweep_done
        global ds_antenna_timer, ds_antenna_done, ds_sweep_clean_count
        ds_energy  = 70
        ds_warmth  = 85
        ds_dust    = 15
        ds_water   = 5
        ds_science = 10
        ds_comms   = 100
        ds_sol     = 1
        ds_tau     = 0.5
        ds_heater  = "eco"
        ds_smart   = 0
        ds_brave   = 0
        ds_risky   = 0
        ds_quiz    = 0
        ds_nougat  = False
        ds_final_tx = False
        ds_frozen  = False
        ds_history = []
        ds_sweep_picked = 0
        ds_panel_picked = [3, 3, 3]
        ds_sweep_timer = 25.0
        ds_sweep_running = False
        ds_sweep_done = False
        ds_antenna_bolts = 0
        ds_antenna_timer = 35.0
        ds_antenna_done = False
        ds_needle_t  = 0.0
        ds_needle_zone = 50.0
        ds_needle_speed = 1.6
        ds_sweep_clean_count = 0

    def ds_solar_gain(sol, dust):
        table = {1: 1.00, 2: 0.78, 3: 0.55, 4: 0.30, 5: 0.06, 6: 0.70}
        sun = table.get(sol, 0.5)
        panel = max(0.15, 1.0 - dust / 100.0 * 0.85)
        return int(round(26 * sun * panel))

    def ds_dust_growth(sol):
        return {1: 10, 2: 12, 3: 14, 4: 16, 5: 20, 6: 8}.get(sol, 12)

    def ds_night_cold(sol):
        return {1: 8, 2: 12, 3: 16, 4: 22, 5: 30, 6: 10}.get(sol, 12)

    def ds_night_loss(sol):
        base = ds_night_cold(sol)
        if ds_heater == "high":
            return max(2, base - 14)
        if ds_heater == "eco":
            return max(1, base - 2)
        return base + 16            # heater off

    def ds_tau_alpha(sol):
        return {1: 0.0, 2: 0.15, 3: 0.30, 4: 0.45, 5: 0.62, 6: 0.20}.get(sol, 0.0)

    def ds_needle_pos():
        import math
        return 50.0 + 46.0 * math.sin(ds_needle_t * ds_needle_speed)

    def ds_log(line):
        ds_history.append(line)

# ---------------------------------------------------------------- images

image bg_station = "images/bg/mars outpost.jpg"
image img_suhail         = "images/sprites/happy.png"
image img_suhail_happy   = "images/sprites/happy.png"
image img_suhail_afraid  = "images/sprites/afraid.png"
image img_suhail_angry   = "images/sprites/normal with uniform.png"
image img_suhail_amazed  = "images/sprites/amazed.png"
image img_nout           = "images/sprites/ai bot.png"
image img_dustdevil = "images/dustdevil.png"
image img_rock   = "images/rock_sample.png"
image panel_dirty = "images/panel_dirty.png"
image panel_clean = "images/panel_clean.png"
image badge_gold   = "images/badge_gold.png"
image badge_silver = "images/badge_silver.png"
image badge_bronze = "images/badge_bronze.png"
image badge_dark   = "images/badge_dark.png"
image dust_veil  = "images/dust_veil.png"

transform ds_suhail_left:
    xalign 0.05
    yalign 0.98
    zoom 0.5

transform ds_suhail_right:
    xalign 0.95
    yalign 0.98
    zoom 0.5

transform ds_nout_left:
    xalign 0.34
    yalign 0.985
    zoom 0.66

transform ds_nout_right:
    xalign 0.66
    yalign 0.985
    zoom 0.66

transform ds_float:
    yoffset 0.0
    linear 1.6 yoffset -8.0
    linear 1.6 yoffset 0.0
    repeat

transform ds_devil_in:
    xalign 0.75
    ypos -400
    easein 1.6 ypos 210.0

transform ds_rock_spin:
    zoom 1.0
    linear 1.2 zoom 1.15
    linear 1.2 zoom 1.0
    repeat

# ---------------------------------------------------------------- HUD

screen ds_hud():
    zorder 50
    frame:
        xpos 16
        ypos 14
        background Solid("#000000aa")
        padding (14, 10)

        vbox:
            spacing 5
            text "SOL [ds_sol] / 6    TAU = [ds_tau]" size 20 bold True color "#ffd9a0" font "fonts/Vazirmatn.ttf"

            $ gain = ds_solar_gain(ds_sol, ds_dust)
            hbox:
                spacing 8
                text "Power" size 15 color "#ffe9c9" yalign 0.5 xsize 78 font "fonts/Vazirmatn.ttf"
                bar value ds_energy range 100 xsize 150 ysize 12 left_bar Solid("#ffd166") right_bar Solid("#332211")
                text "+[gain]/day" size 13 color "#ffd166" yalign 0.5 font "fonts/Vazirmatn.ttf"

            hbox:
                spacing 8
                text "Warmth" size 15 color "#ffe9c9" yalign 0.5 xsize 78 font "fonts/Vazirmatn.ttf"
                bar value ds_warmth range 100 xsize 150 ysize 12 left_bar Solid("#ff8c42") right_bar Solid("#331511")

            hbox:
                spacing 8
                text "Dust" size 15 color "#ffe9c9" yalign 0.5 xsize 78 font "fonts/Vazirmatn.ttf"
                bar value ds_dust range 100 xsize 150 ysize 12 left_bar Solid("#c98a4b") right_bar Solid("#241811")

            hbox:
                spacing 8
                text "Signal" size 15 color "#ffe9c9" yalign 0.5 xsize 78 font "fonts/Vazirmatn.ttf"
                bar value ds_comms range 100 xsize 150 ysize 12 left_bar Solid("#5ce0ff") right_bar Solid("#112233")

            hbox:
                spacing 8
                text "Science" size 15 color "#ffe9c9" yalign 0.5 xsize 78 font "fonts/Vazirmatn.ttf"
                bar value ds_science range 100 xsize 150 ysize 12 left_bar Solid("#b388ff") right_bar Solid("#221133")

            text "Water × [ds_water]" size 15 color "#a8d8ff" font "fonts/Vazirmatn.ttf"

screen ds_storm_veil():
    zorder 10
    $ frac = ds_tau_alpha(ds_sol)
    if frac > 0:
        add Transform(Solid("#2a1408"), alpha=frac)

# ---------------------------------------------------------------- sweep minigame (clean the panels)

init python:

    def ds_sweep_panel(i):
        global ds_sweep_done, ds_sweep_running
        if not ds_sweep_running or ds_sweep_done:
            return
        if ds_panel_picked[i] > 0:
            ds_panel_picked[i] -= 1
            renpy.sound.play("audio/click.wav")
            if ds_panel_picked[i] == 0:
                renpy.sound.play("audio/clean.wav")

    def ds_sweep_tick():
        global ds_sweep_timer, ds_sweep_done, ds_sweep_running
        if ds_sweep_running and not ds_sweep_done:
            ds_sweep_timer -= 0.1
            if all(p == 0 for p in ds_panel_picked):
                ds_sweep_done = True
                ds_sweep_running = False
                renpy.sound.play("audio/success.wav")
                renpy.end_interaction(True)
                return
            if ds_sweep_timer <= 0:
                ds_sweep_timer = 0.0
                ds_sweep_done = True
                ds_sweep_running = False
                renpy.sound.play("audio/fail.wav")
                renpy.end_interaction(False)

    def ds_antenna_tick():
        global ds_antenna_timer, ds_needle_t, ds_antenna_done
        if ds_antenna_bolts >= 3:
            ds_antenna_done = True
            renpy.end_interaction(True)
            return
        if ds_antenna_done:
            return
        ds_antenna_timer -= 0.05
        ds_needle_t += 0.05
        if ds_antenna_timer <= 0:
            ds_antenna_timer = 0.0
            ds_antenna_done = True
            renpy.sound.play("audio/fail.wav")
            renpy.end_interaction(False)

    def ds_antenna_hit():
        global ds_antenna_bolts, ds_needle_zone, ds_needle_speed, ds_antenna_done
        if ds_antenna_done:
            return
        pos = ds_needle_pos()
        if abs(pos - ds_needle_zone) <= 11.0:
            ds_antenna_bolts += 1
            renpy.sound.play("audio/clean.wav")
            if ds_antenna_bolts >= 3:
                ds_antenna_done = True
                renpy.sound.play("audio/success.wav")
                renpy.end_interaction(True)
            else:
                import random
                ds_needle_zone = random.uniform(18.0, 82.0)
                ds_needle_speed = min(3.4, ds_needle_speed + 0.7)
        else:
            renpy.sound.play("audio/hit.wav")

    def ds_antenna_bail():
        global ds_antenna_done
        if not ds_antenna_done:
            ds_antenna_done = True
            renpy.end_interaction(False)

screen ds_sweep_game():
    modal True
    timer 0.1 repeat True action Function(ds_sweep_tick)
    add "bg_station"
    add Solid("#00000077")

    text "Clean the Solar Panels!" size 44 bold True color "#ffd9a0" xalign 0.5 ypos 30 font "fonts/Vazirmatn.ttf"
    text "Click each dirty panel 3 times" size 20 color "#ffe9c9" xalign 0.5 ypos 92 font "fonts/Vazirmatn.ttf"

    frame:
        xalign 0.5
        ypos 140
        background Solid("#000000cc")
        padding (24, 14)
        vbox:
            spacing 6
            text "Suit time" size 16 color "#ff8866" xalign 0.5 font "fonts/Vazirmatn.ttf"
            bar value ds_sweep_timer range 25.0 xsize 420 ysize 18 left_bar Solid("#ff5533") right_bar Solid("#331111")

    hbox:
        xalign 0.5
        ypos 330
        spacing 60

        for i in range(3):
            vbox:
                spacing 10
                if ds_panel_picked[i] > 0:
                    imagebutton:
                        id "panel_[i]"
                        idle "panel_dirty"
                        hover "panel_dirty"
                        action Function(ds_sweep_panel, i)
                else:
                    add "panel_clean"
                if ds_panel_picked[i] > 0:
                    text "Dust × [ds_panel_picked[i]]" size 18 color "#ffaa55" xalign 0.5 font "fonts/Vazirmatn.ttf"
                else:
                    text "Clean" size 18 color "#7dff9a" xalign 0.5 font "fonts/Vazirmatn.ttf"

    text "Water is precious—and dust costs even more." size 16 italic True color "#c9a06a" xalign 0.5 ypos 660 font "fonts/Vazirmatn.ttf"

screen ds_antenna_game():
    modal True
    timer 0.05 repeat True action Function(ds_antenna_tick)

    add "bg_station"
    add Solid("#00000088")

    text "Repair the Antenna in the Storm!" size 38 bold True color "#ffd9a0" xalign 0.5 ypos 40 font "fonts/Vazirmatn.ttf"
    text "Press FIX when the marker is in the green zone" size 20 color "#ffe9c9" xalign 0.5 ypos 100 font "fonts/Vazirmatn.ttf"

    frame:
        xalign 0.5
        ypos 145
        background Solid("#000000cc")
        padding (24, 12)
        vbox:
            spacing 6
            text "Storm exposure" size 16 color "#ff8866" xalign 0.5 font "fonts/Vazirmatn.ttf"
            bar value ds_antenna_timer range 35.0 xsize 420 ysize 16 left_bar Solid("#ff5533") right_bar Solid("#331111")

    frame:
        xpos 340
        ypos 300
        background Solid("#161c26")
        xsize 600
        ysize 70

        frame:
            xpos int((ds_needle_zone - 11.0) / 100.0 * 600)
            yalign 0.5
            background Solid("#1f7a3d")
            xsize int(22.0 / 100.0 * 600)
            ysize 46

        frame:
            xpos int(ds_needle_pos() / 100.0 * 600) - 3
            yalign 0.5
            background Solid("#ffd166")
            xsize 6
            ysize 64

    text "Bolts: [ds_antenna_bolts] / 3" size 22 color "#8be9fd" xalign 0.5 ypos 410 font "fonts/Vazirmatn.ttf"

    textbutton "FIX!":
        xalign 0.5
        ypos 460
        xsize 260
        ysize 74
        background Solid("#b0521e")
        hover_background Solid("#d06028")
        text_size 30
        text_color "#ffe9c9"
        action Function(ds_antenna_hit)

    textbutton "Return to the station (stay safe)":
        xalign 0.5
        ypos 560
        background None
        text_size 17
        text_color "#a8d8ff"
        action Function(ds_antenna_bail)

# ###################################################################
#  STORY
# ###################################################################

label ds_morning:
    python:
        gain = ds_solar_gain(ds_sol, ds_dust)
        ds_energy = min(100, ds_energy + gain)
        ds_dust = min(100, ds_dust + ds_dust_growth(ds_sol))
        ds_tau = {1: 0.5, 2: 1.6, 3: 3.0, 4: 6.5, 5: 10.8, 6: 2.0}[ds_sol]
    return

label ds_nightfall:
    python:
        loss = ds_night_loss(ds_sol)
        ds_warmth = max(0, ds_warmth - loss)
    nout "It’s getting cold fast tonight… we lost [loss] warmth."
    if ds_energy <= 0:
        python:
            ds_warmth = max(0, ds_warmth - 20)
            ds_comms = 0
        nout "The battery is empty! The heater stopped, and our signal is gone."
    if ds_warmth <= 0:
        $ ds_frozen = True
    return

# ---------------------------------------------------------------- INTRO

label ds_intro:
    scene bg_station with fade
    play music "audio/ambient.wav" loop fadein 1.0

    show img_nout at ds_nout_left with dissolve
    show img_suhail at ds_suhail_right with dissolve

    nout "Good morning, Suhail! Perseverance Station says hello from Mars!"
    suhail "Good morning, Mars, Nout! Why is the orbiter sending a red alert?"
    nout "The orbiter has spotted danger: a dust storm is forming near the pole, and it’s growing fast."
    nout "That’s just what happened on May 30, 2018. A week later, the storm seemed to cover the whole planet."

    "Mars — Perseverance Outpost. Suhail is the youngest astronaut trainee, and this is his first time in charge alone."

    suhail "So the storm is coming here?"
    nout "In about six days. When it arrives, the Sun will look dim… then we may not see it at all."
    nout "Suhail… do you know what happened to Opportunity?"

    play sound "audio/squelch.wav"
    nout "Opportunity was a NASA rover that lived on Mars for 15 years, even though it was built to last only 90 days."
    nout "During the 2018 global storm, the dust level reached tau 10.8. The Sun vanished from view."
    nout "Its solar panels stopped charging, and its batteries became too cold. Its last signal reached Earth on June 10, 2018."
    nout "NASA sent it more than 1,000 messages, but got no reply. On February 13, 2019, NASA announced the mission was over."

    suhail "…I don’t want that to happen to us."
    nout "It won’t! I’m here with you. People on Earth are watching, and they’re waiting for news."
    nout "Listen, Suhail: every choice costs us something else. That’s called a trade-off."
    nout "We have enough power for one thing at a time: science, survival, or helping you and me?"
    nout "You’ll need to think carefully. Your name, Suhail, means ‘bright star’—one of the brightest stars in the southern sky."

    suhail "All right… I’m ready. Nout, show me the whole situation."
    nout "Great work. You’re in charge of the station now, Suhail."

    "Your mission: make it through the storm, and give Mars a different story from Opportunity’s."

    return

# ---------------------------------------------------------------- SOL 1 — red alert

label ds_sol1:
    $ ds_sol = 1
    $ ds_tau = 0.5
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    call ds_morning from _call_ds_morning
    show img_nout at ds_nout_right with dissolve
    show img_suhail at ds_suhail_left with dissolve

    nout "Day 1. The Sun is still bright, but the orbiter says dust is gathering in the north."
    nout "We have time to get ready… if we use it well."

    suhail "What should we do first?"

    menu:
        "“Start the research now—the rock won’t study itself!” (Science)":
            $ ds_science = min(100, ds_science + 14)
            $ ds_energy = max(0, ds_energy - 18)
            $ ds_brave += 1
            $ ds_log("Science first: studied the rock just before the storm (+14 science, -18 power)")
            suhail "This rock is one of the oldest things on Mars… I won’t leave it to the storm!"
            nout "That’s brave… but watch the battery."

        "“Turn off extra equipment—let’s prepare for the storm” (Power first)":
            $ ds_energy = min(100, ds_energy + 12)
            $ ds_smart += 1
            $ ds_log("Prepared the station: turned off power-hungry equipment (+12 power)")
            suhail "Shut down everything we don’t need. Put the whole station on standby!"
            nout "Smart choice. Getting ready early makes a difference, Suhail."

    nout "Now… what should we tell Earth? We can send one message today."
    menu:
        "Full message to Earth (12 minutes to arrive)":
            $ ds_energy = max(0, ds_energy - 16)
            $ ds_comms = 100
            $ ds_smart += 1
            $ ds_log("Sent Earth all the storm details (-16 power, signal 100)")
            nout "Mission Control is glad! “Thanks for warning us.”"
            play sound "audio/squelch.wav"

        "A short signal—to let them know we’re safe":
            $ ds_energy = max(0, ds_energy - 6)
            $ ds_comms = max(ds_comms, 70)
            $ ds_smart += 1
            $ ds_log("Sent a short message to Earth (-6 power)")
            nout "A quick message: “We made it. We’re safe and holding on.”"

        "Nothing—the power matters more":
            $ ds_comms = max(0, ds_comms - 25)
            $ ds_risky += 1
            $ ds_log("Cut contact with Earth to save power (-25 signal)")
            nout "Earth has no idea how we’re doing… that’s a big risk."

    nout "Science fact: On May 30, 2018, satellites spotted a small storm near Mars’s north pole. Ten days later, it covered the planet."
    nout "Someone at JPL knew it was coming… but no one could stop it."

    call ds_nightfall from _call_ds_nightfall
    jump ds_sol2

# ---------------------------------------------------------------- SOL 2 — dust is building up

label ds_sol2:
    $ ds_sol = 2
    $ ds_tau = 1.6
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    call ds_morning from _call_ds_morning_1
    show img_nout at ds_nout_left with dissolve
    show img_suhail at ds_suhail_right with dissolve

    nout "Day 2. The sky is still orange… but it’s getting darker."
    nout "Dust has been building up on the panels for three days. If the Sun gets dimmer, dirty panels won’t give us much power."

    if ds_water >= 1 and ds_energy >= 8:
        menu:
            "“Clean the panels now—put on the spacesuit!” (1 water + 8 power)":
                $ ds_water -= 1
                $ ds_energy = max(0, ds_energy - 8)
                $ ds_smart += 1
                $ ds_log("Cleaned the solar panels (-1 water, -8 power)")
                call ds_play_sweep from _call_ds_play_sweep
                $ ds_dust = max(0, ds_dust - ds_sweep_clean_count * 34)
                if ds_sweep_clean_count >= 3:
                    nout "The panels are shining again! Our power should be steady."
                elif ds_sweep_clean_count >= 1:
                    nout "We cleaned some of them… enough for the panels to catch some sunlight."
                else:
                    nout "Time ran out before we finished… the dust is still there."

            "“Leave the dust—we’ll wait for dust devils”":
                $ ds_risky += 1
                $ ds_log("Left the panels dirty (bet on dust devils)")
                nout "A gamble! Dust devils sometimes come… and sometimes they don’t."
    else:
        nout "We don’t have enough water or power to clean today… the panels will stay dirty."
        $ ds_risky += 1
        $ ds_log("Not enough water or power to clean—the panels became a burden")

    nout "Science fact: Opportunity lasted for years partly because dust devils cleaned its panels. Cameras saw the panels shine again in 2004 and 2014."

    call ds_nightfall from _call_ds_nightfall_1
    jump ds_sol3

# ---------------------------------------------------------------- SWEEP host

label ds_play_sweep:
    $ ds_panel_picked = [3, 3, 3]
    $ ds_sweep_timer = 25.0
    $ ds_sweep_running = True
    $ ds_sweep_done = False
    $ ds_sweep_clean_count = 0
    window hide
    show screen ds_sweep_game
    $ renpy.pause(3600.0, hard=True)
    hide screen ds_sweep_game
    window auto
    python:
        ds_sweep_clean_count = sum(1 for p in ds_panel_picked if p == 0)
    return

# ---------------------------------------------------------------- SOL 3 — the cold night

label ds_sol3:
    $ ds_sol = 3
    $ ds_tau = 3.0
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    call ds_morning from _call_ds_morning_2
    show img_nout at ds_nout_left with dissolve
    show img_suhail at ds_suhail_right with dissolve

    nout "Day 3. The sky is turning darker orange… and the Sun looks like a faint circle."
    nout "Tonight, the temperature could drop below -100°. This cold can ruin batteries."

    menu:
        "“Run the heaters on high all night—safety first”":
            $ ds_heater = "high"
            $ ds_energy = max(0, ds_energy - 22)
            $ ds_smart += 1
            $ ds_log("Heaters on high: spent power to keep the station safe (-22 power)")
            nout "Warm and safe… but it costs power. A safe choice, Suhail."

        "“Economy mode—some warmth, with power to spare”":
            $ ds_heater = "eco"
            $ ds_energy = max(0, ds_energy - 10)
            $ ds_smart += 1
            $ ds_log("Economy mode: balanced warmth and power (-10 power)")
            nout "Being smart doesn’t mean spending more… it means using just what you need."

        "“Turn off the heaters—power is more important”":
            $ ds_heater = "off"
            $ ds_risky += 1
            $ ds_log("Turned off all heaters… the cold reached the batteries")
            nout "This cold is serious, Suhail… a frozen battery won’t charge even when the Sun comes back."

    nout "Science fact: A Martian night can reach -110°! Opportunity needed its heaters. When its batteries got too cold, they stopped charging."

    call ds_nightfall from _call_ds_nightfall_2
    jump ds_sol4

# ---------------------------------------------------------------- SOL 4 — the antenna broke!

label ds_sol4:
    $ ds_sol = 4
    $ ds_tau = 6.5
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    play sound "audio/alarm.wav"
    call ds_morning from _call_ds_morning_3
    show img_nout at ds_nout_right with dissolve
    show img_suhail at ds_suhail_left with dissolve

    nout "Warning! A strong gust hit the roof… the antenna broke at its base!"
    nout "Without the antenna, Earth can’t send us instructions or hear from us."

    menu:
        "“I’m free—I’ll go fix it!” (Spacewalk risk)":
            $ ds_energy = max(0, ds_energy - 6)
            $ ds_warmth = max(0, ds_warmth - 10)
            $ ds_log("Suhail went out to fix the antenna in the storm (-6 power, -10 warmth)")
            call ds_play_antenna from _call_ds_play_antenna
            if ds_antenna_bolts >= 3:
                $ ds_comms = min(100, ds_comms + 20)
                $ ds_smart += 1
                $ ds_log("Fully repaired the antenna! Signal is stronger than before")
                nout "Excellent! The antenna is perfect—Earth can hear you clearly!"
            elif ds_antenna_bolts == 2:
                nout "We fixed half of it… the signal is a little weak."
            else:
                $ ds_comms = max(0, ds_comms - 40)
                $ ds_risky += 1
                $ ds_log("Tried to fix the antenna, but cold and dust won (-40 signal)")
                nout "You went out for nothing… let’s not try that again, Suhail."

        "“Send Nout—he’s built for rough weather!”":
            $ ds_energy = max(0, ds_energy - 15)
            $ ds_nougat = True
            $ ds_smart += 1
            $ ds_log("Nout went to fix the antenna—the robot is right for the job (-15 power)")
            nout "At your service! I’m made of aluminum and code. This cold doesn’t scare me."
            $ renpy.pause(1.2, hard=False)
            python:
                import random
                fixed = random.random() < 0.72
            if fixed:
                nout "All done! The antenna is as good as new."
                nout "All three bolts are in… signal is at 100!"
                $ ds_comms = 100
            else:
                nout "One bolt is stuck! Dust got into the wires… the signal is a little weak."
                $ ds_comms = max(0, ds_comms - 20)
            nout "Suhail… was I really in danger in that cold and dust?"
            suhail "And remember: you’re not just a machine. You’re my friend."
            nout "…Okay. Thanks, Suhail. I’ll call this ‘Nout’s Brave Day’ in the station log."

        "“Stay inside—we’ll use the backup transmitter”":
            $ ds_comms = max(0, ds_comms - 40)
            $ ds_smart += 1
            $ ds_log("Chose safety: used the weak backup transmitter (-40 signal)")
            nout "Our messages will be weak… but we’re safe, and that matters."

    nout "Science fact: A message from Earth takes 12 minutes to reach Mars. When Opportunity went quiet, engineers spent months sending it instructions—but got no reply."

    call ds_nightfall from _call_ds_nightfall_3
    jump ds_sol5

label ds_play_antenna:
    $ ds_antenna_bolts = 0
    $ ds_antenna_timer = 35.0
    $ ds_antenna_done = False
    $ ds_needle_t = 0.0
    $ ds_needle_zone = 50.0
    $ ds_needle_speed = 1.6
    window hide
    show screen ds_antenna_game
    $ renpy.pause(3600.0, hard=True)
    hide screen ds_antenna_game
    window auto
    return

# ---------------------------------------------------------------- SOL 5 — the dark day

label ds_sol5:
    $ ds_sol = 5
    $ ds_tau = 10.8
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    play sound "audio/wind_howl.wav"
    play sound "audio/alarm.wav"
    call ds_morning from _call_ds_morning_4
    show img_nout at ds_nout_left with dissolve
    show img_suhail at ds_suhail_right with dissolve

    nout "This is the worst of it. Tau reached 10.8. The Sun is only a faint circle… like someone drew it in chalk."
    nout "Just like June 10, 2018… the day Opportunity went quiet."

    suhail "But I’m not going quiet."

    nout "The plan says: turn everything off and survive. But… there’s one more thing you could do."
    nout "We have enough power for just one thing… what will it be?"

    menu:
        "“Send our discovery to Earth—a 4-billion-year-old rock!” (Science)":
            $ ds_final_tx = True
            $ ds_science = min(100, ds_science + 25)
            $ ds_comms = min(100, ds_comms + 15)
            $ ds_energy = max(0, ds_energy - 28)
            $ ds_brave += 1
            $ ds_log("Sent our final science discovery to Earth before the storm peak (-28 power, +25 science)")
            show img_rock at ds_rock_spin
            suhail "Earth, can you hear me? I found a 4-billion-year-old rock with signs of ancient water inside!"
            nout "The message is on its way… it’ll arrive in 12 minutes! This is the biggest discovery of our mission."
            play sound "audio/squelch.wav"
            hide img_rock

        "“Turn everything off and save power for the heaters” (Survival)":
            $ ds_heater = "high"
            $ ds_energy = max(0, ds_energy - 10)
            $ ds_warmth = min(100, ds_warmth + 10)
            $ ds_smart += 1
            $ ds_log("Turned everything off except the heaters (-10 power, +10 warmth)")
            nout "The cold is what stopped Opportunity… you won’t end up the same way. Let’s turn things off and survive."

        "“Share the last power with Nout” (Crew)":
            $ ds_energy = max(0, ds_energy - 18)
            $ ds_science = max(0, ds_science - 8)
            $ ds_nougat = True
            $ ds_smart += 1
            $ ds_log("Shared our last power with Nout instead of the science equipment (-18 power, -8 science)")
            nout "…Me? You’re protecting me?"
            suhail "You’re my first friend on all of Mars. I won’t let anything happen to you."
            nout "All right… that’s the best thing in the station. Don’t put that in the official log, Suhail!"

    nout "Science fact: Tau 10.8 means less than 1%% of the usual sunlight gets through. The Martian Sun almost disappeared."
    nout "Opportunity said, ‘I’m sleeping… I’ll wake when the Sun comes back.’ But it never woke up."

    call ds_nightfall from _call_ds_nightfall_4
    jump ds_sol6

# ---------------------------------------------------------------- SOL 6 — the dust devil

label ds_sol6:
    $ ds_sol = 6
    $ ds_tau = 2.0
    scene bg_station with fade
    show screen ds_hud
    show screen ds_storm_veil
    call ds_morning from _call_ds_morning_5
    show img_nout at ds_nout_right with dissolve
    show img_suhail at ds_suhail_left with dissolve

    nout "Day 6… the Sun is back! Look—it’s dim, but it’s there."
    nout "But the panels are covered in thick dust. The camera says only about 3%% of the sunlight gets through."

    show img_dustdevil at ds_devil_in
    nout "Wait… I see something moving… a little dust devil is coming our way!"

    suhail "A dust devil! If I open the panel covers, it might sweep off all the dust!"
    nout "Or it could hit the station and break things… you’re taking another chance, Suhail!"

    menu:
        "“Open the covers—let the dust devil do its work!” (Gamble!)":
            $ ds_brave += 1
            python:
                import random
                ds_devil_lucky = random.random() < 0.7
            if ds_devil_lucky:
                $ ds_dust = 5
                $ ds_energy = min(100, ds_energy + 20)
                $ ds_log("Opened the covers for the dust devil… it cleaned the panels! (dust 5, +20 power)")
                nout "The dust devil spun… spun… and left! The panels are shining like new!"
                nout "That really happened on Mars—dust devils brought the panels back to life!"
                suhail "Mars itself helped us!"
            else:
                $ ds_log("Opened the covers… the dust devil passed without helping")
                nout "It passed… and cleaned nothing! At least the panels are still standing."
        "“Close everything and wait—safety first” (Safe)":
            $ ds_smart += 1
            $ ds_log("Closed the covers and waited for the dust devil to pass safely")
            nout "A wise choice—survival first. We can check the panels tomorrow."

    hide img_dustdevil

    nout "Science fact: In 2004 and 2014, Opportunity’s cameras saw small dust devils clean its panels. Without them, it might not have lasted so long."

    "The storm is over. Mars slowly begins to breathe again… the battlefield is quiet."

    call ds_nightfall from _call_ds_nightfall_5
    jump ds_ending_dispatch

# ###################################################################
#  ENDINGS
# ###################################################################

label ds_ending_dispatch:
    hide screen ds_hud
    hide screen ds_storm_veil
    stop music fadeout 1.2
    if ds_frozen:
        jump ds_ending_dark
    if ds_final_tx and ds_science >= 45:
        jump ds_ending_brave
    if ds_smart >= 4 and ds_comms >= 40:
        jump ds_ending_gold
    jump ds_ending_silver

label ds_ending_gold:
    $ ds_cert_badge = "badge_gold"
    $ ds_cert_title = "Responsible Astronaut"
    $ ds_cert_sub   = "THE RESPONSIBLE ASTRONAUT"
    $ ds_cert_line  = "A perfect balance of science, survival, and teamwork… that’s what real astronauts do every day."
    scene bg_station with fade
    show img_nout at ds_nout_left with dissolve
    show img_suhail_happy at ds_suhail_right with dissolve
    play sound "audio/success.wav"
    nout "The storm is over, the panels are clean… and all your gauges look good!"
    nout "From Earth: ‘Well done, Suhail! Balance is an astronaut’s most important skill.’"
    suhail "I did all this with my choices… and every choice had a cost!"
    nout "That’s the lesson Opportunity taught us… and you made it through by thinking carefully."
    $ persistent.ds_best_tier = max(persistent.ds_best_tier, 3)
    $ persistent.ds_runs += 1
    jump ds_outro

label ds_ending_silver:
    $ ds_cert_badge = "badge_silver"
    $ ds_cert_title = "Cool-Headed Survivor"
    $ ds_cert_sub   = "THE COOL-HEADED SURVIVOR"
    $ ds_cert_line  = "You survived… but it cost you a lot. Next time, try to make more balanced choices."
    scene bg_station with fade
    show img_nout at ds_nout_left with dissolve
    show img_suhail_afraid at ds_suhail_right with dissolve
    play sound "audio/start.wav"
    nout "We made it! But we had to give up some things along the way…"
    suhail "I know… each choice took something away from something else."
    nout "We all learn. The important thing is that you’re here to tell the story. Next time, you’ll be even wiser."
    $ persistent.ds_best_tier = max(persistent.ds_best_tier, 2)
    $ persistent.ds_runs += 1
    jump ds_outro

label ds_ending_brave:
    $ ds_cert_badge = "badge_bronze"
    $ ds_cert_title = "Brave Heart for Science"
    $ ds_cert_sub   = "THE BRAVE HEART"
    $ ds_cert_line  = "Science first! Your discovery reached Earth… but risky choices cost a lot. Mars rewards careful thinkers."
    scene bg_station with fade
    show img_nout at ds_nout_left with dissolve
    show img_suhail_amazed at ds_suhail_right with dissolve
    show img_rock at ds_rock_spin
    play sound "audio/success.wav"
    nout "Earth got the discovery! Science teams around the world are talking about your rock!"
    suhail "The risk was worth it to protect this discovery."
    nout "Science needs a brave heart like yours… and a thoughtful mind, too. Keep a balance!"
    hide img_rock
    $ persistent.ds_best_tier = max(persistent.ds_best_tier, 1)
    $ persistent.ds_runs += 1
    jump ds_outro

label ds_ending_dark:
    $ ds_cert_badge = "badge_dark"
    $ ds_cert_title = "Opportunity’s Silence"
    $ ds_cert_sub   = "ECHO OF OPPORTUNITY"
    $ ds_cert_line  = "The batteries froze… just like Opportunity’s. But every journey can begin again."
    scene bg_station with fade
    show img_nout at ds_nout_left with dissolve
    show img_suhail_afraid at ds_suhail_right with dissolve
    play sound "audio/freeze.wav"
    suhail "…Nout?"
    nout "…I’m here, Suhail. But the batteries are completely dead."
    "The screen went dark. The cold filled the station. Mars fell silent around its new heroes."
    nout "Suhail… you’re not Opportunity. You’re a hero who learns from every try."
    nout "NASA’s engineers tried more than 1,000 times to reach Opportunity… and you have many more chances than that."
    $ persistent.ds_runs += 1
    jump ds_outro

# ###################################################################
#  OUTRO: quiz + certificate
# ###################################################################

label ds_outro:
    hide screen ds_hud
    hide screen ds_storm_veil
    call ds_quiz from _call_ds_quiz
    call ds_certificate from _call_ds_certificate
    return

label ds_quiz:
    scene bg_station with fade
    show img_nout at ds_nout_left with dissolve
    show img_suhail at ds_suhail_right with dissolve

    nout "I’m proud of you… now let’s see what you learned about Mars! Just three questions."

    $ ds_quiz = 0

    menu:
        "1) What does tau measure in a dust storm?"
        "… How thick the dust is, or how much it blocks the Sun":
            $ ds_quiz += 1
            nout "That’s right! A high tau means the Sun is hidden. In 2018 it reached 10.8—almost like night in the middle of the day!"
        "… Wind speed at the surface":
            nout "Not quite. Wind speed matters, but tau measures how thick the dust is and how much light gets through."
        "… The temperature on Mars":
            nout "Not quite. Temperature tells us how hot or cold it is. Tau tells us how much dust blocks the Sun."

    menu:
        "2) How did Curiosity keep working during the planet-wide storm?"
        "… It was the strongest rover on Mars":
            nout "Not quite. Curiosity uses nuclear power (an RTG), not sunlight."
        "… It uses an RTG, so it doesn’t depend on sunlight":
            $ ds_quiz += 1
            nout "Well done! Curiosity and Perseverance use nuclear power. The Sun was hidden for a week, but they kept working."
        "… It was on a mountain, above the dust":
            nout "Not quite. A mountain can’t protect a rover from dust. Nuclear power kept Curiosity running."

    menu:
        "3) What can Martian dust devils do?"
        "… Sometimes they clean solar panels and help them work again":
            $ ds_quiz += 1
            nout "That’s right! NASA saw them sweep dust off the panels. They helped Opportunity last for 15 years!"
        "… They always break stations":
            nout "Not always! They’re usually small, but a strong hit could break something."
        "… They don’t exist on Mars":
            nout "They do! Mars has many small dust devils, and satellites have photographed lots of them."

    nout "Want to see your score? [ds_quiz] out of 3. Science always helps us on our journey."
    return

# --- astronaut certificate

default ds_cert_badge = "badge_gold"
default ds_cert_title = "Responsible Astronaut"
default ds_cert_sub   = "THE RESPONSIBLE ASTRONAUT"
default ds_cert_line  = ""

init python:
    def ds_best_name():
        return {0: "—", 1: "Brave Heart (Bronze)", 2: "Cool-Headed Survivor (Silver)", 3: "Responsible Astronaut (Gold)"}.get(persistent.ds_best_tier, "—")

screen ds_cert():
    modal True
    add Solid("#000000cc")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 8

        text "Astronaut Certificate" size 32 bold True color "#ffd9a0" xalign 0.5 font "fonts/Vazirmatn.ttf"

        add ds_cert_badge xalign 0.5 zoom 0.58

        text ds_cert_title size 38 bold True color "#ffe9c9" xalign 0.5 font "fonts/Vazirmatn.ttf"
        text ds_cert_sub size 19 bold True color "#c9a06a" xalign 0.5 font "fonts/Vazirmatn.ttf"

        frame:
            background Solid("#1a0f06dd")
            padding (28, 12)
            xalign 0.5
            vbox:
                spacing 4
                text "Science: [ds_science] / 100" size 20 color "#b388ff" xalign 0.5 font "fonts/Vazirmatn.ttf"
                text "Signal to Earth: [ds_comms] / 100" size 20 color "#5ce0ff" xalign 0.5 font "fonts/Vazirmatn.ttf"
                text "Water left: [ds_water] units" size 20 color "#a8d8ff" xalign 0.5 font "fonts/Vazirmatn.ttf"
                text "Balanced choices: [ds_smart]     Brave: [ds_brave]     Risky: [ds_risky]" size 17 color "#ffe9c9" xalign 0.5 font "fonts/Vazirmatn.ttf"
                text "Mars quiz: [ds_quiz] / 3" size 17 color "#ffd166" xalign 0.5 font "fonts/Vazirmatn.ttf"
                text "Best badge so far: [ds_best_name()]" size 16 italic True color "#c9a06a" xalign 0.5 font "fonts/Vazirmatn.ttf"

        text ds_cert_line size 18 italic True color "#ffe9c9" xalign 0.5 text_align 0.5 font "fonts/Vazirmatn.ttf"

        textbutton "Dust off! All right!" xalign 0.5 yoffset 4 action Function(renpy.end_interaction, True) text_color "#ffd9a0" text_size 22

label ds_certificate:
    scene bg_station with fade
    stop music fadeout 0.8
    window hide
    show screen ds_cert
    $ renpy.pause(3600.0, hard=True)
    hide screen ds_cert
    window auto
    return

# ###################################################################
#  ENTRY POINTS
# ###################################################################

label dust_storm_story:
    $ renpy.block_rollback()
    $ ds_reset_game()
    call ds_intro from _call_ds_intro
    call ds_sol1 from _call_ds_sol1
    return

label dust_storm_start:
    $ renpy.block_rollback()
    $ ds_reset_game()
    call ds_intro from _call_ds_intro_1
    call ds_sol1 from _call_ds_sol1_1

    menu:
        "Try again — choose a different plan":
            jump dust_storm_start
        "Return to the menu":
            return
