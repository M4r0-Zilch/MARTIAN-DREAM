################################################################################
##  SOLAR FLARE  -  drop-in minigame (single file)
################################################################################
##
##  HOW TO INTEGRATE INTO YOUR REN'PY GAME (3 steps):
##
##   1. Copy this file (solar_flare.rpy) into your project's game/ folder.
##   2. Copy the contents of game/images/ and game/audio/ into your project's
##      game/images/ and game/audio/ folders (merge, don't overwrite).
##   3. In your story, call it:
##
##        call solar_flare_start          # standalone (title screen, game over)
##        # or
##        call solar_flare_story          # embedded (no title, returns when done)
##
##  That's it. No other files needed. No gui.rpy or screens.rpy changes.
##
##  The game uses only standard Ren'Py + pygame (included with Ren'Py).
##  Resolution: 1280x720. Assets: bg, ship, flare, boom, dots, mars + audio.
##
##  CURRENT GAME DESIGN (SOLAR FLARE):
##   - The whole game lasts 30 SECONDS = 10 danger-zone rounds x 3 seconds.
##   - The RED ZONE covers the whole screen except ONE small safe spot,
##     and that spot changes position every round.
##   - The Solar Flare is visible at the bottom (static) and shoots FIRE.
##   - Press X to raise a SHIELD that deflects / blocks the flames.
##   - The fire NEVER enters the safe spot (difficulty stays logical).
##   - Win = survive the 30 seconds. Lose = suit integrity reaches 0.
##
################################################################################

default persistent.solar_best = 0

init -20 python:
    import math
    import random
    try:
        import pygame
    except ImportError:
        import renpy.pygame as pygame


init -10 python:
    from renpy.display import im as _sf_im
    from renpy.text.text import Text as _SfText

    def _sf_make_images():
        d = {}
        d["bg"] = _sf_im.Image("images/bg_space.png")
        d["stars"] = _sf_im.Image("images/bg_stars.png")
        d["vig"] = _sf_im.Image("images/vignette.png")
        d["ship"] = [_sf_im.Image("images/ship_left.png"),
                     _sf_im.Image("images/ship.png"),
                     _sf_im.Image("images/ship_right.png")]
        d["glow"] = _sf_im.Image("images/ship_glow.png")
        d["boom"] = [_sf_im.Image("images/boom_%02d.png" % i) for i in range(14)]
        d["dots"] = {}
        for c in ("white", "orange", "cyan", "grey"):
            for s in (8, 16, 28):
                for a in range(3):
                    d["dots"][(c, s, a)] = _sf_im.Image("images/dot_%s_%d_%d.png" % (c, s, a))
        d["mars"] = _sf_im.Image("images/mars.png")
        d["flare"] = _sf_im.Image("images/flare.png")
        return d

    SF = _sf_make_images()

    def sf_col(t):
        t = max(0.0, min(1.0, t))
        r = int(70 + 185 * t)
        g = int(225 - 145 * t)
        b = int(255 - 185 * t)
        return "#%02x%02x%02x" % (r, g, b)


init -5 python:
    import math, random

    class SfSpark(object):
        def __init__(self, x, y, vx, vy, life, color, size, drag=2.0):
            self.x = x; self.y = y; self.vx = vx; self.vy = vy
            self.life = life; self.max_life = life
            self.color = color; self.size = size; self.drag = drag

    class SolarFlareGame(renpy.Displayable):
        def __init__(self, best=0, **kwargs):
            super(SolarFlareGame, self).__init__(**kwargs)
            self.best = int(best)
            self.w = 1280; self.h = 720
            self.last_st = None
            self._texts = {}; self._scache = {}
            self.reset()

        def reset(self):
            self.t = 0.0; self.state = "ready"
            self.ready = 0.6; self.go = 0.6
            self.total = 30.0             # whole game = 30 seconds
            self.round = 0                # current danger-zone round (0..9)
            self.round_len = 3.0          # each challenge is 3 seconds
            self.rounds_total = 10        # 10 challenges = 30 seconds
            self.round_t = 0.0
            self.grace = 0.0              # short grace at round start
            self.death_t = 0.0; self.win_t = 0.0
            self.shake = 0.0; self.flash = 0.0
            self.paused = False; self.finished = False; self.result = None
            self.ship_x = self.w * 0.5; self.ship_y = self.h * 0.62
            self.tilt = 0.0
            self.dash_cd = 0.0; self.dash_timer = 0.0; self.invincible = 0.0
            self.dash_dir = (0.0, 0.0)
            self.flare_anim = 0.0
            self.hp = 100.0
            self.fire = []                # solar flare fire bolts
            self.fire_cd = 0.0
            self.shield_cd = 0.0          # cooldown until next shield use
            self.shield_timer = 0.0       # shield active time left
            # safe spot: the one small area that is NOT red - changes each round
            self.safe = {"x": self.w*0.5 - 180.0, "y": self.h*0.30 - 120.0,
                         "w": 360.0, "h": 240.0}
            self.sparks = []
            self.bg_off = 0.0; self.stars_off = 0.0
            self.prev_esc = False; self.prev_space = False; self.prev_shift = False; self.prev_x = False
            self.mouse_mode = False; self.mouse_last = None
            self.thrust = 0.0; self.boom_pos = None
            self.win_flash = 0.0; self._dark = None

        def score(self):
            return int(self.t * 100.0) + (1000 if self.state == "won" else 0)

        def finish(self, quit=False, won=False):
            if self.finished: return
            sc = self.score()
            self.result = {"score": sc, "time": self.t, "won": won,
                           "best": max(self.best, sc), "new_best": sc > self.best,
                           "quit": quit}
            self.finished = True
            self.state = "won" if won else "lost"
            renpy.end_interaction(self.result)

        def _keys(self):
            try: return pygame.key.get_pressed()
            except Exception: return None

        def _in_safe(self):
            s = self.safe
            return (self.ship_x > s["x"] and self.ship_x < s["x"] + s["w"] and
                    self.ship_y > s["y"] and self.ship_y < s["y"] + s["h"])

        def _new_safe(self):
            # new small safe spot each round - changes position every time
            old = self.safe
            for _ in range(30):
                x = random.uniform(90.0, self.w - 90.0 - 360.0)
                y = random.uniform(120.0, self.h - 90.0 - 240.0)
                if abs(x - old["x"]) > 150.0 or abs(y - old["y"]) > 150.0:
                    return {"x": x, "y": y, "w": 360.0, "h": 240.0}
            return {"x": self.w*0.5 - 180.0, "y": 130.0, "w": 360.0, "h": 240.0}

        def _burst(self, x, y, color, scale=1.0):
            for i in range(10):
                a = random.uniform(0, math.pi*2)
                sp = random.uniform(60, 220) * scale
                self.sparks.append(SfSpark(x, y,
                    math.cos(a)*sp, math.sin(a)*sp,
                    random.uniform(0.3,0.6), color, 8, 1.2))

        def step(self, dt):
            if self.finished: return
            keys = self._keys()
            # pause / quit
            esc = False
            if keys is not None:
                try: esc = bool(keys[pygame.K_ESCAPE])
                except Exception: esc = False
            if esc and not self.prev_esc: self.paused = not self.paused
            self.prev_esc = esc
            if self.paused: return
            # dash input
            space = shift = False
            if keys is not None:
                try:
                    space = bool(keys[pygame.K_SPACE])
                    shift = bool(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
                except Exception: space = shift = False
            want_dash = (space and not self.prev_space) or (shift and not self.prev_shift)
            self.prev_space = space; self.prev_shift = shift
            # shield input (X button)
            x_key = False
            if keys is not None:
                try: x_key = bool(keys[pygame.K_x])
                except Exception: x_key = False
            want_shield = x_key and not self.prev_x
            self.prev_x = x_key
            # movement
            kx = ky = 0
            if keys is not None:
                try:
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]: kx -= 1
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: kx += 1
                    if keys[pygame.K_UP] or keys[pygame.K_w]: ky -= 1
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]: ky += 1
                except Exception: kx = ky = 0
            if want_shield and self.shield_cd <= 0.0:
                self.shield_timer = 1.4
                self.shield_cd = 4.0
                renpy.sound.play("audio/shield.wav")
                self._burst(self.ship_x, self.ship_y, "cyan", 1.4)
            if want_dash and self.dash_cd <= 0.0:
                self.dash_cd = 1.35; self.dash_timer = 0.22; self.invincible = 0.30
                if kx or ky:
                    ln = math.hypot(kx, ky) or 1.0
                    self.dash_dir = (kx/ln, ky/ln)
                else:
                    self.dash_dir = (0.0, -1.0)
                renpy.sound.play("audio/dash.wav")
                for i in range(8):
                    self.sparks.append(SfSpark(self.ship_x, self.ship_y,
                        -self.dash_dir[0]*random.uniform(40,120),
                        -self.dash_dir[1]*random.uniform(40,120),
                        random.uniform(0.2,0.4), "cyan", 12, 4.0))
            if self.dash_timer > 0.0: sp = 720.0
            else: sp = 360.0
            if kx or ky:
                self.mouse_mode = False
                ln = math.hypot(kx, ky) or 1.0
                self.ship_x += kx/ln * sp * dt
                self.ship_y += ky/ln * sp * dt
                self.tilt += (kx - self.tilt) * min(1.0, dt*12.0)
            else:
                try: mx, my = renpy.get_mouse_pos()
                except Exception: mx, my = -1, -1
                if self.mouse_last is not None and mx >= 0 and my >= 0:
                    if abs(mx-self.mouse_last[0])+abs(my-self.mouse_last[1]) >= 4:
                        self.mouse_mode = True
                self.mouse_last = (mx, my)
                if self.mouse_mode and 0 <= mx <= self.w and 0 <= my <= self.h:
                    kk = 1.0 - math.exp(-dt*14.0)
                    self.ship_x += (mx-self.ship_x)*kk
                    self.ship_y += (my-self.ship_y)*kk
                self.tilt += (0.0-self.tilt) * min(1.0, dt*9.0)
            if self.dash_timer > 0.0:
                self.ship_x += self.dash_dir[0]*520.0*dt
                self.ship_y += self.dash_dir[1]*520.0*dt
            m = 40.0
            self.ship_x = min(max(self.ship_x, m), self.w-m)
            self.ship_y = min(max(self.ship_y, 60.0), self.h-60.0)
            if self.dash_cd > 0: self.dash_cd -= dt
            if self.dash_timer > 0: self.dash_timer -= dt
            if self.invincible > 0: self.invincible -= dt
            if self.shield_cd > 0: self.shield_cd -= dt
            if self.shield_timer > 0: self.shield_timer -= dt
            # state machine
            world_dt = dt
            if self.state == "ready":
                self.ready -= dt
                if self.ready <= 0.0:
                    self.state = "play"; self.go = 0.6
                    renpy.sound.play("audio/start.wav")
            elif self.state == "play":
                self.t += dt
                if self.t >= self.total:
                    self.win(); return
                # ---- danger-zone rounds: each 3 seconds, 10 rounds ----
                self.round_t += dt
                self.round = min(self.rounds_total - 1, int(self.t / self.round_len))
                self.grace = max(0.0, self.grace - dt)
                if self.round_t >= self.round_len:
                    self.round_t = 0.0
                    self.safe = self._new_safe()   # the small spot MOVES each round
                    self.grace = 0.6
                # ---- the solar flare (visible at the bottom) shoots FIRE ----
                self.fire_cd -= dt
                if self.fire_cd <= 0.0:
                    self.fire_cd = random.uniform(0.55, 0.8)
                    bx = self.w * 0.5; by = self.h - 90.0
                    ang = math.atan2(self.ship_y - by, self.ship_x - bx)
                    self.fire.append({"x": bx, "y": by,
                                      "vx": math.cos(ang), "vy": math.sin(ang),
                                      "speed": 340.0, "life": 2.6, "max_life": 2.6, "size": 16})
                # ---- update fire bolts ----
                for b in self.fire[:]:
                    b["life"] -= dt
                    b["x"] += b["vx"] * b["speed"] * dt
                    b["y"] += b["vy"] * b["speed"] * dt
                    s = self.safe
                    # fire NEVER merges with / enters the safe spot of the
                    # danger-zone challenge (difficulty stays logical)
                    if (b["x"] > s["x"] and b["x"] < s["x"] + s["w"] and
                        b["y"] > s["y"] and b["y"] < s["y"] + s["h"]):
                        self._burst(b["x"], b["y"], "orange", 0.5)
                        self.fire.remove(b)
                        continue
                    if b["life"] <= 0.0:
                        self.fire.remove(b)
                # ---- ship health: safe inside the small spot, burning outside ----
                if self._in_safe():
                    self.hp = min(100.0, self.hp + 6.0 * dt)
                elif self.grace <= 0.0:
                    self.hp -= 20.0 * dt
                # ---- fire vs ship (shield deflects it) ----
                if self.shield_timer > 0.0 or self.invincible > 0.0:
                    for b in self.fire[:]:
                        if math.hypot(b["x"]-self.ship_x, b["y"]-self.ship_y) < (22.0 + b["size"]):
                            self.fire.remove(b)
                            self._burst(b["x"], b["y"], "cyan", 0.8)
                            renpy.sound.play("audio/dash.wav")
                elif self.invincible <= 0.0:
                    for b in self.fire[:]:
                        if math.hypot(b["x"]-self.ship_x, b["y"]-self.ship_y) < (16.0 + b["size"]):
                            self.fire.remove(b)
                            self.hp -= 25.0
                            renpy.sound.play("audio/hit.wav")
                            self.shake = max(self.shake, 0.35)
                            self.flash = max(self.flash, 0.25)
                            if self.hp <= 0.0: break
                if self.hp <= 0.0:
                    self.hp = 0.0
                    self.die(); return
                # thrust sparks under ship
                self.thrust += dt*50.0
                while self.thrust >= 1.0:
                    self.thrust -= 1.0
                    self.sparks.append(SfSpark(self.ship_x+random.uniform(-6,6),
                        self.ship_y+14.0, random.uniform(-20,20), random.uniform(30,80),
                        random.uniform(0.2,0.35), "cyan", 8, 3.0))
            elif self.state == "dying":
                world_dt = dt*0.3; self.death_t += dt
                self.shake = max(0.0, self.shake - dt*1.6)
                if self.death_t >= 1.6: self.finish(quit=False, won=False)
            elif self.state == "won":
                world_dt = dt*0.6; self.win_t += dt
                self.win_flash = min(1.0, self.win_flash + dt*1.2)
                if self.win_t >= 2.4: self.finish(quit=False, won=True)
            self.flare_anim += dt*6.0
            for s in self.sparks:
                s.life -= world_dt; s.x += s.vx*world_dt; s.y += s.vy*world_dt
                if s.drag:
                    f = max(0.0, 1.0 - s.drag*world_dt); s.vx *= f; s.vy *= f
            if self.sparks and self.sparks[0].life <= 0.0:
                self.sparks = [s for s in self.sparks if s.life > 0.0]
            self.bg_off = (self.bg_off + world_dt*(28.0 + self.t*0.6)) % self.h
            self.stars_off = (self.stars_off + world_dt*(60.0 + self.t*1.2)) % self.h
            self.flash = max(0.0, self.flash - dt*2.4)

        def win(self):
            if self.state != "play": return
            self.state = "won"; self.win_t = 0.0; self.win_flash = 0.0
            self.boom_pos = None
            renpy.sound.play("audio/win.wav")
            for i in range(40):
                a = random.uniform(0, math.pi*2); sp = random.uniform(60,260)
                self.sparks.append(SfSpark(self.ship_x, self.ship_y,
                    math.cos(a)*sp, math.sin(a)*sp, random.uniform(0.6,1.4), "cyan", 16, 1.0))
            for i in range(20):
                a = random.uniform(0, math.pi*2); sp = random.uniform(30,140)
                self.sparks.append(SfSpark(self.ship_x, self.ship_y,
                    math.cos(a)*sp, math.sin(a)*sp, random.uniform(0.9,1.8), "white", 8, 0.8))

        def die(self):
            if self.state in ("dying","won","lost","done"): return
            self.state = "dying"; self.death_t = 0.0
            self.shake = 1.0; self.flash = 0.9
            self.boom_pos = (self.ship_x, self.ship_y)
            renpy.sound.play("audio/explosion.wav")
            for i in range(30):
                a = random.uniform(0, math.pi*2); sp = random.uniform(100,420)
                self.sparks.append(SfSpark(self.ship_x, self.ship_y,
                    math.cos(a)*sp, math.sin(a)*sp, random.uniform(0.5,1.2),
                    random.choice(("orange","white","orange")), 16, 1.2))
            for i in range(12):
                a = random.uniform(0, math.pi*2); sp = random.uniform(40,160)
                self.sparks.append(SfSpark(self.ship_x, self.ship_y,
                    math.cos(a)*sp, math.sin(a)*sp, random.uniform(1.0,2.0), "grey", 28, 0.8))

        def text(self, key, s, size, color="#eaf7ff", kerning=0):
            sig = (s, size, color, kerning)
            cached = self._texts.get(key)
            if cached is not None and cached[0] == sig: return cached[1]
            t = _SfText(s, size=size, color=color, bold=True, kerning=kerning,
                        outlines=[(2, "#04091a", 0, 0)])
            self._texts[key] = (sig, t); return t

        def blit_text(self, rv, key, s, size, x, y, color="#eaf7ff", kerning=0,
                      st=0.0, at=0.0, align="left", shake_x=0, shake_y=0):
            t = self.text(key, s, size, color, kerning)
            tr = renpy.render(t, self.w, self.h, st, at)
            if align == "center": x = x - tr.width*0.5
            elif align == "right": x = x - tr.width
            rv.blit(tr, (int(x+shake_x), int(y+shake_y))); return tr

        def render(self, width, height, st, at):
            self.w = width; self.h = height
            if self.last_st is None: dt = 0.0
            else: dt = st - self.last_st
            self.last_st = st; dt = max(0.0, min(dt, 0.05))
            self.step(dt)
            rv = renpy.Render(width, height)
            self.draw(rv, st, at)
            renpy.redraw(self, 0); return rv

        def draw(self, rv, st, at):
            w = self.w; h = self.h
            sx = sy = 0
            if self.shake > 0.01:
                amp = self.shake*14.0
                sx = random.uniform(-amp, amp); sy = random.uniform(-amp, amp)
            # background
            bg = renpy.render(Transform(SF["bg"], xysize=(w,h)), w, h, st, at)
            rv.blit(bg, (0,0))
            stars = renpy.render(Transform(SF["stars"], xysize=(w,h)), w, h, st, at)
            off = int(self.stars_off) % max(1,h)
            rv.blit(stars, (0, off)); rv.blit(stars, (0, off-h))
            # mars (top) - only visible on win
            if self.state == "won":
                mars_bg = renpy.render(Transform(SF["mars"], zoom=3.0), w, h, st, at)
                mx = int(w*0.5 - mars_bg.width*0.5 + sx)
                my = int(60 - mars_bg.height*0.5 + sy)
                rv.blit(mars_bg, (mx, my))
            # ---- the SOLAR FLARE, static at the bottom, shooting fire ----
            sun = renpy.render(Transform(SF["glow"], zoom=5.0), w, h, st, at)
            rv.blit(sun, (int(w*0.5 - sun.width*0.5 + sx), int(h - sun.height*0.45 + sy)))
            flare_h = 170
            fl = renpy.render(Transform(SF["flare"], xysize=(w, flare_h),
                                       alpha=0.85 + 0.15*math.sin(self.flare_anim)),
                              w, h, st, at)
            rv.blit(fl, (int(sx), int(h - flare_h + sy)))
            # ---- the RED ZONE: covers the whole screen EXCEPT the small safe spot ----
            s = self.safe
            if self.state in ("ready", "play"):
                red = "#ff2222"
                panels = [
                    (0, 0, w, s["y"]),                                  # top
                    (0, s["y"], s["x"], s["h"]),                         # left
                    (s["x"] + s["w"], s["y"], w - (s["x"] + s["w"]), s["h"]),  # right
                    (0, s["y"] + s["h"], w, h - (s["y"] + s["h"])),      # bottom
                ]
                for (px, py, pw, ph) in panels:
                    if pw > 0 and ph > 0:
                        rd = renpy.render(Transform(Solid(red), alpha=0.32,
                                                     xysize=(int(pw), int(ph))),
                                          w, h, st, at)
                        rv.blit(rd, (int(px+sx), int(py+sy)))
                # safe spot: a clearly green, gently pulsing gameplay zone
                # (the green fill makes sure it never reads as a dark textbox)
                tint_a = 0.18 + 0.07 * (0.5 + 0.5 * math.sin(self.flare_anim * 0.9))
                tint = renpy.render(Transform(Solid("#00ff88"), alpha=tint_a,
                                              xysize=(int(s["w"]), int(s["h"]))),
                                    w, h, st, at)
                rv.blit(tint, (int(s["x"]+sx), int(s["y"]+sy)))
                # safe spot border (green)
                bd = [(0, 0, s["w"], 5), (0, s["h"]-5, s["w"], 5),
                      (0, 0, 5, s["h"]), (s["w"]-5, 0, 5, s["h"])]
                for (bx, by, bw, bh) in bd:
                    gd = renpy.render(Transform(Solid("#00ff88"), alpha=0.95,
                                                 xysize=(int(bw), int(bh))),
                                      w, h, st, at)
                    rv.blit(gd, (int(s["x"]+bx+sx), int(s["y"]+by+sy)))
                self.blit_text(rv, "safe", "SAFE ZONE", 14, s["x"]+s["w"]*0.5, s["y"]+s["h"]*0.5-7,
                               color="#00ff88", st=st, at=at, align="center")
            # ---- fire bolts ----
            for b in self.fire:
                frac = b["life"]/b["max_life"] if b["max_life"] else 0.0
                ai = 0 if frac > 0.62 else (1 if frac > 0.30 else 2)
                img = SF["dots"][(b["color"], b["size"], ai)] if "color" in b else SF["dots"][("orange", 16, ai)]
                cr = renpy.render(Transform(img, zoom=1.5), w, h, st, at)
                rv.blit(cr, (int(b["x"]-cr.width*0.5+sx), int(b["y"]-cr.height*0.5+sy)))
            # ---- sparks ----
            for s in self.sparks:
                frac = s.life/s.max_life if s.max_life else 0.0
                ai = 0 if frac > 0.62 else (1 if frac > 0.30 else 2)
                img = SF["dots"][(s.color, s.size, ai)]
                cr = renpy.render(Transform(img, zoom=1.5), w, h, st, at)
                rv.blit(cr, (int(s.x-cr.width*0.5+sx), int(s.y-cr.height*0.5+sy)))
            # ---- ship + shield bubble ----
            if self.state in ("ready", "play"):
                if self.shield_timer > 0.0:
                    sh = renpy.render(Transform(SF["glow"], zoom=3.4, alpha=0.7), w, h, st, at)
                    rv.blit(sh, (int(self.ship_x-sh.width*0.5+sx), int(self.ship_y-sh.height*0.5+sy)))
                idx = 0 if self.tilt < -0.35 else (2 if self.tilt > 0.35 else 1)
                cr = renpy.render(Transform(SF["ship"][idx], zoom=1.5), w, h, st, at)
                rv.blit(cr, (int(self.ship_x-cr.width*0.5+sx), int(self.ship_y-cr.height*0.5+sy)))
                gl = renpy.render(Transform(SF["glow"], zoom=2.2), w, h, st, at)
                rv.blit(gl, (int(self.ship_x-gl.width*0.5+sx), int(self.ship_y-gl.height*0.5+sy)))
            # dash trail
            if self.dash_timer > 0.0:
                tr = renpy.render(Transform(SF["glow"], zoom=2.0), w, h, st, at)
                rv.blit(tr, (int(self.ship_x-tr.width*0.5+sx), int(self.ship_y-tr.height*0.5+sy)))
            # explosion
            if self.boom_pos is not None:
                fi = min(13, int(self.death_t/1.6*14.0))
                cr = renpy.render(Transform(SF["boom"][fi], zoom=2.5), w, h, st, at)
                rv.blit(cr, (int(self.boom_pos[0]-cr.width*0.5+sx), int(self.boom_pos[1]-cr.height*0.5+sy)))
            # flash
            if self.flash > 0.01:
                fl = renpy.render(Transform(Solid("#ff0044"), alpha=self.flash*0.5), w, h, st, at)
                rv.blit(fl, (0,0))
            # win flash
            if self.win_flash > 0.01:
                fl = renpy.render(Transform(Solid("#ffffff"), alpha=self.win_flash*0.35), w, h, st, at)
                rv.blit(fl, (0,0))
            # vignette
            vg = renpy.render(Transform(SF["vig"], xysize=(w,h)), w, h, st, at)
            rv.blit(vg, (0,0))
            # ---- HUD ---- (no text in-game; only "SAFE ZONE" is shown)
            # health bar (graphic only - no text)
            hpw = 260.0
            hpfrac = max(0.0, min(1.0, self.hp/100.0))
            hp_bg = renpy.render(Transform(Solid("#331111"), xysize=(int(hpw), 12)), w, h, st, at)
            rv.blit(hp_bg, (24, 20))
            if hpfrac > 0.01:
                hpc = "#00ff88" if hpfrac > 0.5 else ("#ffd166" if hpfrac > 0.25 else "#ff0044")
                hp_fb = renpy.render(Transform(Solid(hpc), xysize=(int(hpw*hpfrac), 12)), w, h, st, at)
                rv.blit(hp_fb, (24, 20))
            # pause (silent dark overlay - no text)
            if self.paused:
                if self._dark is None: self._dark = Transform(Solid("#000000"), alpha=0.7)
                dk = renpy.render(self._dark, w, h, st, at); rv.blit(dk, (0,0))


################################################################################
##  Screens
################################################################################

screen solar_flare_game(game):
    add game
    key "game_menu" action NullAction()


################################################################################
##  Entry points
################################################################################

label solar_flare_story:
    $ renpy.block_rollback()
    window hide
    $ _sf_game = SolarFlareGame(best=persistent.solar_best)
    show screen solar_flare_game(game=_sf_game)
    $ _sf_result = renpy.pause(3600.0, hard=True)
    hide screen solar_flare_game
    window auto
    $ _sf_game = None
    $ _sf_result = None
    return

label solar_flare_start:
    $ renpy.block_rollback()
    window hide
    $ sf_game = SolarFlareGame(best=persistent.solar_best)
    show screen solar_flare_game(game=sf_game)
    $ sf_result = renpy.pause(3600.0, hard=True)
    hide screen solar_flare_game
    window auto
    $ sf_game = None
    if sf_result is not None and sf_result.get("new_best"):
        $ persistent.solar_best = sf_result["best"]
    return
