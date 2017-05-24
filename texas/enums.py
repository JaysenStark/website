from enum import IntEnum

class ActionType(IntEnum):

    CALL = 0
    RAISE = 1
    FOLD = 2

class Round(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


ActionNames = {
    ActionType.CALL : "CALL",
    ActionType.RAISE : "RAISE",
    ActionType.FOLD : "FOLD",
}

RoundNames = {
    Round.PREFLOP : "PREFLOP",
    Round.FLOP : "FLOP",
    Round.TURN : "TURN", 
    Round.RIVER : "RIVER", 
}

