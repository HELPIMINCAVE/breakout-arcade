import pygame, random, math, sys, json, os

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game Constants
WIDTH, HEIGHT = 950, 800
FPS = 60

# Colors (Neon Arcade Palette)
BLACK = (10, 10, 15)
WHITE = (245, 245, 245)
RED = (235, 87, 87)
ORANGE = (242, 153, 74)
YELLOW = (242, 201, 76)
GREEN = (39, 174, 96)
CYAN = (86, 204, 242)
PURPLE = (155, 89, 182)
DARK_GRAY = (40, 40, 50)
LIGHT_BLUE = (52, 152, 219)
PINK = (255, 105, 180)
SAVE_FILE = "save_data.json"

# 25 Permanent Gem Upgrades Definition
GEM_UPGRADES_DEF = [
    {"id": "gem_life", "name": "Extra Starting Life", "max": 5, "base_cost": 10,
     "desc": "Start runs with +1 life per tier"},
    {"id": "gem_cash", "name": "Stash of Cash", "max": 5, "base_cost": 15,
     "desc": "Start runs with +$50 cash per tier"},
    {"id": "gem_gem_mult", "name": "Gem Hoarder", "max": 5, "base_cost": 25, "desc": "+15% more gems earned per tier"},
    {"id": "gem_paddle", "name": "Wide Grip", "max": 5, "base_cost": 20, "desc": "Permanent +15 base paddle width"},
    {"id": "gem_damage", "name": "Heavy Impact", "max": 5, "base_cost": 30, "desc": "Permanent +1 base ball damage"},
    {"id": "gem_drop", "name": "Lucky Drops", "max": 5, "base_cost": 20, "desc": "+5% power-up drop chance per tier"},
    {"id": "gem_score", "name": "High Scorer", "max": 5, "base_cost": 15, "desc": "+10% score multiplier per tier"},
    {"id": "gem_laser_start", "name": "Laser Ready", "max": 1, "base_cost": 50,
     "desc": "Start every run with Laser Enabled"},
    {"id": "gem_shield", "name": "Shield Barrier", "max": 3, "base_cost": 35,
     "desc": "Start runs with 1-3 bottom shield charges"},
    {"id": "gem_magnet", "name": "Paddle Magnet", "max": 1, "base_cost": 40,
     "desc": "Start runs with Magnet Paddle active"},
    {"id": "gem_reroll_disc", "name": "Bargain Hunter", "max": 5, "base_cost": 20,
     "desc": "Shop rerolls cost 15% less per tier"},
    {"id": "gem_hp_buff", "name": "Armor Breaker", "max": 5, "base_cost": 25,
     "desc": "Bricks scale 5% less health per level"},
    {"id": "gem_crit", "name": "Critical Strike", "max": 5, "base_cost": 30,
     "desc": "+4% chance for ball hits to deal double damage"},
    {"id": "gem_interest", "name": "Compound Interest", "max": 5, "base_cost": 40,
     "desc": "Earn 3% cash interest between levels"},
    {"id": "gem_multiball_start", "name": "Twin Start", "max": 2, "base_cost": 50,
     "desc": "Start runs with 1-2 extra multiballs"},
    {"id": "gem_slow_start", "name": "Zen Focus", "max": 3, "base_cost": 25,
     "desc": "Initial ball speed slightly reduced for control"},
    {"id": "gem_particles", "name": "Supernova FX", "max": 1, "base_cost": 30,
     "desc": "Extra vibrant destruction particle bursts"},
    {"id": "gem_boss_bounty", "name": "Reinforced Bounty", "max": 5, "base_cost": 35,
     "desc": "+20% cash when destroying tough bricks"},
    {"id": "gem_shop_slot", "name": "Supermarket", "max": 1, "base_cost": 75,
     "desc": "Show 4 shop upgrade options instead of 3"},
    {"id": "gem_laser_speed", "name": "Hyper Lasers", "max": 5, "base_cost": 20,
     "desc": "Lasers travel 20% faster per tier"},
    {"id": "gem_paddle_spd", "name": "Reflex Speed", "max": 5, "base_cost": 25,
     "desc": "Permanent +0.5 paddle movement speed"},
    {"id": "gem_revive", "name": "Second Wind", "max": 3, "base_cost": 60,
     "desc": "15% chance per tier to revive with 1 life on death"},
    {"id": "gem_gem_drop", "name": "Gemstone Bricks", "max": 5, "base_cost": 45,
     "desc": "Rare chance for bricks to drop bonus Gems"},
    {"id": "gem_upgrade_disc", "name": "Wholesale", "max": 5, "base_cost": 40,
     "desc": "Shop upgrades cost 5% less per tier"},
    {"id": "gem_max_lives", "name": "Iron Will", "max": 5, "base_cost": 50, "desc": "+1 maximum life capacity per tier"}
]

ACHIEVEMENT_DEFINITIONS = [
    ("default_settler", "Default Settler", "Start a game without changing default settings"),
    ("rich_gamer", "High Roller", "Accumulate at least $500 cash in a single run"),
    ("first_steps", "First Steps", "Clear Level 1"),
    ("laser_master", "Laser Master", "Upgrade Laser System to Tier 5"),
    ("multiball_mayhem", "Multiball Mayhem", "Have 5 or more balls active on screen"),
    ("shielded", "Shielded", "Activate or start with a Shield Wall charge"),
    ("big_spender", "Big Spender", "Spend $300 or more in shop purchases"),
    ("gem_collector", "Gem Collector", "Possess 50 or more Gems"),
    ("hardcore_survivor", "Hardcore Survivor", "Complete a level on Hard difficulty"),
    ("magnetized", "Magnetized", "Catch a ball with the Magnet Paddle"),
    ("brick_breaker", "Brick Breaker", "Reach 1,000 points in a single run"),
    ("level_5_vet", "Level 5 Veteran", "Reach Level 5 in a run")
]

def load_save_data():
    default_achievements = {k: False for k, _, _ in ACHIEVEMENT_DEFINITIONS}
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                if "gems" not in data: data["gems"] = 0
                if "gem_upgrades" not in data: data["gem_upgrades"] = {}
                if "difficulty" not in data: data["difficulty"] = "normal"
                if "achievements" not in data:
                    data["achievements"] = default_achievements
                else:
                    for k in default_achievements:
                        if k not in data["achievements"]:
                            data["achievements"][k] = False
                return data
        except:
            pass
    return {
        "gems": 0,
        "gem_upgrades": {},
        "difficulty": "normal",
        "active_run": None,
        "achievements": default_achievements
    }

def save_game_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

class Button:
    def __init__(self, x, y, w, h, text, color, text_color=WHITE, font_size=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
    
    def draw(self, surface, hovered=False):
        col = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255),
               min(self.color[2] + 40, 255)) if hovered else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        txt = self.font.render(self.text, True, self.text_color)
        surface.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Paddle:
    def __init__(self, speed, width):
        self.width = width
        self.rect = pygame.Rect((WIDTH - self.width) // 2, HEIGHT - 55, self.width, 14)
        self.speed = speed
    
    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
    
    def draw(self, surface):
        pygame.draw.rect(surface, CYAN, self.rect, border_radius=7)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=7)

class Ball:
    def __init__(self, x, y, dx, dy, damage=1, is_multiball=False):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(dx)
        self.dy = float(dy)
        self.radius = 9
        self.damage = damage
        self.is_multiball = is_multiball
        self.respawn_timer = 0
        self.stuck_to_paddle = False
    
    def update(self):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            return
        if self.stuck_to_paddle:
            return
        self.x += self.dx
        self.y += self.dy
        
        if self.x - self.radius <= 0:
            self.x = self.radius;
            self.dx = -self.dx
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius;
            self.dx = -self.dx
        if self.y - self.radius <= 0:
            self.y = self.radius;
            self.dy = -self.dy
    
    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
    
    def draw(self, surface):
        if self.respawn_timer > 0: return
        color = PURPLE if self.is_multiball else WHITE
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), self.radius - 3)

class Brick:
    def __init__(self, x, y, hp, brick_type):
        self.rect = pygame.Rect(x, y, 74, 22)
        self.max_hp = hp
        self.hp = hp
        self.type = brick_type
        
        if self.type == 'unbreakable':
            self.color = DARK_GRAY
        elif self.hp >= 3:
            self.color = PURPLE
        elif self.hp == 2:
            self.color = ORANGE
        else:
            self.color = RED
    
    def draw(self, surface):
        color = self.color
        if self.type == 'reinforced' and self.hp == 1: color = YELLOW
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=4)
        if self.type != 'unbreakable' and self.max_hp > 1:
            font = pygame.font.SysFont("Arial", 14, bold=True)
            txt = font.render(str(self.hp), True, WHITE)
            surface.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))

class Particle:
    def __init__(self, x, y, color):
        self.x = x;
        self.y = y;
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.dx;
        self.y += self.dy;
        self.life -= 1
    
    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

class BreakoutGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ultimate Arcade Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        self.save_data = load_save_data()
        self.state = "MENU"
        self.steam_popups = []
        self.notifications = []
        self.gem_shop_page = 0
        self.shop_spent_in_visit = 0
        
        self.init_ui_buttons()
    
    def init_ui_buttons(self):
        self.btn_play = Button(WIDTH // 2 - 120, HEIGHT // 2 - 80, 240, 45, "PLAY GAME", GREEN)
        self.btn_gems = Button(WIDTH // 2 - 120, HEIGHT // 2 - 25, 240, 45, "GEM UPGRADES", PINK)
        self.btn_settings = Button(WIDTH // 2 - 120, HEIGHT // 2 + 30, 240, 45, "SETTINGS", LIGHT_BLUE)
        self.btn_achievements = Button(WIDTH // 2 - 120, HEIGHT // 2 + 85, 240, 45, "ACHIEVEMENTS", PURPLE)
        self.btn_quit = Button(WIDTH // 2 - 120, HEIGHT // 2 + 140, 240, 45, "QUIT", RED)
        
        self.btn_back = Button(WIDTH // 2 - 100, HEIGHT - 90, 200, 45, "BACK TO MENU", DARK_GRAY)
        self.btn_diff_easy = Button(WIDTH // 2 - 220, 300, 130, 40, "EASY", GREEN)
        self.btn_diff_normal = Button(WIDTH // 2 - 65, 300, 130, 40, "NORMAL", LIGHT_BLUE)
        self.btn_diff_hard = Button(WIDTH // 2 + 90, 300, 130, 40, "HARD", RED)
        
        self.btn_resume = Button(WIDTH // 2 - 120, HEIGHT // 2 - 70, 240, 45, "RESUME", GREEN)
        self.btn_save_quit = Button(WIDTH // 2 - 120, HEIGHT // 2 - 10, 240, 45, "SAVE & QUIT", ORANGE)
        self.btn_end_run = Button(WIDTH // 2 - 120, HEIGHT // 2 + 50, 240, 45, "END RUN", RED)
        
        self.btn_cont_yes = Button(WIDTH // 2 - 160, HEIGHT // 2 + 20, 150, 45, "CONTINUE RUN", GREEN)
        self.btn_cont_no = Button(WIDTH // 2 + 10, HEIGHT // 2 + 20, 150, 45, "NEW RUN", RED)
        
        self.btn_gem_prev = Button(WIDTH // 2 - 150, HEIGHT - 120, 130, 40, "< PREV", DARK_GRAY)
        self.btn_gem_next = Button(WIDTH // 2 + 20, HEIGHT - 120, 130, 40, "NEXT >", DARK_GRAY)
        self.btn_gem_back = Button(WIDTH // 2 - 100, HEIGHT - 70, 200, 40, "BACK TO MENU", DARK_GRAY)
        
        self.btn_ach_back = Button(WIDTH // 2 - 100, HEIGHT - 90, 200, 45, "BACK TO MENU", DARK_GRAY)
        
        self.shop_buttons = []
        self.gem_shop_buttons = []
        self.reroll_cost = 25
        self.btn_reroll = None
        self.btn_next_level = None
    
    def get_gem_level(self, up_id):
        return self.save_data["gem_upgrades"].get(up_id, 0)
    
    def start_new_run(self):
        gem_life = self.get_gem_level("gem_life")
        gem_cash = self.get_gem_level("gem_cash")
        gem_paddle = self.get_gem_level("gem_paddle")
        gem_laser = self.get_gem_level("gem_laser_start")
        gem_shield = self.get_gem_level("gem_shield")
        gem_magnet = self.get_gem_level("gem_magnet")
        gem_multiball = self.get_gem_level("gem_multiball_start")
        
        self.score = 0
        self.money = gem_cash * 50
        self.level = 1
        self.lives = 3 + gem_life
        self.score_multiplier = 1.0 + (self.get_gem_level("gem_score") * 0.1)
        self.laser_enabled = (gem_laser > 0)
        self.laser_cooldown_timer = 0
        self.shield_charges = gem_shield
        self.magnet_active = (gem_magnet > 0)
        
        if self.shield_charges > 0: self.unlock_achievement("shielded")
        
        self.run_upgrades = {"damage_tier": 0, "paddle_tier": 0, "life_tier": 0, "coin_tier": 0, "laser_tier": 0}
        
        paddle_w = 100 + (gem_paddle * 15)
        self.paddle = Paddle(6.0 + (self.get_gem_level("gem_paddle_spd") * 0.5), paddle_w)
        self.balls = []
        self.bricks = []
        self.powerups = []
        self.lasers = []
        self.particles = []
        self.notifications = []
        
        self.spawn_ball()
        for _ in range(gem_multiball):
            self.balls.append(
                Ball(self.paddle.rect.centerx, self.paddle.rect.top - 12, random.choice([-5, 5]), -5, damage=1,
                     is_multiball=True))
        
        self.create_level()
        self.state = "PLAYING"
    
    def save_current_run(self):
        run_data = {
            "score": self.score,
            "money": self.money,
            "level": self.level,
            "lives": self.lives,
            "score_multiplier": self.score_multiplier,
            "laser_enabled": self.laser_enabled,
            "shield_charges": self.shield_charges,
            "magnet_active": self.magnet_active,
            "paddle_x": self.paddle.rect.x,
            "paddle_width": self.paddle.width,
            "run_upgrades": self.run_upgrades,
            "balls": [{"x": b.x, "y": b.y, "dx": b.dx, "dy": b.dy, "damage": b.damage, "is_multiball": b.is_multiball}
                      for b in self.balls],
            "bricks": [{"x": b.rect.x, "y": b.rect.y, "hp": b.hp, "max_hp": b.max_hp, "type": b.type} for b in
                       self.bricks]
        }
        self.save_data["active_run"] = run_data
        save_game_data(self.save_data)
    
    def load_saved_run(self):
        run = self.save_data["active_run"]
        if not run: return
        self.score = run["score"]
        self.money = run["money"]
        self.level = run["level"]
        self.lives = run["lives"]
        self.score_multiplier = run["score_multiplier"]
        self.laser_enabled = run["laser_enabled"]
        self.shield_charges = run["shield_charges"]
        self.magnet_active = run["magnet_active"]
        self.run_upgrades = run["run_upgrades"]
        
        self.paddle = Paddle(6.0, run["paddle_width"])
        self.paddle.rect.x = run["paddle_x"]
        
        self.balls = [Ball(b["x"], b["y"], b["dx"], b["dy"], damage=b["damage"], is_multiball=b["is_multiball"]) for b
                      in run["balls"]]
        self.bricks = [Brick(b["x"], b["y"], b["hp"], b["type"]) for b in run["bricks"]]
        for b in self.bricks: b.max_hp = b["max_hp"]
        
        self.powerups = []
        self.lasers = []
        self.particles = []
        self.notifications = []
        self.state = "PLAYING"
    
    def end_run_and_calc_gems(self, victory=False):
        diff = self.save_data["difficulty"]
        diff_mult = {"easy": 0.5, "normal": 1.0, "hard": 2.0}[diff]
        gem_mult = 1.0 + (self.get_gem_level("gem_gem_mult") * 0.15)
        
        gems_earned = int((self.money / max(1, self.level)) * diff_mult * gem_mult)
        if victory: gems_earned *= 2
        
        self.save_data["gems"] += gems_earned
        self.save_data["active_run"] = None
        save_game_data(self.save_data)
        
        if self.save_data["gems"] >= 50: self.unlock_achievement("gem_collector")
        self.add_steam_popup("RUN ENDED", f"Earned +{gems_earned} Gems!")
        self.state = "GAMEOVER"
    
    def add_steam_popup(self, title, text):
        self.steam_popups.append({"title": title, "text": text, "timer": 180, "x": -320, "target_x": 20, "y": 70})
    
    def unlock_achievement(self, key):
        if not self.save_data["achievements"].get(key, False):
            self.save_data["achievements"][key] = True
            save_game_data(self.save_data)
            self.add_steam_popup("ACHIEVEMENT UNLOCKED", key.replace('_', ' ').title())
    
    def create_level(self):
        self.bricks.clear()
        cols = 10
        offset_left = (WIDTH - (cols * (74 + 6) - 6)) // 2
        pattern = self.level % 5
        
        hp_reduction = self.get_gem_level("gem_hp_buff") * 0.05
        diff = self.save_data["difficulty"]
        hp_scale_rate = {"easy": 0.01, "normal": 0.03, "hard": 0.05}[diff]
        hp_mult = max(0.5, 1.0 + (self.level * hp_scale_rate) - hp_reduction)
        
        for row in range(6):
            for col in range(cols):
                x = offset_left + col * (74 + 6)
                y = 80 + row * (22 + 6)
                
                skip = False
                if pattern == 1 and (col + row) % 2 == 0:
                    skip = True
                elif pattern == 2 and (col < 2 or col > 7):
                    skip = True
                elif pattern == 3 and abs(col - 4.5) > (5 - row):
                    skip = True
                elif pattern == 4 and (row in [1, 4] and col not in [2, 7]):
                    skip = True
                
                if skip: continue
                
                rand = random.random()
                if self.level >= 3 and row == 0 and rand < 0.25:
                    b_type = 'unbreakable';
                    hp = 999
                elif rand < 0.3:
                    b_type = 'reinforced';
                    hp = max(1, int(2 * hp_mult))
                else:
                    b_type = 'normal';
                    hp = max(1, int(1 * hp_mult))
                
                self.bricks.append(Brick(x, y, hp, b_type))
    
    def spawn_ball(self):
        angle = random.uniform(math.pi / 4, 3 * math.pi / 4)
        speed = 5.0 if self.get_gem_level("gem_slow_start") == 0 else 4.2
        dx = speed * math.cos(angle)
        dy = -speed * math.sin(angle)
        damage = 1 + self.run_upgrades["damage_tier"] + self.get_gem_level("gem_damage")
        self.balls.append(Ball(self.paddle.rect.centerx, self.paddle.rect.top - 12, dx, dy, damage=damage))
    
    def add_notification(self, text, color=YELLOW):
        self.notifications.append({"text": text, "timer": 90, "color": color, "y": HEIGHT - 100})
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
    
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            
            if self.state == "MENU":
                if self.btn_play.is_clicked(event):
                    if self.save_data["active_run"]:
                        self.state = "SAVE_CONFIRM"
                    else:
                        self.start_new_run()
                elif self.btn_gems.is_clicked(event):
                    self.gem_shop_page = 0;
                    self.setup_gem_shop_buttons();
                    self.state = "GEM_SHOP"
                elif self.btn_settings.is_clicked(event):
                    self.state = "SETTINGS"
                elif self.btn_achievements.is_clicked(event):
                    self.state = "ACHIEVEMENTS"
                elif self.btn_quit.is_clicked(event):
                    pygame.quit(); sys.exit()
            
            elif self.state == "SAVE_CONFIRM":
                if self.btn_cont_yes.is_clicked(event):
                    self.load_saved_run()
                elif self.btn_cont_no.is_clicked(event):
                    self.start_new_run()
            
            elif self.state == "SETTINGS":
                if self.btn_back.is_clicked(event):
                    self.state = "MENU"
                elif self.btn_diff_easy.is_clicked(event):
                    self.save_data["difficulty"] = "easy";
                    save_game_data(self.save_data)
                elif self.btn_diff_normal.is_clicked(event):
                    self.save_data["difficulty"] = "normal";
                    save_game_data(self.save_data)
                elif self.btn_diff_hard.is_clicked(event):
                    self.save_data["difficulty"] = "hard";
                    save_game_data(self.save_data)
            
            elif self.state == "ACHIEVEMENTS":
                if self.btn_ach_back.is_clicked(event): self.state = "MENU"
            
            elif self.state == "GEM_SHOP":
                if self.btn_gem_back.is_clicked(event):
                    self.state = "MENU"
                elif self.btn_gem_prev.is_clicked(event) and self.gem_shop_page > 0:
                    self.gem_shop_page -= 1;
                    self.setup_gem_shop_buttons()
                elif self.btn_gem_next.is_clicked(event) and self.gem_shop_page < 4:
                    self.gem_shop_page += 1;
                    self.setup_gem_shop_buttons()
                else:
                    for item in self.gem_shop_buttons:
                        if item["button"].is_clicked(event):
                            up_def = item["def"]
                            tier = self.get_gem_level(up_def["id"])
                            cost = int(up_def["base_cost"] * (1.5 ** tier))
                            if tier < up_def["max"] and self.save_data["gems"] >= cost:
                                self.save_data["gems"] -= cost
                                self.save_data["gem_upgrades"][up_def["id"]] = tier + 1
                                save_game_data(self.save_data)
                                if self.save_data["gems"] >= 50: self.unlock_achievement("gem_collector")
                                self.setup_gem_shop_buttons()
            
            elif self.state == "PAUSED":
                if self.btn_resume.is_clicked(event):
                    self.state = "PLAYING"
                elif self.btn_save_quit.is_clicked(event):
                    self.save_current_run();
                    self.state = "MENU"
                elif self.btn_end_run.is_clicked(event):
                    self.end_run_and_calc_gems()
            
            elif self.state == "SHOP":
                for item in self.shop_buttons:
                    if item["button"].is_clicked(event):
                        upgrade = item["upgrade"]
                        disc = 1.0 - (self.get_gem_level("gem_upgrade_disc") * 0.05)
                        actual_cost = int(upgrade["cost"] * disc)
                        if self.money >= actual_cost and upgrade["tier"] < upgrade["max_tier"]:
                            self.money -= actual_cost
                            self.shop_spent_in_visit += actual_cost
                            self.run_upgrades[upgrade["key"]] += 1
                            
                            if self.run_upgrades["laser_tier"] >= 5: self.unlock_achievement("laser_master")
                            if self.shop_spent_in_visit >= 300: self.unlock_achievement("big_spender")
                            if self.money >= 500: self.unlock_achievement("rich_gamer")
                            
                            upgrade["tier"] = self.run_upgrades[upgrade["key"]]
                            upgrade["cost"] = int(upgrade["base_cost"] * (2.0 ** upgrade["tier"]))
                            item["button"].text = f"{upgrade['name']} (Tier {upgrade['tier']}/{upgrade['max_tier']})"
                
                if self.btn_reroll and self.btn_reroll.is_clicked(event):
                    disc = 1.0 - (self.get_gem_level("gem_reroll_disc") * 0.15)
                    actual_reroll_cost = int(self.reroll_cost * disc)
                    if self.money >= actual_reroll_cost:
                        self.money -= actual_reroll_cost
                        self.shop_spent_in_visit += actual_reroll_cost
                        if self.shop_spent_in_visit >= 300: self.unlock_achievement("big_spender")
                        self.reroll_cost = int(self.reroll_cost * 1.5)
                        self.btn_reroll.text = f"Reroll Shop (${actual_reroll_cost})"
                        self.generate_shop_items()
                
                if self.btn_next_level and self.btn_next_level.is_clicked(event):
                    if self.level == 1: self.unlock_achievement("first_steps")
                    if self.save_data["difficulty"] == "hard": self.unlock_achievement("hardcore_survivor")
                    self.level += 1
                    if self.level >= 5: self.unlock_achievement("level_5_vet")
                    interest = 1.0 + (self.get_gem_level("gem_interest") * 0.03)
                    self.money = int(self.money * interest)
                    self.balls.clear()
                    self.create_level()
                    self.spawn_ball()
                    self.state = "PLAYING"
            
            elif self.state == "GAMEOVER":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "MENU"
            
            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "PAUSED"
                    elif event.key == pygame.K_SPACE:
                        if self.magnet_active:
                            self.magnet_active = False
                            for b in self.balls: b.stuck_to_paddle = False
                        elif self.laser_enabled and int(self.run_upgrades["laser_tier"]) < 4:
                            self.try_shoot_laser()
        
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]: self.state = "PAUSED"
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.paddle.move(-self.paddle.speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.paddle.move(self.paddle.speed)
            if self.laser_enabled and int(self.run_upgrades["laser_tier"]) >= 4 and keys[pygame.K_SPACE]:
                self.try_shoot_laser()
    
    def setup_gem_shop_buttons(self):
        self.gem_shop_buttons = []
        start_idx = self.gem_shop_page * 5
        page_defs = GEM_UPGRADES_DEF[start_idx: start_idx + 5]
        
        for i, up_def in enumerate(page_defs):
            btn = Button(WIDTH // 2 - 200, 180 + (i * 95), 400, 75, "", DARK_GRAY, font_size=16)
            self.gem_shop_buttons.append({"button": btn, "def": up_def})
    
    def try_shoot_laser(self):
        if self.laser_cooldown_timer <= 0:
            tier = int(self.run_upgrades["laser_tier"])
            cooldown_map = {0: 30, 1: 24, 2: 18, 3: 15, 4: 6, 5: 6}
            self.laser_cooldown_timer = cooldown_map.get(tier, 6)
            
            if tier >= 5:
                self.lasers.append(pygame.Rect(self.paddle.rect.left + 10, self.paddle.rect.top, 4, 18))
                self.lasers.append(pygame.Rect(self.paddle.rect.right - 14, self.paddle.rect.top, 4, 18))
            else:
                pcx = (self.paddle.rect.left + self.paddle.rect.right) // 2
                self.lasers.append(pygame.Rect(pcx - 2, self.paddle.rect.top, 4, 18))
    
    def prepare_shop(self):
        self.shop_spent_in_visit = 0
        diff = self.save_data["difficulty"]
        score_divisor = {"easy": 5, "normal": 10, "hard": 20}[diff]
        earned_money = (self.score // score_divisor) * (1 + self.run_upgrades["coin_tier"])
        self.money += earned_money
        
        if self.money >= 500: self.unlock_achievement("rich_gamer")
        
        self.reroll_cost = 25
        self.btn_reroll = Button(WIDTH // 2 - 120, HEIGHT - 140, 240, 45, f"Reroll Shop ($25)", PURPLE)
        self.btn_next_level = Button(WIDTH // 2 - 120, HEIGHT - 85, 240, 45, "START NEXT LEVEL", GREEN)
        
        self.generate_shop_items()
    
    def generate_shop_items(self):
        diff = self.save_data["difficulty"]
        cost_mult = {"easy": 0.8, "normal": 1.0, "hard": 1.5}[diff]
        
        pool = [
            {"name": "Permanent Damage Up", "key": "damage_tier", "base_cost": int(80 * cost_mult),
             "desc": "Increases ball base damage", "max_tier": 5},
            {"name": "Wider Starting Paddle", "key": "paddle_tier", "base_cost": int(65 * cost_mult),
             "desc": "Wider paddle at level start", "max_tier": 5},
            {"name": "Extra Starting Life", "key": "life_tier", "base_cost": int(90 * cost_mult),
             "desc": "Start runs with extra lives", "max_tier": 5},
            {"name": "Coin Multiplier", "key": "coin_tier", "base_cost": int(110 * cost_mult),
             "desc": "Earn more cash per score point", "max_tier": 5},
            {"name": "Laser System Upgrade", "key": "laser_tier", "fixed_costs": [50, 100, 150, 200, 250],
             "desc": "Faster cooldown, auto-fire & double laser", "max_tier": 5}
        ]
        
        num_slots = 4 if self.get_gem_level("gem_shop_slot") > 0 else 3
        selected = random.sample(pool, min(num_slots, len(pool)))
        self.shop_buttons = []
        
        for i, up in enumerate(selected):
            current_tier = self.run_upgrades[up["key"]]
            max_t = up["max_tier"]
            
            if "fixed_costs" in up:
                cost = int(up["fixed_costs"][current_tier] * cost_mult) if current_tier < max_t else 9999
            else:
                cost = int(up["base_cost"] * (2.0 ** current_tier))
            
            up_data = {
                "name": up["name"], "key": up["key"], "tier": current_tier,
                "base_cost": up.get("base_cost", 50), "cost": cost, "desc": up["desc"], "max_tier": max_t
            }
            btn = Button(WIDTH // 2 - 200, 160 + (i * 105), 400, 80, f"{up['name']} (Tier {current_tier}/{max_t})",
                         DARK_GRAY)
            self.shop_buttons.append({"button": btn, "upgrade": up_data})
    
    def get_random_powerup(self):
        choices = ["Wider Paddle", "Multiball (+2)", "2x Score", "Speed Up", "Extra Life", "Slow Ball", "Giant Ball",
                   "Shield Wall", "Magnet Paddle", "Cash Surge"]
        if not self.laser_enabled: choices.append("Laser Enabled")
        return random.choice(choices)
    
    def update(self):
        for popup in self.steam_popups[:]:
            popup["timer"] -= 1
            if popup["x"] < popup["target_x"]: popup["x"] += min(15, popup["target_x"] - popup["x"])
            if popup["timer"] < 30: popup["x"] -= 15
            if popup["timer"] <= 0: self.steam_popups.remove(popup)
        
        if self.state != "PLAYING": return
        
        if self.score >= 1000: self.unlock_achievement("brick_breaker")
        if len(self.balls) >= 5: self.unlock_achievement("multiball_mayhem")
        
        if self.laser_cooldown_timer > 0: self.laser_cooldown_timer -= 1
        
        for note in self.notifications[:]:
            note["timer"] -= 1;
            note["y"] -= 0.5
            if note["timer"] <= 0: self.notifications.remove(note)
        
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)
        
        # Ball-to-Ball Collisions
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1 = self.balls[i];
                b2 = self.balls[j]
                if b1.respawn_timer == 0 and b2.respawn_timer == 0 and not b1.stuck_to_paddle and not b2.stuck_to_paddle:
                    dist_x = b2.x - b1.x;
                    dist_y = b2.y - b1.y
                    distance = math.hypot(dist_x, dist_y)
                    min_dist = b1.radius + b2.radius
                    if distance < min_dist and distance > 0:
                        nx = dist_x / distance;
                        ny = dist_y / distance
                        overlap = min_dist - distance
                        b1.x -= nx * overlap / 2;
                        b2.x += nx * overlap / 2
                        b1.y -= ny * overlap / 2;
                        b2.y += ny * overlap / 2
                        kx = b1.dx - b2.dx;
                        ky = b1.dy - b2.dy
                        p_val = 2 * (nx * kx + ny * ky) / 2
                        b1.dx -= p_val * nx;
                        b1.dy -= p_val * ny
                        b2.dx += p_val * nx;
                        b2.dy += p_val * ny
        
        for ball in self.balls[:]:
            if ball.respawn_timer > 0:
                ball.respawn_timer -= 1
                if ball.respawn_timer == 0:
                    ball.x = self.paddle.rect.centerx;
                    ball.y = self.paddle.rect.top - 12
                    ball.dx = random.choice([-4, 4]);
                    ball.dy = -5
                continue
            
            if ball.stuck_to_paddle:
                ball.x = self.paddle.rect.centerx
                ball.y = self.paddle.rect.top - ball.radius
                continue
            
            ball.update()
            ball_rect = ball.get_rect()
            
            if ball_rect.colliderect(self.paddle.rect) and ball.dy > 0:
                if self.magnet_active:
                    ball.stuck_to_paddle = True
                    self.unlock_achievement("magnetized")
                else:
                    rel = (ball.x - self.paddle.rect.centerx) / (self.paddle.width / 2)
                    angle = rel * (math.pi / 3)
                    speed = math.hypot(ball.dx, ball.dy)
                    ball.dx = speed * math.sin(angle);
                    ball.dy = -speed * math.cos(angle)
                    ball.y = self.paddle.rect.top - ball.radius
            
            for brick in self.bricks[:]:
                if ball_rect.colliderect(brick.rect):
                    ol = ball_rect.right - brick.rect.left;
                    oright = brick.rect.right - ball_rect.left
                    ot = ball_rect.bottom - brick.rect.top;
                    ob = brick.rect.bottom - ball_rect.top
                    min_o = min(ol, oright, ot, ob)
                    if min_o == ot or min_o == ob:
                        ball.dy = -ball.dy
                    else:
                        ball.dx = -ball.dx
                    
                    if brick.type != 'unbreakable':
                        crit_chance = self.get_gem_level("gem_crit") * 0.04
                        dmg = ball.damage * (2 if random.random() < crit_chance else 1)
                        brick.hp -= dmg
                        
                        if brick.hp <= 0:
                            self.score += int(10 * self.score_multiplier)
                            num_p = 15 if self.get_gem_level("gem_particles") > 0 else 10
                            for _ in range(num_p):
                                self.particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))
                            
                            diff = self.save_data["difficulty"]
                            drop_chance = {"easy": 0.375, "normal": 0.25, "hard": 0.125}[diff] + (
                                        self.get_gem_level("gem_drop") * 0.05)
                            if random.random() < drop_chance:
                                u_type = self.get_random_powerup()
                                self.powerups.append(
                                    {"rect": pygame.Rect(brick.rect.centerx - 12, brick.rect.centery - 12, 24, 24),
                                     "type": u_type})
                            
                            self.bricks.remove(brick)
                    break
            
            if ball.y - ball.radius >= HEIGHT:
                if ball.is_multiball:
                    ball.respawn_timer = 90
                else:
                    self.balls.remove(ball)
        
        active_main_balls = [b for b in self.balls if not b.is_multiball and b.respawn_timer == 0]
        if not any(not b.is_multiball for b in self.balls) or (not active_main_balls and len(self.balls) == 0):
            if self.shield_charges > 0:
                self.shield_charges -= 1
                self.spawn_ball()
                self.add_notification("Shield Wall Blocked Death!", CYAN)
            else:
                revive_chance = self.get_gem_level("gem_revive") * 0.15
                if revive_chance > 0 and random.random() < revive_chance:
                    self.lives = 1
                    self.spawn_ball()
                    self.add_notification("Second Wind Revive!", GREEN)
                else:
                    self.lives -= 1
                    if self.lives > 0:
                        self.balls.clear();
                        self.spawn_ball()
                    else:
                        self.end_run_and_calc_gems(victory=False)
        
        for pu in self.powerups[:]:
            pu["rect"].y += 4
            if pu["rect"].colliderect(self.paddle.rect):
                self.apply_powerup(pu["type"])
                self.powerups.remove(pu)
            elif pu["rect"].top > HEIGHT:
                self.powerups.remove(pu)
        
        for laser in self.lasers[:]:
            laser.y -= int(12 * (1.0 + self.get_gem_level("gem_laser_speed") * 0.2))
            laser_removed = False
            for brick in self.bricks[:]:
                if laser.colliderect(brick.rect):
                    if brick.type != 'unbreakable':
                        brick.hp -= 1
                        if brick.hp <= 0:
                            self.score += int(10 * self.score_multiplier)
                            for _ in range(8):
                                self.particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))
                            self.bricks.remove(brick)
                    self.lasers.remove(laser)
                    laser_removed = True
                    break
            if not laser_removed and laser.bottom <= 0: self.lasers.remove(laser)
        
        breakable = [b for b in self.bricks if b.type != 'unbreakable']
        if not breakable:
            self.prepare_shop()
            self.state = "SHOP"
    
    def apply_powerup(self, u_type):
        self.add_notification(f"+ {u_type}!", GREEN)
        if u_type == "Wider Paddle":
            self.paddle.width = min(self.paddle.width + 30, 260)
            self.paddle.rect.width = self.paddle.width
        elif u_type == "Multiball (+2)":
            if self.balls:
                b = self.balls[0]
                self.balls.append(Ball(b.x, b.y, -b.dx, b.dy, damage=b.damage, is_multiball=True))
                self.balls.append(Ball(b.x, b.y, b.dx, -b.dy, damage=b.damage, is_multiball=True))
        elif u_type == "2x Score":
            self.score_multiplier *= 2.0
        elif u_type == "Speed Up":
            for b in self.balls: b.dx *= 1.15; b.dy *= 1.15
        elif u_type == "Extra Life":
            max_l = 3 + self.get_gem_level("gem_life")
            self.lives = min(self.lives + 1, max_l + 3)
        elif u_type == "Slow Ball":
            for b in self.balls: b.dx *= 0.85; b.dy *= 0.85
        elif u_type == "Giant Ball":
            for b in self.balls: b.radius = min(b.radius + 3, 20)
        elif u_type == "Shield Wall":
            self.shield_charges += 1
            self.unlock_achievement("shielded")
        elif u_type == "Magnet Paddle":
            self.magnet_active = True
        elif u_type == "Cash Surge":
            self.money += 75
        elif u_type == "Laser Enabled":
            self.laser_enabled = True
    
    def render(self):
        self.screen.fill(BLACK)
        
        if self.state == "MENU":
            title = self.title_font.render("ULTIMATE BREAKOUT ARCADE", True, CYAN)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 110))
            
            gems_txt = self.font.render(
                f"Gems: 💎 {self.save_data['gems']}   |   Difficulty: {self.save_data['difficulty'].upper()}", True,
                YELLOW)
            self.screen.blit(gems_txt, (WIDTH // 2 - gems_txt.get_width() // 2, 160))
            
            self.btn_play.draw(self.screen, self.btn_play.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_gems.draw(self.screen, self.btn_gems.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_settings.draw(self.screen, self.btn_settings.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_achievements.draw(self.screen, self.btn_achievements.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_quit.draw(self.screen, self.btn_quit.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "SAVE_CONFIRM":
            title = self.title_font.render("RESUME RUN?", True, YELLOW)
            sub = self.font.render("You have a saved run in progress.", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 30))
            self.btn_cont_yes.draw(self.screen, self.btn_cont_yes.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_cont_no.draw(self.screen, self.btn_cont_no.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "SETTINGS":
            title = self.title_font.render("DIFFICULTY SETTINGS", True, LIGHT_BLUE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
            
            diff = self.save_data["difficulty"]
            self.btn_diff_easy.draw(self.screen,
                                    diff == "easy" or self.btn_diff_easy.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_diff_normal.draw(self.screen, diff == "normal" or self.btn_diff_normal.rect.collidepoint(
                pygame.mouse.get_pos()))
            self.btn_diff_hard.draw(self.screen,
                                    diff == "hard" or self.btn_diff_hard.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_back.draw(self.screen, self.btn_back.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "ACHIEVEMENTS":
            title = self.title_font.render("ACHIEVEMENTS", True, PURPLE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            
            for i, (key, name, desc) in enumerate(ACHIEVEMENT_DEFINITIONS):
                unlocked = self.save_data["achievements"].get(key, False)
                status = "[UNLOCKED]" if unlocked else "[LOCKED]"
                col = GREEN if unlocked else RED
                
                y_pos = 110 + (i * 50)
                name_txt = pygame.font.SysFont("Arial", 16, bold=True).render(f"{name} {status}", True, col)
                desc_txt = pygame.font.SysFont("Arial", 14).render(desc, True, WHITE)
                
                self.screen.blit(name_txt, (WIDTH // 2 - 280, y_pos))
                self.screen.blit(desc_txt, (WIDTH // 2 - 280, y_pos + 20))
            
            self.btn_ach_back.draw(self.screen, self.btn_ach_back.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "GEM_SHOP":
            title = self.title_font.render(f"GEM UPGRADES (Page {self.gem_shop_page + 1}/5)", True, PINK)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
            
            gems_txt = self.font.render(f"Available Gems: 💎 {self.save_data['gems']}", True, YELLOW)
            self.screen.blit(gems_txt, (WIDTH // 2 - gems_txt.get_width() // 2, 90))
            
            for item in self.gem_shop_buttons:
                btn = item["button"]
                up_def = item["def"]
                tier = self.get_gem_level(up_def["id"])
                cost = int(up_def["base_cost"] * (1.5 ** tier))
                
                status_text = f"Cost: 💎{cost}" if tier < up_def["max"] else "MAXED OUT"
                btn.text = f"{up_def['name']} (Tier {tier}/{up_def['max']}) - {status_text}"
                btn.draw(self.screen, btn.rect.collidepoint(pygame.mouse.get_pos()))
                
                desc_surf = pygame.font.SysFont("Arial", 14).render(up_def["desc"], True, WHITE)
                self.screen.blit(desc_surf, (btn.rect.x, btn.rect.y - 18))
            
            self.btn_gem_prev.draw(self.screen, self.btn_gem_prev.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_gem_next.draw(self.screen, self.btn_gem_next.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_gem_back.draw(self.screen, self.btn_gem_back.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "PAUSED":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            title = self.title_font.render("GAME PAUSED", True, CYAN)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 140))
            
            self.btn_resume.draw(self.screen, self.btn_resume.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_save_quit.draw(self.screen, self.btn_save_quit.rect.collidepoint(pygame.mouse.get_pos()))
            self.btn_end_run.draw(self.screen, self.btn_end_run.rect.collidepoint(pygame.mouse.get_pos()))
        
        elif self.state == "SHOP":
            title = self.title_font.render("BETWEEN LEVELS - SHOP", True, YELLOW)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 35))
            
            money_txt = self.font.render(f"Cash: ${self.money}   |   Gems: 💎 {self.save_data['gems']}", True, GREEN)
            self.screen.blit(money_txt, (WIDTH // 2 - money_txt.get_width() // 2, 85))
            
            for item in self.shop_buttons:
                btn = item["button"]
                up = item["upgrade"]
                btn.draw(self.screen, btn.rect.collidepoint(pygame.mouse.get_pos()))
                
                disc = 1.0 - (self.get_gem_level("gem_upgrade_disc") * 0.05)
                actual_cost = int(up['cost'] * disc)
                cost_text = f"Cost: ${actual_cost}" if up['tier'] < up['max_tier'] else "MAXED OUT"
                desc_txt = self.font.render(f"{up['desc']} | {cost_text}", True, WHITE)
                self.screen.blit(desc_txt, (btn.rect.x, btn.rect.y - 20))
            
            if self.btn_reroll: self.btn_reroll.draw(self.screen,
                                                     self.btn_reroll.rect.collidepoint(pygame.mouse.get_pos()))
            if self.btn_next_level: self.btn_next_level.draw(self.screen, self.btn_next_level.rect.collidepoint(
                pygame.mouse.get_pos()))
        
        elif self.state in ["PLAYING", "GAMEOVER"]:
            score_txt = self.font.render(
                f"Score: {self.score}   Lives: {self.lives}   Level: {self.level}   Cash: ${self.money}   Shields: {self.shield_charges}",
                True, WHITE)
            self.screen.blit(score_txt, (20, 20))
            
            if self.laser_enabled:
                laser_msg = "LASER [AUTO]" if int(self.run_upgrades["laser_tier"]) >= 4 else "LASER [SPACE]"
                self.screen.blit(self.font.render(laser_msg, True, CYAN), (WIDTH - 220, 20))
            
            self.paddle.draw(self.screen)
            for ball in self.balls: ball.draw(self.screen)
            for brick in self.bricks: brick.draw(self.screen)
            for pu in self.powerups:
                pygame.draw.rect(self.screen, PURPLE, pu["rect"], border_radius=4)
                pygame.draw.rect(self.screen, WHITE, pu["rect"], 2, border_radius=4)
            for laser in self.lasers: pygame.draw.rect(self.screen, CYAN, laser, border_radius=2)
            for p in self.particles: p.draw(self.screen)
            for note in self.notifications:
                self.screen.blit(self.font.render(note["text"], True, note["color"]),
                                 (WIDTH // 2 - 100, int(note["y"])))
            
            if self.state == "GAMEOVER":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 210))
                self.screen.blit(overlay, (0, 0))
                go_txt = self.title_font.render("RUN OVER", True, RED)
                sub_txt = self.font.render("Click anywhere to return to Menu", True, WHITE)
                self.screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, HEIGHT // 2 - 40))
                self.screen.blit(sub_txt, (WIDTH // 2 - sub_txt.get_width() // 2, HEIGHT // 2 + 15))
        
        for popup in self.steam_popups:
            popup_rect = pygame.Rect(popup["x"], popup["y"], 300, 64)
            pygame.draw.rect(self.screen, (25, 25, 35), popup_rect, border_radius=6)
            pygame.draw.rect(self.screen, CYAN, popup_rect, 2, border_radius=6)
            self.screen.blit(pygame.font.SysFont("Arial", 14, bold=True).render(popup["title"], True, YELLOW),
                             (popup["x"] + 12, popup["y"] + 10))
            self.screen.blit(pygame.font.SysFont("Arial", 16, bold=True).render(popup["text"], True, WHITE),
                             (popup["x"] + 12, popup["y"] + 32))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()