from card import Card
import random
from hand_evaluator import HandEvaluator

class Deck():

    def __init__(self):

        self.deck = []
        for rank in range(2, 14+1):
            for suit in range(1, 4+1):
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def prepare_cards(self):
        self.shuffle()
        hand1 = self.deck[0:2]
        hand2 = self.deck[2:4]
        board = self.deck[4:9]
        return (hand1, hand2, board)

def test():
    d = Deck()
    for i in range(1000):
        hand1, hand2, board = d.prepare_cards()
        score1 = HandEvaluator.evaluate_hand(hand1, board)
        score2 = HandEvaluator.evaluate_hand(hand2, board)
        print(score1, score2)

test()
