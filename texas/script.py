import os, sys
import subprocess
import time
import socket

SRCIPT_DEBUG = True

class Starter():

    def __init__(self, ports=None, quick_start=True):

        if quick_start:
            self.quick_setting(ports)
        else:
            pass

    def setting(self, ports, a_name, p_name, seed):
        self.default_setting() # server = 0.0.0.0
        self.path_setting(agent=None)
        self.ports_setting(ports)
        self.name_setting(agent_name=a_name, player_name=p_name)
        self.game_setting(rng_seed=seed)
        self.command_setting()


    def default_setting(self):
        self.server = '0.0.0.0'

    def quick_setting(self, ports):
        
        self.default_setting()
        self.path_setting()
        self.ports_setting(ports)
        self.name_setting()
        self.game_setting()
        self.command_setting()

    def game_setting(self, game=None, match_name='default_match_name', hand_number=1000, rng_seed=0):
        if game:
            pass # todo, set game_path for game
        else:
            self.game_path = './texas/game/holdem.limit.2p.reverse_blinds.game'

        self.match_name = match_name
        self.hand_number = hand_number
        self.rng_seed = rng_seed

    def name_setting(self, agent_name='default_agent_name', player_name='default_player_name'):
        self.agent_name = agent_name
        self.player_name = player_name

    def path_setting(self, agent = None):
        self.dealer_path = './texas/program/dealer'
        # self.proxy_path = './program/dealerproxy.py'
        # self.proxy_path = './texas/dealerproxy.py'
        if agent:
            pass # todo, set path for given agent
        else:
            self.agent_path = './texas/program/example_player'

    def command_setting(self):
        self.dealer_command = '%s %s %s %d %d %s %s -p %d,%d' % (self.dealer_path, self.match_name, 
            self.game_path, self.hand_number, self.rng_seed, self.agent_name, self.player_name, 
            self.right_agent_port, self.right_player_port)
        

        self.agent_command = '%s %s %s %d' % (self.agent_path, self.game_path, self.server, self.right_agent_port)
       


    def ports_setting(self, ports):
        self.right_agent_port = ports[0]
        self.right_player_port = ports[1]

    def start_acpc_dealer(self, command):
        subprocess.Popen(command, shell=True)
        # if SRCIPT_DEBUG:
        #     logging.debug('Dealer started.')

    def start_proxy(self, command):
        subprocess.Popen(command, shell=True)
        # if SRCIPT_DEBUG:
        #     logging.debug('Proxy started.')

    def start_agent(self, command):
        subprocess.Popen(command, shell=True)
        # if SRCIPT_DEBUG:
        #     logging.debug('Agent started.')

    def quick_start(self):
        self.start_acpc_dealer(self.dealer_command)
        time.sleep(0.2)
        
        print('acpc staarted!')
        # time.sleep(5)
        player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_socket.connect(('0.0.0.0', self.right_player_port)) 
        player_socket.send(b'VERSION:2.0.0\r\n')
        return player_socket

def main(argv=None):
    if argv == None:
        argv = sys.argv

    ports = [int(x) for x in argv[1:]]
    
    starter = Starter(ports)
    starter.quick_start()
    

if __name__ == '__main__':
    main()
    
    