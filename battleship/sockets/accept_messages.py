from random import randint

from battleship.instance import game


def check_accept_message(message: str) -> None:
    if message == ".enemy":
        game.start_server_objects.add_user("Противник")

    if message == "placement finished":
        if not game.my_field.ships[-1].end_ship:
            game.draw_message = "Противник закончил расстановку кораблей."

        else:
            if randint(0, 1):
                game.draw_message = "Вы начинаете игру."
                game.client.send_message("start game enemy")
                game.is_my_turn = True

            else:
                game.draw_message = "Противник начинает игру."
                game.client.send_message("start game")

            game.is_two_players_start = True
    
    elif message == "start game":
        game.draw_message = "Вы начинаете игру."
        game.is_two_players_start = True
        game.is_my_turn = True

    elif message == "start game enemy":
        game.draw_message = "Противник начинает игру."
        game.is_two_players_start = True

    elif message.startswith("attack"):
        game.draw_message = "Ваш ход."
        x, y = eval(message.split("attack")[1])

        for ship in game.my_field.ships:
            ship_x, ship_y = ship.get_coordinates()

            if ship.orientation == "horizontally":
                if ship.size == 1:
                    ship_x = [ship_x]

                else:
                    ship_x = range(ship_x, ship_x + ship.size)

                ship_y = [ship_y]

            else:
                if ship.size == 1:
                    ship_y = [ship_y]

                else:
                    ship_y = range(ship_y, ship_y + ship.size)

                ship_x = [ship_x]

            if x + 1 in ship_x and y + 1 in ship_y:
                ship.health -= 1
                ship_x, ship_y = ship.get_coordinates()

                game.draw_message = "Ход противника."
                game.client.send_message("hit")
                game.my_field.field_cross.append((x, y))
                game.is_my_turn = False

                if ship.health == 0:
                    orientation = 1 if ship.orientation == "horizontally" else 0
                    game.client.send_message(f"dead ({ship_x}, {ship_y}, {ship.size}, {orientation})")
                    game.my_field.dead_ships.append((ship_x, ship_y, ship.size, ship.orientation))

                    game.enemy_field.ships_counter[ship.size] -= 1

                    if not any(game.enemy_field.ships_counter.values()):
                        game.draw_message = "Вы проиграли..."
                        game.client.send_message("game over")

                break

        else:
            game.client.send_message("miss")
            game.draw_message = "Ваш ход."
            game.is_my_turn = True
            game.my_field.field_dot.append((x, y))

    elif message == "hit":
        game.draw_message = "Ваш ход."
        game.is_my_turn = True
        game.enemy_field.marks.append("cross")

    elif message == "miss":
        game.draw_message = "Ход противника."
        game.enemy_field.marks.append("dot")
    
    elif message.startswith("dead"):
        data = eval(message.split("dead")[1])
        game.draw_message = "Ваш ход."
        game.is_my_turn = True
        game.enemy_field.dead_ships.append(data)
    
    elif message == "game over":
        game.draw_message = "Вы победили!"


def accept_messages() -> None:
    while True:
        message = game.client.accept_messages().decode('utf-8')
        check_accept_message(message)
