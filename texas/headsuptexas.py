from . basegame import BaseGame
from . communicator import Communicator

class HeadsUpTexas(BaseGame):

    def __init__(self, agentname, username, gamestate, player_socket):
        self.username = username
        self.agentname = agentname
        
        self.gamestate = gamestate
        self.player_socket = player_socket


    def update_gamestate(self, msg):
        print(msg)
        self.gamestate.update(msg)


    def reset_gamestate(self):
        self.gamestate.reset()


    # def get_player_socket(self):
    #     return self.get_player_socket


    def send_response(self, context):
        response = self.construct_response(context)
        Communicator.send_msg(self.player_socket, response)


    def receive_msg(self):
        msg = Communicator.receive(self.player_socket)
        # self.gamestate.update(msg)
        return msg


    def gamestate_to_dict(self):
        return self.gamestate.to_dict()


    def construct_response(self):
        pass


class LimitHeadsUpTexas(HeadsUpTexas):
    
    def construct_response(self):
        pass


class NoLimitHeadsUpTexas(HeadsUpTexas):
    
    # use gamestate to construct response
    # may change in future
    def construct_response(self, context):
        # msg = context['msg']
        action = context['action']
        amount = context['amount']

        return self.gamestate.construct_response(action, amount)

        