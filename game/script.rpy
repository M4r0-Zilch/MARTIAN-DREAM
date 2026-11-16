# The script of the game goes in this file.

# Character definitions
define suhail = Character("Suhail", color="#ff9944")
define teacher = Character("Teacher", color="#ffffff")
define nut = Character("Nout", color="#5ce0ff")

# Intro characters (spaceship)
define s = Character("Suhail", color="#ff9944")
define n = Character("Nout", color="#5ce0ff")
define ship_sys = Character("Ship System", color="#e57373", what_italic=True)

# Image definitions (scaled to the game's 1280x720 resolution)
image bg classroom = Transform("images/bg/at school.jpg", xysize=(1280, 720), fit="fill")
image bg research = Transform("images/bg/research.jpg", xysize=(1280, 720), fit="fill")
image bg sleepy = Transform("images/bg/fall in sleep (2).jpg", xysize=(1280, 720), fit="fill")
image bg bedroom = Transform("images/bg/bed.png", xysize=(1280, 720), fit="fill")
image bg colony = Transform("images/bg/UnderGround Bunker space station.jpeg", xysize=(1280, 720), fit="fill")
image bg alert = Transform("images/bg/monitoring power alert.jpg", xysize=(1280, 720), fit="fill")
image bg corridor = Transform("images/bg/running away.jpeg.jpeg", xysize=(1280, 720), fit="fill")
image bg command = Transform("images/bg/servers room.png", xysize=(1280, 720), fit="fill")
image bg hydroponics = Transform("images/bg/plant control unit.png", xysize=(1280, 720), fit="fill")
image bg mars_outpost = Transform("images/bg/mars outpost.png", xysize=(1280, 720), fit="fill")
image bg welcome = Transform("images/bg/welcome to mars.png", xysize=(1280, 720), fit="fill")

image suhail uniform = Transform("images/sprites/normal with uniform.png", zoom=0.8)
image suhail suit = Transform("images/sprites/normal with suit.png", zoom=0.8)
image suhail happy = Transform("images/sprites/happy.png", zoom=0.4)
image suhail amazed = Transform("images/sprites/amazed.png", zoom=0.4)
image suhail afraid = Transform("images/sprites/afraid.png", zoom=0.4)
image suhail scared = Transform("images/sprites/scared.png", zoom=0.4)
image nut = Transform("images/sprites/ai bot.png", zoom=0.8)

# Stat tracking
default oxygen_level = 100
default water_level = 100
default energy_level = 100
default food_level = 100

# Resource HUD
screen resource_hud():
    frame:
        xalign 0.5
        yalign 0.02
        padding (15, 8)
        background "#000000aa"
        hbox:
            spacing 25
            text "O2: [oxygen_level]%" color "#00ffff" size 20
            text "WATER: [water_level]%" color "#4da6ff" size 20
            text "ENERGY: [energy_level]%" color "#ffcc00" size 20
            text "FOOD: [food_level]%" color "#66ff66" size 20

# Image definitions for intro spaceship scenes
image bg spaceship_cabin = Transform("images/bg/servers room.png", xysize=(1280, 720), fit="fill")
image bg spaceship_cabin_red = Transform("images/bg/monitoring power alert.jpg", xysize=(1280, 720), fit="fill")
image not_robot neutral = Transform("images/sprites/ai bot.png", zoom=1.0)

# The game starts here.
label start:

    # SCENE 1: CLASSROOM
    scene bg classroom
    with fade

    teacher "Class, today we’re talking about Mars, the fourth planet from the Sun. It may be one of the places where people could live in the future."

    suhail "But, teacher, I don’t think scientists have studied Mars enough yet."

    teacher "Why don’t you try doing some research yourself?"

    suhail "Oxygen... food... water... power... and medical problems. This is really complicated!"

    suhail "That’s okay. I can do it!"

    suhail "I’ll find a way to solve this."

    suhail "I can..."

    # SCENE 1: LATE-NIGHT RESEARCH AND RESOLVE
    scene bg research
    with dissolve

    "The room is quiet except for the hum of the computer. Suhail drops his bag, opens his laptop, and begins typing as notes and sketches of Mars cover the desk."

    "He stops typing and stares at the complicated data on the screen. Then he gives a quiet, determined smile."

    suhail "It doesn’t matter how hard it gets. I can do this."

    suhail "No one else is going to figure it out. I’ll be the one to solve this problem."

    # SCENE 2: EXHAUSTION AND FALLING ASLEEP
    scene bg sleepy
    with dissolve

    "Outside the window, the night sky grows dark. The desk lamp is the only light. Suhail’s eyelids grow heavy, and at last his head drops toward the desk."

    "He rests on his handwritten notes. His breathing slows as the desk lamp flickers and dims."

    suhail "I will… make it to Mars…"

    scene black
    with fade

    scene bg spaceship_cabin with fade
    play sound "audio/ambient.wav" loop
    show suhail suit at left with dissolve

    "..."
    "A soft beep sounds in the distance. The bed gives a small shake."

    s "What?! Where am I? Am I dreaming?"

    show not_robot neutral at center with dissolve
    "A robot named Nout floats over and shines a light ahead."

    n "Good morning, Suhail. Your temperature is normal, and your heart is beating 85 times a minute. That’s normal after a long sleep in orbit."

    s "Suhail?! How do you know my name? And who are you?"

    n "I’m N.O.T., the ship’s Navigation and Operations Tech robot. We’re heading to Mars, about 140 million kilometers from Earth."

    s "Mars?! I was just asleep in my bed! How did I suddenly become an astronaut?"

    n "The quick trip may have confused your memory, or your mind may still be catching up. Anyway, you’re in charge of this science mission."

    s "A science mission? What are we going there to do?"

    n "Our mission has two main parts."

    n "First, we’ll study Mars and its space environment. Its air is very thin—less than 1%% as thick as Earth’s. It is 95%% carbon dioxide, and Mars has no magnetic field to protect it."

    n "Second, and most important, we’ll study how space conditions affect living things. This is called space biology."

    s "What does that mean?"

    n "We’ll test how Mars’s gravity—which is only 38%% as strong as Earth’s—and space radiation affect cells, muscles, and the plants we’ll need to live there."

    s "So we’re finding out how people and plants could handle living on Mars?"

    n "Exactly! Long exposure to radiation and low gravity can stress cells and change how genes work. We brought living samples to test in the Mars lab."

    # Dramatic turn: solar flare alert
    stop sound
    play sound "audio/alarm.wav" loop
    scene bg spaceship_cabin_red with vpunch
    show suhail suit at left with dissolve
    show not_robot neutral at right with dissolve

    "Suddenly, every screen turns red. A loud alarm fills the ship."

    ship_sys "Warning! Dangerous solar activity detected!"

    s "What’s that sound? Why did the screens turn red?"

    n "It’s the space weather warning system! Satellites spotted a huge solar storm. A cloud of solar material is racing toward us at 1,800 kilometers per second!"

    s "What does that mean? Are we going to burn up?"

    n "Heat isn’t the main danger. The real danger is the storm of solar particles and harmful radiation. Out here, the ship alone can’t block enough of it. The equipment could fail, and the radiation could badly hurt you."

    s "What can we do, Nout?"

    n "We need to make an emergency landing on Mars right now! Mars has thin air, but we can shelter under the ground and block much of the radiation until the storm passes."

    s "How much time do we have?"

    n "Less than 12 minutes before the first wave hits! Strap in, Suhail. We’re using full power to enter Mars’s atmosphere now!"

    stop sound
    scene black with fade
    "The engines roar to life. The ship shakes hard as we race toward the Red Planet."

    jump mars_landing

label mars_landing:
    # Hide the dialogue window itself, not just the say screen.  Hiding only the
    # screen leaves the empty textbox background on screen during the games.
    window hide

    # Solar flare minigame
    call solar_flare_story from _call_solar_flare_story

    # Keep the dialogue window hidden for the dust storm too.
    window hide
    call dust_storm_story from _call_dust_storm_story

    # Restore normal automatic dialogue-window handling for the ending.
    window auto

    # Ending
    scene bg colony
    with fade

    show nut at right with dissolve
    show suhail happy at left with dissolve

    nut "Thank you. It was an honor to meet you."

    nut "Knowing the truth and seeing how hard things are doesn’t mean you should give up. I believe in you."

    # As Nout bids farewell to Suhail, a bright light fills everything (Suhail wakes up in his bed)
    hide nut
    hide suhail
    scene expression Solid("#ffffff")
    with fade
    scene bg bedroom
    with fade

    suhail "Was all of that just a dream?"

    # In class where he is talking to his teacher (show the class scene and don't show the boy's sprite)
    scene bg classroom
    with fade

    suhail "And that’s how I learned to run a colony on Mars!"

    return

