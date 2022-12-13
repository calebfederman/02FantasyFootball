#-------------------------------------------------------------------------------------------------#
# Player.py houses the Player class
# Caleb Federman
#-------------------------------------------------------------------------------------------------#

class Player:
    def __init__(self, name, age, team, pos):
        self.name = name
        self.age = age
        self.team = team
        self.pos = pos

    def printAll(player):
        print('{} {} {} {}'.format(player.name,player.age,player.team,player.pos))


players = []


players.append(Player("Sauce Gardner",22,"NYJ","CB"))
players.append(Player("Lamar Jackson",25,"BAL","QB"))

for x in players:
    x.printAll()
