#!/usr/bin/env python3

import pygame
import random
import json
import os
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
SOUNDS_DIR = BASE_DIR / "sounds"
MUSIC_DIR = BASE_DIR / "music"
ICONS_DIR = BASE_DIR / "icons"
SETTINGS_FILE = BASE_DIR / "stratagem_hero_settings.json"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors (Helldivers-inspired palette)
BLACK = (10, 12, 18)
DARK_BG = (15, 20, 30)
PANEL_BG = (25, 32, 48)
ACCENT_YELLOW = (255, 200, 50)
ACCENT_ORANGE = (255, 140, 30)
ACCENT_RED = (220, 50, 50)
ACCENT_GREEN = (50, 200, 100)
ACCENT_BLUE = (60, 140, 220)
WHITE = (240, 240, 245)
GRAY = (140, 150, 170)
DARK_GRAY = (60, 70, 90)
LIGHT_GRAY = (180, 190, 210)

# Directions
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
DIR_MAP = {
    pygame.K_w: UP, pygame.K_UP: UP,
    pygame.K_s: DOWN, pygame.K_DOWN: DOWN,
    pygame.K_a: LEFT, pygame.K_LEFT: LEFT,
    pygame.K_d: RIGHT, pygame.K_RIGHT: RIGHT,
}
DIR_SYMBOLS = {UP: "↑", DOWN: "↓", LEFT: "←", RIGHT: "→"}
DIR_COLORS = {UP: ACCENT_YELLOW, DOWN: ACCENT_BLUE, LEFT: ACCENT_GREEN, RIGHT: ACCENT_ORANGE}

# ---------------------------------------------------------------------------
# Stratagem Database
# ---------------------------------------------------------------------------
STRATAGEMS = [
    # Mission / General
    {"name": "Reinforce", "code": [UP, DOWN, RIGHT, LEFT, UP], "category": "Mission", "color": (255, 220, 50)},
    {"name": "Resupply", "code": [DOWN, DOWN, UP, RIGHT], "category": "Mission", "color": (255, 220, 50)},
    {"name": "SOS Beacon", "code": [UP, DOWN, RIGHT, UP], "category": "Mission", "color": (255, 220, 50)},
    {"name": "Eagle Rearm", "code": [UP, UP, LEFT, UP, RIGHT], "category": "Mission", "color": (255, 220, 50)},
    {"name": "Hellbomb", "code": [DOWN, UP, LEFT, DOWN, UP, RIGHT, DOWN, UP], "category": "Mission", "color": (255, 220, 50)},

    # Orbital
    {"name": "Orbital Precision Strike", "code": [RIGHT, RIGHT, UP], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Gatling Barrage", "code": [RIGHT, DOWN, LEFT, UP, UP], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Airburst Strike", "code": [RIGHT, RIGHT, RIGHT], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital 120mm HE Barrage", "code": [RIGHT, RIGHT, DOWN, LEFT, RIGHT, DOWN], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital 380mm HE Barrage", "code": [RIGHT, DOWN, UP, UP, LEFT, DOWN, DOWN], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Walking Barrage", "code": [RIGHT, DOWN, RIGHT, DOWN, RIGHT, DOWN], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Laser", "code": [RIGHT, DOWN, UP, RIGHT, DOWN], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Railcannon Strike", "code": [RIGHT, UP, DOWN, DOWN, RIGHT], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Napalm Barrage", "code": [RIGHT, RIGHT, DOWN, LEFT, RIGHT, UP], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Gas Strike", "code": [RIGHT, RIGHT, DOWN, RIGHT], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital EMS Strike", "code": [RIGHT, RIGHT, LEFT, DOWN], "category": "Orbital", "color": (220, 60, 60)},
    {"name": "Orbital Smoke Strike", "code": [RIGHT, RIGHT, DOWN, UP], "category": "Orbital", "color": (220, 60, 60)},

    # Eagle
    {"name": "Eagle Strafing Run", "code": [UP, RIGHT, RIGHT], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle Airstrike", "code": [UP, RIGHT, DOWN, RIGHT], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle Cluster Bomb", "code": [UP, RIGHT, DOWN, DOWN, RIGHT], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle Napalm Airstrike", "code": [UP, RIGHT, DOWN, UP], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle Smoke Strike", "code": [UP, RIGHT, UP, DOWN], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle 110mm Rocket Pods", "code": [UP, RIGHT, UP, LEFT], "category": "Eagle", "color": (255, 140, 40)},
    {"name": "Eagle 500kg Bomb", "code": [UP, RIGHT, DOWN, DOWN, DOWN], "category": "Eagle", "color": (255, 140, 40)},

    # Support Weapons
    {"name": "MG-43 Machine Gun", "code": [DOWN, LEFT, DOWN, UP, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "APW-1 Anti-Materiel Rifle", "code": [DOWN, LEFT, RIGHT, UP, DOWN], "category": "Support", "color": (60, 140, 220)},
    {"name": "M-105 Stalwart", "code": [DOWN, LEFT, DOWN, UP, UP, LEFT], "category": "Support", "color": (60, 140, 220)},
    {"name": "EAT-17 Expendable Anti-Tank", "code": [DOWN, DOWN, LEFT, UP, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "GR-8 Recoilless Rifle", "code": [DOWN, LEFT, RIGHT, RIGHT, LEFT], "category": "Support", "color": (60, 140, 220)},
    {"name": "FLAM-40 Flamethrower", "code": [DOWN, LEFT, UP, DOWN, UP], "category": "Support", "color": (60, 140, 220)},
    {"name": "AC-8 Autocannon", "code": [DOWN, LEFT, DOWN, UP, UP, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "MG-206 Heavy Machine Gun", "code": [DOWN, LEFT, UP, DOWN, DOWN], "category": "Support", "color": (60, 140, 220)},
    {"name": "RS-422 Railgun", "code": [DOWN, RIGHT, DOWN, UP, LEFT, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "FAF-14 Spear", "code": [DOWN, DOWN, UP, DOWN, DOWN], "category": "Support", "color": (60, 140, 220)},
    {"name": "LAS-98 Laser Cannon", "code": [DOWN, LEFT, DOWN, UP, LEFT], "category": "Support", "color": (60, 140, 220)},
    {"name": "ARC-3 Arc Thrower", "code": [DOWN, RIGHT, DOWN, UP, LEFT, LEFT], "category": "Support", "color": (60, 140, 220)},
    {"name": "GL-21 Grenade Launcher", "code": [DOWN, LEFT, UP, LEFT, DOWN], "category": "Support", "color": (60, 140, 220)},
    {"name": "LAS-99 Quasar Cannon", "code": [DOWN, DOWN, UP, LEFT, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "RL-77 Airburst Rocket Launcher", "code": [DOWN, UP, UP, LEFT, RIGHT], "category": "Support", "color": (60, 140, 220)},
    {"name": "MLS-4X Commando", "code": [DOWN, LEFT, UP, DOWN, RIGHT], "category": "Support", "color": (60, 140, 220)},

    # Backpacks
    {"name": "B-1 Supply Pack", "code": [DOWN, LEFT, DOWN, UP, UP, DOWN], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "LIFT-850 Jump Pack", "code": [DOWN, UP, UP, DOWN, UP], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "SH-32 Shield Generator Pack", "code": [DOWN, UP, LEFT, RIGHT, LEFT, RIGHT], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "AX/LAS-5 Rover", "code": [DOWN, UP, LEFT, UP, RIGHT, RIGHT], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "AX/AR-23 Guard Dog", "code": [DOWN, UP, LEFT, UP, RIGHT, DOWN], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "SH-20 Ballistic Shield Backpack", "code": [DOWN, LEFT, DOWN, DOWN, UP, LEFT], "category": "Backpack", "color": (80, 180, 120)},
    {"name": "B-100 Portable Hellbomb", "code": [DOWN, RIGHT, UP, UP, UP], "category": "Backpack", "color": (80, 180, 120)},

    # Defensive / Sentries
    {"name": "A/MG-43 Machine Gun Sentry", "code": [DOWN, UP, RIGHT, RIGHT, UP], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/G-16 Gatling Sentry", "code": [DOWN, UP, RIGHT, LEFT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/AC-8 Autocannon Sentry", "code": [DOWN, UP, RIGHT, UP, LEFT, UP], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/MLS-4X Rocket Sentry", "code": [DOWN, UP, RIGHT, RIGHT, LEFT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/M-12 Mortar Sentry", "code": [DOWN, UP, RIGHT, RIGHT, DOWN], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/M-23 EMS Mortar Sentry", "code": [DOWN, UP, RIGHT, DOWN, RIGHT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "A/ARC-3 Tesla Tower", "code": [DOWN, UP, RIGHT, UP, LEFT, RIGHT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "FX-12 Shield Generator Relay", "code": [DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "MD-6 Anti-Personnel Minefield", "code": [DOWN, LEFT, UP, RIGHT], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "MD-I4 Incendiary Mines", "code": [DOWN, LEFT, LEFT, DOWN], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "MD-17 Anti-Tank Mines", "code": [DOWN, LEFT, UP, UP], "category": "Defensive", "color": (100, 200, 100)},
    {"name": "E/MG-101 HMG Emplacement", "code": [DOWN, UP, LEFT, RIGHT, RIGHT, LEFT], "category": "Defensive", "color": (100, 200, 100)},
]

DEFAULT_ENABLED = {s["name"]: True for s in STRATAGEMS}

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------
def draw_text(surface, text, font, color, x, y, center=False, shadow=False):
    if shadow:
        shadow_surf = font.render(text, True, (0, 0, 0))
        rect = shadow_surf.get_rect(center=(x + 2, y + 2) if center else (x + 2, y + 2))
        if not center:
            rect.topleft = (x + 2, y + 2)
        surface.blit(shadow_surf, rect)
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(x, y) if center else (x, y))
    if not center:
        rect.topleft = (x, y)
    surface.blit(text_surf, rect)
    return rect


def draw_rounded_rect(surface, color, rect, radius=12, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def draw_simple_arrow(surface, direction, x, y, size=40, color=WHITE, filled=False):
    """Plain arrow symbol (no button background)."""
    s = size // 2
    if direction == UP:
        points = [(x, y - s), (x - s * 0.7, y + s * 0.5), (x + s * 0.7, y + s * 0.5)]
    elif direction == DOWN:
        points = [(x, y + s), (x - s * 0.7, y - s * 0.5), (x + s * 0.7, y - s * 0.5)]
    elif direction == LEFT:
        points = [(x - s, y), (x + s * 0.5, y - s * 0.7), (x + s * 0.5, y + s * 0.7)]
    else:
        points = [(x + s, y), (x - s * 0.5, y - s * 0.7), (x - s * 0.5, y + s * 0.7)]
    if filled:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, 3)


def draw_colored_arrow_button(surface, direction, x, y, size=48, filled=False, highlight=False):
    """Original coloured button style."""
    color = DIR_COLORS[direction]
    if highlight:
        color = WHITE
    bg = ACCENT_GREEN if filled else PANEL_BG
    border = ACCENT_GREEN if filled else color
    rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
    draw_rounded_rect(surface, bg, rect, radius=8, border=3, border_color=border)
    cx, cy = x, y
    s = size // 3
    if direction == UP:
        points = [(cx, cy - s), (cx - s, cy + s // 2), (cx + s, cy + s // 2)]
    elif direction == DOWN:
        points = [(cx, cy + s), (cx - s, cy - s // 2), (cx + s, cy - s // 2)]
    elif direction == LEFT:
        points = [(cx - s, cy), (cx + s // 2, cy - s), (cx + s // 2, cy + s)]
    else:
        points = [(cx + s, cy), (cx - s // 2, cy - s), (cx - s // 2, cy + s)]
    pygame.draw.polygon(surface, color if not filled else WHITE, points)


def draw_stratagem_icon(surface, stratagem, x, y, size=80, icon_cache=None):
    """Draw icon from file if available, otherwise procedural shape."""
    name_key = stratagem["name"].replace(" ", "_").replace("/", "_")
    if icon_cache and name_key in icon_cache:
        img = icon_cache[name_key]
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
        return

    # Procedural fallback
    color = stratagem["color"]
    rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
    draw_rounded_rect(surface, PANEL_BG, rect, radius=10, border=3, border_color=color)
    cat = stratagem["category"]
    cx, cy = x, y
    s = size // 3
    if cat == "Orbital":
        pygame.draw.circle(surface, color, (cx, cy), s, 3)
        pygame.draw.line(surface, color, (cx - s - 4, cy), (cx + s + 4, cy), 2)
        pygame.draw.line(surface, color, (cx, cy - s - 4), (cx, cy + s + 4), 2)
    elif cat == "Eagle":
        points = [(cx, cy - s), (cx - s, cy + s // 2), (cx + s, cy + s // 2)]
        pygame.draw.polygon(surface, color, points, 3)
    elif cat == "Support":
        pygame.draw.rect(surface, color, (cx - s, cy - 4, s * 2, 8), border_radius=2)
        pygame.draw.circle(surface, color, (cx + s - 4, cy), 6, 2)
    elif cat == "Backpack":
        pygame.draw.rect(surface, color, (cx - s, cy - s, s * 2, s * 2), 3, border_radius=4)
        pygame.draw.line(surface, color, (cx, cy - s), (cx, cy + s), 2)
    elif cat == "Defensive":
        points = [(cx, cy - s), (cx + s, cy - s // 3), (cx + s // 2, cy + s),
                  (cx - s // 2, cy + s), (cx - s, cy - s // 3)]
        pygame.draw.polygon(surface, color, points, 3)
    else:
        pygame.draw.circle(surface, color, (cx, cy), s, 3)
        pygame.draw.circle(surface, color, (cx, cy), 4)


# ---------------------------------------------------------------------------
# Game States
# ---------------------------------------------------------------------------
class GameState:
    MENU = "menu"
    SETTINGS = "settings"
    SPEED = "speed"
    MEMORY = "memory"
    GAME_OVER = "game_over"


# ---------------------------------------------------------------------------
# Main Game
# ---------------------------------------------------------------------------
class StratagemHero:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.display.set_caption("Stratagem Hero – Helldivers 2 Code Trainer")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_title = pygame.font.SysFont("segoeui", 64, bold=True)
        self.font_large = pygame.font.SysFont("segoeui", 42, bold=True)
        self.font_med = pygame.font.SysFont("segoeui", 28)
        self.font_small = pygame.font.SysFont("segoeui", 22)
        self.font_tiny = pygame.font.SysFont("segoeui", 16)
        self.font_code = pygame.font.SysFont("consolas", 36, bold=True)

        # Load settings (includes gameplay options)
        self.settings = self.load_settings()
        self.enabled = self.settings.get("enabled", DEFAULT_ENABLED.copy())
        self.colored_arrows = self.settings.get("colored_arrows", True)
        self.max_time = float(self.settings.get("max_time", 15.0))
        self.max_lives = int(self.settings.get("max_lives", 5))
        self.time_bonus = float(self.settings.get("time_bonus", 3.5))
        self.music_volume = float(self.settings.get("music_volume", 0.35))
        self.sfx_volume = float(self.settings.get("sfx_volume", 0.6))

        # State
        self.state = GameState.MENU
        self.menu_selection = 0
        self.settings_page = 0  # 0 = stratagems, 1 = options
        self.settings_scroll = 0
        self.settings_selected = 0

        # Gameplay
        self.current_stratagem = None
        self.player_input = []
        self.score = 0
        self.combo = 0
        self.lives = self.max_lives
        self.timer = 0.0
        self.feedback = ""
        self.feedback_timer = 0.0
        self.game_over_reason = ""

        # Audio
        self.click_sound = None
        self.load_audio()
        self.icon_cache = self.load_icons()
        self.pulse = 0.0

    # ------------------------------------------------------------------
    # Audio & Icons
    # ------------------------------------------------------------------
    def load_audio(self):
        click_path = SOUNDS_DIR / "click.wav"
        if click_path.exists():
            try:
                self.click_sound = pygame.mixer.Sound(str(click_path))
                self.click_sound.set_volume(self.sfx_volume)
            except Exception:
                self.click_sound = None

        music_path = MUSIC_DIR / "bg_music.mp3"
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # loop forever
            except Exception as e:
                print("Could not load background music:", e)

    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

    def load_icons(self):
        cache = {}
        if not ICONS_DIR.exists():
            return cache
        for s in STRATAGEMS:
            key = s["name"].replace(" ", "_").replace("/", "_")
            for ext in (".png", ".jpg", ".jpeg"):
                p = ICONS_DIR / (key + ext)
                if p.exists():
                    try:
                        img = pygame.image.load(str(p)).convert_alpha()
                        img = pygame.transform.smoothscale(img, (96, 96))
                        cache[key] = img
                    except Exception:
                        pass
                    break
        return cache

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------
    def load_settings(self):
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                # Ensure all stratagems present
                enabled = DEFAULT_ENABLED.copy()
                enabled.update(data.get("enabled", {}))
                data["enabled"] = enabled
                return data
            except Exception:
                pass
        return {
            "enabled": DEFAULT_ENABLED.copy(),
            "colored_arrows": True,
            "max_time": 15.0,
            "max_lives": 5,
            "time_bonus": 3.5,
            "music_volume": 0.35,
            "sfx_volume": 0.6,
        }

    def save_settings(self):
        data = {
            "enabled": self.enabled,
            "colored_arrows": self.colored_arrows,
            "max_time": self.max_time,
            "max_lives": self.max_lives,
            "time_bonus": self.time_bonus,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def get_active_stratagems(self):
        return [s for s in STRATAGEMS if self.enabled.get(s["name"], True)]

    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------
    def start_speed_mode(self):
        active = self.get_active_stratagems()
        if not active:
            self.feedback = "No stratagems enabled!"
            self.feedback_timer = 2.0
            return
        self.state = GameState.SPEED
        self.score = 0
        self.combo = 0
        self.timer = self.max_time
        self.player_input = []
        self.feedback = ""
        self.next_stratagem()

    def start_memory_mode(self):
        active = self.get_active_stratagems()
        if not active:
            self.feedback = "No stratagems enabled!"
            self.feedback_timer = 2.0
            return
        self.state = GameState.MEMORY
        self.score = 0
        self.combo = 0
        self.lives = self.max_lives
        self.player_input = []
        self.feedback = ""
        self.next_stratagem()

    def next_stratagem(self):
        active = self.get_active_stratagems()
        if not active:
            self.end_game("No active stratagems")
            return
        candidates = [s for s in active if s != self.current_stratagem] or active
        self.current_stratagem = random.choice(candidates)
        self.player_input = []
        self.feedback = ""

    def process_input(self, direction):
        if self.state not in (GameState.SPEED, GameState.MEMORY):
            return
        if not self.current_stratagem:
            return

        self.play_click()
        expected = self.current_stratagem["code"]
        self.player_input.append(direction)

        idx = len(self.player_input) - 1
        if self.player_input[idx] != expected[idx]:
            self.player_input = []
            self.combo = 0
            self.feedback = "wrong"
            self.feedback_timer = 0.6
            if self.state == GameState.MEMORY:
                self.lives -= 1
                if self.lives <= 0:
                    self.end_game("Out of lives")
            return

        if len(self.player_input) == len(expected):
            self.score += 100 + self.combo * 25
            self.combo += 1
            self.feedback = "correct"
            self.feedback_timer = 0.5
            if self.state == GameState.SPEED:
                self.timer = min(self.timer + self.time_bonus, self.max_time)
            elif self.state == GameState.MEMORY:
                # Award a life back (capped at max_lives)
                if self.lives < self.max_lives:
                    self.lives += 1
            self.next_stratagem()

    def end_game(self, reason):
        self.game_over_reason = reason
        self.state = GameState.GAME_OVER

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state in (GameState.SPEED, GameState.MEMORY, GameState.GAME_OVER):
                        self.state = GameState.MENU
                    elif self.state == GameState.SETTINGS:
                        self.save_settings()
                        self.state = GameState.MENU
                    else:
                        self.running = False
                    return

                if event.key in DIR_MAP and self.state in (GameState.SPEED, GameState.MEMORY):
                    self.process_input(DIR_MAP[event.key])
                    return

                if self.state == GameState.MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_selection = (self.menu_selection - 1) % 4
                        self.play_click()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_selection = (self.menu_selection + 1) % 4
                        self.play_click()
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.play_click()
                        if self.menu_selection == 0:
                            self.start_speed_mode()
                        elif self.menu_selection == 1:
                            self.start_memory_mode()
                        elif self.menu_selection == 2:
                            self.state = GameState.SETTINGS
                            self.settings_page = 0
                            self.settings_selected = 0
                            self.settings_scroll = 0
                        elif self.menu_selection == 3:
                            self.running = False

                elif self.state == GameState.SETTINGS:
                    self.handle_settings_keys(event)

                elif self.state == GameState.GAME_OVER:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = GameState.MENU

    def handle_settings_keys(self, event):
        # Tab / Left-Right to switch pages
        if event.key in (pygame.K_TAB, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
            if event.key in (pygame.K_LEFT, pygame.K_a) or (event.key == pygame.K_TAB and pygame.key.get_mods() & pygame.KMOD_SHIFT):
                self.settings_page = 0
            else:
                self.settings_page = 1 - self.settings_page
            self.settings_selected = 0
            self.settings_scroll = 0
            self.play_click()
            return

        if self.settings_page == 0:
            # Stratagem list
            if event.key in (pygame.K_UP, pygame.K_w):
                self.settings_selected = max(0, self.settings_selected - 1)
                if self.settings_selected < self.settings_scroll:
                    self.settings_scroll = self.settings_selected
                self.play_click()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.settings_selected = min(len(STRATAGEMS) - 1, self.settings_selected + 1)
                if self.settings_selected >= self.settings_scroll + 12:
                    self.settings_scroll = self.settings_selected - 11
                self.play_click()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                name = STRATAGEMS[self.settings_selected]["name"]
                self.enabled[name] = not self.enabled.get(name, True)
                self.play_click()
            elif event.key == pygame.K_e:  # Enable all
                for s in STRATAGEMS:
                    self.enabled[s["name"]] = True
                self.play_click()
            elif event.key == pygame.K_q:  # Disable all
                for s in STRATAGEMS:
                    self.enabled[s["name"]] = False
                self.play_click()
        else:
            # Options page
            options = ["colored_arrows", "max_time", "max_lives", "time_bonus", "music_volume", "sfx_volume"]
            if event.key in (pygame.K_UP, pygame.K_w):
                self.settings_selected = (self.settings_selected - 1) % len(options)
                self.play_click()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.settings_selected = (self.settings_selected + 1) % len(options)
                self.play_click()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.adjust_option(options[self.settings_selected], -1)
                self.play_click()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.adjust_option(options[self.settings_selected], +1)
                self.play_click()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if options[self.settings_selected] == "colored_arrows":
                    self.colored_arrows = not self.colored_arrows
                    self.play_click()

    def adjust_option(self, key, direction):
        if key == "max_time":
            self.max_time = max(5.0, min(60.0, self.max_time + direction * 1.0))
        elif key == "max_lives":
            self.max_lives = max(1, min(10, self.max_lives + direction))
        elif key == "time_bonus":
            self.time_bonus = max(1.0, min(10.0, self.time_bonus + direction * 0.5))
        elif key == "music_volume":
            self.music_volume = max(0.0, min(1.0, self.music_volume + direction * 0.05))
            pygame.mixer.music.set_volume(self.music_volume)
        elif key == "sfx_volume":
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + direction * 0.05))
            if self.click_sound:
                self.click_sound.set_volume(self.sfx_volume)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt):
        self.pulse += dt * 3.0
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback = ""

        if self.state == GameState.SPEED:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                self.end_game("Time's up!")

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw_background(self):
        self.screen.fill(DARK_BG)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (20, 25, 35), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 25, 35), (0, y), (SCREEN_WIDTH, y), 1)

    def draw_menu(self):
        self.draw_background()
        draw_text(self.screen, "STRATAGEM HERO", self.font_title, ACCENT_YELLOW,
                  SCREEN_WIDTH // 2, 120, center=True, shadow=True)
        draw_text(self.screen, "Helldivers 2 Code Trainer", self.font_med, GRAY,
                  SCREEN_WIDTH // 2, 185, center=True)

        options = [
            ("SPEED MODE", f"Timer (max {self.max_time:.0f}s) – codes shown"),
            ("MEMORY MODE", f"{self.max_lives} lives – codes hidden, correct restores life"),
            ("SETTINGS", "Stratagems + options (arrows, time, lives…)"),
            ("QUIT", "Return to democracy"),
        ]
        for i, (title, desc) in enumerate(options):
            y = 280 + i * 90
            selected = i == self.menu_selection
            bg_color = PANEL_BG if not selected else (40, 55, 80)
            border = ACCENT_YELLOW if selected else DARK_GRAY
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y - 30, 600, 70)
            draw_rounded_rect(self.screen, bg_color, rect, radius=10, border=3, border_color=border)
            color = ACCENT_YELLOW if selected else WHITE
            draw_text(self.screen, title, self.font_med, color, SCREEN_WIDTH // 2, y - 8, center=True)
            draw_text(self.screen, desc, self.font_tiny, GRAY, SCREEN_WIDTH // 2, y + 20, center=True)

        active = len(self.get_active_stratagems())
        draw_text(self.screen, f"{active} / {len(STRATAGEMS)} stratagems active",
                  self.font_small, GRAY, SCREEN_WIDTH // 2, 240, center=True)
        draw_text(self.screen, "↑↓ Navigate   Enter Confirm   Esc Quit",
                  self.font_tiny, DARK_GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, center=True)

    def draw_settings(self):
        self.draw_background()
        draw_text(self.screen, "SETTINGS", self.font_large, ACCENT_YELLOW,
                  SCREEN_WIDTH // 2, 30, center=True, shadow=True)

        # Page tabs
        tab1_color = ACCENT_YELLOW if self.settings_page == 0 else GRAY
        tab2_color = ACCENT_YELLOW if self.settings_page == 1 else GRAY
        draw_text(self.screen, "[ Stratagems ]", self.font_small, tab1_color, SCREEN_WIDTH // 2 - 120, 80, center=True)
        draw_text(self.screen, "[ Options ]", self.font_small, tab2_color, SCREEN_WIDTH // 2 + 120, 80, center=True)
        draw_text(self.screen, "Tab / ←→ switch page   Esc save & back", self.font_tiny, GRAY,
                  SCREEN_WIDTH // 2, 105, center=True)

        if self.settings_page == 0:
            self.draw_settings_stratagems()
        else:
            self.draw_settings_options()

    def draw_settings_stratagems(self):
        draw_text(self.screen, "Enter = Toggle   E = Enable All   Q = Disable All",
                  self.font_tiny, GRAY, SCREEN_WIDTH // 2, 125, center=True)
        visible = 12
        start = self.settings_scroll
        end = min(start + visible, len(STRATAGEMS))
        for i in range(start, end):
            s = STRATAGEMS[i]
            idx = i - start
            y = 150 + idx * 42
            selected = i == self.settings_selected
            enabled = self.enabled.get(s["name"], True)
            bg = (40, 55, 80) if selected else PANEL_BG
            rect = pygame.Rect(60, y, SCREEN_WIDTH - 120, 38)
            draw_rounded_rect(self.screen, bg, rect, radius=6)
            toggle_color = ACCENT_GREEN if enabled else ACCENT_RED
            pygame.draw.circle(self.screen, toggle_color, (95, y + 19), 9)
            draw_text(self.screen, "ON" if enabled else "OFF", self.font_tiny, toggle_color, 115, y + 10)
            draw_text(self.screen, s["name"], self.font_small, WHITE if selected else LIGHT_GRAY, 170, y + 8)
            draw_text(self.screen, s["category"], self.font_tiny, s["color"], 580, y + 12)
            code_str = " ".join(DIR_SYMBOLS[d] for d in s["code"])
            draw_text(self.screen, code_str, self.font_tiny, GRAY, 780, y + 12)
        if len(STRATAGEMS) > visible:
            draw_text(self.screen, f"{start + 1}-{end} of {len(STRATAGEMS)}",
                      self.font_tiny, GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25, center=True)

    def draw_settings_options(self):
        options = [
            ("Colored Arrow Buttons", "colored_arrows", "ON" if self.colored_arrows else "OFF (simple arrows)"),
            ("Max Timer (Speed Mode)", "max_time", f"{self.max_time:.0f} seconds"),
            ("Max Lives (Memory Mode)", "max_lives", f"{self.max_lives}"),
            ("Time Bonus per correct", "time_bonus", f"+{self.time_bonus:.1f}s"),
            ("Music Volume", "music_volume", f"{int(self.music_volume * 100)}%"),
            ("SFX Volume", "sfx_volume", f"{int(self.sfx_volume * 100)}%"),
        ]
        draw_text(self.screen, "↑↓ select   ←→ adjust   Enter toggle (arrows style)",
                  self.font_tiny, GRAY, SCREEN_WIDTH // 2, 130, center=True)

        for i, (label, key, value) in enumerate(options):
            y = 180 + i * 70
            selected = i == self.settings_selected
            bg = (40, 55, 80) if selected else PANEL_BG
            border = ACCENT_YELLOW if selected else DARK_GRAY
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 320, y, 640, 55)
            draw_rounded_rect(self.screen, bg, rect, radius=8, border=2, border_color=border)
            draw_text(self.screen, label, self.font_med, WHITE if selected else LIGHT_GRAY,
                      SCREEN_WIDTH // 2 - 280, y + 12)
            draw_text(self.screen, value, self.font_med, ACCENT_YELLOW if selected else GRAY,
                      SCREEN_WIDTH // 2 + 200, y + 12)

    def draw_gameplay(self, show_code=True):
        self.draw_background()
        if not self.current_stratagem:
            return
        s = self.current_stratagem

        # Header
        pygame.draw.rect(self.screen, PANEL_BG, (0, 0, SCREEN_WIDTH, 70))
        mode_name = "SPEED MODE" if self.state == GameState.SPEED else "MEMORY MODE"
        draw_text(self.screen, mode_name, self.font_med, ACCENT_YELLOW, 30, 18)
        score_surf = self.font_med.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (SCREEN_WIDTH - score_surf.get_width() - 30, 18))

        if self.state == GameState.SPEED:
            bar_w = 400
            bar_x = SCREEN_WIDTH // 2 - bar_w // 2
            ratio = max(0.0, self.timer / self.max_time)
            bar_color = ACCENT_GREEN if self.timer > self.max_time * 0.5 else (
                ACCENT_ORANGE if self.timer > self.max_time * 0.25 else ACCENT_RED)
            pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, 25, bar_w, 20), border_radius=6)
            pygame.draw.rect(self.screen, bar_color, (bar_x, 25, int(bar_w * ratio), 20), border_radius=6)
            draw_text(self.screen, f"{self.timer:.1f}s / {self.max_time:.0f}s", self.font_small, WHITE,
                      SCREEN_WIDTH // 2, 50, center=True)
        else:
            lives_text = "♥ " * self.lives + "♡ " * (self.max_lives - self.lives)
            draw_text(self.screen, lives_text.strip(), self.font_med, ACCENT_RED,
                      SCREEN_WIDTH // 2, 20, center=True)

        if self.combo > 1:
            draw_text(self.screen, f"COMBO x{self.combo}", self.font_small, ACCENT_ORANGE,
                      SCREEN_WIDTH // 2, 95, center=True)

        # Icon + name
        draw_stratagem_icon(self.screen, s, SCREEN_WIDTH // 2, 200, size=100, icon_cache=self.icon_cache)
        draw_text(self.screen, s["name"], self.font_large, WHITE, SCREEN_WIDTH // 2, 280, center=True, shadow=True)
        draw_text(self.screen, s["category"], self.font_small, s["color"], SCREEN_WIDTH // 2, 325, center=True)

        # Code display
        code = s["code"]
        total = len(code)
        spacing = 70
        start_x = SCREEN_WIDTH // 2 - (total - 1) * spacing // 2

        if show_code:
            for i, d in enumerate(code):
                filled = i < len(self.player_input)
                highlight = i == len(self.player_input)
                if self.colored_arrows:
                    draw_colored_arrow_button(self.screen, d, start_x + i * spacing, 420, size=56,
                                              filled=filled, highlight=highlight)
                else:
                    col = ACCENT_GREEN if filled else (WHITE if highlight else GRAY)
                    draw_simple_arrow(self.screen, d, start_x + i * spacing, 420, size=44, color=col, filled=filled)
        else:
            for i in range(total):
                filled = i < len(self.player_input)
                if filled:
                    if self.colored_arrows:
                        draw_colored_arrow_button(self.screen, self.player_input[i],
                                                  start_x + i * spacing, 420, size=56, filled=True)
                    else:
                        draw_simple_arrow(self.screen, self.player_input[i],
                                          start_x + i * spacing, 420, size=44, color=ACCENT_GREEN, filled=True)
                else:
                    if self.colored_arrows:
                        rect = pygame.Rect(start_x + i * spacing - 28, 420 - 28, 56, 56)
                        draw_rounded_rect(self.screen, PANEL_BG, rect, radius=8, border=2, border_color=DARK_GRAY)
                        draw_text(self.screen, "?", self.font_med, DARK_GRAY, start_x + i * spacing, 420, center=True)
                    else:
                        draw_text(self.screen, "?", self.font_large, DARK_GRAY, start_x + i * spacing, 420, center=True)

        if self.feedback == "correct":
            draw_text(self.screen, "✓ DEMOCRACY SECURED", self.font_med, ACCENT_GREEN,
                      SCREEN_WIDTH // 2, 520, center=True)
        elif self.feedback == "wrong":
            draw_text(self.screen, "✗ WRONG INPUT", self.font_med, ACCENT_RED,
                      SCREEN_WIDTH // 2, 520, center=True)

        draw_text(self.screen, "WASD / Arrow Keys   Esc = Menu",
                  self.font_tiny, GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, center=True)

    def draw_game_over(self):
        self.draw_background()
        draw_text(self.screen, "MISSION FAILED", self.font_title, ACCENT_RED,
                  SCREEN_WIDTH // 2, 200, center=True, shadow=True)
        draw_text(self.screen, self.game_over_reason, self.font_med, GRAY,
                  SCREEN_WIDTH // 2, 280, center=True)
        draw_text(self.screen, f"Final Score: {self.score}", self.font_large, ACCENT_YELLOW,
                  SCREEN_WIDTH // 2, 360, center=True)
        if self.combo > 1:
            draw_text(self.screen, f"Best Combo: x{self.combo}", self.font_med, ACCENT_ORANGE,
                      SCREEN_WIDTH // 2, 420, center=True)
        draw_text(self.screen, "Press Enter to return to menu", self.font_small, WHITE,
                  SCREEN_WIDTH // 2, 520, center=True)

    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state == GameState.SPEED:
            self.draw_gameplay(show_code=True)
        elif self.state == GameState.MEMORY:
            self.draw_gameplay(show_code=False)
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        self.save_settings()
        pygame.quit()


if __name__ == "__main__":
    game = StratagemHero()
    game.run()
