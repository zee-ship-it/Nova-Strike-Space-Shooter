
# """
# ╔══════════════════════════════════════════════════════════════╗
# ║         🚀 NOVA STRIKE — Advanced Space Shooter v2.0        ║
# ║                Python 3.13 + Pygame ONLY                    ║
# ╠══════════════════════════════════════════════════════════════╣
# ║  FEATURES:                                                   ║
# ║  ✅ Beautiful Animated Main Menu                             ║
# ║  ✅ Neon Glow Effects + Animated Nebula Background           ║
# ║  ✅ Enemy AI Ships (chase + shoot player)                    ║
# ║  ✅ Boss Fights (every 5 levels, 3 attack patterns)         ║
# ║  ✅ Power-ups (Shield / Triple Shot / Speed / Nuke)         ║
# ║  ✅ Weapon Upgrade Tree (3 levels: Laser→Plasma→Ion Cannon) ║
# ║  ✅ Achievement System (10 unlockable achievements)         ║
# ║  ✅ High Score Leaderboard (saved to file)                  ║
# ║  ✅ End Game Stats Screen                                    ║
# ║  ✅ Screen Shake + Particle Explosions                       ║
# ╠══════════════════════════════════════════════════════════════╣
# ║  HOW TO RUN:                                                 ║
# ║    pip install pygame                                        ║
# ║    python space_shooter_v2.py                               ║
# ╠══════════════════════════════════════════════════════════════╣
# ║  CONTROLS:                                                   ║
# ║    W/A/S/D or Arrow Keys = Move & Rotate                    ║
# ║    SPACE = Shoot                                             ║
# ║    U     = Upgrade Weapon (costs 200 score)                 ║
# ║    P     = Pause                                             ║
# ║    ESC   = Quit                                             ║
# ╚══════════════════════════════════════════════════════════════╝
# """

# import pygame
# import random
# import math
# import sys
# import json
# import os

# pygame.init()

# # ══════════════════════════════════════════
# # CONSTANTS
# # ══════════════════════════════════════════
# SW, SH = 1000, 700
# FPS    = 60
# TITLE  = "NOVA STRIKE — Space Shooter v2.0"

# # Color Palette (Neon Theme)
# BG          = (3, 5, 20)
# WHITE       = (255, 255, 255)
# CYAN        = (0, 255, 255)
# CYAN_DIM    = (0, 140, 160)
# YELLOW      = (255, 220, 0)
# RED         = (255, 40, 40)
# RED_DIM     = (180, 20, 20)
# ORANGE      = (255, 130, 0)
# BLUE        = (30, 80, 255)
# BLUE_DIM    = (20, 50, 180)
# PURPLE      = (180, 0, 255)
# PURPLE_DIM  = (100, 0, 160)
# GREEN       = (0, 255, 120)
# GREEN_DIM   = (0, 160, 80)
# PINK        = (255, 60, 180)
# GREY        = (110, 115, 130)
# DARK_PANEL  = (8, 12, 35)

# SCORE_FILE = "nova_strike_scores.json"

# # ══════════════════════════════════════════
# # UTILITY: NEON GLOW DRAW
# # ══════════════════════════════════════════
# def draw_glow_circle(surf, color, pos, radius, layers=3):
#     for i in range(layers, 0, -1):
#         r = min(255, color[0] // i)
#         g = min(255, color[1] // i)
#         b = min(255, color[2] // i)
#         glow_surf = pygame.Surface((radius*2*i, radius*2*i), pygame.SRCALPHA)
#         pygame.draw.circle(glow_surf, (r, g, b, 40), (radius*i, radius*i), radius*i)
#         surf.blit(glow_surf, (pos[0]-radius*i, pos[1]-radius*i))
#     pygame.draw.circle(surf, color, pos, radius)

# def draw_glow_line(surf, color, p1, p2, width=2, glow=6):
#     pygame.draw.line(surf, (color[0]//4, color[1]//4, color[2]//4), p1, p2, width+glow)
#     pygame.draw.line(surf, (color[0]//2, color[1]//2, color[2]//2), p1, p2, width+glow//2)
#     pygame.draw.line(surf, color, p1, p2, width)

# def draw_glow_polygon(surf, color, pts, width=0, glow=4):
#     if len(pts) < 3: return
#     dim = (color[0]//3, color[1]//3, color[2]//3)
#     if width == 0:
#         pygame.draw.polygon(surf, dim, pts)
#         pygame.draw.polygon(surf, color, pts, 2)
#     else:
#         pygame.draw.polygon(surf, dim, pts, width+glow)
#         pygame.draw.polygon(surf, color, pts, width)

# def draw_text_glow(surf, text, font, color, x, y, center=True):
#     glow_col = (min(255,color[0]//2), min(255,color[1]//2), min(255,color[2]//2))
#     for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
#         t = font.render(text, True, glow_col)
#         r = t.get_rect()
#         if center: r.center = (x, y)
#         else: r.topleft = (x, y)
#         surf.blit(t, (r.x+dx, r.y+dy))
#     t = font.render(text, True, color)
#     r = t.get_rect()
#     if center: r.center = (x, y)
#     else: r.topleft = (x, y)
#     surf.blit(t, r)

# # ══════════════════════════════════════════
# # LEADERBOARD
# # ══════════════════════════════════════════
# def load_scores():
#     if os.path.exists(SCORE_FILE):
#         try:
#             with open(SCORE_FILE) as f:
#                 return json.load(f)
#         except:
#             pass
#     return []

# def save_score(name, score, level, kills):
#     scores = load_scores()
#     scores.append({"name": name, "score": score, "level": level, "kills": kills})
#     scores.sort(key=lambda x: x["score"], reverse=True)
#     scores = scores[:10]
#     with open(SCORE_FILE, "w") as f:
#         json.dump(scores, f)
#     return scores

# # ══════════════════════════════════════════
# # ACHIEVEMENTS
# # ══════════════════════════════════════════
# ACHIEVEMENTS_DEF = [
#     {"id": "first_kill",   "name": "First Blood",     "desc": "Destroy your first enemy",      "icon": "💀"},
#     {"id": "score_1000",   "name": "Rising Star",     "desc": "Reach score 1,000",             "icon": "⭐"},
#     {"id": "score_5000",   "name": "Space Veteran",   "desc": "Reach score 5,000",             "icon": "🎖️"},
#     {"id": "boss_kill",    "name": "Boss Slayer",      "desc": "Defeat your first Boss",        "icon": "👑"},
#     {"id": "powerup_10",   "name": "Power Hungry",    "desc": "Collect 10 power-ups",          "icon": "⚡"},
#     {"id": "weapon_max",   "name": "Ion Master",      "desc": "Max out weapon to Ion Cannon",  "icon": "🔫"},
#     {"id": "no_damage",    "name": "Untouchable",     "desc": "Complete a level without damage","icon": "🛡️"},
#     {"id": "kills_50",     "name": "Ace Pilot",       "desc": "Destroy 50 enemies",            "icon": "🚀"},
#     {"id": "kills_100",    "name": "Galaxy Guardian", "desc": "Destroy 100 enemies",           "icon": "🌌"},
#     {"id": "level_10",     "name": "Deep Space",      "desc": "Reach Level 10",                "icon": "🪐"},
# ]

# class AchievementSystem:
#     def __init__(self):
#         self.unlocked = set()
#         self.popups = []

#     def check(self, key, score=0, kills=0, level=0, powerups=0, weapon=0, no_dmg=False, boss=False):
#         new = []
#         if key == "kill" and kills >= 1 and "first_kill" not in self.unlocked:
#             new.append("first_kill")
#         if score >= 1000 and "score_1000" not in self.unlocked:
#             new.append("score_1000")
#         if score >= 5000 and "score_5000" not in self.unlocked:
#             new.append("score_5000")
#         if boss and "boss_kill" not in self.unlocked:
#             new.append("boss_kill")
#         if powerups >= 10 and "powerup_10" not in self.unlocked:
#             new.append("powerup_10")
#         if weapon >= 3 and "weapon_max" not in self.unlocked:
#             new.append("weapon_max")
#         if no_dmg and "no_damage" not in self.unlocked:
#             new.append("no_damage")
#         if kills >= 50 and "kills_50" not in self.unlocked:
#             new.append("kills_50")
#         if kills >= 100 and "kills_100" not in self.unlocked:
#             new.append("kills_100")
#         if level >= 10 and "level_10" not in self.unlocked:
#             new.append("level_10")
#         for aid in new:
#             self.unlocked.add(aid)
#             ach = next(a for a in ACHIEVEMENTS_DEF if a["id"] == aid)
#             self.popups.append({"text": f"{ach['icon']} {ach['name']}", "timer": 200})

#     def update(self):
#         for p in self.popups:
#             p["timer"] -= 1
#         self.popups = [p for p in self.popups if p["timer"] > 0]

#     def draw(self, surf, font):
#         y = 120
#         for p in self.popups:
#             alpha = min(255, p["timer"] * 3)
#             t = font.render(f"ACHIEVEMENT: {p['text']}", True, YELLOW)
#             x = SW - t.get_width() - 20
#             pygame.draw.rect(surf, (20, 20, 5), (x-8, y-4, t.get_width()+16, t.get_height()+8), border_radius=6)
#             pygame.draw.rect(surf, YELLOW, (x-8, y-4, t.get_width()+16, t.get_height()+8), 2, border_radius=6)
#             surf.blit(t, (x, y))
#             y += 40

# # ══════════════════════════════════════════
# # NEBULA BACKGROUND
# # ══════════════════════════════════════════
# class Nebula:
#     def __init__(self):
#         self.blobs = []
#         for _ in range(12):
#             self.blobs.append({
#                 "x": random.randint(0, SW), "y": random.randint(0, SH),
#                 "r": random.randint(80, 200),
#                 "color": random.choice([PURPLE_DIM, BLUE_DIM, (0,40,80), (40,0,60)]),
#                 "speed": random.uniform(0.05, 0.2),
#                 "phase": random.uniform(0, math.pi*2)
#             })
#         self.t = 0
#         self.surf = pygame.Surface((SW, SH), pygame.SRCALPHA)

#     def update(self):
#         self.t += 0.01

#     def draw(self, surface):
#         self.surf.fill((0,0,0,0))
#         for b in self.blobs:
#             pulse = 1 + 0.15 * math.sin(self.t * 0.7 + b["phase"])
#             r = int(b["r"] * pulse)
#             cx, cy = int(b["x"]), int(b["y"] + math.sin(self.t * b["speed"] + b["phase"]) * 20)
#             for i in range(4, 0, -1):
#                 alpha = 18 - i * 3
#                 col = (*b["color"], max(0, alpha))
#                 pygame.draw.circle(self.surf, col, (cx, cy), r * i // 4)
#         surface.blit(self.surf, (0,0))

# class StarField:
#     def __init__(self, count=300):
#         self.stars = [[random.randint(0,SW), random.randint(0,SH),
#                        random.uniform(0.1,1.8), random.randint(1,3),
#                        random.randint(140,255)] for _ in range(count)]

#     def update(self, speed_mult=1.0):
#         for s in self.stars:
#             s[1] += s[2] * speed_mult
#             if s[1] > SH:
#                 s[1] = 0
#                 s[0] = random.randint(0, SW)

#     def draw(self, surf):
#         for s in self.stars:
#             c = s[4]
#             pygame.draw.circle(surf, (c, c, min(255,c+40)), (int(s[0]),int(s[1])), s[3])

# # ══════════════════════════════════════════
# # SCREEN SHAKE
# # ══════════════════════════════════════════
# class ScreenShake:
#     def __init__(self):
#         self.intensity = 0
#         self.offset = (0, 0)

#     def shake(self, amount):
#         self.intensity = max(self.intensity, amount)

#     def update(self):
#         if self.intensity > 0:
#             self.offset = (random.randint(-int(self.intensity), int(self.intensity)),
#                            random.randint(-int(self.intensity), int(self.intensity)))
#             self.intensity *= 0.85
#             if self.intensity < 0.5:
#                 self.intensity = 0
#                 self.offset = (0, 0)

# # ══════════════════════════════════════════
# # PARTICLES
# # ══════════════════════════════════════════
# class Particle:
#     def __init__(self, x, y, color, speed=3, life=40):
#         self.x, self.y = x, y
#         self.color = color
#         angle = random.uniform(0, math.pi*2)
#         spd = random.uniform(0.5, speed)
#         self.vx = math.cos(angle) * spd
#         self.vy = math.sin(angle) * spd
#         self.life = random.randint(life//2, life)
#         self.max_life = self.life
#         self.size = random.randint(2, 5)

#     def update(self):
#         self.x += self.vx
#         self.y += self.vy
#         self.vy += 0.05
#         self.vx *= 0.98
#         self.life -= 1

#     def draw(self, surf):
#         if self.life <= 0: return
#         ratio = self.life / self.max_life
#         r = min(255, int(self.color[0] * ratio))
#         g = min(255, int(self.color[1] * ratio))
#         b = min(255, int(self.color[2] * ratio))
#         size = max(1, int(self.size * ratio))
#         pygame.draw.circle(surf, (r,g,b), (int(self.x), int(self.y)), size)

#     @property
#     def alive(self): return self.life > 0

# def spawn_explosion(particles, x, y, colors=None, count=35, speed=4):
#     if colors is None: colors = [ORANGE, YELLOW, RED, WHITE]
#     for _ in range(count):
#         particles.append(Particle(x, y, random.choice(colors), speed))

# # ══════════════════════════════════════════
# # POWER-UPS
# # ══════════════════════════════════════════
# POWERUP_TYPES = [
#     {"type": "shield",      "color": CYAN,   "icon": "S", "label": "SHIELD RESTORE"},
#     {"type": "triple",      "color": GREEN,  "icon": "3", "label": "TRIPLE SHOT"},
#     {"type": "speed",       "color": YELLOW, "icon": "»", "label": "SPEED BOOST"},
#     {"type": "nuke",        "color": ORANGE, "icon": "N", "label": "NUKE"},
#     {"type": "score",       "color": PURPLE, "icon": "$", "label": "+500 SCORE"},
# ]

# class PowerUp:
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#         self.data = random.choice(POWERUP_TYPES)
#         self.type = self.data["type"]
#         self.color = self.data["color"]
#         self.icon = self.data["icon"]
#         self.speed = 2.0
#         self.alive = True
#         self.t = random.uniform(0, math.pi*2)
#         self.radius = 16

#     def update(self):
#         self.y += self.speed
#         self.t += 0.08
#         if self.y > SH + 30:
#             self.alive = False

#     def draw(self, surf):
#         pulse = 1 + 0.12 * math.sin(self.t)
#         r = int(self.radius * pulse)
#         cx, cy = int(self.x), int(self.y)
#         # Outer glow ring
#         pygame.draw.circle(surf, (self.color[0]//3, self.color[1]//3, self.color[2]//3), (cx,cy), r+6)
#         pygame.draw.circle(surf, self.color, (cx,cy), r, 2)
#         pygame.draw.circle(surf, DARK_PANEL, (cx,cy), r-2)
#         font = pygame.font.SysFont("Courier", 16, bold=True)
#         t = font.render(self.icon, True, self.color)
#         surf.blit(t, (cx - t.get_width()//2, cy - t.get_height()//2))

#     def collide(self, px, py):
#         return math.hypot(self.x-px, self.y-py) < self.radius + 22

# # ══════════════════════════════════════════
# # WEAPON SYSTEM
# # ══════════════════════════════════════════
# WEAPONS = [
#     {"name": "LASER",      "color": CYAN,   "speed": 13, "damage": 1, "spread": 0, "cost": 0},
#     {"name": "PLASMA",     "color": GREEN,  "speed": 15, "damage": 2, "spread": 1, "cost": 200},
#     {"name": "ION CANNON", "color": PURPLE, "speed": 18, "damage": 3, "spread": 2, "cost": 500},
# ]

# class Laser:
#     def __init__(self, x, y, angle, weapon_level=0, color=None):
#         self.x, self.y = x, y
#         w = WEAPONS[weapon_level]
#         self.speed = w["speed"]
#         self.color = color or w["color"]
#         self.vx = math.sin(math.radians(angle)) * self.speed
#         self.vy = -math.cos(math.radians(angle)) * self.speed
#         self.alive = True
#         self.damage = w["damage"]
#         self.width = 2 + weapon_level

#     def update(self):
#         self.x += self.vx
#         self.y += self.vy
#         if self.y < -50 or self.y > SH+50 or self.x < -50 or self.x > SW+50:
#             self.alive = False

#     def draw(self, surf):
#         ex = self.x - self.vx * 1.8
#         ey = self.y - self.vy * 1.8
#         draw_glow_line(surf, self.color, (int(self.x),int(self.y)), (int(ex),int(ey)), self.width, 5)

# # ══════════════════════════════════════════
# # ASTEROID
# # ══════════════════════════════════════════
# class Asteroid3D:
#     def __init__(self, speed_mult=1.0):
#         self.reset(speed_mult)

#     def reset(self, speed_mult=1.0):
#         self.x = random.uniform(60, SW-60)
#         self.y = random.uniform(-180, -30)
#         self.z = random.uniform(1, 4)
#         self.speed = random.uniform(1.5, 3.5) * speed_mult
#         self.rot_z = random.uniform(0, 360)
#         self.rot_x = random.uniform(0, 360)
#         self.rot_spd_z = random.uniform(-2.5, 2.5)
#         self.rot_spd_x = random.uniform(-1.5, 1.5)
#         self.base_radius = random.randint(20, 42)
#         self.color = random.choice([GREY, (100,80,60), (85,90,110), (70,100,80)])
#         self.points = self._gen()
#         self.alive = True
#         self.hit_flash = 0
#         self.hp = 1
#         self.speed_mult = speed_mult

#     def _gen(self):
#         pts = []
#         for i in range(12):
#             a = math.radians(i * 30)
#             r = self.base_radius * random.uniform(0.65, 1.35)
#             pts.append((math.cos(a)*r, math.sin(a)*r))
#         return pts

#     def update(self):
#         self.y += self.speed
#         self.rot_z += self.rot_spd_z
#         self.rot_x += self.rot_spd_x
#         if self.hit_flash > 0: self.hit_flash -= 1
#         if self.y > SH + 120: self.reset(self.speed_mult)

#     def projected(self):
#         scale = 1 / self.z
#         rz = math.radians(self.rot_z)
#         rx = math.radians(self.rot_x)
#         result = []
#         for px, py in self.points:
#             rx2 = px*math.cos(rz) - py*math.sin(rz)
#             ry2 = px*math.sin(rz) + py*math.cos(rz)
#             sx = rx2*scale + self.x
#             sy = ry2*scale*math.cos(rx) + self.y
#             result.append((int(sx), int(sy)))
#         return result

#     def draw(self, surf):
#         pts = self.projected()
#         if len(pts) < 3: return
#         shadow = [(p[0]+5, p[1]+5) for p in pts]
#         pygame.draw.polygon(surf, (15,15,25), shadow)
#         color = RED if self.hit_flash > 0 else self.color
#         draw_glow_polygon(surf, color, pts, 0)
#         r = max(3, self.base_radius//4)
#         cx, cy = int(self.x), int(self.y)
#         pygame.draw.circle(surf, (50,50,60), (cx-r//2, cy-r//2), r//2)
#         pygame.draw.circle(surf, (50,50,60), (cx+r//3, cy+r//3), r//3)

#     def collide(self, lx, ly):
#         pts = self.projected()
#         if len(pts) < 3: return False
#         n = len(pts); inside = False; j = n-1
#         for i in range(n):
#             xi,yi = pts[i]; xj,yj = pts[j]
#             if ((yi>ly) != (yj>ly)) and (lx < (xj-xi)*(ly-yi)/(yj-yi+1e-9)+xi):
#                 inside = not inside
#             j = i
#         return inside

# # ══════════════════════════════════════════
# # ENEMY AI SHIP
# # ══════════════════════════════════════════
# class EnemyShip:
#     def __init__(self, level=1):
#         self.x = random.uniform(80, SW-80)
#         self.y = random.uniform(-200, -50)
#         self.hp = 2 + level
#         self.max_hp = self.hp
#         self.speed = random.uniform(1.5, 2.5 + level*0.2)
#         self.angle = 0
#         self.lasers = []
#         self.shoot_cd = random.randint(60, 120)
#         self.alive = True
#         self.hit_flash = 0
#         self.size = 22
#         self.patrol_t = random.uniform(0, math.pi*2)
#         self.patrol_speed = random.uniform(0.02, 0.04)
#         self.score_value = 30 * level

#     def update(self, player_x, player_y):
#         # Chase player
#         dx = player_x - self.x
#         dy = player_y - self.y
#         dist = math.hypot(dx, dy) + 1e-9
#         target_angle = math.degrees(math.atan2(dx, -dy))
#         diff = (target_angle - self.angle + 180) % 360 - 180
#         self.angle += diff * 0.04

#         # Move toward player but maintain distance
#         if dist > 180:
#             self.x += (dx/dist) * self.speed
#             self.y += (dy/dist) * self.speed
#         else:
#             # Patrol side to side
#             self.patrol_t += self.patrol_speed
#             self.x += math.cos(self.patrol_t) * 2

#         # Shoot
#         self.shoot_cd -= 1
#         if self.shoot_cd <= 0 and dist < 400:
#             self.lasers.append(Laser(self.x, self.y, self.angle + random.uniform(-8,8), 0, RED))
#             self.shoot_cd = random.randint(50, 100)

#         for l in self.lasers: l.update()
#         self.lasers = [l for l in self.lasers if l.alive]
#         if self.hit_flash > 0: self.hit_flash -= 1

#         if self.y > SH + 100: self.alive = False

#     def take_damage(self, dmg):
#         self.hp -= dmg
#         self.hit_flash = 10
#         if self.hp <= 0:
#             self.alive = False
#             return True
#         return False

#     def draw(self, surf):
#         ar = math.radians(self.angle)
#         s = self.size
#         def rot(px, py):
#             rx = px*math.cos(ar) - py*math.sin(ar)
#             ry = px*math.sin(ar) + py*math.cos(ar)
#             return (self.x+rx, self.y+ry)

#         color = ORANGE if self.hit_flash > 0 else RED
#         dim   = RED_DIM if self.hit_flash == 0 else ORANGE

#         nose  = rot(0, -s)
#         lw    = rot(-s*0.8, s*0.5)
#         rw    = rot( s*0.8, s*0.5)
#         lb    = rot(-s*0.3, s*0.85)
#         rb    = rot( s*0.3, s*0.85)
#         ctr   = rot(0, s*0.25)

#         draw_glow_polygon(surf, color, [nose,lw,ctr,rw], 0)
#         draw_glow_polygon(surf, dim,   [lw,lb,ctr], 0)
#         draw_glow_polygon(surf, dim,   [rw,rb,ctr], 0)
#         pygame.draw.polygon(surf, color, [nose,lw,lb,rb,rw], 2)

#         # HP bar
#         bw = 36
#         bx = int(self.x - bw//2)
#         by = int(self.y + s + 5)
#         pygame.draw.rect(surf, (60,0,0), (bx, by, bw, 5))
#         hw = int(bw * self.hp / self.max_hp)
#         pygame.draw.rect(surf, RED, (bx, by, hw, 5))

#         for l in self.lasers: l.draw(surf)

# # ══════════════════════════════════════════
# # BOSS
# # ══════════════════════════════════════════
# class Boss:
#     def __init__(self, level):
#         self.x = SW // 2
#         self.y = -120
#         self.target_y = 130
#         self.hp = 40 + level * 15
#         self.max_hp = self.hp
#         self.lasers = []
#         self.alive = True
#         self.phase = 0        # 0=enter, 1=fight, 2=rage
#         self.t = 0
#         self.shoot_cd = 0
#         self.size = 55
#         self.hit_flash = 0
#         self.level = level
#         self.pattern = 0
#         self.pattern_t = 0
#         self.score_value = 500 + level * 100

#     def update(self, player_x, player_y):
#         self.t += 0.02
#         self.hit_flash = max(0, self.hit_flash - 1)
#         self.pattern_t += 1

#         # Enter phase
#         if self.phase == 0:
#             self.y += 2
#             if self.y >= self.target_y:
#                 self.y = self.target_y
#                 self.phase = 1

#         # Rage phase
#         if self.hp < self.max_hp * 0.35:
#             self.phase = 2

#         # Movement
#         if self.phase >= 1:
#             self.x = SW//2 + math.sin(self.t * 0.8) * 280

#         # Shooting patterns
#         self.shoot_cd -= 1
#         if self.shoot_cd <= 0 and self.phase >= 1:
#             self._shoot(player_x, player_y)
#             self.shoot_cd = 25 if self.phase < 2 else 15

#         # Change pattern every 3 seconds
#         if self.pattern_t % 180 == 0:
#             self.pattern = (self.pattern + 1) % 3

#         for l in self.lasers: l.update()
#         self.lasers = [l for l in self.lasers if l.alive]

#     def _shoot(self, px, py):
#         dx = px - self.x; dy = py - self.y
#         angle_to_player = math.degrees(math.atan2(dx, -dy))

#         if self.pattern == 0:  # Aimed burst
#             for spread in [-10, 0, 10]:
#                 self.lasers.append(Laser(self.x, self.y+30, angle_to_player+spread, 0, ORANGE))

#         elif self.pattern == 1:  # Radial spread
#             num = 8 if self.phase < 2 else 12
#             for i in range(num):
#                 a = i * (360/num) + self.t*20
#                 self.lasers.append(Laser(self.x, self.y, a, 0, RED))

#         elif self.pattern == 2:  # Spiral
#             for i in range(4):
#                 a = angle_to_player + i*90 + self.t*30
#                 self.lasers.append(Laser(self.x, self.y, a, 0, PURPLE))

#     def take_damage(self, dmg):
#         self.hp -= dmg
#         self.hit_flash = 8
#         if self.hp <= 0:
#             self.alive = False
#             return True
#         return False

#     def draw(self, surf):
#         cx, cy = int(self.x), int(self.y)
#         s = self.size
#         color = WHITE if self.hit_flash > 0 else ORANGE
#         accent = YELLOW

#         # Main body hexagon
#         pts = []
#         for i in range(6):
#             a = math.radians(i*60 + self.t*10)
#             pts.append((cx + math.cos(a)*s, cy + math.sin(a)*s*0.7))
#         draw_glow_polygon(surf, color, pts, 0)

#         # Inner core
#         pts2 = []
#         for i in range(6):
#             a = math.radians(i*60 - self.t*15)
#             pts2.append((cx + math.cos(a)*s*0.5, cy + math.sin(a)*s*0.4))
#         draw_glow_polygon(surf, RED, pts2, 0)

#         # Cannons
#         for side in [-1, 1]:
#             pygame.draw.rect(surf, GREY,
#                 (cx + side*s - 8, cy + s//2 - 6, 16, 30), border_radius=4)
#             pygame.draw.rect(surf, accent,
#                 (cx + side*s - 8, cy + s//2 - 6, 16, 30), 2, border_radius=4)

#         # Pulsing core glow
#         draw_glow_circle(surf, RED, (cx,cy), int(12 + 5*math.sin(self.t*3)), 2)

#         # HP Bar
#         bw = 300; bx = SW//2 - bw//2; by = 15
#         pygame.draw.rect(surf, (60,0,0), (bx-2, by-2, bw+4, 22), border_radius=5)
#         hw = int(bw * self.hp / self.max_hp)
#         hp_color = GREEN if self.hp > self.max_hp*0.6 else (YELLOW if self.hp > self.max_hp*0.3 else RED)
#         pygame.draw.rect(surf, hp_color, (bx, by, hw, 18), border_radius=5)
#         pygame.draw.rect(surf, WHITE, (bx-2, by-2, bw+4, 22), 2, border_radius=5)

#         font = pygame.font.SysFont("Courier", 14, bold=True)
#         t = font.render(f"BOSS  HP: {self.hp}/{self.max_hp}  {'★ RAGE MODE ★' if self.phase==2 else ''}", True, WHITE)
#         surf.blit(t, (SW//2 - t.get_width()//2, by))

#         for l in self.lasers: l.draw(surf)

# # ══════════════════════════════════════════
# # PLAYER SPACESHIP
# # ══════════════════════════════════════════
# class Spaceship:
#     def __init__(self):
#         self.x = SW // 2
#         self.y = SH - 110
#         self.angle = 0
#         self.size = 34
#         self.lasers = []
#         self.shoot_cd = 0
#         self.shield = 100
#         self.speed = 5.0
#         self.weapon_level = 0
#         self.triple_timer = 0
#         self.speed_timer = 0
#         self.engine_particles = []
#         self.invincible = 0
#         # ── Touch / Mouse controls ──
#         self.touch_target = None   # (x, y) where player tapped
#         self.touch_active = False  # is finger/mouse held down
#         self.is_moving = False     # for engine trail

#     def set_touch_target(self, x, y):
#         """Called when screen is tapped/clicked"""
#         self.touch_target = (x, y)
#         self.touch_active = True

#     def clear_touch(self):
#         self.touch_active = False
#         self.touch_target = None

#     def handle_input(self, keys):
#         # ── Keyboard controls (unchanged) ──
#         if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.angle -= 3.2
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.angle += 3.2
#         spd = self.speed * (1.5 if self.speed_timer > 0 else 1.0)
#         kb_moving = False
#         if keys[pygame.K_UP]   or keys[pygame.K_w]:
#             self.x += math.sin(math.radians(self.angle)) * spd
#             self.y -= math.cos(math.radians(self.angle)) * spd
#             kb_moving = True
#         if keys[pygame.K_DOWN] or keys[pygame.K_s]:
#             self.x -= math.sin(math.radians(self.angle)) * spd * 0.5
#             self.y += math.cos(math.radians(self.angle)) * spd * 0.5

#         # ── Touch / Mouse controls ──
#         if self.touch_target and self.touch_active:
#             tx, ty = self.touch_target
#             dx = tx - self.x
#             dy = ty - self.y
#             dist = math.hypot(dx, dy)

#             if dist > 6:  # Move toward tap point
#                 # Rotate ship to face target
#                 target_angle = math.degrees(math.atan2(dx, -dy))
#                 diff = (target_angle - self.angle + 180) % 360 - 180
#                 self.angle += diff * 0.18

#                 # Move toward target
#                 move_spd = spd * min(1.0, dist / 60)
#                 self.x += (dx / dist) * move_spd
#                 self.y += (dy / dist) * move_spd
#                 kb_moving = True
#             else:
#                 # Reached target — stop & auto-shoot
#                 self.touch_target = None

#         self.is_moving = kb_moving
#         self.x = max(35, min(SW-35, self.x))
#         self.y = max(35, min(SH-35, self.y))

#         # Auto-shoot when moving via touch
#         if self.touch_active and self.shoot_cd <= 0:
#             self._shoot()
#             self.shoot_cd = max(6, 14 - self.weapon_level * 2)

#         if keys[pygame.K_SPACE] and self.shoot_cd <= 0:
#             self._shoot()
#             self.shoot_cd = max(6, 14 - self.weapon_level * 2)

#     def _shoot(self):
#         tip_x = self.x + math.sin(math.radians(self.angle)) * self.size
#         tip_y = self.y - math.cos(math.radians(self.angle)) * self.size
#         self.lasers.append(Laser(tip_x, tip_y, self.angle, self.weapon_level))
#         if self.triple_timer > 0 or self.weapon_level >= 1:
#             self.lasers.append(Laser(tip_x, tip_y, self.angle - 18, self.weapon_level))
#             self.lasers.append(Laser(tip_x, tip_y, self.angle + 18, self.weapon_level))

#     def update(self):
#         if self.shoot_cd > 0: self.shoot_cd -= 1
#         if self.triple_timer > 0: self.triple_timer -= 1
#         if self.speed_timer > 0: self.speed_timer -= 1
#         if self.invincible > 0: self.invincible -= 1
#         for l in self.lasers: l.update()
#         self.lasers = [l for l in self.lasers if l.alive]

#         # Engine trail
#         if self.is_moving:
#             tail_x = self.x - math.sin(math.radians(self.angle)) * self.size*0.75
#             tail_y = self.y + math.cos(math.radians(self.angle)) * self.size*0.75
#             for _ in range(4):
#                 c = random.choice([ORANGE, YELLOW, (255,80,0), CYAN])
#                 self.engine_particles.append(Particle(
#                     tail_x + random.uniform(-5,5),
#                     tail_y + random.uniform(-5,5), c, 2, 25))
#         for p in self.engine_particles: p.update()
#         self.engine_particles = [p for p in self.engine_particles if p.alive]

#     def draw(self, surf):
#         for p in self.engine_particles: p.draw(surf)
#         for l in self.lasers: l.draw(surf)

#         ar = math.radians(self.angle)
#         s  = self.size
#         def rot(px, py):
#             rx = px*math.cos(ar) - py*math.sin(ar)
#             ry = px*math.sin(ar) + py*math.cos(ar)
#             return (self.x+rx, self.y+ry)

#         nose  = rot(0, -s)
#         lWing = rot(-s*0.85, s*0.55)
#         rWing = rot( s*0.85, s*0.55)
#         lBack = rot(-s*0.38, s*0.88)
#         rBack = rot( s*0.38, s*0.88)
#         ctr   = rot(0, s*0.28)

#         wcolor = WEAPONS[self.weapon_level]["color"]

#         # Invincible flicker
#         if self.invincible > 0 and self.invincible % 6 < 3:
#             return

#         draw_glow_polygon(surf, wcolor,    [nose,lWing,ctr,rWing], 0)
#         draw_glow_polygon(surf, BLUE_DIM,  [lWing,lBack,ctr], 0)
#         draw_glow_polygon(surf, BLUE_DIM,  [rWing,rBack,ctr], 0)
#         pygame.draw.polygon(surf, wcolor, [nose,lWing,lBack,rBack,rWing], 2)

#         cockpit = rot(0, -s*0.28)
#         draw_glow_circle(surf, YELLOW, (int(cockpit[0]),int(cockpit[1])), 6, 2)

#         # Shield glow when high
#         if self.shield > 75:
#             draw_glow_circle(surf, (0,100,255), (int(self.x),int(self.y)), s+5, 1)

#     def get_rect(self):
#         return pygame.Rect(self.x-22, self.y-22, 44, 44)

# # ══════════════════════════════════════════
# # HUD
# # ══════════════════════════════════════════
# def draw_hud(surf, font, bfont, score, lives, level, shield, weapon_level, triple_t, speed_t, upgrade_cost):
#     # Left panel
#     pygame.draw.rect(surf, DARK_PANEL, (0, 0, 220, 90), border_radius=8)
#     pygame.draw.rect(surf, CYAN_DIM,   (0, 0, 220, 90), 1, border_radius=8)
#     draw_text_glow(surf, f"SCORE: {score:06d}", bfont, CYAN, 12, 14, center=False)
#     lives_str = "♥ " * max(0, lives)
#     draw_text_glow(surf, f"LIVES: {lives_str}", font, RED, 12, 48, center=False)
#     draw_text_glow(surf, f"WEAPON: {WEAPONS[weapon_level]['name']}", font, WEAPONS[weapon_level]['color'], 12, 70, center=False)

#     # Right panel
#     pygame.draw.rect(surf, DARK_PANEL, (SW-230, 0, 230, 90), border_radius=8)
#     pygame.draw.rect(surf, CYAN_DIM,   (SW-230, 0, 230, 90), 1, border_radius=8)
#     draw_text_glow(surf, f"LEVEL: {level}", bfont, YELLOW, SW-12, 14, center=False)

#     # Shield bar
#     bx, by = SW-225, 48
#     pygame.draw.rect(surf, (30,30,50), (bx, by, 200, 16), border_radius=5)
#     hw = int(200 * shield / 100)
#     sc = GREEN if shield>60 else (YELLOW if shield>30 else RED)
#     pygame.draw.rect(surf, sc, (bx, by, hw, 16), border_radius=5)
#     pygame.draw.rect(surf, WHITE, (bx, by, 200, 16), 1, border_radius=5)
#     t = font.render(f"SHIELD {shield}%", True, WHITE)
#     surf.blit(t, (bx + 200//2 - t.get_width()//2, by))

#     # Upgrade hint
#     if weapon_level < 2:
#         draw_text_glow(surf, f"[U] UPGRADE → {WEAPONS[weapon_level+1]['name']} ({upgrade_cost} pts)", font,
#                        WEAPONS[weapon_level+1]['color'], SW//2, SH-22)

#     # Active power-up timers
#     px = 230
#     if triple_t > 0:
#         t = font.render(f"⚡ TRIPLE: {triple_t//60+1}s", True, GREEN)
#         surf.blit(t, (px, 8)); px += t.get_width() + 20
#     if speed_t > 0:
#         t = font.render(f"» SPEED: {speed_t//60+1}s", True, YELLOW)
#         surf.blit(t, (px, 8))

# # ══════════════════════════════════════════
# # SCREENS
# # ══════════════════════════════════════════
# def main_menu(screen, clock, stars, nebula, font, bfont, tfont):
#     t = 0
#     while True:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT: pygame.quit(); sys.exit()
#             if e.type == pygame.KEYDOWN:
#                 if e.key == pygame.K_RETURN: return "play"
#                 if e.key == pygame.K_l:      return "leaderboard"
#                 if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

#         t += 1
#         nebula.update()
#         stars.update(0.5)
#         screen.fill(BG)
#         nebula.draw(screen)
#         stars.draw(screen)

#         # Animated title
#         scale = 1 + 0.03 * math.sin(t * 0.04)
#         title_surf = tfont.render("NOVA STRIKE", True, CYAN)
#         w, h = title_surf.get_size()
#         scaled = pygame.transform.scale(title_surf, (int(w*scale), int(h*scale)))
#         screen.blit(scaled, (SW//2 - scaled.get_width()//2, 140))

#         draw_text_glow(screen, "SPACE SHOOTER v2.0", bfont, PURPLE, SW//2, 230)

#         # Menu options
#         pulse = abs(math.sin(t * 0.05))
#         col = (int(200+55*pulse), int(200+55*pulse), 0)
#         draw_text_glow(screen, "[ ENTER ]  START GAME", bfont, col, SW//2, 320)
#         draw_text_glow(screen, "[  L  ]  LEADERBOARD",  font, CYAN_DIM, SW//2, 370)
#         draw_text_glow(screen, "[ ESC ]  QUIT",          font, GREY,    SW//2, 410)

#         # Controls box
#         pygame.draw.rect(screen, DARK_PANEL, (SW//2-230, 460, 460, 110), border_radius=10)
#         pygame.draw.rect(screen, CYAN_DIM,   (SW//2-230, 460, 460, 110), 1, border_radius=10)
#         draw_text_glow(screen, "CONTROLS", font, CYAN, SW//2, 480)
#         draw_text_glow(screen, "W/A/S/D = Move    SPACE = Shoot", font, WHITE, SW//2, 505)
#         draw_text_glow(screen, "U = Upgrade Weapon    P = Pause", font, WHITE, SW//2, 530)
#         draw_text_glow(screen, "Destroy enemies & bosses to earn score!", font, YELLOW, SW//2, 555)

#         pygame.display.flip()
#         clock.tick(FPS)

# def leaderboard_screen(screen, clock, font, bfont, tfont):
#     scores = load_scores()
#     while True:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT: pygame.quit(); sys.exit()
#             if e.type == pygame.KEYDOWN: return

#         screen.fill(BG)
#         draw_text_glow(screen, "🏆 LEADERBOARD", tfont, YELLOW, SW//2, 60)
#         draw_text_glow(screen, "Press any key to go back", font, GREY, SW//2, 110)

#         if not scores:
#             draw_text_glow(screen, "No scores yet! Play a game first.", bfont, CYAN, SW//2, SH//2)
#         else:
#             headers = ["RANK", "NAME", "SCORE", "LEVEL", "KILLS"]
#             cols = [SW//2-300, SW//2-180, SW//2, SW//2+130, SW//2+240]
#             for i, h in enumerate(headers):
#                 draw_text_glow(screen, h, font, CYAN, cols[i], 150)
#             pygame.draw.line(screen, CYAN_DIM, (SW//2-320, 170), (SW//2+280, 170), 1)

#             for ri, s in enumerate(scores[:10]):
#                 y = 190 + ri * 42
#                 colors = [YELLOW, (200,200,200), (180,120,50)] + [WHITE]*7
#                 c = colors[ri]
#                 medal = ["🥇","🥈","🥉"] + [f"#{ri+1}"] * 7
#                 draw_text_glow(screen, medal[ri],             font, c, cols[0], y)
#                 draw_text_glow(screen, s.get("name","???"),   font, c, cols[1], y)
#                 draw_text_glow(screen, f"{s['score']:06d}",   font, c, cols[2], y)
#                 draw_text_glow(screen, str(s.get("level",1)), font, c, cols[3], y)
#                 draw_text_glow(screen, str(s.get("kills",0)), font, c, cols[4], y)

#         pygame.display.flip()
#         clock.tick(FPS)

# def game_over_screen(screen, clock, font, bfont, tfont, score, level, kills, powerups_collected, achievements):
#     # Get player name
#     name = ""
#     input_active = True
#     while input_active:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT: pygame.quit(); sys.exit()
#             if e.type == pygame.KEYDOWN:
#                 if e.key == pygame.K_RETURN and name.strip():
#                     input_active = False
#                 elif e.key == pygame.K_BACKSPACE:
#                     name = name[:-1]
#                 elif len(name) < 12 and e.unicode.isprintable():
#                     name += e.unicode.upper()

#         screen.fill(BG)
#         draw_text_glow(screen, "GAME OVER", tfont, RED, SW//2, 100)
#         draw_text_glow(screen, "Enter your name:", bfont, YELLOW, SW//2, 200)
#         pygame.draw.rect(screen, DARK_PANEL, (SW//2-150, 235, 300, 45), border_radius=8)
#         pygame.draw.rect(screen, CYAN, (SW//2-150, 235, 300, 45), 2, border_radius=8)
#         draw_text_glow(screen, name + "|", bfont, WHITE, SW//2, 258)
#         draw_text_glow(screen, "Press ENTER to confirm", font, GREY, SW//2, 295)
#         pygame.display.flip()
#         clock.tick(FPS)

#     scores = save_score(name.strip() or "PILOT", score, level, kills)

#     # Show stats
#     while True:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT: pygame.quit(); sys.exit()
#             if e.type == pygame.KEYDOWN:
#                 if e.key == pygame.K_r: return "restart"
#                 if e.key == pygame.K_m: return "menu"
#                 if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

#         screen.fill(BG)
#         draw_text_glow(screen, "MISSION REPORT", tfont, CYAN, SW//2, 60)

#         # Stats box
#         pygame.draw.rect(screen, DARK_PANEL, (SW//2-300, 110, 600, 260), border_radius=12)
#         pygame.draw.rect(screen, CYAN_DIM,   (SW//2-300, 110, 600, 260), 2, border_radius=12)

#         stats = [
#             ("PILOT",      name, YELLOW),
#             ("FINAL SCORE", f"{score:06d}", CYAN),
#             ("LEVEL REACHED", str(level), GREEN),
#             ("ENEMIES DESTROYED", str(kills), RED),
#             ("POWER-UPS COLLECTED", str(powerups_collected), PURPLE),
#         ]
#         for i, (label, val, col) in enumerate(stats):
#             y = 135 + i*44
#             draw_text_glow(screen, label+":", font, GREY, SW//2-220, y, center=False)
#             draw_text_glow(screen, val, bfont, col, SW//2+180, y)

#         # Achievements unlocked
#         if achievements.unlocked:
#             draw_text_glow(screen, f"ACHIEVEMENTS: {len(achievements.unlocked)}/{len(ACHIEVEMENTS_DEF)}", font, YELLOW, SW//2, 390)
#             ach_names = [next(a["icon"]+" "+a["name"] for a in ACHIEVEMENTS_DEF if a["id"]==aid)
#                          for aid in list(achievements.unlocked)[:5]]
#             draw_text_glow(screen, "  ".join(ach_names), font, WHITE, SW//2, 415)

#         # Top 3 scores preview
#         draw_text_glow(screen, "TOP SCORES", bfont, YELLOW, SW//2, 450)
#         for i, s in enumerate(scores[:3]):
#             colors = [YELLOW, (200,200,200), (180,120,50)]
#             draw_text_glow(screen, f"#{i+1}  {s.get('name','???'):12s}  {s['score']:06d}", font, colors[i], SW//2, 480+i*30)

#         pulse = abs(math.sin(pygame.time.get_ticks()*0.003))
#         col = (int(200+55*pulse), int(200+55*pulse), 0)
#         draw_text_glow(screen, "[ R ] RESTART    [ M ] MAIN MENU    [ ESC ] QUIT", bfont, col, SW//2, 600)

#         pygame.display.flip()
#         clock.tick(FPS)

# # ══════════════════════════════════════════
# # MAIN GAME LOOP
# # ══════════════════════════════════════════
# def game_loop(screen, clock, font, bfont, tfont):
#     stars  = StarField(300)
#     nebula = Nebula()
#     shake  = ScreenShake()
#     ship   = Spaceship()
#     achievements = AchievementSystem()

#     asteroids  = [Asteroid3D() for _ in range(8)]
#     enemies    = []
#     powerups   = []
#     particles  = []
#     boss       = None

#     score = 0; lives = 3; level = 1
#     kills = 0; powerups_collected = 0
#     game_over = False; paused = False
#     flash_t = 0; level_up_t = 0
#     boss_announced = 0
#     level_damage_taken = False
#     enemy_spawn_t = 0

#     UPGRADE_COSTS = [0, 200, 500]

#     def nuke_all():
#         nonlocal score
#         for a in asteroids:
#             spawn_explosion(particles, a.x, a.y, [ORANGE,YELLOW,RED], 20)
#             score += 5 * level
#             a.reset(1 + level * 0.08)
#         for e in enemies:
#             spawn_explosion(particles, e.x, e.y, [RED,ORANGE,WHITE], 20)
#             score += e.score_value // 2
#             e.alive = False

#     def apply_powerup(ptype):
#         nonlocal score, powerups_collected
#         powerups_collected += 1
#         if ptype == "shield":
#             ship.shield = min(100, ship.shield + 50)
#         elif ptype == "triple":
#             ship.triple_timer = 600
#         elif ptype == "speed":
#             ship.speed_timer = 400
#         elif ptype == "nuke":
#             nuke_all()
#             shake.shake(15)
#         elif ptype == "score":
#             score += 500

#     # ── LOOP ──
#     while not game_over:
#         clock.tick(FPS)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     return "menu"
#                 if event.key == pygame.K_p:
#                     paused = not paused
#                 if not paused and event.key == pygame.K_u:
#                     wl = ship.weapon_level
#                     if wl < 2:
#                         cost = UPGRADE_COSTS[wl+1]
#                         if score >= cost:
#                             score -= cost
#                             ship.weapon_level += 1
#                             spawn_explosion(particles, ship.x, ship.y,
#                                 [WEAPONS[ship.weapon_level]["color"], WHITE], 20, 3)

#             # ── MOUSE / TOUCH EVENTS ──
#             if not paused:
#                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     mx, my = event.pos
#                     # Check touch buttons (top-right area)
#                     # Pause button: top-right corner
#                     if SW-60 <= mx <= SW-10 and 10 <= my <= 55:
#                         paused = True
#                     # Upgrade button: bottom-right
#                     elif SW-180 <= mx <= SW-10 and SH-65 <= my <= SH-10:
#                         wl = ship.weapon_level
#                         if wl < 2:
#                             cost = UPGRADE_COSTS[wl+1]
#                             if score >= cost:
#                                 score -= cost
#                                 ship.weapon_level += 1
#                                 spawn_explosion(particles, ship.x, ship.y,
#                                     [WEAPONS[ship.weapon_level]["color"], WHITE], 20, 3)
#                     else:
#                         ship.set_touch_target(mx, my)

#                 elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                     ship.clear_touch()

#                 elif event.type == pygame.MOUSEMOTION:
#                     if event.buttons[0]:  # Drag = continuous move
#                         mx, my = event.pos
#                         if not (SW-60 <= mx <= SW-10 and 10 <= my <= 55):
#                             ship.set_touch_target(mx, my)

#                 # Finger touch events (real touch screens)
#                 elif event.type == pygame.FINGERDOWN:
#                     fx = int(event.x * SW)
#                     fy = int(event.y * SH)
#                     ship.set_touch_target(fx, fy)

#                 elif event.type == pygame.FINGERUP:
#                     ship.clear_touch()

#                 elif event.type == pygame.FINGERMOTION:
#                     fx = int(event.x * SW)
#                     fy = int(event.y * SH)
#                     ship.set_touch_target(fx, fy)

#         if paused:
#             screen.fill(BG)
#             draw_text_glow(screen, "⏸  PAUSED", tfont, YELLOW, SW//2, SH//2-40)
#             draw_text_glow(screen, "Press P to Resume", bfont, WHITE, SW//2, SH//2+30)
#             pygame.display.flip()
#             continue

#         # ── UPDATE ──
#         keys = pygame.key.get_pressed()
#         ship.handle_input(keys)
#         ship.update()
#         nebula.update()
#         stars.update(1.0 + level * 0.05)
#         shake.update()
#         achievements.update()

#         # Level progression
#         new_level = score // 600 + 1
#         if new_level > level:
#             level = new_level
#             level_up_t = 150
#             if not level_damage_taken:
#                 achievements.check("no_damage", no_dmg=True)
#             level_damage_taken = False
#             for _ in range(min(3, level//2)):
#                 a = Asteroid3D(1 + level * 0.08)
#                 asteroids.append(a)
#             if level % 5 == 0 and boss is None:
#                 boss = Boss(level)
#                 boss_announced = 200

#         # Boss spawn announcement
#         if boss_announced > 0:
#             boss_announced -= 1

#         # Enemy spawning
#         enemy_spawn_t += 1
#         spawn_interval = max(120, 300 - level * 15)
#         if enemy_spawn_t >= spawn_interval and len(enemies) < min(6, level):
#             enemies.append(EnemyShip(level))
#             enemy_spawn_t = 0

#         # Update asteroids
#         speed_mult = 1 + level * 0.08
#         for a in asteroids:
#             a.speed_mult = speed_mult
#             a.update()

#         # Update enemies
#         for e in enemies:
#             e.update(ship.x, ship.y)
#         enemies = [e for e in enemies if e.alive]

#         # Update boss
#         if boss:
#             boss.update(ship.x, ship.y)
#             if not boss.alive:
#                 spawn_explosion(particles, boss.x, boss.y,
#                     [ORANGE,YELLOW,RED,WHITE,PURPLE], 80, 8)
#                 score += boss.score_value
#                 kills += 1
#                 shake.shake(20)
#                 achievements.check("boss", boss=True)
#                 boss = None

#         # Update powerups
#         for p in powerups: p.update()
#         powerups = [p for p in powerups if p.alive]

#         # Update particles
#         for p in particles: p.update()
#         particles = [p for p in particles if p.alive]

#         if flash_t > 0: flash_t -= 1
#         if level_up_t > 0: level_up_t -= 1

#         # ── COLLISIONS ──
#         ship_rect = ship.get_rect()

#         # Player laser vs asteroid
#         for laser in ship.lasers[:]:
#             for a in asteroids:
#                 if a.collide(laser.x, laser.y):
#                     laser.alive = False
#                     a.hit_flash = 8
#                     score += 10 * level
#                     kills += 1
#                     spawn_explosion(particles, a.x, a.y)
#                     a.reset(speed_mult)
#                     if random.random() < 0.18:
#                         powerups.append(PowerUp(a.x, a.y))
#                     achievements.check("kill", score=score, kills=kills, level=level,
#                                        powerups=powerups_collected, weapon=ship.weapon_level)

#         # Player laser vs enemy
#         for laser in ship.lasers[:]:
#             for e in enemies[:]:
#                 if math.hypot(laser.x-e.x, laser.y-e.y) < e.size + 5:
#                     laser.alive = False
#                     if e.take_damage(laser.damage):
#                         score += e.score_value
#                         kills += 1
#                         spawn_explosion(particles, e.x, e.y, [RED,ORANGE,WHITE], 30)
#                         shake.shake(6)
#                         if random.random() < 0.25:
#                             powerups.append(PowerUp(e.x, e.y))
#                         achievements.check("kill", score=score, kills=kills, level=level,
#                                            powerups=powerups_collected, weapon=ship.weapon_level)

#         # Player laser vs boss
#         if boss:
#             for laser in ship.lasers[:]:
#                 if math.hypot(laser.x-boss.x, laser.y-boss.y) < boss.size + 10:
#                     laser.alive = False
#                     boss.take_damage(laser.damage)
#                     spawn_explosion(particles, laser.x, laser.y, [ORANGE,WHITE], 8, 2)

#         # Asteroid vs player
#         if ship.invincible == 0:
#             for a in asteroids:
#                 pts = a.projected()
#                 for px, py in pts:
#                     if ship_rect.collidepoint(px, py):
#                         ship.shield -= 15
#                         level_damage_taken = True
#                         flash_t = 28
#                         ship.invincible = 80
#                         shake.shake(10)
#                         spawn_explosion(particles, ship.x, ship.y, [CYAN,WHITE,BLUE], 15, 2)
#                         a.reset(speed_mult)
#                         if ship.shield <= 0:
#                             lives -= 1; ship.shield = 100
#                             if lives <= 0: game_over = True
#                         break

#         # Enemy laser vs player
#         if ship.invincible == 0:
#             for e in enemies:
#                 for el in e.lasers[:]:
#                     if ship_rect.collidepoint(el.x, el.y):
#                         el.alive = False
#                         ship.shield -= 12
#                         level_damage_taken = True
#                         flash_t = 20
#                         ship.invincible = 60
#                         shake.shake(8)
#                         if ship.shield <= 0:
#                             lives -= 1; ship.shield = 100
#                             if lives <= 0: game_over = True

#         # Boss laser vs player
#         if boss and ship.invincible == 0:
#             for bl in boss.lasers[:]:
#                 if ship_rect.collidepoint(bl.x, bl.y):
#                     bl.alive = False
#                     ship.shield -= 18
#                     level_damage_taken = True
#                     flash_t = 30
#                     ship.invincible = 70
#                     shake.shake(12)
#                     if ship.shield <= 0:
#                         lives -= 1; ship.shield = 100
#                         if lives <= 0: game_over = True

#         # Powerup collection
#         for p in powerups[:]:
#             if p.collide(ship.x, ship.y):
#                 apply_powerup(p.type)
#                 p.alive = False
#                 achievements.check("powerup", powerups=powerups_collected)
#                 spawn_explosion(particles, p.x, p.y, [p.color, WHITE], 15, 2)

#         achievements.check("score_check", score=score, kills=kills, level=level,
#                            powerups=powerups_collected, weapon=ship.weapon_level)

#         # ── DRAW ──
#         ox, oy = shake.offset
#         draw_surf = pygame.Surface((SW, SH))
#         draw_surf.fill(BG)
#         nebula.draw(draw_surf)
#         stars.draw(draw_surf)

#         if flash_t > 0 and flash_t % 6 < 3:
#             fl = pygame.Surface((SW, SH), pygame.SRCALPHA)
#             fl.fill((255,0,0,50))
#             draw_surf.blit(fl, (0,0))

#         for a in asteroids: a.draw(draw_surf)
#         for e in enemies:   e.draw(draw_surf)
#         if boss:            boss.draw(draw_surf)
#         for p in powerups:  p.draw(draw_surf)
#         for p in particles: p.draw(draw_surf)
#         if not game_over:   ship.draw(draw_surf)

#         upgrade_cost = UPGRADE_COSTS[ship.weapon_level+1] if ship.weapon_level < 2 else 0
#         draw_hud(draw_surf, font, bfont, score, lives, level, ship.shield,
#                  ship.weapon_level, ship.triple_timer, ship.speed_timer, upgrade_cost)

#         # ── TOUCH UI BUTTONS ──
#         # Tap target indicator
#         if ship.touch_target and ship.touch_active:
#             tx, ty = ship.touch_target
#             r = int(14 + 4 * math.sin(pygame.time.get_ticks() * 0.01))
#             pygame.draw.circle(draw_surf, CYAN, (int(tx), int(ty)), r, 2)
#             pygame.draw.circle(draw_surf, CYAN, (int(tx), int(ty)), 4)

#         # Pause button (top-right)
#         pygame.draw.rect(draw_surf, DARK_PANEL, (SW-58, 8, 50, 48), border_radius=8)
#         pygame.draw.rect(draw_surf, CYAN_DIM,   (SW-58, 8, 50, 48), 2, border_radius=8)
#         draw_text_glow(draw_surf, "II", font, YELLOW, SW-33, 32)

#         # Upgrade button (bottom-right) — only if upgradeable
#         if ship.weapon_level < 2:
#             can_upgrade = score >= upgrade_cost
#             btn_col = GREEN if can_upgrade else GREY
#             pygame.draw.rect(draw_surf, DARK_PANEL, (SW-178, SH-62, 168, 52), border_radius=10)
#             pygame.draw.rect(draw_surf, btn_col,    (SW-178, SH-62, 168, 52), 2, border_radius=10)
#             draw_text_glow(draw_surf, f"⚡ UPGRADE", font, btn_col, SW-95, SH-45)
#             draw_text_glow(draw_surf, f"{upgrade_cost} pts", font,
#                            GREEN if can_upgrade else RED, SW-95, SH-22)

#         achievements.draw(draw_surf, font)

#         if level_up_t > 0:
#             draw_text_glow(draw_surf, f"⭐ LEVEL {level} !", tfont, YELLOW, SW//2, SH//2-40)

#         if boss_announced > 0:
#             pulse = abs(math.sin(boss_announced * 0.1))
#             c = (int(255*pulse), 0, 0)
#             draw_text_glow(draw_surf, "⚠ BOSS INCOMING ⚠", tfont, c, SW//2, SH//2-20)

#         screen.blit(draw_surf, (ox, oy))
#         pygame.display.flip()

#     return "game_over", score, level, kills, powerups_collected, achievements

# # ══════════════════════════════════════════
# # ENTRY POINT
# # ══════════════════════════════════════════
# def main():
#     screen = pygame.display.set_mode((SW, SH))
#     pygame.display.set_caption(TITLE)
#     clock = pygame.time.Clock()

#     font  = pygame.font.SysFont("Courier", 18, bold=True)
#     bfont = pygame.font.SysFont("Courier", 24, bold=True)
#     tfont = pygame.font.SysFont("Courier", 54, bold=True)

#     stars  = StarField(300)
#     nebula = Nebula()

#     while True:
#         result = main_menu(screen, clock, stars, nebula, font, bfont, tfont)

#         if result == "leaderboard":
#             leaderboard_screen(screen, clock, font, bfont, tfont)
#             continue

#         if result == "play":
#             outcome = game_loop(screen, clock, font, bfont, tfont)

#             if outcome == "menu":
#                 continue

#             if outcome[0] == "game_over":
#                 _, score, level, kills, powerups, achievements = outcome
#                 next_action = game_over_screen(
#                     screen, clock, font, bfont, tfont,
#                     score, level, kills, powerups, achievements)
#                 if next_action == "restart":
#                     continue
#                 elif next_action == "menu":
#                     continue

# if __name__ == "__main__":
#     main()




##clickable buttons

"""
╔══════════════════════════════════════════════════════════════╗
║         🚀 NOVA STRIKE — Advanced Space Shooter v2.0         ║
║                Python 3.13 + Pygame ONLY                     ║
╠══════════════════════════════════════════════════════════════╣
║  FEATURES:                                                  ║
║  ✅ Beautiful Animated Main Menu                            ║
║  ✅ Neon Glow Effects + Animated Nebula Background          ║
║  ✅ Enemy AI Ships (chase + shoot player)                   ║
║  ✅ Boss Fights (every 5 levels, 3 attack patterns)         ║
║  ✅ Power-ups (Shield / Triple Shot / Speed / Nuke)         ║
║  ✅ Weapon Upgrade Tree (3 levels: Laser→Plasma→Ion Cannon) ║
║  ✅ Achievement System (10 unlockable achievements)         ║
║  ✅ High Score Leaderboard (saved to file)                  ║
║  ✅ End Game Stats Screen                                   ║
║  ✅ Screen Shake + Particle Explosions                      ║
╠══════════════════════════════════════════════════════════════╣
║  HOW TO RUN:                                                 ║
║    pip install pygame                                        ║
║    python space_shooter_v2.py                                ║
╠══════════════════════════════════════════════════════════════╣
║  CONTROLS:                                                   ║
║    W/A/S/D or Arrow Keys = Move & Rotate                     ║
║    SPACE = Shoot                                             ║
║    U     = Upgrade Weapon (costs 200 score)                  ║
║    P     = Pause                                             ║
║    ESC   = Quit                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import pygame
import random
import math
import sys
import json
import os

pygame.init()

# ══════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════
SW, SH = 1000, 700
FPS    = 60
TITLE  = "NOVA STRIKE — Space Shooter v2.0"

# Color Palette (Neon Theme)
BG          = (3, 5, 20)
WHITE       = (255, 255, 255)
CYAN        = (0, 255, 255)
CYAN_DIM    = (0, 140, 160)
YELLOW      = (255, 220, 0)
RED         = (255, 40, 40)
RED_DIM     = (180, 20, 20)
ORANGE      = (255, 130, 0)
BLUE        = (30, 80, 255)
BLUE_DIM    = (20, 50, 180)
PURPLE      = (180, 0, 255)
PURPLE_DIM  = (100, 0, 160)
GREEN       = (0, 255, 120)
GREEN_DIM   = (0, 160, 80)
PINK        = (255, 60, 180)
GREY        = (110, 115, 130)
DARK_PANEL  = (8, 12, 35)

SCORE_FILE = "nova_strike_scores.json"

# ══════════════════════════════════════════
# UTILITY: NEON GLOW DRAW
# ══════════════════════════════════════════
def draw_glow_circle(surf, color, pos, radius, layers=3):
    for i in range(layers, 0, -1):
        r = min(255, color[0] // i)
        g = min(255, color[1] // i)
        b = min(255, color[2] // i)
        glow_surf = pygame.Surface((radius*2*i, radius*2*i), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (r, g, b, 40), (radius*i, radius*i), radius*i)
        surf.blit(glow_surf, (pos[0]-radius*i, pos[1]-radius*i))
    pygame.draw.circle(surf, color, pos, radius)

def draw_glow_line(surf, color, p1, p2, width=2, glow=6):
    pygame.draw.line(surf, (color[0]//4, color[1]//4, color[2]//4), p1, p2, width+glow)
    pygame.draw.line(surf, (color[0]//2, color[1]//2, color[2]//2), p1, p2, width+glow//2)
    pygame.draw.line(surf, color, p1, p2, width)

def draw_glow_polygon(surf, color, pts, width=0, glow=4):
    if len(pts) < 3: return
    dim = (color[0]//3, color[1]//3, color[2]//3)
    if width == 0:
        pygame.draw.polygon(surf, dim, pts)
        pygame.draw.polygon(surf, color, pts, 2)
    else:
        pygame.draw.polygon(surf, dim, pts, width+glow)
        pygame.draw.polygon(surf, color, pts, width)

def draw_text_glow(surf, text, font, color, x, y, center=True):
    glow_col = (min(255,color[0]//2), min(255,color[1]//2), min(255,color[2]//2))
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        t = font.render(text, True, glow_col)
        r = t.get_rect()
        if center: r.center = (x, y)
        else: r.topleft = (x, y)
        surf.blit(t, (r.x+dx, r.y+dy))
    t = font.render(text, True, color)
    r = t.get_rect()
    if center: r.center = (x, y)
    else: r.topleft = (x, y)
    surf.blit(t, r)

# ══════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════
def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f)
        except:
            pass
    return []

def save_score(name, score, level, kills):
    scores = load_scores()
    scores.append({"name": name, "score": score, "level": level, "kills": kills})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)
    return scores

# ══════════════════════════════════════════
# ACHIEVEMENTS
# ══════════════════════════════════════════
ACHIEVEMENTS_DEF = [
    {"id": "first_kill",   "name": "First Blood",     "desc": "Destroy your first enemy",      "icon": "💀"},
    {"id": "score_1000",   "name": "Rising Star",     "desc": "Reach score 1,000",             "icon": "⭐"},
    {"id": "score_5000",   "name": "Space Veteran",   "desc": "Reach score 5,000",             "icon": "🎖️"},
    {"id": "boss_kill",    "name": "Boss Slayer",      "desc": "Defeat your first Boss",        "icon": "👑"},
    {"id": "powerup_10",   "name": "Power Hungry",    "desc": "Collect 10 power-ups",          "icon": "⚡"},
    {"id": "weapon_max",   "name": "Ion Master",      "desc": "Max out weapon to Ion Cannon",  "icon": "🔫"},
    {"id": "no_damage",    "name": "Untouchable",     "desc": "Complete a level without damage","icon": "🛡️"},
    {"id": "kills_50",     "name": "Ace Pilot",       "desc": "Destroy 50 enemies",            "icon": "🚀"},
    {"id": "kills_100",    "name": "Galaxy Guardian", "desc": "Destroy 100 enemies",           "icon": "🌌"},
    {"id": "level_10",     "name": "Deep Space",      "desc": "Reach Level 10",                "icon": "🪐"},
]

class AchievementSystem:
    def __init__(self):
        self.unlocked = set()
        self.popups = []

    def check(self, key, score=0, kills=0, level=0, powerups=0, weapon=0, no_dmg=False, boss=False):
        new = []
        if key == "kill" and kills >= 1 and "first_kill" not in self.unlocked:
            new.append("first_kill")
        if score >= 1000 and "score_1000" not in self.unlocked:
            new.append("score_1000")
        if score >= 5000 and "score_5000" not in self.unlocked:
            new.append("score_5000")
        if boss and "boss_kill" not in self.unlocked:
            new.append("boss_kill")
        if powerups >= 10 and "powerup_10" not in self.unlocked:
            new.append("powerup_10")
        if weapon >= 3 and "weapon_max" not in self.unlocked:
            new.append("weapon_max")
        if no_dmg and "no_damage" not in self.unlocked:
            new.append("no_damage")
        if kills >= 50 and "kills_50" not in self.unlocked:
            new.append("kills_50")
        if kills >= 100 and "kills_100" not in self.unlocked:
            new.append("kills_100")
        if level >= 10 and "level_10" not in self.unlocked:
            new.append("level_10")
        for aid in new:
            self.unlocked.add(aid)
            ach = next(a for a in ACHIEVEMENTS_DEF if a["id"] == aid)
            self.popups.append({"text": f"{ach['icon']} {ach['name']}", "timer": 200})

    def update(self):
        for p in self.popups:
            p["timer"] -= 1
        self.popups = [p for p in self.popups if p["timer"] > 0]

    def draw(self, surf, font):
        y = 120
        for p in self.popups:
            alpha = min(255, p["timer"] * 3)
            t = font.render(f"ACHIEVEMENT: {p['text']}", True, YELLOW)
            x = SW - t.get_width() - 20
            pygame.draw.rect(surf, (20, 20, 5), (x-8, y-4, t.get_width()+16, t.get_height()+8), border_radius=6)
            pygame.draw.rect(surf, YELLOW, (x-8, y-4, t.get_width()+16, t.get_height()+8), 2, border_radius=6)
            surf.blit(t, (x, y))
            y += 40

# ══════════════════════════════════════════
# NEBULA BACKGROUND
# ══════════════════════════════════════════
class Nebula:
    def __init__(self):
        self.blobs = []
        for _ in range(12):
            self.blobs.append({
                "x": random.randint(0, SW), "y": random.randint(0, SH),
                "r": random.randint(80, 200),
                "color": random.choice([PURPLE_DIM, BLUE_DIM, (0,40,80), (40,0,60)]),
                "speed": random.uniform(0.05, 0.2),
                "phase": random.uniform(0, math.pi*2)
            })
        self.t = 0
        self.surf = pygame.Surface((SW, SH), pygame.SRCALPHA)

    def update(self):
        self.t += 0.01

    def draw(self, surface):
        self.surf.fill((0,0,0,0))
        for b in self.blobs:
            pulse = 1 + 0.15 * math.sin(self.t * 0.7 + b["phase"])
            r = int(b["r"] * pulse)
            cx, cy = int(b["x"]), int(b["y"] + math.sin(self.t * b["speed"] + b["phase"]) * 20)
            for i in range(4, 0, -1):
                alpha = 18 - i * 3
                col = (*b["color"], max(0, alpha))
                pygame.draw.circle(self.surf, col, (cx, cy), r * i // 4)
        surface.blit(self.surf, (0,0))

class StarField:
    def __init__(self, count=300):
        self.stars = [[random.randint(0,SW), random.randint(0,SH),
                       random.uniform(0.1,1.8), random.randint(1,3),
                       random.randint(140,255)] for _ in range(count)]

    def update(self, speed_mult=1.0):
        for s in self.stars:
            s[1] += s[2] * speed_mult
            if s[1] > SH:
                s[1] = 0
                s[0] = random.randint(0, SW)

    def draw(self, surf):
        for s in self.stars:
            c = s[4]
            pygame.draw.circle(surf, (c, c, min(255,c+40)), (int(s[0]),int(s[1])), s[3])

# ══════════════════════════════════════════
# SCREEN SHAKE
# ══════════════════════════════════════════
class ScreenShake:
    def __init__(self):
        self.intensity = 0
        self.offset = (0, 0)

    def shake(self, amount):
        self.intensity = max(self.intensity, amount)

    def update(self):
        if self.intensity > 0:
            self.offset = (random.randint(-int(self.intensity), int(self.intensity)),
                           random.randint(-int(self.intensity), int(self.intensity)))
            self.intensity *= 0.85
            if self.intensity < 0.5:
                self.intensity = 0
                self.offset = (0, 0)

# ══════════════════════════════════════════
# PARTICLES
# ══════════════════════════════════════════
class Particle:
    def __init__(self, x, y, color, speed=3, life=40):
        self.x, self.y = x, y
        self.color = color
        angle = random.uniform(0, math.pi*2)
        spd = random.uniform(0.5, speed)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd
        self.life = random.randint(life//2, life)
        self.max_life = self.life
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.vx *= 0.98
        self.life -= 1

    def draw(self, surf):
        if self.life <= 0: return
        ratio = self.life / self.max_life
        r = min(255, int(self.color[0] * ratio))
        g = min(255, int(self.color[1] * ratio))
        b = min(255, int(self.color[2] * ratio))
        size = max(1, int(self.size * ratio))
        pygame.draw.circle(surf, (r,g,b), (int(self.x), int(self.y)), size)

    @property
    def alive(self): return self.life > 0

def spawn_explosion(particles, x, y, colors=None, count=35, speed=4):
    if colors is None: colors = [ORANGE, YELLOW, RED, WHITE]
    for _ in range(count):
        particles.append(Particle(x, y, random.choice(colors), speed))

# ══════════════════════════════════════════
# POWER-UPS
# ══════════════════════════════════════════
POWERUP_TYPES = [
    {"type": "shield",      "color": CYAN,   "icon": "S", "label": "SHIELD RESTORE"},
    {"type": "triple",      "color": GREEN,  "icon": "3", "label": "TRIPLE SHOT"},
    {"type": "speed",       "color": YELLOW, "icon": "»", "label": "SPEED BOOST"},
    {"type": "nuke",        "color": ORANGE, "icon": "N", "label": "NUKE"},
    {"type": "score",       "color": PURPLE, "icon": "$", "label": "+500 SCORE"},
]

class PowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.data = random.choice(POWERUP_TYPES)
        self.type = self.data["type"]
        self.color = self.data["color"]
        self.icon = self.data["icon"]
        self.speed = 2.0
        self.alive = True
        self.t = random.uniform(0, math.pi*2)
        self.radius = 16

    def update(self):
        self.y += self.speed
        self.t += 0.08
        if self.y > SH + 30:
            self.alive = False

    def draw(self, surf):
        pulse = 1 + 0.12 * math.sin(self.t)
        r = int(self.radius * pulse)
        cx, cy = int(self.x), int(self.y)
        # Outer glow ring
        pygame.draw.circle(surf, (self.color[0]//3, self.color[1]//3, self.color[2]//3), (cx,cy), r+6)
        pygame.draw.circle(surf, self.color, (cx,cy), r, 2)
        pygame.draw.circle(surf, DARK_PANEL, (cx,cy), r-2)
        font = pygame.font.SysFont("Courier", 16, bold=True)
        t = font.render(self.icon, True, self.color)
        surf.blit(t, (cx - t.get_width()//2, cy - t.get_height()//2))

    def collide(self, px, py):
        return math.hypot(self.x-px, self.y-py) < self.radius + 22

# ══════════════════════════════════════════
# WEAPON SYSTEM
# ══════════════════════════════════════════
WEAPONS = [
    {"name": "LASER",      "color": CYAN,   "speed": 13, "damage": 1, "spread": 0, "cost": 0},
    {"name": "PLASMA",     "color": GREEN,  "speed": 15, "damage": 2, "spread": 1, "cost": 200},
    {"name": "ION CANNON", "color": PURPLE, "speed": 18, "damage": 3, "spread": 2, "cost": 500},
]

class Laser:
    def __init__(self, x, y, angle, weapon_level=0, color=None):
        self.x, self.y = x, y
        w = WEAPONS[weapon_level]
        self.speed = w["speed"]
        self.color = color or w["color"]
        self.vx = math.sin(math.radians(angle)) * self.speed
        self.vy = -math.cos(math.radians(angle)) * self.speed
        self.alive = True
        self.damage = w["damage"]
        self.width = 2 + weapon_level

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y < -50 or self.y > SH+50 or self.x < -50 or self.x > SW+50:
            self.alive = False

    def draw(self, surf):
        ex = self.x - self.vx * 1.8
        ey = self.y - self.vy * 1.8
        draw_glow_line(surf, self.color, (int(self.x),int(self.y)), (int(ex),int(ey)), self.width, 5)

# ══════════════════════════════════════════
# ASTEROID
# ══════════════════════════════════════════
class Asteroid3D:
    def __init__(self, speed_mult=1.0):
        self.reset(speed_mult)

    def reset(self, speed_mult=1.0):
        self.x = random.uniform(60, SW-60)
        self.y = random.uniform(-180, -30)
        self.z = random.uniform(1, 4)
        self.speed = random.uniform(1.5, 3.5) * speed_mult
        self.rot_z = random.uniform(0, 360)
        self.rot_x = random.uniform(0, 360)
        self.rot_spd_z = random.uniform(-2.5, 2.5)
        self.rot_spd_x = random.uniform(-1.5, 1.5)
        self.base_radius = random.randint(20, 42)
        self.color = random.choice([GREY, (100,80,60), (85,90,110), (70,100,80)])
        self.points = self._gen()
        self.alive = True
        self.hit_flash = 0
        self.hp = 1
        self.speed_mult = speed_mult

    def _gen(self):
        pts = []
        for i in range(12):
            a = math.radians(i * 30)
            r = self.base_radius * random.uniform(0.65, 1.35)
            pts.append((math.cos(a)*r, math.sin(a)*r))
        return pts

    def update(self):
        self.y += self.speed
        self.rot_z += self.rot_spd_z
        self.rot_x += self.rot_spd_x
        if self.hit_flash > 0: self.hit_flash -= 1
        if self.y > SH + 120: self.reset(self.speed_mult)

    def projected(self):
        scale = 1 / self.z
        rz = math.radians(self.rot_z)
        rx = math.radians(self.rot_x)
        result = []
        for px, py in self.points:
            rx2 = px*math.cos(rz) - py*math.sin(rz)
            ry2 = px*math.sin(rz) + py*math.cos(rz)
            sx = rx2*scale + self.x
            sy = ry2*scale*math.cos(rx) + self.y
            result.append((int(sx), int(sy)))
        return result

    def draw(self, surf):
        pts = self.projected()
        if len(pts) < 3: return
        shadow = [(p[0]+5, p[1]+5) for p in pts]
        pygame.draw.polygon(surf, (15,15,25), shadow)
        color = RED if self.hit_flash > 0 else self.color
        draw_glow_polygon(surf, color, pts, 0)
        r = max(3, self.base_radius//4)
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(surf, (50,50,60), (cx-r//2, cy-r//2), r//2)
        pygame.draw.circle(surf, (50,50,60), (cx+r//3, cy+r//3), r//3)

    def collide(self, lx, ly):
        pts = self.projected()
        if len(pts) < 3: return False
        n = len(pts); inside = False; j = n-1
        for i in range(n):
            xi,yi = pts[i]; xj,yj = pts[j]
            if ((yi>ly) != (yj>ly)) and (lx < (xj-xi)*(ly-yi)/(yj-yi+1e-9)+xi):
                inside = not inside
            j = i
        return inside

# ══════════════════════════════════════════
# ENEMY AI SHIP
# ══════════════════════════════════════════
class EnemyShip:
    def __init__(self, level=1):
        self.x = random.uniform(80, SW-80)
        self.y = random.uniform(-200, -50)
        self.hp = 2 + level
        self.max_hp = self.hp
        self.speed = random.uniform(1.5, 2.5 + level*0.2)
        self.angle = 0
        self.lasers = []
        self.shoot_cd = random.randint(60, 120)
        self.alive = True
        self.hit_flash = 0
        self.size = 22
        self.patrol_t = random.uniform(0, math.pi*2)
        self.patrol_speed = random.uniform(0.02, 0.04)
        self.score_value = 30 * level

    def update(self, player_x, player_y):
        # Chase player
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy) + 1e-9
        target_angle = math.degrees(math.atan2(dx, -dy))
        diff = (target_angle - self.angle + 180) % 360 - 180
        self.angle += diff * 0.04

        # Move toward player but maintain distance
        if dist > 180:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed
        else:
            # Patrol side to side
            self.patrol_t += self.patrol_speed
            self.x += math.cos(self.patrol_t) * 2

        # Shoot
        self.shoot_cd -= 1
        if self.shoot_cd <= 0 and dist < 400:
            self.lasers.append(Laser(self.x, self.y, self.angle + random.uniform(-8,8), 0, RED))
            self.shoot_cd = random.randint(50, 100)

        for l in self.lasers: l.update()
        self.lasers = [l for l in self.lasers if l.alive]
        if self.hit_flash > 0: self.hit_flash -= 1

        if self.y > SH + 100: self.alive = False

    def take_damage(self, dmg):
        self.hp -= dmg
        self.hit_flash = 10
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surf):
        ar = math.radians(self.angle)
        s = self.size
        def rot(px, py):
            rx = px*math.cos(ar) - py*math.sin(ar)
            ry = px*math.sin(ar) + py*math.cos(ar)
            return (self.x+rx, self.y+ry)

        color = ORANGE if self.hit_flash > 0 else RED
        dim   = RED_DIM if self.hit_flash == 0 else ORANGE

        nose  = rot(0, -s)
        lw    = rot(-s*0.8, s*0.5)
        rw    = rot( s*0.8, s*0.5)
        lb    = rot(-s*0.3, s*0.85)
        rb    = rot( s*0.3, s*0.85)
        ctr   = rot(0, s*0.25)

        draw_glow_polygon(surf, color, [nose,lw,ctr,rw], 0)
        draw_glow_polygon(surf, dim,   [lw,lb,ctr], 0)
        draw_glow_polygon(surf, dim,   [rw,rb,ctr], 0)
        pygame.draw.polygon(surf, color, [nose,lw,lb,rb,rw], 2)

        # HP bar
        bw = 36
        bx = int(self.x - bw//2)
        by = int(self.y + s + 5)
        pygame.draw.rect(surf, (60,0,0), (bx, by, bw, 5))
        hw = int(bw * self.hp / self.max_hp)
        pygame.draw.rect(surf, RED, (bx, by, hw, 5))

        for l in self.lasers: l.draw(surf)

# ══════════════════════════════════════════
# BOSS
# ══════════════════════════════════════════
class Boss:
    def __init__(self, level):
        self.x = SW // 2
        self.y = -120
        self.target_y = 130
        self.hp = 40 + level * 15
        self.max_hp = self.hp
        self.lasers = []
        self.alive = True
        self.phase = 0        # 0=enter, 1=fight, 2=rage
        self.t = 0
        self.shoot_cd = 0
        self.size = 55
        self.hit_flash = 0
        self.level = level
        self.pattern = 0
        self.pattern_t = 0
        self.score_value = 500 + level * 100

    def update(self, player_x, player_y):
        self.t += 0.02
        self.hit_flash = max(0, self.hit_flash - 1)
        self.pattern_t += 1

        # Enter phase
        if self.phase == 0:
            self.y += 2
            if self.y >= self.target_y:
                self.y = self.target_y
                self.phase = 1

        # Rage phase
        if self.hp < self.max_hp * 0.35:
            self.phase = 2

        # Movement
        if self.phase >= 1:
            self.x = SW//2 + math.sin(self.t * 0.8) * 280

        # Shooting patterns
        self.shoot_cd -= 1
        if self.shoot_cd <= 0 and self.phase >= 1:
            self._shoot(player_x, player_y)
            self.shoot_cd = 25 if self.phase < 2 else 15

        # Change pattern every 3 seconds
        if self.pattern_t % 180 == 0:
            self.pattern = (self.pattern + 1) % 3

        for l in self.lasers: l.update()
        self.lasers = [l for l in self.lasers if l.alive]

    def _shoot(self, px, py):
        dx = px - self.x; dy = py - self.y
        angle_to_player = math.degrees(math.atan2(dx, -dy))

        if self.pattern == 0:  # Aimed burst
            for spread in [-10, 0, 10]:
                self.lasers.append(Laser(self.x, self.y+30, angle_to_player+spread, 0, ORANGE))

        elif self.pattern == 1:  # Radial spread
            num = 8 if self.phase < 2 else 12
            for i in range(num):
                a = i * (360/num) + self.t*20
                self.lasers.append(Laser(self.x, self.y, a, 0, RED))

        elif self.pattern == 2:  # Spiral
            for i in range(4):
                a = angle_to_player + i*90 + self.t*30
                self.lasers.append(Laser(self.x, self.y, a, 0, PURPLE))

    def take_damage(self, dmg):
        self.hp -= dmg
        self.hit_flash = 8
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        s = self.size
        color = WHITE if self.hit_flash > 0 else ORANGE
        accent = YELLOW

        # Main body hexagon
        pts = []
        for i in range(6):
            a = math.radians(i*60 + self.t*10)
            pts.append((cx + math.cos(a)*s, cy + math.sin(a)*s*0.7))
        draw_glow_polygon(surf, color, pts, 0)

        # Inner core
        pts2 = []
        for i in range(6):
            a = math.radians(i*60 - self.t*15)
            pts2.append((cx + math.cos(a)*s*0.5, cy + math.sin(a)*s*0.4))
        draw_glow_polygon(surf, RED, pts2, 0)

        # Cannons
        for side in [-1, 1]:
            pygame.draw.rect(surf, GREY,
                (cx + side*s - 8, cy + s//2 - 6, 16, 30), border_radius=4)
            pygame.draw.rect(surf, accent,
                (cx + side*s - 8, cy + s//2 - 6, 16, 30), 2, border_radius=4)

        # Pulsing core glow
        draw_glow_circle(surf, RED, (cx,cy), int(12 + 5*math.sin(self.t*3)), 2)

        # HP Bar
        bw = 300; bx = SW//2 - bw//2; by = 15
        pygame.draw.rect(surf, (60,0,0), (bx-2, by-2, bw+4, 22), border_radius=5)
        hw = int(bw * self.hp / self.max_hp)
        hp_color = GREEN if self.hp > self.max_hp*0.6 else (YELLOW if self.hp > self.max_hp*0.3 else RED)
        pygame.draw.rect(surf, hp_color, (bx, by, hw, 18), border_radius=5)
        pygame.draw.rect(surf, WHITE, (bx-2, by-2, bw+4, 22), 2, border_radius=5)

        font = pygame.font.SysFont("Courier", 14, bold=True)
        t = font.render(f"BOSS  HP: {self.hp}/{self.max_hp}  {'★ RAGE MODE ★' if self.phase==2 else ''}", True, WHITE)
        surf.blit(t, (SW//2 - t.get_width()//2, by))

        for l in self.lasers: l.draw(surf)

# ══════════════════════════════════════════
# PLAYER SPACESHIP
# ══════════════════════════════════════════
class Spaceship:
    def __init__(self):
        self.x = SW // 2
        self.y = SH - 110
        self.angle = 0
        self.size = 34
        self.lasers = []
        self.shoot_cd = 0
        self.shield = 100
        self.speed = 5.0
        self.weapon_level = 0
        self.triple_timer = 0
        self.speed_timer = 0
        self.engine_particles = []
        self.invincible = 0
        # ── Touch / Mouse controls ──
        self.touch_target = None   # (x, y) where player tapped
        self.touch_active = False  # is finger/mouse held down
        self.is_moving = False     # for engine trail

    def set_touch_target(self, x, y):
        """Called when screen is tapped/clicked"""
        self.touch_target = (x, y)
        self.touch_active = True

    def clear_touch(self):
        self.touch_active = False
        self.touch_target = None

    def handle_input(self, keys):
        # ── Keyboard controls (unchanged) ──
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.angle -= 3.2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.angle += 3.2
        spd = self.speed * (1.5 if self.speed_timer > 0 else 1.0)
        kb_moving = False
        if keys[pygame.K_UP]   or keys[pygame.K_w]:
            self.x += math.sin(math.radians(self.angle)) * spd
            self.y -= math.cos(math.radians(self.angle)) * spd
            kb_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.x -= math.sin(math.radians(self.angle)) * spd * 0.5
            self.y += math.cos(math.radians(self.angle)) * spd * 0.5

        # ── Touch / Mouse controls ──
        if self.touch_target and self.touch_active:
            tx, ty = self.touch_target
            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)

            if dist > 6:  # Move toward tap point
                # Rotate ship to face target
                target_angle = math.degrees(math.atan2(dx, -dy))
                diff = (target_angle - self.angle + 180) % 360 - 180
                self.angle += diff * 0.18

                # Move toward target
                move_spd = spd * min(1.0, dist / 60)
                self.x += (dx / dist) * move_spd
                self.y += (dy / dist) * move_spd
                kb_moving = True
            else:
                # Reached target — stop & auto-shoot
                self.touch_target = None

        self.is_moving = kb_moving
        self.x = max(35, min(SW-35, self.x))
        self.y = max(35, min(SH-35, self.y))

        # Auto-shoot when moving via touch
        if self.touch_active and self.shoot_cd <= 0:
            self._shoot()
            self.shoot_cd = max(6, 14 - self.weapon_level * 2)

        if keys[pygame.K_SPACE] and self.shoot_cd <= 0:
            self._shoot()
            self.shoot_cd = max(6, 14 - self.weapon_level * 2)

    def _shoot(self):
        tip_x = self.x + math.sin(math.radians(self.angle)) * self.size
        tip_y = self.y - math.cos(math.radians(self.angle)) * self.size
        self.lasers.append(Laser(tip_x, tip_y, self.angle, self.weapon_level))
        if self.triple_timer > 0 or self.weapon_level >= 1:
            self.lasers.append(Laser(tip_x, tip_y, self.angle - 18, self.weapon_level))
            self.lasers.append(Laser(tip_x, tip_y, self.angle + 18, self.weapon_level))

    def update(self):
        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.triple_timer > 0: self.triple_timer -= 1
        if self.speed_timer > 0: self.speed_timer -= 1
        if self.invincible > 0: self.invincible -= 1
        for l in self.lasers: l.update()
        self.lasers = [l for l in self.lasers if l.alive]

        # Engine trail
        if self.is_moving:
            tail_x = self.x - math.sin(math.radians(self.angle)) * self.size*0.75
            tail_y = self.y + math.cos(math.radians(self.angle)) * self.size*0.75
            for _ in range(4):
                c = random.choice([ORANGE, YELLOW, (255,80,0), CYAN])
                self.engine_particles.append(Particle(
                    tail_x + random.uniform(-5,5),
                    tail_y + random.uniform(-5,5), c, 2, 25))
        for p in self.engine_particles: p.update()
        self.engine_particles = [p for p in self.engine_particles if p.alive]

    def draw(self, surf):
        for p in self.engine_particles: p.draw(surf)
        for l in self.lasers: l.draw(surf)

        ar = math.radians(self.angle)
        s  = self.size
        def rot(px, py):
            rx = px*math.cos(ar) - py*math.sin(ar)
            ry = px*math.sin(ar) + py*math.cos(ar)
            return (self.x+rx, self.y+ry)

        nose  = rot(0, -s)
        lWing = rot(-s*0.85, s*0.55)
        rWing = rot( s*0.85, s*0.55)
        lBack = rot(-s*0.38, s*0.88)
        rBack = rot( s*0.38, s*0.88)
        ctr   = rot(0, s*0.28)

        wcolor = WEAPONS[self.weapon_level]["color"]

        # Invincible flicker
        if self.invincible > 0 and self.invincible % 6 < 3:
            return

        draw_glow_polygon(surf, wcolor,    [nose,lWing,ctr,rWing], 0)
        draw_glow_polygon(surf, BLUE_DIM,  [lWing,lBack,ctr], 0)
        draw_glow_polygon(surf, BLUE_DIM,  [rWing,rBack,ctr], 0)
        pygame.draw.polygon(surf, wcolor, [nose,lWing,lBack,rBack,rWing], 2)

        cockpit = rot(0, -s*0.28)
        draw_glow_circle(surf, YELLOW, (int(cockpit[0]),int(cockpit[1])), 6, 2)

        # Shield glow when high
        if self.shield > 75:
            draw_glow_circle(surf, (0,100,255), (int(self.x),int(self.y)), s+5, 1)

    def get_rect(self):
        return pygame.Rect(self.x-22, self.y-22, 44, 44)

# ══════════════════════════════════════════
# HUD
# ══════════════════════════════════════════
def draw_hud(surf, font, bfont, score, lives, level, shield, weapon_level, triple_t, speed_t, upgrade_cost):
    # Left panel
    pygame.draw.rect(surf, DARK_PANEL, (0, 0, 220, 90), border_radius=8)
    pygame.draw.rect(surf, CYAN_DIM,   (0, 0, 220, 90), 1, border_radius=8)
    draw_text_glow(surf, f"SCORE: {score:06d}", bfont, CYAN, 12, 14, center=False)
    lives_str = "♥ " * max(0, lives)
    draw_text_glow(surf, f"LIVES: {lives_str}", font, RED, 12, 48, center=False)
    draw_text_glow(surf, f"WEAPON: {WEAPONS[weapon_level]['name']}", font, WEAPONS[weapon_level]['color'], 12, 70, center=False)

    # Right panel
    pygame.draw.rect(surf, DARK_PANEL, (SW-230, 0, 230, 90), border_radius=8)
    pygame.draw.rect(surf, CYAN_DIM,   (SW-230, 0, 230, 90), 1, border_radius=8)
    draw_text_glow(surf, f"LEVEL: {level}", bfont, YELLOW, SW-12, 14, center=False)

    # Shield bar
    bx, by = SW-225, 48
    pygame.draw.rect(surf, (30,30,50), (bx, by, 200, 16), border_radius=5)
    hw = int(200 * shield / 100)
    sc = GREEN if shield>60 else (YELLOW if shield>30 else RED)
    pygame.draw.rect(surf, sc, (bx, by, hw, 16), border_radius=5)
    pygame.draw.rect(surf, WHITE, (bx, by, 200, 16), 1, border_radius=5)
    t = font.render(f"SHIELD {shield}%", True, WHITE)
    surf.blit(t, (bx + 200//2 - t.get_width()//2, by))

    # Upgrade hint
    if weapon_level < 2:
        draw_text_glow(surf, f"[U] UPGRADE → {WEAPONS[weapon_level+1]['name']} ({upgrade_cost} pts)", font,
                       WEAPONS[weapon_level+1]['color'], SW//2, SH-22)

    # Active power-up timers
    px = 230
    if triple_t > 0:
        t = font.render(f"⚡ TRIPLE: {triple_t//60+1}s", True, GREEN)
        surf.blit(t, (px, 8)); px += t.get_width() + 20
    if speed_t > 0:
        t = font.render(f"» SPEED: {speed_t//60+1}s", True, YELLOW)
        surf.blit(t, (px, 8))

# ══════════════════════════════════════════
# REUSABLE CLICKABLE BUTTON
# ══════════════════════════════════════════
def draw_button(surf, font, text, x, y, w, h, color, hover=False, icon=""):
    """Draw a neon clickable button. Returns its rect."""
    rect = pygame.Rect(x - w//2, y - h//2, w, h)
    # Shadow
    shadow = pygame.Rect(rect.x+4, rect.y+4, w, h)
    pygame.draw.rect(surf, (0,0,0), shadow, border_radius=12)
    # Background
    bg = (color[0]//5, color[1]//5, color[2]//5)
    if hover:
        bg = (color[0]//3, color[1]//3, color[2]//3)
    pygame.draw.rect(surf, bg, rect, border_radius=12)
    # Border glow
    border_w = 3 if hover else 2
    pygame.draw.rect(surf, color, rect, border_w, border_radius=12)
    if hover:
        glow_rect = pygame.Rect(rect.x-3, rect.y-3, w+6, h+6)
        pygame.draw.rect(surf, (color[0]//2, color[1]//2, color[2]//2), glow_rect, 1, border_radius=14)
    # Text
    label = f"{icon}  {text}" if icon else text
    draw_text_glow(surf, label, font, color if not hover else WHITE, x, y)
    return rect

def is_hovered(rect):
    mx, my = pygame.mouse.get_pos()
    return rect.collidepoint(mx, my)

# ══════════════════════════════════════════
# SCREENS
# ══════════════════════════════════════════
def main_menu(screen, clock, stars, nebula, font, bfont, tfont):
    t = 0
    while True:
        mx, my = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN: return "play"
                if e.key == pygame.K_l:      return "leaderboard"
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_play.collidepoint(mx, my):    return "play"
                if btn_leader.collidepoint(mx, my):  return "leaderboard"
                if btn_quit.collidepoint(mx, my):    pygame.quit(); sys.exit()

        t += 1
        nebula.update()
        stars.update(0.5)
        screen.fill(BG)
        nebula.draw(screen)
        stars.draw(screen)

        # Animated title
        scale = 1 + 0.03 * math.sin(t * 0.04)
        title_surf = tfont.render("NOVA STRIKE", True, CYAN)
        w, h = title_surf.get_size()
        scaled = pygame.transform.scale(title_surf, (int(w*scale), int(h*scale)))
        screen.blit(scaled, (SW//2 - scaled.get_width()//2, 110))
        draw_text_glow(screen, "SPACE SHOOTER v2.0", bfont, PURPLE, SW//2, 205)

        # ── Clickable Buttons ──
        BW, BH = 320, 58
        btn_play   = draw_button(screen, bfont, "START GAME",   SW//2, 295, BW, BH, GREEN,  is_hovered(pygame.Rect(SW//2-BW//2, 295-BH//2, BW, BH)), "🚀")
        btn_leader = draw_button(screen, bfont, "LEADERBOARD",  SW//2, 375, BW, BH, CYAN,   is_hovered(pygame.Rect(SW//2-BW//2, 375-BH//2, BW, BH)), "🏆")
        btn_quit   = draw_button(screen, bfont, "QUIT",         SW//2, 455, BW, BH, RED,    is_hovered(pygame.Rect(SW//2-BW//2, 455-BH//2, BW, BH)), "✖")

        # Controls box
        pygame.draw.rect(screen, DARK_PANEL, (SW//2-240, 520, 480, 115), border_radius=10)
        pygame.draw.rect(screen, CYAN_DIM,   (SW//2-240, 520, 480, 115), 1, border_radius=10)
        draw_text_glow(screen, "CONTROLS", font, CYAN, SW//2, 538)
        draw_text_glow(screen, "CLICK / TAP anywhere = Move ship", font, WHITE, SW//2, 562)
        draw_text_glow(screen, "Hold = Auto shoot   U = Upgrade", font, WHITE, SW//2, 585)
        draw_text_glow(screen, "P = Pause    ESC = Menu", font, YELLOW, SW//2, 610)

        pygame.display.flip()
        clock.tick(FPS)

def leaderboard_screen(screen, clock, font, bfont, tfont):
    scores = load_scores()
    while True:
        mx, my = pygame.mouse.get_pos()
        BW, BH = 240, 52
        btn_back = pygame.Rect(SW//2-BW//2, SH-75, BW, BH)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN: return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_back.collidepoint(mx, my): return

        screen.fill(BG)
        draw_text_glow(screen, "LEADERBOARD", tfont, YELLOW, SW//2, 55)

        if not scores:
            draw_text_glow(screen, "No scores yet! Play a game first.", bfont, CYAN, SW//2, SH//2)
        else:
            headers = ["RANK", "NAME", "SCORE", "LEVEL", "KILLS"]
            cols = [SW//2-300, SW//2-180, SW//2, SW//2+130, SW//2+240]
            for i, h in enumerate(headers):
                draw_text_glow(screen, h, font, CYAN, cols[i], 130)
            pygame.draw.line(screen, CYAN_DIM, (SW//2-320, 150), (SW//2+280, 150), 1)

            for ri, s in enumerate(scores[:10]):
                y = 172 + ri * 40
                colors = [YELLOW, (200,200,200), (180,120,50)] + [WHITE]*7
                c = colors[ri]
                medal = ["🥇","🥈","🥉"] + [f"#{ri+1}"] * 7
                draw_text_glow(screen, medal[ri],             font, c, cols[0], y)
                draw_text_glow(screen, s.get("name","???"),   font, c, cols[1], y)
                draw_text_glow(screen, f"{s['score']:06d}",   font, c, cols[2], y)
                draw_text_glow(screen, str(s.get("level",1)), font, c, cols[3], y)
                draw_text_glow(screen, str(s.get("kills",0)), font, c, cols[4], y)

        # Back button
        draw_button(screen, bfont, "BACK TO MENU", SW//2, SH-50, BW, BH, CYAN,
                    btn_back.collidepoint(mx, my), "←")

        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(screen, clock, font, bfont, tfont, score, level, kills, powerups_collected, achievements):
    # Get player name
    name = ""
    input_active = True
    while input_active:
        mx, my = pygame.mouse.get_pos()
        confirm_rect = pygame.Rect(SW//2-130, 310, 260, 48)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and e.unicode.isprintable():
                    name += e.unicode.upper()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if confirm_rect.collidepoint(mx, my) and name.strip():
                    input_active = False

        screen.fill(BG)
        draw_text_glow(screen, "GAME OVER", tfont, RED, SW//2, 100)
        draw_text_glow(screen, "Enter your name:", bfont, YELLOW, SW//2, 210)

        # Name input box
        pygame.draw.rect(screen, DARK_PANEL, (SW//2-160, 240, 320, 50), border_radius=8)
        pygame.draw.rect(screen, CYAN, (SW//2-160, 240, 320, 50), 2, border_radius=8)
        draw_text_glow(screen, name + "|", bfont, WHITE, SW//2, 265)

        # Confirm button
        draw_button(screen, bfont, "CONFIRM", SW//2, 335, 260, 48,
                    GREEN if name.strip() else GREY,
                    confirm_rect.collidepoint(mx, my) and bool(name.strip()), "✔")

        pygame.display.flip()
        clock.tick(FPS)

    scores = save_score(name.strip() or "PILOT", score, level, kills)

    # Show stats
    while True:
        mx, my = pygame.mouse.get_pos()
        BW, BH = 240, 52
        btn_restart = pygame.Rect(SW//2 - 260, SH - 85, BW, BH)
        btn_menu    = pygame.Rect(SW//2 - 10,  SH - 85, BW, BH)
        btn_quit2   = pygame.Rect(SW//2 + 280, SH - 85, 160, BH)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "restart"
                if e.key == pygame.K_m: return "menu"
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_restart.collidepoint(mx, my): return "restart"
                if btn_menu.collidepoint(mx, my):    return "menu"
                if btn_quit2.collidepoint(mx, my):   pygame.quit(); sys.exit()

        screen.fill(BG)
        draw_text_glow(screen, "MISSION REPORT", tfont, CYAN, SW//2, 55)

        # Stats box
        pygame.draw.rect(screen, DARK_PANEL, (SW//2-310, 105, 620, 270), border_radius=12)
        pygame.draw.rect(screen, CYAN_DIM,   (SW//2-310, 105, 620, 270), 2, border_radius=12)

        stats = [
            ("PILOT",               name,         YELLOW),
            ("FINAL SCORE",         f"{score:06d}", CYAN),
            ("LEVEL REACHED",       str(level),   GREEN),
            ("ENEMIES DESTROYED",   str(kills),   RED),
            ("POWER-UPS COLLECTED", str(powerups_collected), PURPLE),
        ]
        for i, (label, val, col) in enumerate(stats):
            y = 128 + i * 44
            draw_text_glow(screen, label + ":", font, GREY, SW//2-230, y, center=False)
            draw_text_glow(screen, val, bfont, col, SW//2+180, y)

        # Achievements
        if achievements.unlocked:
            draw_text_glow(screen, f"ACHIEVEMENTS UNLOCKED: {len(achievements.unlocked)}/{len(ACHIEVEMENTS_DEF)}",
                           font, YELLOW, SW//2, 395)
            ach_names = [next(a["icon"]+" "+a["name"] for a in ACHIEVEMENTS_DEF if a["id"]==aid)
                         for aid in list(achievements.unlocked)[:4]]
            draw_text_glow(screen, "  ".join(ach_names), font, WHITE, SW//2, 418)

        # Top 3
        draw_text_glow(screen, "TOP SCORES", bfont, YELLOW, SW//2, 450)
        for i, s in enumerate(scores[:3]):
            row_colors = [YELLOW, (200,200,200), (180,120,50)]
            draw_text_glow(screen, f"#{i+1}  {s.get('name','???'):12s}  {s['score']:06d}",
                           font, row_colors[i], SW//2, 478 + i*28)

        # Clickable buttons
        draw_button(screen, bfont, "PLAY AGAIN", SW//2-130, SH-58, BW, BH,
                    GREEN,  btn_restart.collidepoint(mx, my), "🔄")
        draw_button(screen, bfont, "MAIN MENU",  SW//2+120, SH-58, BW, BH,
                    CYAN,   btn_menu.collidepoint(mx, my),    "🏠")
        draw_button(screen, font,  "QUIT",       SW//2+360, SH-58, 160, BH,
                    RED,    btn_quit2.collidepoint(mx, my),   "✖")

        pygame.display.flip()
        clock.tick(FPS)

# ══════════════════════════════════════════
# MAIN GAME LOOP
# ══════════════════════════════════════════
def game_loop(screen, clock, font, bfont, tfont):
    stars  = StarField(300)
    nebula = Nebula()
    shake  = ScreenShake()
    ship   = Spaceship()
    achievements = AchievementSystem()

    asteroids  = [Asteroid3D() for _ in range(8)]
    enemies    = []
    powerups   = []
    particles  = []
    boss       = None

    score = 0; lives = 3; level = 1
    kills = 0; powerups_collected = 0
    game_over = False; paused = False
    flash_t = 0; level_up_t = 0
    boss_announced = 0
    level_damage_taken = False
    enemy_spawn_t = 0

    UPGRADE_COSTS = [0, 200, 500]

    def nuke_all():
        nonlocal score
        for a in asteroids:
            spawn_explosion(particles, a.x, a.y, [ORANGE,YELLOW,RED], 20)
            score += 5 * level
            a.reset(1 + level * 0.08)
        for e in enemies:
            spawn_explosion(particles, e.x, e.y, [RED,ORANGE,WHITE], 20)
            score += e.score_value // 2
            e.alive = False

    def apply_powerup(ptype):
        nonlocal score, powerups_collected
        powerups_collected += 1
        if ptype == "shield":
            ship.shield = min(100, ship.shield + 50)
        elif ptype == "triple":
            ship.triple_timer = 600
        elif ptype == "speed":
            ship.speed_timer = 400
        elif ptype == "nuke":
            nuke_all()
            shake.shake(15)
        elif ptype == "score":
            score += 500

    # ── LOOP ──
    while not game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused and event.key == pygame.K_u:
                    wl = ship.weapon_level
                    if wl < 2:
                        cost = UPGRADE_COSTS[wl+1]
                        if score >= cost:
                            score -= cost
                            ship.weapon_level += 1
                            spawn_explosion(particles, ship.x, ship.y,
                                [WEAPONS[ship.weapon_level]["color"], WHITE], 20, 3)

            # ── MOUSE / TOUCH EVENTS ──
            if not paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Check touch buttons (top-right area)
                    # Pause button: top-right corner
                    if SW-60 <= mx <= SW-10 and 10 <= my <= 55:
                        paused = True
                    # Upgrade button: bottom-right
                    elif SW-180 <= mx <= SW-10 and SH-65 <= my <= SH-10:
                        wl = ship.weapon_level
                        if wl < 2:
                            cost = UPGRADE_COSTS[wl+1]
                            if score >= cost:
                                score -= cost
                                ship.weapon_level += 1
                                spawn_explosion(particles, ship.x, ship.y,
                                    [WEAPONS[ship.weapon_level]["color"], WHITE], 20, 3)
                    else:
                        ship.set_touch_target(mx, my)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    ship.clear_touch()

                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Drag = continuous move
                        mx, my = event.pos
                        if not (SW-60 <= mx <= SW-10 and 10 <= my <= 55):
                            ship.set_touch_target(mx, my)

                # Finger touch events (real touch screens)
                elif event.type == pygame.FINGERDOWN:
                    fx = int(event.x * SW)
                    fy = int(event.y * SH)
                    ship.set_touch_target(fx, fy)

                elif event.type == pygame.FINGERUP:
                    ship.clear_touch()

                elif event.type == pygame.FINGERMOTION:
                    fx = int(event.x * SW)
                    fy = int(event.y * SH)
                    ship.set_touch_target(fx, fy)

        if paused:
            screen.fill(BG)
            draw_text_glow(screen, "⏸  PAUSED", tfont, YELLOW, SW//2, SH//2-40)
            draw_text_glow(screen, "Press P to Resume", bfont, WHITE, SW//2, SH//2+30)
            pygame.display.flip()
            continue

        # ── UPDATE ──
        keys = pygame.key.get_pressed()
        ship.handle_input(keys)
        ship.update()
        nebula.update()
        stars.update(1.0 + level * 0.05)
        shake.update()
        achievements.update()

        # Level progression
        new_level = score // 600 + 1
        if new_level > level:
            level = new_level
            level_up_t = 150
            if not level_damage_taken:
                achievements.check("no_damage", no_dmg=True)
            level_damage_taken = False
            for _ in range(min(3, level//2)):
                a = Asteroid3D(1 + level * 0.08)
                asteroids.append(a)
            if level % 5 == 0 and boss is None:
                boss = Boss(level)
                boss_announced = 200

        # Boss spawn announcement
        if boss_announced > 0:
            boss_announced -= 1

        # Enemy spawning
        enemy_spawn_t += 1
        spawn_interval = max(120, 300 - level * 15)
        if enemy_spawn_t >= spawn_interval and len(enemies) < min(6, level):
            enemies.append(EnemyShip(level))
            enemy_spawn_t = 0

        # Update asteroids
        speed_mult = 1 + level * 0.08
        for a in asteroids:
            a.speed_mult = speed_mult
            a.update()

        # Update enemies
        for e in enemies:
            e.update(ship.x, ship.y)
        enemies = [e for e in enemies if e.alive]

        # Update boss
        if boss:
            boss.update(ship.x, ship.y)
            if not boss.alive:
                spawn_explosion(particles, boss.x, boss.y,
                    [ORANGE,YELLOW,RED,WHITE,PURPLE], 80, 8)
                score += boss.score_value
                kills += 1
                shake.shake(20)
                achievements.check("boss", boss=True)
                boss = None

        # Update powerups
        for p in powerups: p.update()
        powerups = [p for p in powerups if p.alive]

        # Update particles
        for p in particles: p.update()
        particles = [p for p in particles if p.alive]

        if flash_t > 0: flash_t -= 1
        if level_up_t > 0: level_up_t -= 1

        # ── COLLISIONS ──
        ship_rect = ship.get_rect()

        # Player laser vs asteroid
        for laser in ship.lasers[:]:
            for a in asteroids:
                if a.collide(laser.x, laser.y):
                    laser.alive = False
                    a.hit_flash = 8
                    score += 10 * level
                    kills += 1
                    spawn_explosion(particles, a.x, a.y)
                    a.reset(speed_mult)
                    if random.random() < 0.18:
                        powerups.append(PowerUp(a.x, a.y))
                    achievements.check("kill", score=score, kills=kills, level=level,
                                       powerups=powerups_collected, weapon=ship.weapon_level)

        # Player laser vs enemy
        for laser in ship.lasers[:]:
            for e in enemies[:]:
                if math.hypot(laser.x-e.x, laser.y-e.y) < e.size + 5:
                    laser.alive = False
                    if e.take_damage(laser.damage):
                        score += e.score_value
                        kills += 1
                        spawn_explosion(particles, e.x, e.y, [RED,ORANGE,WHITE], 30)
                        shake.shake(6)
                        if random.random() < 0.25:
                            powerups.append(PowerUp(e.x, e.y))
                        achievements.check("kill", score=score, kills=kills, level=level,
                                           powerups=powerups_collected, weapon=ship.weapon_level)

        # Player laser vs boss
        if boss:
            for laser in ship.lasers[:]:
                if math.hypot(laser.x-boss.x, laser.y-boss.y) < boss.size + 10:
                    laser.alive = False
                    boss.take_damage(laser.damage)
                    spawn_explosion(particles, laser.x, laser.y, [ORANGE,WHITE], 8, 2)

        # Asteroid vs player
        if ship.invincible == 0:
            for a in asteroids:
                pts = a.projected()
                for px, py in pts:
                    if ship_rect.collidepoint(px, py):
                        ship.shield -= 15
                        level_damage_taken = True
                        flash_t = 28
                        ship.invincible = 80
                        shake.shake(10)
                        spawn_explosion(particles, ship.x, ship.y, [CYAN,WHITE,BLUE], 15, 2)
                        a.reset(speed_mult)
                        if ship.shield <= 0:
                            lives -= 1; ship.shield = 100
                            if lives <= 0: game_over = True
                        break

        # Enemy laser vs player
        if ship.invincible == 0:
            for e in enemies:
                for el in e.lasers[:]:
                    if ship_rect.collidepoint(el.x, el.y):
                        el.alive = False
                        ship.shield -= 12
                        level_damage_taken = True
                        flash_t = 20
                        ship.invincible = 60
                        shake.shake(8)
                        if ship.shield <= 0:
                            lives -= 1; ship.shield = 100
                            if lives <= 0: game_over = True

        # Boss laser vs player
        if boss and ship.invincible == 0:
            for bl in boss.lasers[:]:
                if ship_rect.collidepoint(bl.x, bl.y):
                    bl.alive = False
                    ship.shield -= 18
                    level_damage_taken = True
                    flash_t = 30
                    ship.invincible = 70
                    shake.shake(12)
                    if ship.shield <= 0:
                        lives -= 1; ship.shield = 100
                        if lives <= 0: game_over = True

        # Powerup collection
        for p in powerups[:]:
            if p.collide(ship.x, ship.y):
                apply_powerup(p.type)
                p.alive = False
                achievements.check("powerup", powerups=powerups_collected)
                spawn_explosion(particles, p.x, p.y, [p.color, WHITE], 15, 2)

        achievements.check("score_check", score=score, kills=kills, level=level,
                           powerups=powerups_collected, weapon=ship.weapon_level)

        # ── DRAW ──
        ox, oy = shake.offset
        draw_surf = pygame.Surface((SW, SH))
        draw_surf.fill(BG)
        nebula.draw(draw_surf)
        stars.draw(draw_surf)

        if flash_t > 0 and flash_t % 6 < 3:
            fl = pygame.Surface((SW, SH), pygame.SRCALPHA)
            fl.fill((255,0,0,50))
            draw_surf.blit(fl, (0,0))

        for a in asteroids: a.draw(draw_surf)
        for e in enemies:   e.draw(draw_surf)
        if boss:            boss.draw(draw_surf)
        for p in powerups:  p.draw(draw_surf)
        for p in particles: p.draw(draw_surf)
        if not game_over:   ship.draw(draw_surf)

        upgrade_cost = UPGRADE_COSTS[ship.weapon_level+1] if ship.weapon_level < 2 else 0
        draw_hud(draw_surf, font, bfont, score, lives, level, ship.shield,
                 ship.weapon_level, ship.triple_timer, ship.speed_timer, upgrade_cost)

        # ── TOUCH UI BUTTONS ──
        # Tap target indicator
        if ship.touch_target and ship.touch_active:
            tx, ty = ship.touch_target
            r = int(14 + 4 * math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.circle(draw_surf, CYAN, (int(tx), int(ty)), r, 2)
            pygame.draw.circle(draw_surf, CYAN, (int(tx), int(ty)), 4)

        # Pause button (top-right)
        pygame.draw.rect(draw_surf, DARK_PANEL, (SW-58, 8, 50, 48), border_radius=8)
        pygame.draw.rect(draw_surf, CYAN_DIM,   (SW-58, 8, 50, 48), 2, border_radius=8)
        draw_text_glow(draw_surf, "II", font, YELLOW, SW-33, 32)

        # Upgrade button (bottom-right) — only if upgradeable
        if ship.weapon_level < 2:
            can_upgrade = score >= upgrade_cost
            btn_col = GREEN if can_upgrade else GREY
            pygame.draw.rect(draw_surf, DARK_PANEL, (SW-178, SH-62, 168, 52), border_radius=10)
            pygame.draw.rect(draw_surf, btn_col,    (SW-178, SH-62, 168, 52), 2, border_radius=10)
            draw_text_glow(draw_surf, f"⚡ UPGRADE", font, btn_col, SW-95, SH-45)
            draw_text_glow(draw_surf, f"{upgrade_cost} pts", font,
                           GREEN if can_upgrade else RED, SW-95, SH-22)

        achievements.draw(draw_surf, font)

        if level_up_t > 0:
            draw_text_glow(draw_surf, f"⭐ LEVEL {level} !", tfont, YELLOW, SW//2, SH//2-40)

        if boss_announced > 0:
            pulse = abs(math.sin(boss_announced * 0.1))
            c = (int(255*pulse), 0, 0)
            draw_text_glow(draw_surf, "⚠ BOSS INCOMING ⚠", tfont, c, SW//2, SH//2-20)

        screen.blit(draw_surf, (ox, oy))
        pygame.display.flip()

    return "game_over", score, level, kills, powerups_collected, achievements

# ══════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════
def main():
    screen = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font  = pygame.font.SysFont("Courier", 18, bold=True)
    bfont = pygame.font.SysFont("Courier", 24, bold=True)
    tfont = pygame.font.SysFont("Courier", 54, bold=True)

    stars  = StarField(300)
    nebula = Nebula()

    while True:
        result = main_menu(screen, clock, stars, nebula, font, bfont, tfont)

        if result == "leaderboard":
            leaderboard_screen(screen, clock, font, bfont, tfont)
            continue

        if result == "play":
            outcome = game_loop(screen, clock, font, bfont, tfont)

            if outcome == "menu":
                continue

            if outcome[0] == "game_over":
                _, score, level, kills, powerups, achievements = outcome
                next_action = game_over_screen(
                    screen, clock, font, bfont, tfont,
                    score, level, kills, powerups, achievements)
                if next_action == "restart":
                    continue
                elif next_action == "menu":
                    continue

if __name__ == "__main__":
    main()