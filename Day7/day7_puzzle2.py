#
# Day 7 Puzzle 1
#
from enum import Enum

hands = []
total = 0

class Card:
    def __init__(self,value):
        self.value = value
    def __lt__(self, other):
        if self.value == 'J':
            return True
        if other.value == 'J':
            return False
        if self.value == 'A':
            return False
        if self.value == 'K':
            if other.value in 'QT98765432':
                return False
            return True
        if self.value == 'Q':
            if other.value in 'T98765432':
                return False
            return True
        if self.value == 'T':
            if other.value in '98765432':
                return False
            return True
        if other.value in 'AKQT':
            return True
        return int(self.value) < int(other.value)

class CardGroup:
    def __init__(self, value):
        self.numCards = 0
        self.value = value
    def __str__(self):
        return self.value + "-" + str(self.numCards) + " "
    
class CardGroups:
    def __init__(self):
        self.cardGroups = []
    def __str__(self):
        string = ""
        for card in self.cardGroups:
            string += str(card)
        return string
    
    def addGroup(self, card):
        if len(self.cardGroups) == 0:
            self.cardGroups.append(CardGroup(card))
        else:
            i = 0
            while i < len(self.cardGroups) and card > self.cardGroups[i].value:
                i += 1
            self.cardGroups.insert(i+1, CardGroup(card))

    def findGroup(self, card):
        for i in range(0, len(self.cardGroups)):
            if card == self.cardGroups[i].value:
                return i
        return -1

    def addCard(self, card):
        i = self.findGroup(card)
        if i != -1:
            self.cardGroups[i].numCards += 1
        return self.cardGroups[i].numCards
        
    def getMaxCard(self):
        maxCard = 0
        index = 0
        while index < len(self.cardGroups):
            if self.cardGroups[index].numCards > maxCard:
                if self.cardGroups[index].value != 'J':
                    maxCard = self.cardGroups[index].numCards
            index += 1
        return maxCard

def determineNewType(handType, newNumCard):
    if newNumCard == 2:
        if handType == HandType.HIGH_CARD:
            handType = HandType.ONE_PAIR
        elif handType == HandType.ONE_PAIR:
            handType = HandType.TWO_PAIRS
        elif handType == HandType.THREE_OF_A_KIND:
            handType = HandType.FULL_HOUSE
    elif newNumCard == 3:
        if handType == HandType.HIGH_CARD:
            handType = HandType.THREE_OF_A_KIND
        if handType == HandType.ONE_PAIR:
            handType = HandType.THREE_OF_A_KIND
        elif handType == HandType.TWO_PAIRS:
            handType = HandType.FULL_HOUSE
    elif newNumCard == 4:
        handType = HandType.FOUR_OF_A_KIND
    elif newNumCard == 5:
        handType = HandType.FIVE_OF_A_KIND
    return handType

class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
    def __lt__(self, other):
        return self.value < other.value
    
class Hand:
    def __init__(self, cardsStr, bet):
        self.cards = cardsStr
        self.bet = bet
        self.handType = HandType.HIGH_CARD
        self.cardGroups = CardGroups()
        self.numWildcard = 0
        i = 0
        for card in cardsStr:
            if self.cardGroups.findGroup(card) == -1:
                self.cardGroups.addGroup(card)
            newNumCard = self.cardGroups.addCard(card)
            i += 1
            if card == 'J':
                self.numWildcard += 1
                continue
            self.handType = determineNewType(self.handType, newNumCard)
        if self.numWildcard != 0:
            maxCards = self.cardGroups.getMaxCard()
            maxCards += self.numWildcard
            if maxCards > 5:
                maxCards = 5
            self.handType = determineNewType(self.handType, maxCards)

    def __str__(self):
        return "bet:" + str(self.bet) + " " + str(self.handType) + " "+ str(self.cardGroups)
    
    def __lt__(self, other):
        if self.handType != other.handType:
            return self.handType < other.handType
        else:
            for i in range(0, len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return Card(self.cards[i]) < Card(other.cards[i]) 
            
def insertHand(handStr, bet):
    hand = Hand(handStr,bet)
    if len(hands) == 0:
        hands.append(hand)
    else:
        i = 0
        while i < len(hands) and hand > hands[i]:
            i += 1
        hands.insert(i, hand)

file = open('Day7/input2.txt', 'r')
Lines = file.readlines()
for line in Lines:
    deck=line.split()
    handStr=deck[0]
    bet=int(deck[1])
    insertHand(handStr, bet)

total = 0
factor = 1
for hand in hands:
    print(hand.handType,hand.cards, factor, hand.bet)
    total += hand.bet * factor
    factor += 1
print(total)