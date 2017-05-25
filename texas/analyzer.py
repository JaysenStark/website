from enums import ActionType, ActionNames, Round, RoundNames, CardType, CardNames


class Analyzer(object):
    """docstring for Analyzer"""
    
    @classmethod
    def filter(cls, games):
        pass


    @classmethod
    def rebuild_games(cls, records):
        games = []
        for record in records:
            games.append(cls.rebuild_game(record))


    @classmethod
    def rebuild_game(cls, record):
        tp = record.split(":")
        _, hands, betting_histroy, cards_history, scores, players = tp
        player1, player2 = players.split("|")
        score1, score2 = scores.split("|")
        preflop_cards = cards_history.split("/")[0]
        hole1, hole2 = preflop_cards.split("|")

        card_generator = cls.round_cards(cards_history)
        action_generator = cls.betting_actions(betting_histroy)

        # record a list of Actions object
        actions = []

        card_view1 = []
        card_view2 = []

        actions_str = ""
        for action in action_generator:
            if action.type == ActionType.NEXT_ROUND:
                actions_str += "/"
                actions[-1].actions_str += "/"
                actions[-1].round += 1
            else:
                actions_str += action.action_str
                actions.append(Actions(actions_str, action.round))
                

        for i in actions:
            print(i)

        cards = []
        l = list(card_generator)
        for i, card in enumerate(l):
            cards.append(Cards(l[0:i + 1]))

        for i in cards:
            print(i)
           

        res = cls.merge_history(actions, cards)
        print(res)

    @classmethod
    def round_cards(cls, cards_history):
        cards_list = cards_history.split("/")
        for i, card in enumerate(cards_list):
            yield Card(card, Round.PREFLOP + i)


    @classmethod
    def betting_actions(cls, betting_histroy):
        round = Round.PREFLOP

        # yield a null action
        yield Action("", round) 

        part_action = None
        for char in betting_histroy:
            if char == "c":
                if part_action:
                    yield Action(part_action, round)
                    part_action = None
                yield Action(char, round)
            elif char == "f":
                if part_action:
                    yield Action(part_action, round)
                    part_action = None
                yield Action(char, round)
            elif char == "r":
                if part_action:
                    yield Action(part_action, round)
                part_action = "r"
            elif char in "0123456789":
                part_action += char
            elif char == "/":
                if part_action:
                    yield Action(part_action, round)
                    part_action = None
                yield Action("/", round)
                round += 1
        # end for loop
        if part_action:
            yield Action(part_action, round)

    @classmethod
    def merge_history(cls, actions, cards):
        res = []
        for action in actions:
            for card in cards:
                if action.round == card.round:
                    res.append(action.actions_str + ":" + card.cards_str)
                    break
        return res


class Action():

    def __init__(self, action_str, round=None):
        self.action_str = action_str
        self.round = round
        if action_str == "":
            self.round = Round.PREFLOP
            self.type = ActionType.EMPTY
        elif action_str == "c" or action_str == "C":
            self.type = ActionType.CALL
        elif action_str == "f" or action_str == "F":
            self.type = ActionType.FOLD
        elif action_str[0] == "r" or action_str[0] == "R":
            self.type = ActionType.RAISE
            self.amount = int(action_str[1:])
        elif action_str == "/":
            self.type = ActionType.NEXT_ROUND
        else:
            raise Exception

    def __str__(self):
        if self.type == ActionType.RAISE:
            return "<action: %s To %s %s>" % (self.type, self.amount, self.round)
        else:
            return "<action: %s %s>" % (self.type, self.round)


class Actions():
    ''' a consquent sequence of Action instance '''
    def __init__(self, actions_str, round):
        self.actions_str = actions_str
        self.round = round
        
    def __str__(self):
        return "<actions : %s %s>" % (self.actions_str, self.round)


class Cards():
    ''' a consquent sequence of Card instance '''
    def __init__(self, cards):
        cards_str = "/".join([card.cards_str for card in cards])
        self.cards_str = cards_str
        self.round = cards[-1].round
        self.cards = cards

    def __str__(self):
        return "<cards : %s %s>" % (self.cards_str, self.round)


class Card():
    ''' a class for cards per round, can be one or two or three cards together '''
    def __init__(self, cards_str, round):
        self.cards_str = cards_str
        if round == Round.PREFLOP:
            self.hole1, self.hole2 = cards_str.split("|")
            self.round = Round.PREFLOP
        elif round == Round.FLOP:
            self.round = Round.FLOP
        elif round == Round.TURN:
            self.round = Round.TURN
        elif round == Round.RIVER:
            self.round = Round.RIVER


    def __str__(self):
        return "<cards: %s %s>" % (self.cards_str, self.round)



g = Analyzer.rebuild_game("STATE:165:r300c/cr900c/cr2025c/cr4554r20000f:8cTd|AhTc/9c7hAd/Qd/Jd:4554|-4554:guest1|hkl")
# for i in g:
#     print(i)

                
# print(Action("r500"))

# Analyzer.rebuild_game("STATE:5:r600f:5d7s|AcKs:-100|100:guest1|hkl")

    