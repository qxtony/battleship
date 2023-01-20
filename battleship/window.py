from os import getpid, kill
from signal import SIGKILL, SIGTERM
from typing import Optional

from battleship.config import server
from battleship.elements import *
from battleship.objects import *
from battleship.resources.load import Screen
from battleship.sockets import Client, data


class BattleShip:
    def __init__(self) -> None:
        self.client = Client()

    def init_data(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((CONFIG.WIDTH, CONFIG.HEIGHT))
        self.clock = pygame.time.Clock()

        self.is_start_screen: bool = True
        self.is_settings_screen: bool = False
        self.is_start_server_screen: bool = False
        self.is_get_server_ip_screen: bool = False

        self.start_game_objects = StartMenu()
        self.settings_objects = SettingsMenu()
        self.start_server_objects = ServerMenu()
        self.get_server_ip_objects = GetServerIPMenu()

        pygame.display.set_caption(CONFIG.TITLE)
        pygame.display.set_icon(Screen.ICON_APPLICATION)
        Screen.BACKGROUND_MUSIC.play(-1)

        self.my_field: Field = None
        self.enemy_field: EnemyField = None
        self.draw_message: str = None

        self.is_two_players_start: bool = False
        self.is_my_turn: bool = False

        self.start_game()

    def start_game(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    kill(getpid(), SIGTERM)
                    kill(getpid(), SIGKILL)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        kill(getpid(), SIGTERM)
                        kill(getpid(), SIGKILL)

                if self.is_start_screen:
                    clicks: List[bool] = [
                        button.check_click(event)
                        for button in self.start_game_objects.get_buttons()
                    ]

                    if clicks[0]:
                        self.is_start_screen = False

                        if not server.allow:
                            self.is_get_server_ip_screen = True

                        else:
                            self.init_fields()

                    elif clicks[1]:
                        self.is_start_screen = False
                        self.is_start_server_screen = True
                        server.allow_reception()
                        self.client.send_message(".")
                        self.start_server_objects.add_user("Вы")

                    elif clicks[2]:
                        self.is_start_screen = False
                        self.is_settings_screen = True

                elif self.is_settings_screen:
                    click: bool = self.settings_objects.back.check_click(event)

                    if click:
                        self.is_start_screen = True
                        self.is_settings_screen = False

                    if variables := self.settings_objects.check_events(event):
                        for name, changed_data in variables.items():
                            if CONFIG.get_property(name) != changed_data:
                                if not check_correct_number(changed_data):
                                    continue

                                self.client.send_message(
                                    f"{name} {changed_data}"
                                )
                                CONFIG.set_property(name, int(changed_data))

                elif self.is_start_server_screen:
                    click: bool = self.start_server_objects.back.check_click(
                        event
                    )

                    if click:
                        self.is_start_screen = True
                        self.is_start_server_screen = False

                elif self.is_get_server_ip_screen:
                    ip_address = self.get_server_ip_objects.get(event)

                    if ip_address:
                        data.SERVER_IP = ip_address
                        self.is_get_server_ip_screen = False
                        self.init_fields()

                else:
                    if event.type == pygame.KEYDOWN:
                        self.on_key_press(event.key)

            self.display_update()
            self.clock.tick(60)

    def init_fields(self):
        self.my_field: Field = Field(*CONFIG.START_FIELD_COORDINATES)
        self.enemy_field: EnemyField = EnemyField(
            *CONFIG.START_ENEMY_FIELD_COORDINATES
        )

        if not server.allow:
            self.client.send_message(".enemy")

    def display_update(self) -> None:
        self.screen.fill(CONFIG.WHITE_COLOR)
        draw_background(self.screen)

        if self.is_start_screen:
            self.start_game_objects.draw(self.screen)

        elif self.is_settings_screen:
            self.settings_objects.update()
            self.settings_objects.draw(self.screen)

        elif self.is_start_server_screen:
            self.start_server_objects.draw(self.screen)

        elif self.is_get_server_ip_screen:
            self.get_server_ip_objects.update()
            self.get_server_ip_objects.draw(self.screen)

        else:
            self.screen.blit(Screen.BACKGROUND, (CONFIG.WIDTH / 10, 10))

            self.my_field.draw(self.screen)
            self.enemy_field.draw(self.screen)

            self.my_field.draw_ships(self.screen)
            draw_message(self.screen, self.draw_message)

            if self.is_two_players_start:
                self.enemy_field.draw_ships(self.screen)

        pygame.display.update()

    def on_key_press(self, pressed_key: int) -> Optional[None]:
        selected_ship: Ship = self.my_field.ships[-1]

        if selected_ship.end_ship:
            if not self.is_my_turn:
                return

            actions: dict = {
                pygame.K_s: self.enemy_field.down,
                pygame.K_w: self.enemy_field.up,
                pygame.K_a: self.enemy_field.left,
                pygame.K_d: self.enemy_field.right,
                pygame.K_RETURN: self.enemy_field.apply,
            }

            if pressed_key in actions:
                if pressed_key == pygame.K_RETURN:
                    actions[pressed_key](self.client)
                    self.is_my_turn = False

                else:
                    actions[pressed_key]()

        else:
            actions: dict = {
                pygame.K_s: selected_ship.up,
                pygame.K_w: selected_ship.down,
                pygame.K_a: selected_ship.left,
                pygame.K_d: selected_ship.right,
                pygame.K_SPACE: selected_ship.rotate,
                pygame.K_RETURN: self.my_field.append_new_ship,
            }

            if pressed_key in actions:
                actions[pressed_key]()

            selected_ship: Ship = self.my_field.ships[-1]

            if selected_ship.end_ship:
                if not self.is_two_players_start:
                    self.draw_message = (
                        "Ожидание расстановки второго игрока..."
                    )
                    self.client.send_message("placement finished")
                    return
