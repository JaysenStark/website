import random
import time
from . gamestate import GameState
from . communicator import Communicator
from . dumbscript import Starter
from . headsuptexas import NoLimitHeadsUpTexas as Game

class BaseGameHandler():

    random.seed(time.time())


    # start game
    @classmethod
    def start(cls):
        pass

    # generate ports for acpc dealer
    @classmethod
    def generate_ports(cls, number=2):
        ports = []
        while True:
            for i in range(number):
                ports.append(random.randint(1025, 10000))
            if len(set(ports)) == number:
                break
        return ports


    # generate game seed for acpc dealer 
    @classmethod
    def generate_seed(cls):
        return random.randint(1, 1000)


class HeadsUpTexasHandler(BaseGameHandler):
    """mantain game pool, one game per user"""
    game_pool = {}

    @classmethod
    def start(cls, agentname, username):
        ports = cls.generate_ports()
        seed = cls.generate_seed()

        # no matter old game exist or not, overwrite it.

        # user starter to start one game
        starter = Starter(ports, False)
        starter.setting(ports, 'hkl', username, seed)
        player_socket = starter.quick_start()
        gamestate = GameState()
        game = Game(agentname, username, gamestate, player_socket)
        cls.game_pool[username] = game


    @classmethod
    def update_gamestate(cls, username, msg):
        game = cls.game_pool.get(username, None)
        if not game:
            raise Exception
        game.update_gamestate(msg)


    @classmethod
    def reset_gamestate(cls, username):
        game = cls.game_pool.get(username, None)
        if not game:
            raise Exception
        game.reset_gamestate()


    @classmethod
    def send_response(cls, username, context):
        game = cls.game_pool.get(username, None)
        if not game:
            raise Exception

        game.send_response(context)


    @classmethod
    def receive_msg(cls, username):
        game = cls.game_pool.get(username, None)
        if not game:
            raise Exception

        return game.receive_msg()


    @classmethod
    def gamestate_to_dict(cls, username):
        game = cls.game_pool.get(username, None)
        if not game:
            print(cls.game_pool)
            raise Exception
        return game.gamestate_to_dict()


class LimitHeadsUpTexasHandler(HeadsUpTexasHandler):
    pass


class NoLimitHeadsUpTexasHandler(HeadsUpTexasHandler):
    pass

        

