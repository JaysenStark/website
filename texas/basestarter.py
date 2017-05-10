from . debug import STARTER_VERBOSE

from . utils import generate_ports
from . communicator import Communicator
from . logging import getLogger
from . script_for_hkl import start_hkl

import subprocess
import time
import socket

starterLogger = getLogger('starter')

class BaseStarter():


    def __init__(self, agent_name, player_name, ports=None):
        self.agent_name = agent_name
        self.player_name = player_name
        self.ports = ports if ports else generate_ports()
        self.server = '0.0.0.0'

    def game_setting(self, game='LimitHeadsUpTexas', hand_number=1000, rng_seed=0):
        
        if game == 'LimitHeadsUpTexas':
            self.game_path = './texas/game/holdem.limit.2p.reverse_blinds.game'
        elif game == 'NoLimitHeadsUpTexas':
            self.game_path = './texas/game/holdem.nolimit.2p.reverse_blinds.game'
        time_str = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) 
        self.match_name = '[%s]vs[%s]at[%s]' % (self.agent_name, self.player_name, time_str)
        self.hand_number = hand_number
        self.rng_seed = rng_seed


    def start(self, command):
        subprocess.Popen(command, shell=True)


class DealerStarter(BaseStarter):
    

    def __init__(self, agent_name, player_name, ports):
        super().__init__(agent_name, player_name, ports)
        self.agent_port = ports[0]
        self.player_port = ports[1]


    def _dealer_setting(self):
        self.dealer_path = './texas/program/dealer'  
        self.dealer_command = '%s %s %s %d %d %s %s -p %d,%d' % (self.dealer_path, self.match_name, 
            self.game_path, self.hand_number, self.rng_seed, self.agent_name, self.player_name, 
            self.agent_port, self.player_port)

    def quick_setting(self, game, hand_number, rng_seed):
        self.game_setting(game, hand_number, rng_seed)
        self._dealer_setting()


    def start(self):
        super().start(self.dealer_command)


class AgentStarter(BaseStarter):


    def __init__(self, agent_name, player_name, ports):
        super().__init__(agent_name, player_name, ports)
        self.agent_port = ports[0]


    def _agent_setting(self):
        if self.agent_name == 'hkl':
            pass
        elif self.agent_name == 'wpc':
            pass
        elif self.agent_name == 'acpc_example':
            pass


    def quick_setting(self):
        self._agent_setting()


    def start(self):
        start_hkl(self.agent_port)


class PlayerStarter(BaseStarter):
    '''connect player to dealer, return connetion'''


    def __init__(self, agent_name, player_name, ports):
        super().__init__(agent_name, player_name, ports)
        self.player_port = ports[1]

    def quick_setting(self):
        self.addr = (self.server, self.player_port)


    def start(self):
        player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_socket.connect(self.addr)
        Communicator.send_binary_msg(player_socket, b'VERSION:2.0.0\r\n')
        return player_socket
        

class QuickStarter(BaseStarter):


    def __init__(self, agent_name, player_name, ports=None):
        super().__init__(agent_name, player_name, ports)


    def quick_setting_and_start(self, game, hand_number, rng_seed):
        self.quick_setting(game, hand_number, rng_seed)
        player_socket = self.quick_start()
        return player_socket


    def quick_setting(self, game, hand_number, rng_seed):

        # currently useless, but still keeps
        self.game = game
        self.hand_number = hand_number
        self.rng_seed = rng_seed


        self.dealer = DealerStarter(self.agent_name, self.player_name, self.ports)
        self.agent = AgentStarter(self.agent_name, self.player_name, self.ports)
        self.player = PlayerStarter(self.agent_name, self.player_name, self.ports)

        self.dealer.quick_setting(self.game, self.hand_number, self.rng_seed)
        self.agent.quick_setting()
        self.player.quick_setting()


    def quick_start(self):
        self.dealer.start()
        time.sleep(0.2)
        self.agent.start()
        player_socket = self.player.start()
        return player_socket