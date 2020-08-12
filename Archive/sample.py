#from cardClass import CARD

#card1 = CARD(cardName = "Fatal Push") 
#card1.populateInfo()
#card1.printInfo

class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
d.add_trick('roll over')
print(d.tricks)