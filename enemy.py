import pyasge

from fsm import FSM
from charcondition import CharCondition


class Enemy:
    def __init__(self, filename, pos_x, pos_y) -> None:
        super().__init__()
        self.file_texture = filename
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture(self.file_texture)
        self.sprite.x = pos_x
        self.sprite.y = pos_y

        self.laser = pyasge.Sprite()
        self.laser.loadTexture("/data/images/laser.png")
        self.laser.opacity = 0.0
        self.direction_x = -1.0
        self.direction_y = 0.0
        self.laser.rotation = -3.141592 / 2.0
        self.RANGED_DAMAGE = 10

        # init ammo
        self.MAX_AMMO = 6
        self.laser_count = self.MAX_AMMO

        self.sword = pyasge.Sprite()
        self.sword.loadTexture("/data/images/sword2.png")
        self.sword.opacity = 0.0
        self.sword.rotation = 0.0
        self.SWORD_DAMAGE = 20

        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.prev_enemy_condition = CharCondition.HEALTHY
        self.enemy_condition = CharCondition.HEALTHY
        self.hp = 100

        # init step back
        self.MAX_MOVE_POINTS = 5
        self.move_points = self.MAX_MOVE_POINTS
        self.prev_pos = []
        self.prev_steps = []
        self.current_pos = [pos_x, pos_y]
        print("prev pos: " + str(self.prev_pos))
        print("current pos: " + str(self.current_pos))
        print("prev steps(array): " + str(self.prev_steps))

    def update(self, game_time: pyasge.GameTime) -> None:
        """Update FSM and redraw enemy if conditions change"""
        self.fsm.update()
        self.upstates()

    def update_healthy(self):
        """"""
        self.enemy_condition = CharCondition.HEALTHY
        if self.hp <= 60:
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        self.enemy_condition = CharCondition.DAMAGED
        if self.hp <= 30:
            self.fsm.setstate(self.update_very_damaged)

    def update_very_damaged(self):
        """ Create the logic here for the ship when it's very damaged """
        self.enemy_condition = CharCondition.VERY_DAMAGED
        if self.hp <= 0:
            self.fsm.setstate(self.died)

    def died(self):
        """ Create the logic here for the ship is sunk """
        self.enemy_condition = CharCondition.DEAD

    def upstates(self):
        if self.hp == 100:
            if self.file_texture == "/data/images/demonIdle_0.png":
                self.sprite.loadTexture("/data/images/demonIdle_0.png")
            elif self.file_texture == "/data/images/goblinlIdle_0.png":
                self.sprite.loadTexture("/data/images/goblinlIdle_0.png")
            elif self.file_texture == "/data/images/skeletonlIdle_0.png":
                self.sprite.loadTexture("/data/images/skeletonlIdle_0.png")

        elif self.hp == 60:
            if self.file_texture == "/data/images/demonIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/demon_/hurt_/lHurt_0.png")
            elif self.file_texture == "/data/images/goblinlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/goblin_/hurt_/lHurt_0.png")
            elif self.file_texture == "/data/images/skeletonlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/skeleton_/hurt_/lHurt_0.png")

        elif self.hp == 30:
            if self.file_texture == "/data/images/demonIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/demon_/hurt_/lHurt_2.png")
            elif self.file_texture == "/data/images/goblinlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/goblin_/hurt_/lHurt_3.png")
            elif self.file_texture == "/data/images/skeletonlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/skeleton_/hurt_/lHurt_3.png")

        elif self.hp == 0:
            if self.file_texture == "/data/images/demonIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/demon_/death_/lDeath_3.png")
            elif self.file_texture == "/data/images/goblinlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/goblin_/death_/lDeath_3.png")
            elif self.file_texture == "/data/images/skeletonlIdle_0.png":
                self.sprite.loadTexture("/data/images/dungeonSprites_/skeleton_/death_/lDeath_3.png")

    def playerUpdate(self):
        border_left = 0
        border_right = 1024
        border_top = 0
        border_bottom = 576

        if self.laser.opacity == 1.0:
            self.laser.x = self.laser.x + self.direction_x * 10
            self.laser.y = self.laser.y + self.direction_y * 10

            if self.laser.x <= border_left or self.laser.x >= border_right - self.laser.width * 2 or \
                    self.laser.y <= border_top or self.laser.y >= border_bottom:
                self.laser.opacity = 0.0

    def move(self, directionx, directiony):
        if directionx == 0 and directiony != 0:
            self.sprite.y = self.sprite.y + 64 * directiony
            self.direction_x = 0.0
            self.direction_y = directiony
            self.laser.rotation = 0.0

        if directionx != 0 and directiony == 0:
            self.sprite.x = self.sprite.x + 64 * directionx
            self.direction_x = directionx
            self.direction_y = 0.0
            self.laser.rotation = 3.141592 / 2.0

    def enemyUpdate(self):
        border_left = -1
        border_right = 1088
        border_top = -1
        border_bottom = 576

        if self.laser.opacity == 1.0:
            self.laser.x = self.laser.x + self.direction_x * 10
            self.laser.y = self.laser.y + self.direction_y * 10

            if self.laser.x <= border_left or self.laser.x >= border_right - self.laser.width * 2 or \
                    self.laser.y <= border_top or self.laser.y >= border_bottom:
                self.laser.opacity = 0.0

    def inboundCheck(self):
        border_left = -1
        border_right = 1088
        border_top = -1
        border_bottom = 576
        tileWH = 64

        if self.sprite.x <= border_left or self.sprite.x >= border_right - self.sprite.width * 2 or \
                self.sprite.y <= border_top or self.sprite.y >= border_bottom:
            return True
        elif 6 * tileWH <= self.sprite.x <= 9 * tileWH and self.sprite.y <= 1 * tileWH:
            return True
        elif (6 * tileWH <= self.sprite.x <= 9 * tileWH) and (4 * tileWH <= self.sprite.y <= 6 * tileWH):
            return True
        elif (6 * tileWH <= self.sprite.x <= 9 * tileWH) and (self.sprite.y >= 9 * tileWH):
            return True
        else:
            return False

    def resetPos(self):
        self.prev_steps = []
        self.prev_pos = []
        self.current_pos = [self.sprite.x, self.sprite.y]

    def resetSteps(self):
        self.move_points = self.MAX_MOVE_POINTS

    def resetAmmo(self):
        self.laser_count = self.MAX_AMMO

    def reduceStepCount(self, value):
        self.move_points -= value
        print("Steps Left " + str(self.move_points))

    def increaseStepCount(self, value):
        self.move_points += value
        print("Steps Left " + str(self.move_points))

    def stepBack(self):
        if self.inboundCheck():
            self.sprite.x = self.current_pos[0]
            self.sprite.y = self.current_pos[1]
        else:
            temp = self.current_pos
            self.current_pos = [self.sprite.x, self.sprite.y]

            if self.current_pos != self.prev_pos:
                self.prev_pos = temp
                self.prev_steps.append(self.prev_pos)
                self.reduceStepCount(1)
                print("prev pos: " + str(self.prev_pos))
                print("current pos: " + str(self.current_pos))
                print("prev steps(array): " + str(self.prev_steps))

            elif self.prev_pos == self.current_pos:
                del self.prev_steps[len(self.prev_steps) - 1]
                self.increaseStepCount(1)
                self.current_pos = [self.sprite.x, self.sprite.y]

                if len(self.prev_steps) > 0:
                    self.prev_pos = self.prev_steps[len(self.prev_steps) - 1]
                    print("prev pos: " + str(self.prev_pos))
                    print("current pos: " + str(self.current_pos))
                    print("prev steps(array): " + str(self.prev_steps))

                else:
                    self.prev_pos = []
                    print("prev pos: " + str(self.prev_pos))
                    print("current pos: " + str(self.current_pos))
                    print("prev steps(array): " + str(self.prev_steps))

    def spawnSword(self):
        self.sword.opacity = 1.0

        if self.direction_x == 1 and self.direction_y == 0:
            self.sword.x = self.sprite.x + 30
            self.sword.y = self.sprite.y + 20

        if self.direction_x == -1 and self.direction_y == 0:
            self.sword.x = self.sprite.x - 10
            self.sword.y = self.sprite.y + 20

        if self.direction_x == 0 and self.direction_y == 1:
            self.sword.x = self.sprite.x + 20
            self.sword.y = self.sprite.y + 60

        if self.direction_x == 0 and self.direction_y == -1:
            self.sword.x = self.sprite.x + 20
            self.sword.y = self.sprite.y - 10

    def shootCollisionCheck(self, enemies):
        for enemy in enemies:
            enemy_x = enemy.sprite.x
            enemy_y = enemy.sprite.y
            enemy_w = enemy.sprite.width
            enemy_h = enemy.sprite.height

            if self.laser.opacity == 1.0:
                laser_x = self.laser.x
                laser_y = self.laser.y
                if enemy_x < laser_x < enemy_x + enemy_w and enemy_y < laser_y < enemy_y + enemy_h:
                    if enemy.hp >= 0:
                        enemy.hp -= self.RANGED_DAMAGE
                        self.laser.opacity = 0.0
                    print("collision laser")

    def swordCollisionCheck(self, enemies):
        for enemy in enemies:
            enemy_x = enemy.sprite.x
            enemy_y = enemy.sprite.y
            enemy_w = enemy.sprite.width
            enemy_h = enemy.sprite.height

            if self.sword.opacity == 1.0:
                sword_x = self.sword.x
                sword_y = self.sword.y
                if enemy_x < sword_x < enemy_x + enemy_w and enemy_y < sword_y < enemy_y + enemy_h:
                    if enemy.hp >= 0:
                        enemy.hp -= self.SWORD_DAMAGE
                    print("collision sword")

    def cancelSword(self):
        self.sword.opacity = 0.0
