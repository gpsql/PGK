import pyray as pr
from entities import Player, Guard, Rock
import math

class Game:
    def __init__(self, difficulty="NORMAL"):
        self.walls = [
            pr.Rectangle(0, 0, 800, 20),
            pr.Rectangle(0, 580, 800, 20),
            pr.Rectangle(0, 0, 20, 600),
            pr.Rectangle(780, 0, 20, 600),
            
            pr.Rectangle(200, 150, 400, 20),
            pr.Rectangle(200, 400, 400, 20),
            pr.Rectangle(400, 150, 20, 150),
            pr.Rectangle(200, 280, 100, 20)
        ]
        
        self.artifact_rect = pr.Rectangle(420, 200, 30, 30)
        self.exit_rect = pr.Rectangle(20, 500, 60, 60)
        
        self.player = Player(50, 50)
        self.guards = [
            Guard([(250, 100), (650, 100), (650, 450), (250, 450)]),
            Guard([(100, 300), (100, 500), (350, 500), (350, 300)])
        ]
        
        for g in self.guards:
            if difficulty == "EASY":
                g.speed = 50
                g.chase_speed = 80
                g.vision_range = 100
            elif difficulty == "HARD":
                g.speed = 100
                g.chase_speed = 150
                g.vision_range = 220
        
        self.rocks = []
        
        self.state = "PLAYING" # PLAYING, WIN, LOSS
        
        # Audio
        pr.init_audio_device()
        self.snd_distract = pr.load_sound("distract.wav")
        self.snd_caught = pr.load_sound("caught.wav")
        self.snd_win = pr.load_sound("win.wav")

    def __del__(self):
        pr.unload_sound(self.snd_distract)
        pr.unload_sound(self.snd_caught)
        pr.unload_sound(self.snd_win)
        pr.close_audio_device()

    def update(self, dt):
        if self.state != "PLAYING": return

        # Player Movement
        dx, dy = self.player.update(dt)
        
        # Collision X
        self.player.x += dx
        if self._check_wall_collision(self.player.x, self.player.y, self.player.radius):
            self.player.x -= dx
            
        # Collision Y
        self.player.y += dy
        if self._check_wall_collision(self.player.x, self.player.y, self.player.radius):
            self.player.y -= dy

        # Throw Rock Mechanic
        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_RIGHT):
            mx = pr.get_mouse_x()
            my = pr.get_mouse_y()
            self.rocks.append(Rock(self.player.x, self.player.y, mx, my))
            pr.play_sound(self.snd_distract)

        # Update Rocks
        for r in self.rocks:
            r.update(dt)

        # Update Guards
        for g in self.guards:
            g.update(dt, self.player, self.rocks, self._check_wall_collision)
            
            # Guard Vision Collision (Simple Line of Sight Check)
            if g.state == Guard.STATE_CHASE:
                if self._check_circle_collision(self.player.x, self.player.y, self.player.radius, g.x, g.y, g.radius):
                    self.state = "LOSS"
                    pr.play_sound(self.snd_caught)

        # Artifact Pickup
        if not self.player.has_artifact:
            if pr.check_collision_circle_rec(pr.Vector2(self.player.x, self.player.y), self.player.radius, self.artifact_rect):
                self.player.has_artifact = True

        # Win Condition
        if self.player.has_artifact:
            if pr.check_collision_circle_rec(pr.Vector2(self.player.x, self.player.y), self.player.radius, self.exit_rect):
                self.state = "WIN"
                pr.play_sound(self.snd_win)

    def _check_wall_collision(self, x, y, radius):
        for w in self.walls:
            if pr.check_collision_circle_rec(pr.Vector2(x, y), radius, w):
                return True
        return False

    def _check_circle_collision(self, x1, y1, r1, x2, y2, r2):
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return dist < (r1 + r2)

    def draw(self):
        pr.clear_background(pr.RAYWHITE)
        
        # Draw Exit
        pr.draw_rectangle_rec(self.exit_rect, pr.GREEN if self.player.has_artifact else pr.DARKGREEN)
        pr.draw_text("EXIT", int(self.exit_rect.x + 10), int(self.exit_rect.y + 20), 20, pr.WHITE)

        # Draw Artifact
        if not self.player.has_artifact:
            pr.draw_rectangle_rec(self.artifact_rect, pr.GOLD)
            pr.draw_text("ART", int(self.artifact_rect.x), int(self.artifact_rect.y + 10), 10, pr.BLACK)

        # Draw Walls
        for w in self.walls:
            pr.draw_rectangle_rec(w, pr.DARKGRAY)
            
        # Draw Rocks
        for r in self.rocks:
            r.draw()
            
        # Draw Player
        self.player.draw()
        
        # Draw Guards
        for g in self.guards:
            g.draw()

