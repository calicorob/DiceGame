import random
from collections import defaultdict


scores = {
    
     1:100
    ,2:0
    ,3:0
    ,4:0
    ,5:50
    ,6:0
    
    
}

class Dice(object):
    def roll(self):
        return random.randint(1,6)
    
    
class Player(object):
    pid = 1
    def __init__(self):
        self.pid = Player.pid
        self.isin = False
        self.score = 0
        
        Player.pid +=1 
        
    def __repr__(self):
        return "".join(['pid: ',str(self.pid)," score: ",str(self.score)])
    
    def turn(self):
        self.score += self.play()
        
    def play(self):
        temp_score = 0
        
        if self.isin:
            for turn in range(3):
                roll_score = self.check_score(self.rolls())
                if roll_score == 0:
                    return 0 
                else:
                    temp_score += roll_score
                    
            return temp_score

            
        else:
            for turn in range(3):
                temp_score += self.check_score(self.rolls())
                
            if temp_score >= 300:
                self.isin = True
                return temp_score
            else:
                return 0 
        
        
    def roll(self):
        return Dice().roll()
    
    def rolls(self):
        return [self.roll() for _ in range(3)]
    
    def check_score(self,rolls):
        sorted_rolls = sorted(rolls)
        
        if sorted_rolls[0] == sorted_rolls[-1]:
            if sorted_rolls[0] == 1:
                return sorted_rolls[0] * 1000
            else:
                return sorted_rolls[0] * 100
        else:
            return sum([scores[roll] for roll in rolls])
        
        
class TurnBasedPlayer(Player):
    
    def __init__(self,turns):
        super().__init__()
        self.turns = turns
        
    
    def get_min_turns(self):
        return self.turns
    
    def play(self):
        temp_score = 0
        
        turns = self.get_min_turns()
        if self.isin:
            for turn in range(turns):
                roll_score = self.check_score(self.rolls())
                if roll_score == 0:
                    return 0 
                else:
                    temp_score += roll_score
                    
            return temp_score
        
        else:
            for turn in range(3):
                temp_score += self.check_score(self.rolls())
                
            if temp_score >= 300:
                self.isin = True
                return temp_score
            else:
                return 0
            
class RandomTurnBasedPlayer(TurnBasedPlayer):
    def __init__(self,max_turns_choice:int=20):
        super().__init__(None)
        self.max_turns_choice = max_turns_choice
        
    def get_min_turns(self):
        return random.randint(1,self.max_turns_choice)
        
class ScoreBasedPlayer(Player):
    
    def __init__(self,min_score):
        super().__init__()
        self.min_score = min_score
        
    def get_min_score(self):
        return self.min_score
        
    def play(self):
        temp_score = 0
        min_score = self.get_min_score()
        if self.isin:
            while temp_score < min_score:
                roll_score = self.check_score(self.rolls())
                if roll_score == 0:
                    return 0 
                else:
                    temp_score += roll_score
                    
            return temp_score

            
        else:
            for turn in range(3):
                temp_score += self.check_score(self.rolls())
                
            if temp_score >= 300:
                self.isin = True
                return temp_score
            else:
                return 0
            
class RandomScoreBasedPlayer(ScoreBasedPlayer):
    def __init__(self,max_score_choice:int=500):
        super().__init__(None)
        self.max_score_choice = max_score_choice
        
    def get_min_score(self):
        return random.randrange(50,self.max_score_choice+50,50)

        
class Game(object):
    def __init__(self,players,final_score):
        self.players = players
        self.final_score = final_score
        self.winner = None
        self.over = False
        
    def play(self):
        while not self.over:
            for player in self.players:
                player.turn()
                if player.score >= self.final_score:
                    self.winner = player
                    self.over = True
                    return 
        