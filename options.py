import pyasge
from gamestate import GameState, GameStateID
from gamedata import GameData


class Options(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.user_clicked = False
        self.user_quit = False
        self.id = GameStateID.GAME_OVER
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click)

        self.main_font = self.data.renderer.loadFont("/data/fonts/kenvector_future.ttf", 15)
        self.title_font = self.data.renderer.loadFont("/data/fonts/Augusta.ttf", 100)
        self.status_font = self.data.renderer.loadFont("/data/fonts/Augusta.ttf", 50)

        self.title_text = pyasge.Text(self.title_font, "Tactics!")
        self.title_text.colour = pyasge.COLOURS.BLACK
        self.title_text.position = (512 - self.title_text.width / 2, 100)

        self.return_button = pyasge.Sprite()
        self.return_button.loadTexture("/data/images/buttonLong_blue.png")
        self.return_button.scale = 1.2
        self.return_button.x = 1020 - self.return_button.width * 1.2
        self.return_button.y = 764 - self.return_button.height * 1.2
        self.return_button.z_order = 10

        self.return_text = pyasge.Text(self.main_font, "  Enter/Start  \n"
                                                       " Return to game! ")
        self.return_text.colour = pyasge.COLOURS.GOLD
        self.return_text.position = (self.return_button.x + 25, self.return_button.y + 25)
        self.return_text.z_order = 40

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_ENTER: False,
            pyasge.GamePad.START: False,
        }

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_ENTER] or self.keys[pyasge.GamePad.START] or self.user_clicked:
            self.user_clicked = True
            return GameStateID.GAMEPLAY

        return GameStateID.OPTIONS

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.title_text)
        self.data.renderer.render(self.return_button)
        self.data.renderer.render(self.return_text)

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def click(self, event: pyasge.ClickEvent) -> None:
        return_bounds = self.return_button.getWorldBounds()
        if return_bounds.v1.x < event.x < return_bounds.v2.x:
            if return_bounds.v1.y < event.y < return_bounds.v4.y:
                self.user_clicked = True
