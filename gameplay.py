import pyasge
from gamestate import GameState, GameStateID
from fsm import FSM
from enum import Enum
from player import Player
from enemy import Enemy
from map import Map


class TurnState(Enum):
    UNKNOWN = -1
    PLAYERTURN = 1
    ENEMYTURN = 2
    PAUSED = 3


class PhaseState(Enum):
    UNKNOWN = -1
    MOVEPHASE = 1
    ATTACKPHASE = 2
    ENDPHASE = 3


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.inputs = None
        self.id = GameStateID.GAMEPLAY
        self.map = Map()
        self.menu_clicked = False
        self.options_clicked = False
        self.user_quit = False
        self.end_turn = False
        self.attack_m = False
        self.attack_r = False
        self.end_phase = False
        self.attack_phase = False

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click)
        self.ui_font = self.data.renderer.loadFont("/data/fonts/kenvector_future.ttf", 10)
        self.button_font = self.data.renderer.loadFont("/data/fonts/Augusta.ttf", 32)
        self.button_font_small = self.data.renderer.loadFont("/data/fonts/Augusta.ttf", 18)
        # create sprites

        # init FSM
        self.fsm_turn = FSM()
        self.fsm_phase = FSM()
        self.fsm_player = FSM()

        self.fsm_turn.setstate(TurnState.PLAYERTURN)
        self.fsm_phase.setstate(PhaseState.MOVEPHASE)

        self.current_turn = TurnState.PLAYERTURN
        self.current_phase = PhaseState.MOVEPHASE
        self.prev_turn = None

        print("\n" + str(self.current_turn))
        print(str(self.current_phase) + "\n")

        # init Player
        self.player_1 = Player("/data/images/herorIdle_0.png", 64, 64)
        self.player_2 = Player("/data/images/knightrIdle_0.png", 192, 256)
        self.player_3 = Player("/data/images/warlockrIdle_0.png", 128, 448)
        self.enemy_1 = Enemy("/data/images/goblinlIdle_0.png", 704, 128)
        self.enemy_2 = Enemy("/data/images/demonIdle_0.png", 832, 256)
        self.enemy_3 = Enemy("/data/images/skeletonlIdle_0.png", 896, 384)

        # init Teams
        self.team_player = [self.player_1, self.player_2, self.player_3]
        self.team_enemy = [self.enemy_1, self.enemy_2, self.enemy_3]

        # self.initUi()

        # init active char
        self.active_char = self.player_1

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_ENTER: False,
            pyasge.KEYS.KEY_BACKSPACE: False,
            pyasge.KEYS.KEY_ESCAPE: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
            pyasge.KEYS.KEY_O: False,
            pyasge.KEYS.KEY_P: False,

            pyasge.GamePad.CROSS: False,
            pyasge.GamePad.CIRCLE: False,
            pyasge.GamePad.DPAD_UP: False,
            pyasge.GamePad.DPAD_DOWN: False,
            pyasge.GamePad.DPAD_LEFT: False,
            pyasge.GamePad.DPAD_RIGHT: False,
            pyasge.GamePad.START: False,
        }
        """Initializes UI Components"""
        self.action_panel_sprite = pyasge.Sprite()
        self.action_panel_sprite.loadTexture("/data/images/uipack-rpg/buttonLong_beige.png")
        self.action_panel_sprite.scale = 1
        self.action_panel_sprite.x = -10
        self.action_panel_sprite.y = 768 - self.action_panel_sprite.height + 10

        self.menu_button = pyasge.Sprite()
        self.menu_button.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.menu_button.scale = 2
        self.menu_button.x = 1024 - 110
        self.menu_button.y = self.action_panel_sprite.y + 30
        self.menu_button.z_order = 10
        self.menu_button_press = pyasge.Sprite()
        self.menu_button_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.menu_button_press.scale = 2
        self.menu_button_press.x = self.menu_button.x
        self.menu_button_press.y = self.menu_button.y
        self.menu_button_press.z_order = 11

        self.menu_text = pyasge.Text(self.button_font, "Menu")
        self.menu_text.colour = pyasge.COLOURS.BLACK
        self.menu_text.position = (self.menu_button.x + 10, self.menu_button.y + 55)
        self.menu_text.z_order = 12

        self.attack_phase_button = pyasge.Sprite()
        self.attack_phase_button.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.attack_phase_button.scale = 1.6
        self.attack_phase_button.x = self.action_panel_sprite.x + 50
        self.attack_phase_button.y = self.action_panel_sprite.y + 45
        self.attack_phase_button_press = pyasge.Sprite()
        self.attack_phase_button_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.attack_phase_button_press.scale = 1.6
        self.attack_phase_button_press.x = self.attack_phase_button.x
        self.attack_phase_button_press.y = self.attack_phase_button.y

        self.attack_button = pyasge.Sprite()
        self.attack_button.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.attack_button.scale = 1.4
        self.attack_button.x = self.action_panel_sprite.x + 70
        self.attack_button.y = self.action_panel_sprite.y + 45
        self.attack_button_press = pyasge.Sprite()
        self.attack_button_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.attack_button_press.scale = 1.4
        self.attack_button_press.x = self.attack_button.x
        self.attack_button_press.y = self.attack_button.y

        self.attack_button_r = pyasge.Sprite()
        self.attack_button_r.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.attack_button_r.scale = 1.4
        self.attack_button_r.x = self.attack_button.x + 90
        self.attack_button_r.y = self.attack_button.y
        self.attack_button_r_press = pyasge.Sprite()
        self.attack_button_r_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.attack_button_r_press.scale = 1.4
        self.attack_button_r_press.x = self.attack_button_r.x
        self.attack_button_r_press.y = self.attack_button_r.y

        self.end_phase_button = pyasge.Sprite()
        self.end_phase_button.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.end_phase_button.scale = 1.6
        self.end_phase_button.x = self.attack_phase_button.x + 125
        self.end_phase_button.y = self.attack_phase_button.y
        self.end_phase_button_press = pyasge.Sprite()
        self.end_phase_button_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.end_phase_button_press.scale = 1.6
        self.end_phase_button_press.x = self.end_phase_button.x
        self.end_phase_button_press.y = self.end_phase_button.y

        self.end_turn_button = pyasge.Sprite()
        self.end_turn_button.loadTexture("/data/images/uipack-rpg/buttonSquare_blue.png")
        self.end_turn_button.scale = 2
        self.end_turn_button.x = self.attack_button_r.x + 125
        self.end_turn_button.y = self.action_panel_sprite.y + 30
        self.end_turn_button_press = pyasge.Sprite()
        self.end_turn_button_press.loadTexture("/data/images/uipack-rpg/buttonSquare_blue_pressed.png")
        self.end_turn_button_press.scale = 2
        self.end_turn_button_press.x = self.end_turn_button.x
        self.end_turn_button_press.y = self.end_turn_button.y

        self.attack_m_text = pyasge.Text(self.button_font_small, "ATK\n"
                                                                 "Melee")
        self.attack_m_text.colour = pyasge.COLOURS.BLACK
        self.attack_m_text.position = (self.attack_button.x + 11, self.attack_button.y + 25)
        self.attack_m_text.z_order = 50

        self.attack_r_text = pyasge.Text(self.button_font_small, " ATK\n"
                                                                 "Ranged")
        self.attack_r_text.colour = pyasge.COLOURS.BLACK
        self.attack_r_text.position = (self.attack_button_r.x + 4, self.attack_button_r.y + 25)
        self.attack_r_text.z_order = 51

        self.end_phase_text = pyasge.Text(self.button_font_small, " END\n"
                                                                  "Turn")
        self.end_phase_text.colour = pyasge.COLOURS.BLACK
        self.end_phase_text.position = (self.end_phase_button.x + 14, self.end_phase_button.y + 35)
        self.end_phase_text.z_order = 52

        self.attack_phase_text = pyasge.Text(self.button_font_small, " ATK\n"
                                                                     "Phase")
        self.attack_phase_text.colour = pyasge.COLOURS.BLACK
        self.attack_phase_text.position = (self.attack_phase_button.x + 10, self.attack_phase_button.y + 35)
        self.attack_phase_text.z_order = 52

        self.end_turn_text = pyasge.Text(self.button_font, "End\n"
                                                           "Turn")
        self.end_turn_text.colour = pyasge.COLOURS.BLACK
        self.end_turn_text.position = (self.end_turn_button.x + 15, self.end_turn_button.y + 35)
        self.end_turn_text.z_order = 53

        self.menu_quit_button = pyasge.Sprite()
        self.menu_quit_button.loadTexture("/data/images/uipack-rpg/PNG/buttonLong_blue.png")
        self.menu_quit_button.scale = 0.5
        self.menu_quit_button.x = self.menu_button.x
        self.menu_quit_button.y = self.menu_button.y - 40

        self.menu_quit_text = pyasge.Text(self.button_font_small, "Quit")
        self.menu_quit_text.colour = pyasge.COLOURS.BLACK
        self.menu_quit_text.position = (self.menu_quit_button.x + 25, self.menu_quit_button.y + 20)
        self.menu_quit_text.z_order = 55

        self.menu_options_button = pyasge.Sprite()
        self.menu_options_button.loadTexture("/data/images/uipack-rpg/PNG/buttonLong_blue.png")
        self.menu_options_button.scale = 0.5
        self.menu_options_button.x = self.menu_quit_button.x
        self.menu_options_button.y = self.menu_quit_button.y - 40

        self.menu_options_button_text = pyasge.Text(self.button_font_small, "Settings")
        self.menu_options_button_text.colour = pyasge.COLOURS.BLACK
        self.menu_options_button_text.position = (self.menu_options_button.x + 20, self.menu_options_button.y + 20)
        self.menu_options_button_text.z_order = 55

        self.turn_phase_button_sprite = pyasge.Sprite()
        self.turn_phase_button_sprite.loadTexture("/data/images/uipack-rpg/PNG/buttonLong_beige.png")
        self.turn_phase_button_sprite.scale = 1
        self.turn_phase_button_sprite.x = 512 - self.turn_phase_button_sprite.width / 2
        self.turn_phase_button_sprite.y = 5

        """ Player UI Icons"""
        self.hero_sprite_icon = pyasge.Sprite()
        self.hero_sprite_icon.loadTexture("/data/images/herorIdle_0.png")
        self.hero_sprite_icon.scale = 0.5
        self.hero_sprite_icon.x = self.end_turn_button.x + 125
        self.hero_sprite_icon.y = self.action_panel_sprite.y + 15
        self.hero_sprite_icon.z_order = 54

        self.knight_sprite_icon = pyasge.Sprite()
        self.knight_sprite_icon.loadTexture("/data/images/knightrIdle_0.png")
        self.knight_sprite_icon.scale = 0.5
        self.knight_sprite_icon.x = self.hero_sprite_icon.x
        self.knight_sprite_icon.y = self.hero_sprite_icon.y + 40
        self.knight_sprite_icon.z_order = 55

        self.warlock_sprite_icon = pyasge.Sprite()
        self.warlock_sprite_icon.loadTexture("/data/images/warlockrIdle_0.png")
        self.warlock_sprite_icon.scale = 0.5
        self.warlock_sprite_icon.x = self.knight_sprite_icon.x
        self.warlock_sprite_icon.y = self.knight_sprite_icon.y + 40
        self.warlock_sprite_icon.z_order = 55

        """Enemy UI Icons"""
        self.goblin_sprite_icon = pyasge.Sprite()
        self.goblin_sprite_icon.loadTexture("/data/images/goblinlIdle_0.png")
        self.goblin_sprite_icon.scale = 0.5
        self.goblin_sprite_icon.x = self.menu_button.x - 200
        self.goblin_sprite_icon.y = self.action_panel_sprite.y + 15
        self.goblin_sprite_icon.z_order = 55

        self.demon_sprite_icon = pyasge.Sprite()
        self.demon_sprite_icon.loadTexture("/data/images/demonIdle_0.png")
        self.demon_sprite_icon.scale = 0.5
        self.demon_sprite_icon.x = self.goblin_sprite_icon.x
        self.demon_sprite_icon.y = self.goblin_sprite_icon.y + 40
        self.demon_sprite_icon.z_order = 55

        self.skeleton_sprite_icon = pyasge.Sprite()
        self.skeleton_sprite_icon.loadTexture("/data/images/skeletonlIdle_0.png")
        self.skeleton_sprite_icon.scale = 0.5
        self.skeleton_sprite_icon.x = self.goblin_sprite_icon.x
        self.skeleton_sprite_icon.y = self.demon_sprite_icon.y + 40
        self.skeleton_sprite_icon.z_order = 55

        self.player_1_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_1.hp) + "/100")
        self.player_1_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_1.laser_count) + "/6")
        self.player_1_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_1.move_points) + "/5")

        self.player_2_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_2.hp) + "/100")
        self.player_2_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_2.laser_count) + "/6")
        self.player_2_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_2.move_points) + "/5")

        self.player_3_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_3.hp) + "/100")
        self.player_3_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_3.laser_count) + "/6")
        self.player_3_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_3.move_points) + "/5")

        self.enemy_1_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_1.hp) + "/100")
        self.enemy_1_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_1.laser_count) + "/6")
        self.enemy_1_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_1.move_points) + "/5")

        self.enemy_2_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_2.hp) + "/100")
        self.enemy_2_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_2.laser_count) + "/6")
        self.enemy_2_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_2.move_points) + "/5")

        self.enemy_3_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_3.hp) + "/100")
        self.enemy_3_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_3.laser_count) + "/6")
        self.enemy_3_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_3.move_points) + "/5")

        self.player_arrow = pyasge.Sprite()
        self.player_arrow.loadTexture("/data/images/arrowBrown_right.png")

        self.turn_phase_text = pyasge.Text(self.ui_font, "Turn: Player\n"
                                                         "Phase: Move")

    def input(self, event: pyasge.KeyEvent) -> None:
        self.debugKeys()

        if (self.current_turn == TurnState.PLAYERTURN or self.current_turn == TurnState.ENEMYTURN) and \
                self.current_phase == PhaseState.MOVEPHASE:
            self.movementKeys(event)

        if (self.current_turn == TurnState.PLAYERTURN or self.current_turn == TurnState.ENEMYTURN) and \
                (self.current_phase == PhaseState.MOVEPHASE or self.current_phase == PhaseState.ATTACKPHASE):

            # Menu Controls
            if self.keys[pyasge.KEYS.KEY_ESCAPE]:
                """Pause Menu"""
                self.menu_clicked = True
            if self.menu_clicked:
                if self.keys[pyasge.KEYS.KEY_ESCAPE]:
                    """unpause Menu"""
                    self.menu_clicked = False

            if event.action is not pyasge.KEYS.KEY_REPEATED:
                self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        # print("update gameplay")
        # if self.inputs.getGamePad(0).connected:
        #    if self.inputs.getGamePad(0).START:
        #        self.signalExit()

        self.turnTransitionManager()
        self.updateUIPanel()
        self.updatePlayer()
        self.collisionCheck()

        # These would be added to group
        self.player_1.update(game_time)
        self.player_2.update(game_time)
        self.player_3.update(game_time)
        self.enemy_1.update(game_time)
        self.enemy_2.update(game_time)
        self.enemy_3.update(game_time)

        if self.player_1.hp <= 0 and self.player_2.hp <= 0 and self.player_3.hp <= 0:
            return GameStateID.GAME_OVER
        if self.enemy_1.hp <= 0 and self.enemy_2.hp <= 0 and self.enemy_3.hp <= 0:
            return GameStateID.WINNER_WINNER

        if self.user_quit:
            return GameStateID.START_MENU

        if self.options_clicked:
            return GameStateID.OPTIONS

        return GameStateID.GAMEPLAY

    def updateUIPanel(self):

        if self.current_turn == TurnState.PLAYERTURN and self.current_phase == PhaseState.MOVEPHASE:
            """If in player move phase - display ATK Phase and End Phase"""
            self.turn_phase_text = pyasge.Text(self.ui_font, "Turn: Player\n"
                                                             "Phase: Move")
            self.turn_phase_text.colour = pyasge.COLOURS.BLACK
            self.turn_phase_text.position = (self.turn_phase_button_sprite.x + 40, self.turn_phase_button_sprite.y + 20)
            self.turn_phase_text.z_order = 60
        if self.current_turn == TurnState.PLAYERTURN and self.current_phase == PhaseState.ATTACKPHASE:
            """If in player attack phase - display ATK Ranged, ATK Melee, End Phase"""
            self.turn_phase_text = pyasge.Text(self.ui_font, "Turn: Player\n"
                                                             "Phase: Attack")
            self.turn_phase_text.colour = pyasge.COLOURS.BLACK
            self.turn_phase_text.position = (self.turn_phase_button_sprite.x + 40, self.turn_phase_button_sprite.y + 20)
            self.turn_phase_text.z_order = 61

        if self.current_turn == TurnState.ENEMYTURN and self.current_phase == PhaseState.MOVEPHASE:
            """If in enemy move phase"""
            self.turn_phase_text = pyasge.Text(self.ui_font, "Turn: Enemy\n"
                                                             "Phase: Move")
            self.turn_phase_text.colour = pyasge.COLOURS.BLACK
            self.turn_phase_text.position = (self.turn_phase_button_sprite.x + 40, self.turn_phase_button_sprite.y + 20)
            self.turn_phase_text.z_order = 62
        if self.current_turn == TurnState.ENEMYTURN and self.current_phase == PhaseState.ATTACKPHASE:
            """If in enemy attack phase"""
            self.turn_phase_text = pyasge.Text(self.ui_font, "Turn: Enemy\n"
                                                             "Phase: Attack")
            self.turn_phase_text.colour = pyasge.COLOURS.BLACK
            self.turn_phase_text.position = (self.turn_phase_button_sprite.x + 40, self.turn_phase_button_sprite.y + 20)
            self.turn_phase_text.z_order = 63

        if self.active_char == self.player_1:
            self.player_arrow.x = self.hero_sprite_icon.x - 20
            self.player_arrow.y = self.hero_sprite_icon.y + 10
        if self.active_char == self.player_2:
            self.player_arrow.x = self.knight_sprite_icon.x - 20
            self.player_arrow.y = self.knight_sprite_icon.y + 10
        if self.active_char == self.player_3:
            self.player_arrow.x = self.warlock_sprite_icon.x - 20
            self.player_arrow.y = self.warlock_sprite_icon.y + 10

        if self.active_char == self.enemy_1:
            self.player_arrow.x = self.goblin_sprite_icon.x - 20
            self.player_arrow.y = self.goblin_sprite_icon.y + 10
        if self.active_char == self.enemy_2:
            self.player_arrow.x = self.demon_sprite_icon.x - 20
            self.player_arrow.y = self.demon_sprite_icon.y + 10
        if self.active_char == self.enemy_3:
            self.player_arrow.x = self.skeleton_sprite_icon.x - 20
            self.player_arrow.y = self.skeleton_sprite_icon.y + 10

        self.player_1_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_1.hp) + "/100")
        self.player_1_hp_text.colour = pyasge.COLOURS.BLACK
        self.player_1_hp_text.position = (self.hero_sprite_icon.x + 40, self.hero_sprite_icon.y + 15)
        self.player_1_hp_text.z_order = 56
        self.player_1_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_1.laser_count) + "/6")
        self.player_1_ammo_text.colour = pyasge.COLOURS.BLACK
        self.player_1_ammo_text.position = (self.player_1_hp_text.x, self.player_1_hp_text.y + 11)
        self.player_1_ammo_text.z_order = 56
        self.player_1_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_1.move_points) + "/5")
        self.player_1_move_text.colour = pyasge.COLOURS.BLACK
        self.player_1_move_text.position = (self.player_1_ammo_text.x, self.player_1_ammo_text.y + 11)
        self.player_1_move_text.z_order = 56

        self.player_2_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_2.hp) + "/100")
        self.player_2_hp_text.colour = pyasge.COLOURS.BLACK
        self.player_2_hp_text.position = (self.knight_sprite_icon.x + 40, self.knight_sprite_icon.y + 15)
        self.player_2_hp_text.z_order = 56
        self.player_2_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_2.laser_count) + "/6")
        self.player_2_ammo_text.colour = pyasge.COLOURS.BLACK
        self.player_2_ammo_text.position = (self.player_2_hp_text.x, self.player_2_hp_text.y + 11)
        self.player_2_ammo_text.z_order = 56
        self.player_2_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_2.move_points) + "/5")
        self.player_2_move_text.colour = pyasge.COLOURS.BLACK
        self.player_2_move_text.position = (self.player_2_ammo_text.x, self.player_2_ammo_text.y + 11)
        self.player_2_move_text.z_order = 56

        self.player_3_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.player_3.hp) + "/100")
        self.player_3_hp_text.colour = pyasge.COLOURS.BLACK
        self.player_3_hp_text.position = (self.warlock_sprite_icon.x + 40, self.warlock_sprite_icon.y + 15)
        self.player_3_hp_text.z_order = 56
        self.player_3_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.player_3.laser_count) + "/6")
        self.player_3_ammo_text.colour = pyasge.COLOURS.BLACK
        self.player_3_ammo_text.position = (self.player_3_hp_text.x, self.player_3_hp_text.y + 11)
        self.player_3_ammo_text.z_order = 56
        self.player_3_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.player_3.move_points) + "/5")
        self.player_3_move_text.colour = pyasge.COLOURS.BLACK
        self.player_3_move_text.position = (self.player_3_ammo_text.x, self.player_3_ammo_text.y + 11)
        self.player_3_move_text.z_order = 56

        self.enemy_1_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_1.hp) + "/100")
        self.enemy_1_hp_text.colour = pyasge.COLOURS.BLACK
        self.enemy_1_hp_text.position = (self.goblin_sprite_icon.x + 40, self.goblin_sprite_icon.y + 15)
        self.enemy_1_hp_text.z_order = 56
        self.enemy_1_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_1.laser_count) + "/6")
        self.enemy_1_ammo_text.colour = pyasge.COLOURS.BLACK
        self.enemy_1_ammo_text.position = (self.enemy_1_hp_text.x, self.enemy_1_hp_text.y + 11)
        self.enemy_1_ammo_text.z_order = 56
        self.enemy_1_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_1.move_points) + "/5")
        self.enemy_1_move_text.colour = pyasge.COLOURS.BLACK
        self.enemy_1_move_text.position = (self.enemy_1_ammo_text.x, self.enemy_1_ammo_text.y + 11)
        self.enemy_1_move_text.z_order = 56

        self.enemy_2_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_2.hp) + "/100")
        self.enemy_2_hp_text.colour = pyasge.COLOURS.BLACK
        self.enemy_2_hp_text.position = (self.demon_sprite_icon.x + 40, self.demon_sprite_icon.y + 15)
        self.enemy_2_hp_text.z_order = 56
        self.enemy_2_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_2.laser_count) + "/6")
        self.enemy_2_ammo_text.colour = pyasge.COLOURS.BLACK
        self.enemy_2_ammo_text.position = (self.enemy_2_hp_text.x, self.enemy_2_hp_text.y + 11)
        self.enemy_2_ammo_text.z_order = 56
        self.enemy_2_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_2.move_points) + "/5")
        self.enemy_2_move_text.colour = pyasge.COLOURS.BLACK
        self.enemy_2_move_text.position = (self.enemy_2_ammo_text.x, self.enemy_2_ammo_text.y + 11)
        self.enemy_2_move_text.z_order = 56

        self.enemy_3_hp_text = pyasge.Text(self.ui_font, "HP: " + str(self.enemy_3.hp) + "/100")
        self.enemy_3_hp_text.colour = pyasge.COLOURS.BLACK
        self.enemy_3_hp_text.position = (self.skeleton_sprite_icon.x + 40, self.skeleton_sprite_icon.y + 15)
        self.enemy_3_hp_text.z_order = 57
        self.enemy_3_ammo_text = pyasge.Text(self.ui_font, "Ammo: " + str(self.enemy_3.laser_count) + "/6")
        self.enemy_3_ammo_text.colour = pyasge.COLOURS.BLACK
        self.enemy_3_ammo_text.position = (self.enemy_3_hp_text.x, self.enemy_3_hp_text.y + 10)
        self.enemy_3_ammo_text.z_order = 57
        self.enemy_3_move_text = pyasge.Text(self.ui_font, "Move: " + str(self.enemy_3.move_points) + "/5")
        self.enemy_3_move_text.colour = pyasge.COLOURS.BLACK
        self.enemy_3_move_text.position = (self.enemy_3_ammo_text.x, self.enemy_3_ammo_text.y + 10)
        self.enemy_3_move_text.z_order = 57

    def updatePlayer(self):
        self.player_1.moveLaser()
        self.player_2.moveLaser()
        self.player_3.moveLaser()
        self.enemy_1.playerUpdate()
        self.enemy_2.playerUpdate()
        self.enemy_3.playerUpdate()

    def render(self, game_time: pyasge.GameTime) -> None:
        """This section is for items rendered to screen throughout all turns"""
        self.map.render(self.data.renderer)
        self.data.renderer.render(self.action_panel_sprite)

        self.data.renderer.render(self.menu_text)
        if self.menu_clicked:
            self.data.renderer.render(self.menu_button_press)
            self.data.renderer.render(self.menu_quit_button)
            self.data.renderer.render(self.menu_quit_text)
            self.data.renderer.render(self.menu_options_button)
            self.data.renderer.render(self.menu_options_button_text)
        else:
            self.data.renderer.render(self.menu_button)

        self.data.renderer.render(self.player_1.sprite)
        self.data.renderer.render(self.player_2.sprite)
        self.data.renderer.render(self.player_3.sprite)
        self.data.renderer.render(self.enemy_1.sprite)
        self.data.renderer.render(self.enemy_2.sprite)
        self.data.renderer.render(self.enemy_3.sprite)

        for active_player in self.team_player:
            self.data.renderer.render(active_player.laser)
            self.data.renderer.render(active_player.sword)

        for active_enemy in self.team_enemy:
            self.data.renderer.render(active_enemy.laser)
            self.data.renderer.render(active_enemy.sword)

        self.renderGameData()
        self.data.renderer.render(self.turn_phase_button_sprite)
        self.data.renderer.render(self.turn_phase_text)

        """This section is for items rendered based on turn/phase"""
        if self.current_turn == TurnState.PLAYERTURN and self.current_phase == PhaseState.MOVEPHASE:
            """If in player move phase - display ATK Phase and End Phase"""
            if self.end_phase:
                self.data.renderer.render(self.end_phase_button_press)
            else:
                self.data.renderer.render(self.end_phase_button)
            self.data.renderer.render(self.end_phase_text)

            if self.attack_phase:
                self.data.renderer.render(self.attack_phase_button_press)
            else:
                self.data.renderer.render(self.attack_phase_button)
            self.data.renderer.render(self.attack_phase_text)

        if self.current_turn == TurnState.PLAYERTURN and self.current_phase == PhaseState.ATTACKPHASE:
            """If in player attack phase - display ATK Ranged, ATK Melee, End Phase"""
            if self.attack_m:
                self.data.renderer.render(self.attack_button_press)
            else:
                self.data.renderer.render(self.attack_button)

            if self.attack_r:
                self.data.renderer.render(self.attack_button_r_press)
            else:
                self.data.renderer.render(self.attack_button_r)
            self.data.renderer.render(self.end_turn_button)
            self.data.renderer.render(self.attack_m_text)
            self.data.renderer.render(self.attack_r_text)
            self.data.renderer.render(self.end_turn_text)

        if self.current_turn == TurnState.ENEMYTURN and self.current_phase == PhaseState.MOVEPHASE:
            """If in enemy move phase"""
            if self.end_phase:
                self.data.renderer.render(self.end_phase_button_press)
            else:
                self.data.renderer.render(self.end_phase_button)
            self.data.renderer.render(self.end_phase_text)

            if self.attack_phase:
                self.data.renderer.render(self.attack_phase_button_press)
            else:
                self.data.renderer.render(self.attack_phase_button)
            self.data.renderer.render(self.attack_phase_text)

        if self.current_turn == TurnState.ENEMYTURN and self.current_phase == PhaseState.ATTACKPHASE:
            """If in enemy attack phase"""
            if self.attack_m:
                self.data.renderer.render(self.attack_button_press)
            else:
                self.data.renderer.render(self.attack_button)

            if self.attack_r:
                self.data.renderer.render(self.attack_button_r_press)
            else:
                self.data.renderer.render(self.attack_button_r)
            self.data.renderer.render(self.end_turn_button)
            self.data.renderer.render(self.attack_m_text)
            self.data.renderer.render(self.attack_r_text)
            self.data.renderer.render(self.end_turn_text)

    def renderGameData(self) -> None:
        """Render Character Icons"""
        self.data.renderer.render(self.hero_sprite_icon)
        self.data.renderer.render(self.knight_sprite_icon)
        self.data.renderer.render(self.warlock_sprite_icon)
        self.data.renderer.render(self.goblin_sprite_icon)
        self.data.renderer.render(self.demon_sprite_icon)
        self.data.renderer.render(self.skeleton_sprite_icon)

        """Render Player Character Data"""
        self.data.renderer.render(self.player_1_hp_text)
        self.data.renderer.render(self.player_1_ammo_text)
        self.data.renderer.render(self.player_1_move_text)
        self.data.renderer.render(self.player_2_hp_text)
        self.data.renderer.render(self.player_2_ammo_text)
        self.data.renderer.render(self.player_2_move_text)
        self.data.renderer.render(self.player_3_hp_text)
        self.data.renderer.render(self.player_3_ammo_text)
        self.data.renderer.render(self.player_3_move_text)

        """Render Enemy Character Data"""
        self.data.renderer.render(self.enemy_1_hp_text)
        self.data.renderer.render(self.enemy_1_ammo_text)
        self.data.renderer.render(self.enemy_1_move_text)
        self.data.renderer.render(self.enemy_2_hp_text)
        self.data.renderer.render(self.enemy_2_ammo_text)
        self.data.renderer.render(self.enemy_2_move_text)
        self.data.renderer.render(self.enemy_3_hp_text)
        self.data.renderer.render(self.enemy_3_ammo_text)
        self.data.renderer.render(self.enemy_3_move_text)

        self.data.renderer.render(self.player_arrow)

    def collisionCheck(self) -> None:
        """Check Collisions Here"""
        for active_player in self.team_player:
            active_player.shootCollisionCheck(self.team_enemy)

        for active_enemy in self.team_enemy:
            active_enemy.shootCollisionCheck(self.team_player)

    def click(self, event: pyasge.ClickEvent) -> None:
        """Button Bounds"""
        menu_bounds = self.menu_button.getWorldBounds()
        attack_m_bounds = self.attack_button.getWorldBounds()
        attack_r_bounds = self.attack_button_r.getWorldBounds()
        end_phase_bounds = self.end_phase_button.getWorldBounds()
        attack_phase_bounds = self.attack_phase_button.getWorldBounds()
        end_turn_bounds = self.end_turn_button.getWorldBounds()
        menu_quit_bounds = self.menu_quit_button.getWorldBounds()
        menu_options_bounds = self.menu_options_button.getWorldBounds()

        self.playerManager(event)

        """Button Actions"""
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                """Attack Phase"""
                if (self.current_turn == TurnState.PLAYERTURN or self.current_turn == TurnState.ENEMYTURN) and \
                        self.current_phase == PhaseState.ATTACKPHASE:
                    """Melee Attack"""
                    if self.active_char.hp > 0:
                        if attack_m_bounds.v1.x < event.x < attack_m_bounds.v2.x and \
                                attack_m_bounds.v1.y < event.y < attack_m_bounds.v4.y:
                            self.attack_m = True
                            if self.active_char.sword.opacity == 0.0:
                                self.active_char.spawnSword()
                                if self.current_turn == TurnState.PLAYERTURN:
                                    self.active_char.swordCollisionCheck(self.team_enemy)
                                if self.current_turn == TurnState.ENEMYTURN:
                                    self.active_char.swordCollisionCheck(self.team_player)
                        """Ranged Attack"""
                        if attack_r_bounds.v1.x < event.x < attack_r_bounds.v2.x and \
                                attack_r_bounds.v1.y < event.y < attack_r_bounds.v4.y:
                            self.attack_r = True
                            if (self.active_char.laser_count > 0) and (self.active_char.laser.opacity == 0.0):
                                self.active_char.laser.opacity = 1.0
                                self.active_char.laser.x = self.active_char.sprite.x + 10
                                self.active_char.laser.y = self.active_char.sprite.y + 10
                                self.active_char.laser_count = self.active_char.laser_count - 1
                    """End Turn - Attack Phase"""
                    if end_turn_bounds.v1.x < event.x < end_turn_bounds.v2.x and \
                            end_turn_bounds.v1.y < event.y < end_turn_bounds.v4.y:
                        self.endPhaseTransition()

                """Move Phase"""
                if (self.current_turn == TurnState.PLAYERTURN or self.current_turn == TurnState.ENEMYTURN) and \
                        self.current_phase == PhaseState.MOVEPHASE:
                    """End Turn - Move Phase"""
                    if end_phase_bounds.v1.x < event.x < end_phase_bounds.v2.x and \
                            end_phase_bounds.v1.y < event.y < end_phase_bounds.v4.y:
                        self.endPhaseTransition()
                    """Changes to Attack Phase"""
                    if attack_phase_bounds.v1.x < event.x < attack_phase_bounds.v2.x and \
                            attack_phase_bounds.v1.y < event.y < attack_phase_bounds.v4.y:
                        self.atkPhaseTransition()
                """Click Menu Button"""
                if menu_bounds.v1.x < event.x < menu_bounds.v2.x and menu_bounds.v1.y < event.y < menu_bounds.v4.y:
                    if self.menu_clicked:
                        self.menu_clicked = False
                    else:
                        self.menu_clicked = True
                """Menu Quit"""
                if menu_quit_bounds.v1.x < event.x < menu_quit_bounds.v2.x and \
                        menu_quit_bounds.v1.y < event.y < menu_quit_bounds.v4.y and self.menu_clicked:
                    self.user_quit = True
                """Settings Clicked"""
                if menu_options_bounds.v1.x < event.x < menu_options_bounds.v2.x and \
                        menu_options_bounds.v1.y < event.y < menu_options_bounds.v4.y and self.menu_clicked:
                    self.options_clicked = True
            else:
                """Reset variables after clicks"""
                self.end_turn = False
                self.attack_m = False
                self.attack_r = False
                self.end_phase = False
                self.attack_phase = False

    def debugKeys(self):
        """
        Debug Keys
        """
        if self.keys[pyasge.KEYS.KEY_O]:
            return GameStateID.WINNER_WINNER
        if self.keys[pyasge.KEYS.KEY_P]:
            return GameStateID.GAME_OVER

    def movementKeys(self, event):
        if self.active_char.hp > 0:
            if event.key is pyasge.KEYS.KEY_S and event.action is pyasge.KEYS.KEY_PRESSED:
                if self.active_char.move_points > 0:
                    self.active_char.move(0, 1)
                    self.active_char.stepBack()

            if event.key is pyasge.KEYS.KEY_W and event.action is pyasge.KEYS.KEY_PRESSED:
                if self.active_char.move_points > 0:
                    self.active_char.move(0, -1)
                    self.active_char.stepBack()

            if event.key is pyasge.KEYS.KEY_A and event.action is pyasge.KEYS.KEY_PRESSED:
                if self.active_char.move_points > 0:
                    self.active_char.move(-1, 0)
                    self.active_char.stepBack()

            if event.key is pyasge.KEYS.KEY_D and event.action is pyasge.KEYS.KEY_PRESSED:
                if self.active_char.move_points > 0:
                    self.active_char.move(1, 0)
                    self.active_char.stepBack()

    def turnTransitionManager(self):
        if self.current_phase == PhaseState.ENDPHASE:
            if self.current_turn == TurnState.PLAYERTURN:
                self.enemyTurnTransition()
                self.movePhaseTransition()

                for ply in self.team_enemy:
                    ply.resetPos()
                    ply.resetAmmo()
                    ply.resetSteps()

                for ply in self.team_player:
                    ply.cancelSword()

                self.active_char = self.enemy_1

            elif self.current_turn == TurnState.ENEMYTURN:
                self.playerTurnTransition()
                self.movePhaseTransition()

                for ply in self.team_player:
                    ply.resetPos()
                    ply.resetAmmo()
                    ply.resetSteps()

                for ply in self.team_enemy:
                    ply.cancelSword()

                self.active_char = self.player_1

    def playerManager(self, event: pyasge.ClickEvent):
        """Manages switching between characters"""
        self.activeCSelect(event, TurnState.PLAYERTURN, self.team_player)
        self.activeCSelect(event, TurnState.ENEMYTURN, self.team_enemy)

    def activeCSelect(self, event, turn, team):
        """Selects Characters"""
        if self.current_turn == turn:
            for ply in team:
                if ply.sprite.getWorldBounds().v1.x < event.x < ply.sprite.getWorldBounds().v2.x and \
                        ply.sprite.getWorldBounds().v1.y < event.y < ply.sprite.getWorldBounds().v4.y:
                    self.active_char = ply

    def playerTurnTransition(self):
        self.fsm_turn.setstate(TurnState.PLAYERTURN)
        self.current_turn = TurnState.PLAYERTURN
        print("Transition to Player's turn")

    def enemyTurnTransition(self):
        self.fsm_turn.setstate(TurnState.ENEMYTURN)
        self.current_turn = TurnState.ENEMYTURN
        print("Transition to Enemy's turn")

    def movePhaseTransition(self):
        self.fsm_phase.setstate(PhaseState.MOVEPHASE)
        self.current_phase = PhaseState.MOVEPHASE
        print("\n" + str(self.current_turn))
        print(str(self.current_phase) + "\n")

    def atkPhaseTransition(self):
        self.fsm_turn.setstate(PhaseState.ATTACKPHASE)
        self.current_phase = PhaseState.ATTACKPHASE
        print("\n" + str(self.current_turn))
        print(str(self.current_phase) + "\n")

    def endPhaseTransition(self):
        self.fsm_phase.setstate(PhaseState.ENDPHASE)
        self.current_phase = PhaseState.ENDPHASE
        print("\n" + str(self.current_turn))
        print(str(self.current_phase) + "\n")
