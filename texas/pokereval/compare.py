from . hand_evaluator import HandEvaluator
from . card import Card
import random

str_to_rank = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
    'T':10, 'J':11, 'Q':12, 'K': 13, 'A': 14}

str_to_suit = {'c':1, 'd':2, 'h':3, 's':4}


class Compare():

    def compare(hole1, hole2, public_cards):
        hand1 = Compare.make_cards(hole1)
        hand2 = Compare.make_cards(hole2)
        board = Compare.make_cards(public_cards)
        score1 = HandEvaluator.evaluate_hand(hand1, board)
        score2 = HandEvaluator.evaluate_hand(hand2, board)
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            return 0

    def make_cards(cards):
        res = []
        for card in cards:
            rank = str_to_rank[card[0]]
            suit = str_to_suit[card[1]]
            res.append(Card(rank, suit))
        return res




