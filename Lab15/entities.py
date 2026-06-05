import pyray as pr
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 150
        self.color = pr.BLUE
        self.has_artifact = False

    def update(self, dt):
        dx = 0
        dy = 0
        if pr.is_key_down(pr.KEY_W): dy -= 1
        if pr.is_key_down(pr.KEY_S): dy += 1
        if pr.is_key_down(pr.KEY_A): dx -= 1
        if pr.is_key_down(pr.KEY_D): dx += 1

        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length

        return dx * self.speed * dt, dy * self.speed * dt

    def draw(self):
        pr.draw_circle(int(self.x), int(self.y), self.radius, self.color)
        if self.has_artifact:
            pr.draw_circle(int(self.x), int(self.y), 4, pr.YELLOW)


class Rock:
    def __init__(self, x, y, tx, ty):
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty
        self.speed = 300
        self.radius = 4
        self.active = True
        
        dx = tx - x
        dy = ty - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vx = (dx/dist) * self.speed
            self.vy = (dy/dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, dt):
        if not self.active: return
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Check if reached target approx
        dist = math.sqrt((self.tx - self.x)**2 + (self.ty - self.y)**2)
        if dist < 10:
            self.active = False

    def draw(self):
        if self.active:
            pr.draw_circle(int(self.x), int(self.y), self.radius, pr.GRAY)


class Guard:
    STATE_PATROL = 0
    STATE_SUSPICIOUS = 1
    STATE_CHASE = 2
    STATE_RETURN = 3

    def __init__(self, path_points):
        self.path = path_points
        self.path_idx = 0
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.radius = 12
        self.speed = 70
        self.chase_speed = 110
        self.state = self.STATE_PATROL
        self.vision_range = 150
        
        # For suspicious state
        self.suspicious_timer = 0
        self.target_x = 0
        self.target_y = 0

    def update(self, dt, player, rocks, wall_col_func):
        # FSM Logic
        if self.state == self.STATE_PATROL:
            self._move_towards(self.path[self.path_idx][0], self.path[self.path_idx][1], self.speed, dt, wall_col_func)
            if self._distance_to(self.path[self.path_idx][0], self.path[self.path_idx][1]) < 5:
                self.path_idx = (self.path_idx + 1) % len(self.path)
            
            # Check for player
            if self._can_see(player.x, player.y):
                self.state = self.STATE_CHASE
            
            # Check for rock sounds
            for rock in rocks:
                if not rock.active and self._distance_to(rock.x, rock.y) < 200:
                    self.state = self.STATE_SUSPICIOUS
                    self.target_x = rock.x
                    self.target_y = rock.y
                    self.suspicious_timer = 3.0

        elif self.state == self.STATE_SUSPICIOUS:
            self._move_towards(self.target_x, self.target_y, self.speed, dt, wall_col_func)
            self.suspicious_timer -= dt
            if self.suspicious_timer <= 0:
                self.state = self.STATE_RETURN
            if self._can_see(player.x, player.y):
                self.state = self.STATE_CHASE

        elif self.state == self.STATE_CHASE:
            self._move_towards(player.x, player.y, self.chase_speed, dt, wall_col_func)
            if not self._can_see(player.x, player.y):
                self.state = self.STATE_SUSPICIOUS
                self.target_x = player.x
                self.target_y = player.y
                self.suspicious_timer = 3.0

        elif self.state == self.STATE_RETURN:
            # Move back to nearest patrol point
            closest_idx = 0
            min_dist = 9999
            for i, p in enumerate(self.path):
                d = self._distance_to(p[0], p[1])
                if d < min_dist:
                    min_dist = d
                    closest_idx = i
            
            self._move_towards(self.path[closest_idx][0], self.path[closest_idx][1], self.speed, dt, wall_col_func)
            if self._distance_to(self.path[closest_idx][0], self.path[closest_idx][1]) < 5:
                self.path_idx = closest_idx
                self.state = self.STATE_PATROL
            
            if self._can_see(player.x, player.y):
                self.state = self.STATE_CHASE

    def _move_towards(self, tx, ty, speed, dt, wall_col_func):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            mx = (dx/dist) * speed * dt
            my = (dy/dist) * speed * dt
            
            self.x += mx
            if wall_col_func(self.x, self.y, self.radius):
                self.x -= mx
                
            self.y += my
            if wall_col_func(self.x, self.y, self.radius):
                self.y -= my

    def _distance_to(self, tx, ty):
        return math.sqrt((tx - self.x)**2 + (ty - self.y)**2)

    def _can_see(self, px, py):
        return self._distance_to(px, py) < self.vision_range

    def draw(self):
        color = pr.RED
        if self.state == self.STATE_SUSPICIOUS: color = pr.ORANGE
        if self.state == self.STATE_RETURN: color = pr.MAROON
        
        pr.draw_circle(int(self.x), int(self.y), self.radius, color)
        
        # Vision indication
        if self.state == self.STATE_PATROL or self.state == self.STATE_RETURN:
            pr.draw_circle_lines(int(self.x), int(self.y), self.vision_range, pr.fade(pr.RED, 0.3))
        elif self.state == self.STATE_CHASE:
            pr.draw_circle_lines(int(self.x), int(self.y), self.vision_range, pr.RED)

