import os, sys
import subprocess
import time
import socket

from . script_for_hkl import start_hkl


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
        time_str = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) 
        m_name = '[%s]vs[%s]at[%s]' % (a_name, p_name, time_str)
        self.game_setting(rng_seed=seed, match_name=m_name)
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
            self.game_path = './texas/game/holdem.nolimit.2p.reverse_blinds.game'

        self.match_name = match_name
        self.hand_number = hand_number
        self.rng_seed = rng_seed

    def name_setting(self, agent_name='default_agent_name', player_name='default_player_name'):
        self.agent_name = agent_name
        self.player_name = player_name

    def path_setting(self, agent = None):
        self.dealer_path = './texas/program/dealer'        

    def command_setting(self):
        self.dealer_command = '%s %s %s %d %d %s %s -p %d,%d' % (self.dealer_path, self.match_name, 
            self.game_path, self.hand_number, self.rng_seed, self.agent_name, self.player_name, 
            self.right_agent_port, self.right_player_port)


    def ports_setting(self, ports):
        self.right_agent_port = ports[0]
        self.right_player_port = ports[1]

    def start_acpc_dealer(self, command):
        subprocess.Popen(command, shell=True)
        
        
    def start_agent(self, command):
        subprocess.Popen(command, shell=True)
      

    def quick_start(self):
        print(self.dealer_command)
        self.start_acpc_dealer(self.dealer_command)
        time.sleep(0.2)
       
        # self.start_agent(self.agent_command)
        start_hkl(self.right_agent_port)
        
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
