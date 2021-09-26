import pyasge
from gamestate import GameState, GameStateID
from gamedata import GameData


class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.event = None
        self.id = GameStateID.START_MENU
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click)
        self.user_clicked = False
        self.user_quit = False

        self.main_font = self.data.renderer.loadFont("/data/fonts/kenvector_future.ttf", 15)
        self.title_font = self.data.renderer.loadFont("/data/fonts/Augusta.ttf", 100)

        self.title_text = pyasge.Text(self.title_font, "Tactics!")
        self.title_text.colour = pyasge.COLOURS.BLACK
        self.title_text.position = (365, 250)

        self.enter_button = pyasge.Sprite()
        self.enter_button.loadTexture("/data/images/buttonLong_blue.png")
        self.enter_button.scale = 1.2
        self.enter_button.x = 250
        self.enter_button.y = 450
        self.enter_button.z_order = 10

        self.exit_button = pyasge.Sprite()
        self.exit_button.loadTexture("/data/images/buttonLong_blue.png")
        self.exit_button.scale = 1.2
        self.exit_button.x = 550
        self.exit_button.y = 450
        self.exit_button.z_order = 11

        self.text = pyasge.Text(self.main_font, "  Enter/Start \n"
                                                "Start the game!")
        self.text.colour = pyasge.COLOURS.GOLD
        self.text.position = (270, 470)
        self.text.z_order = 50

        self.text_quit = pyasge.Text(self.main_font, "Backspace/Circle\n"
                                                     "  Exit the game!  ")
        self.text_quit.colour = pyasge.COLOURS.GOLD
        self.text_quit.position = (570, 470)
        self.text_quit.z_order = 51

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_ENTER: False,
            pyasge.KEYS.KEY_BACKSPACE: False,

            pyasge.GamePad.CIRCLE: False,
            pyasge.GamePad.START: False,
        }

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        # print("updating gamemenu")
        if self.keys[pyasge.KEYS.KEY_ENTER] or self.keys[pyasge.GamePad.START] or self.user_clicked:
            self.user_clicked = True
            print("Enter pressed")
            return GameStateID.GAMEPLAY
        elif self.keys[pyasge.KEYS.KEY_BACKSPACE] or self.keys[pyasge.GamePad.CIRCLE] or self.user_quit:
            self.user_quit = True
            print("backspace pressed")
            quit()

        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        # print("rendering gamemenu")
        self.data.renderer.setRenderTarget(None)
        self.data.renderer.viewport = pyasge.Viewport(0, 0, 1024, 768)
        self.data.renderer.render(self.title_text)
        self.data.renderer.render(self.enter_button)
        self.data.renderer.render(self.exit_button)
        self.data.renderer.render(self.text)
        self.data.renderer.render(self.text_quit)

    def input(self, event: pyasge.KeyEvent) -> None:
        # print("processing input gamemenu")
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def click(self, event: pyasge.ClickEvent) -> None:
        enter_bounds = self.enter_button.getWorldBounds()
        exit_bounds = self.exit_button.getWorldBounds()
        if enter_bounds.v1.x < event.x < enter_bounds.v2.x:
            if enter_bounds.v1.y < event.y < enter_bounds.v4.y:
                self.user_clicked = True
        if exit_bounds.v1.x < event.x < exit_bounds.v2.x:
            if exit_bounds.v1.y < event.y < exit_bounds.v4.y:
                self.user_quit = True


"""
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                print("Mouse button 1 pressed")
            else:
                print("Mouse button 1 released")
"""
