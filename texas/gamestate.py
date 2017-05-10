# from . constant import *
# from constant import *
from . pokereval.compare import Compare
from . logging import getLogger
import re
# import Queue

GAMESTATE_DEBUG = True

PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3

FOLD = 4


BIG_BLIND_POSITION = 0
SMALL_BLIND_POSITION = 1

SMALL_BLIND = 50
BIG_BLIND = 100

GAME_STACK = 20000

AGENT = 0
PLAYER = 1

# MAX_ROUNDS_RAISES = [3, 4, 4, 4]

HUNLGamestateLogger = getLogger('HUNLGamestate')

class GameState():

    def __init__(self):
        self.msg = ''
        self.score = 0
        self.spent = 0
        self.opponent_spent = 0
        self.hole = []
        self.opponent_hole = []
        self.public_cards = []
        self.showdown = False
        self.gameover = False

        self.round = -1
        self.position = -1
        self.hand_number = -1
        self.player_turn = None
        self.player_folded = None
        self.min_noLimit_raiseTo = 0
        # self.recent_five_action = Queue.Queue(maxsize = 5)
        self.half_pot = 0
        self.one_pot = 0

    def get_recent_five_action(self,msg):
        msg_str = msg.strip('\r\n')
        tp = msg_str.split(':')
        hand_number = int(tp[2])
        #if hand_number > self.hand_number: # game over ,new hand


    def update(self, msg):
        #get_recent_five_action(self,msg)


        self.msg = msg.strip('\r\n')
        tp = self.msg.split(':')
        self.position = int(tp[1])
        self.hand_number = int(tp[2])

        self.betting_history = tp[3]
        self.round = self.betting_history.count('/')
        self.betting_list = self.betting_history.split('/')

        cards = tp[4]
    
        agent_hole_str = cards.split('/')[0].split('|')[self.position]
        self.hole = [agent_hole_str[idx:idx+2] for idx in
         range(0, len(agent_hole_str), 2)]

        public_cards_str = ''.join(cards.split('/')[1:])
        self.public_cards = [public_cards_str[idx:idx+2] for idx in
         range(0, len(public_cards_str), 2)]

        # update spent according to betting_history    
        SMALL_BLIND_SPENT = 50
        BIG_BLIND_SPENT = 100

        if self.betting_history == '':
            if self.position == BIG_BLIND_POSITION:
                self.spent = BIG_BLIND_SPENT
                self.opponent_spent = SMALL_BLIND_SPENT
            elif self.position == SMALL_BLIND_POSITION:
                self.spent = SMALL_BLIND_SPENT
                self.opponent_spent = BIG_BLIND_SPENT

        for round in range(self.round +1 ):
            if round == PREFLOP: # SMALL_BLIND_POSITION goes first
                current_betting_round = self.betting_list[round]
                r = re.compile('[a-z]\d*')
                current_betting_round_list = r.findall(current_betting_round)
                for idx in range(len(current_betting_round_list)):
                    action = current_betting_round_list[idx]
                    if idx % 2 == 0: # it is action from small blind position
                        if action[0] == 'c':
                            SMALL_BLIND_SPENT = BIG_BLIND_SPENT
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                        elif action[0] == 'r':
                            action_size = int(action[1:])
                            SMALL_BLIND_SPENT = action_size
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                            if action_size + action_size - max(self.opponent_spent, self.spent) > self.min_noLimit_raiseTo:
                                self.min_noLimit_raiseTo = action_size + action_size - max(self.opponent_spent, self.spent)
                        else:  #fold
                            pass
                    else:
                        if action[0] == 'c':
                            BIG_BLIND_SPENT = SMALL_BLIND_SPENT
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                        if action[0] == 'r':
                            action_size = int(action[1:])
                            BIG_BLIND_SPENT = action_size
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                            if action_size + action_size - max(self.opponent_spent, self.spent) > self.min_noLimit_raiseTo:
                                self.min_noLimit_raiseTo = action_size + action_size - max(self.opponent_spent, self.spent)

                        else:   #fold
                                pass
            else:
                current_betting_round = self.betting_list[round]
                r = re.compile('[a-z]\d*')
                current_betting_round_list = r.findall(current_betting_round)
                for idx in range(len(current_betting_round_list)):
                    action = current_betting_round_list[idx]
                    if idx % 2 != 0: # it is action from small blind position
                        if action[0] == 'c':
                            SMALL_BLIND_SPENT = BIG_BLIND_SPENT
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                        elif action[0] == 'r':
                            action_size = int(action[1:])
                            SMALL_BLIND_SPENT = action_size
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                            if action_size + action_size - max(self.opponent_spent, self.spent) > self.min_noLimit_raiseTo:
                                self.min_noLimit_raiseTo = action_size + action_size - max(self.opponent_spent, self.spent)
                        else:  #fold
                            pass
                    else:
                        if action[0] == 'c':
                            BIG_BLIND_SPENT = SMALL_BLIND_SPENT
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                        if action[0] == 'r':
                            action_size = int(action[1:])
                            BIG_BLIND_SPENT = action_size
                            if self.position == BIG_BLIND_POSITION:
                                self.spent = BIG_BLIND_SPENT
                                self.opponent_spent = SMALL_BLIND_SPENT
                            elif self.position == SMALL_BLIND_POSITION:
                                self.spent = SMALL_BLIND_SPENT
                                self.opponent_spent = BIG_BLIND_SPENT
                            if action_size + action_size - max(self.opponent_spent, self.spent) > self.min_noLimit_raiseTo:
                                self.min_noLimit_raiseTo = action_size + action_size - max(self.opponent_spent, self.spent)

                        else:   #fold
                            pass

        #  update min_noLimit_raiseTo see if the round or game has ended
        if self.betting_list[-1] == '':
            print("new Round ")
            self.min_noLimit_raiseTo = 1
            if self.min_noLimit_raiseTo < BIG_BLIND:
                self.min_noLimit_raiseTo = BIG_BLIND
            # we finished we finished at least one round, so raise-to = raise-by + maxSpent
            self.min_noLimit_raiseTo += max(self.opponent_spent, self.spent)


        self.showdown = self.is_showdown()
        self.fold = self.is_fold()
        self.gameover = self.is_gameover()
        self.player_turn = self.is_player_turn()
        if self.gameover:
            if self.showdown:
                opponent_hole_str = cards.split('/')[0].split('|')[1 - self.position]
                self.opponent_hole = [opponent_hole_str[idx:idx+2] for idx in
                 range(0, len(opponent_hole_str), 2)]

                # compare cards to decide winner, and update score
                ret = Compare.compare(self.hole, self.opponent_hole, self.public_cards)
                if ret > 0:
                    self.score += self.opponent_spent
                elif ret < 0:
                    self.score -= self.spent
                else:
                    pass
            elif self.fold:
                print('someone_folded')
                if self.is_player_folded():
                    # print('self folded')
                    self.score -= self.spent
                else:
                    # print('ai folded')
                    self.score += self.opponent_spent
            else:
                raise Exception

        # todo valid actions
        self.actions = self.valid_actions()

    def is_player_folded(self):
        return self.spent < self.opponent_spent
        
    def is_player_turn(self):
        if self.gameover:
            return None
        if self.round == PREFLOP:
            current_betting_round = self.betting_history
            r = re.compile('[a-z]\d*')
            current_betting_round_list = r.findall(current_betting_round)
            return not len(current_betting_round_list) % 2 == self.position
        else:
            current_betting_round = self.betting_history.split('/')[-1]
            r = re.compile('[a-z]\d*')
            current_betting_round_list = r.findall(current_betting_round)
            return len(current_betting_round_list) %2 == self.position
        
    def is_gameover(self):
        return self.showdown or self.fold

    def is_showdown(self):
        if self.round < RIVER:
            return False
        river_round_history = self.betting_history.split('/')[-1]
        if river_round_history.count('c') >= 2:
            return True
        if river_round_history.count('c') == 1 and not river_round_history[0] == 'c':
            return True
        if self.spent == GAME_STACK and self.opponent_spent == GAME_STACK:
            return True
        return False

    def is_fold(self):
        return 'f' in self.betting_history

    def is_raise_vaild(self):
        current_betting_round = self.betting_history.split('/')[-1]
        raise_counts = current_betting_round.count('r')
        if raise_counts >= 64: #out of the array
            return False,0
        if self.min_noLimit_raiseTo > GAME_STACK:
            if max(self.opponent_spent,self.spent) > GAME_STACK:
                return False,0
            else:
                self.min_noLimit_raiseTo = GAME_STACK
        return True, self.min_noLimit_raiseTo



    def valid_actions(self):
        if self.gameover:
            return ['next']
        else:
            if self.opponent_spent == self.spent:
                l = ['check']
            else:
                l = ['call']
            # return ['call/check', 'raise/bet', 'fold']
            if self.spent < self.opponent_spent:
                l.append('fold')
            if self.is_half_pot_raise_vaild():
                l.append('half_pot')
            if self.is_pot_raise_vaild():
                l.append('one_pot')
            l.append('all_in')
            can_raise, min_size = self.is_raise_vaild()
            if can_raise == True:
                l.append('min_bet')
                l.append('bet_to')
                # l.append('bet'+str(min_size)+','+str(GAME_STACK))
            # print(l)
            return l


    def is_half_pot_raise_vaild(self):
        pot = self.spent + self.opponent_spent
        # print pot
        pot += abs(self.spent - self.opponent_spent)
        # print pot
        half_pot_raiseto = pot/2 + max(self.spent,self.opponent_spent)
        print(half_pot_raiseto)
        if half_pot_raiseto > GAME_STACK:
            return False
        else:
            self.half_pot = half_pot_raiseto
            return True

    def is_pot_raise_vaild(self):
        pot = self.spent + self.opponent_spent
        pot += abs(self.spent - self.opponent_spent)
        pot_raiseto = pot + max(self.spent,self.opponent_spent)
        print(pot_raiseto)
        if pot_raiseto > GAME_STACK:
            return False
        else:
            self.one_pot = pot_raiseto
            return True

    def construct_response(self, action, amount):
        if action == 'fold':
            return self.msg + ":" + "f" + "\r\n"
        elif action == 'call':
            return self.msg + ":" + "c" + "\r\n"
        elif action == 'check':
            return self.msg + ":" + "c" + "\r\n"
        elif action == 'min_bet':
            return self.msg + ":" + 'r' + str(self.min_noLimit_raiseTo) + "\r\n"
        elif action == 'half_pot': 
            print('half-pot')
            return self.msg + ":" + 'r' + str(self.half_pot) + "\r\n"
        elif action == 'one_pot':
            return self.msg + ":" + 'r' + str(self.one_pot) + "\r\n"
        elif action == 'all_in':
            print(self.msg + ":" + 'r' + str(20000) + "\r\n")
            return self.msg + ":" + 'r' + str(20000) + "\r\n"
        elif action == 'bet_to':
            return self.msg + ":" + 'r' + str(amount) + "\r\n"


    def to_dict(self):
        d = {}
        d['message'] = self.msg
        d['score'] = self.score
        d['spent'] = self.spent
        d['opponent_spent'] = self.opponent_spent
        d['hole'] = self.hole
        d['public_cards'] = self.public_cards
        d['opponent_hole'] = self.opponent_hole
        
        d['showdown'] = self.showdown
        d['gameover'] = self.gameover
        d['round'] = self.round
        d['player_turn'] = self.player_turn
        d['actions'] = self.actions
        d['min_bet'] = self.min_noLimit_raiseTo
        return d

    def reset(self):
        self.msg = ''
        # self.score = 0
        self.spent = 0
        self.opponent_spent = 0
        self.hole = []
        self.opponent_hole = []
        self.public_cards = []
        self.showdown = False
        self.gameover = False

        self.round = -1
        self.position = -1
        self.hand_number = -1
        self.player_turn = None
        self.player_folded = None
        self.min_noLimit_raiseTo = 0
        self.half_pot = 0
        self.one_pot = 0

def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

def main():
    gs = GameState()
    gs.update('MATCHSTATE:1:31:r300r900r3000:|JdTc')
    #gs.is_half_pot_raise_vaild()
    gs.valid_actions()
    #gs.update('MATCHSTATE:1:31:r300r900c/r1800r3600r9000c/r20000c/:KsJs|JdTc/6dJc9c/Kh/Qc')
    # gs.update('MATCHSTATE:0:0:cc/cc/rc/rc:5d5c|9hQd/8dAs8s/4h/6d')
    # gs.update('MATCHSTATE:1:0:cc/:|9hQd/8dAs8s')
    prn_obj(gs)


if __name__ == '__main__':
    main()