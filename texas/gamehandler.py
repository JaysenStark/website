import select
import random
import time

from . dumbscript import Starter
from . gs import GameState
import logging

class GameHandler():
    
    game_pool = {}
    random.seed(time.time())

    # start dealer, agent and connect to dealer
    def start(username):
        # gen two ports
        ports = GameHandler.generate_ports()

        # gen seed for dealer
        seed = GameHandler.generate_seed()

        # start dealer, agent, connect player to dealer
        starter = Starter(ports, False)
        starter.setting(ports, 'hkl', username, seed)
        player_socket = starter.quick_start()
        gamestate = GameState()
        game = Game(username, gamestate, player_socket)
        GameHandler.game_pool[username] = game

    def try_receive(connection):
        readable = select.select([connection],[],[], 0.5)[0]
        if readable:
            return GameHandler.receive(connection)
        else:
            return None

    def receive(connection) -> str:
        s = connection
        msg = ''

        while True:
            part_msg = s.recv(1)
            msg += part_msg.decode()

            # check if full message received
            count = msg.count("\n")

            if count < 1:
                continue
            elif count == 1 and msg.endswith("\n"):
                # ignore comment message, gui message
                if msg.startswith("#") or msg.startswith(";"):
                    pass # todo
                msg = msg.strip("\r\n")
                print(msg)
                return msg
            else:
                raise Exception

    def send(connection, string):
        print('type', type(string))
        connection.send(string.encode())

    def generate_ports(number=2):
        ports = []
        for i in range(number):
            ports.append(random.randint(2000, 10000))
        return ports

    def generate_seed():
        return random.randint(1,1000)

    def advanced_update_gamestate(username, msg):
        game = GameHandler.game_pool[username]
        game.gamestate.update(msg)
        logging.debug(game.gamestate.to_dict())

    def advanced_reset_gamestate(username):
        game = GameHandler.game_pool[username]
        game.gamestate.reset()

    def advanced_gamestate_to_dict(username):
        game = GameHandler.game_pool[username]
        return game.gamestate.to_dict()

    def advanced_receive(username):
        game = GameHandler.game_pool[username]
        player_socket = game.player_socket
        return GameHandler.receive(player_socket)


    def advanced_send(username, response):
        game = GameHandler.game_pool[username]
        player_socket = game.player_socket
        GameHandler.send(player_socket, response)

    def advanced_send_action(username, context):
        game = GameHandler.game_pool[username]
        player_socket = game.player_socket
        response = game.gamestate.construct_response(context['action'], context['amount'])
        print('resp constructed by gs:', response)
        GameHandler.advanced_send(username, response)

    def advanced_try_receive(username):
        game = GameHandler.game_pool[username]
        print(game)
        player_socket = game.player_socket
        return GameHandler.try_receive(player_socket)


class Game():

    def __init__(self, username, gamestate, player_socket):
        self.username = username
        self.gamestate = gamestate
        self.player_socket = player_socket


    
print(GameHandler.generate_seed(), GameHandler.generate_ports())