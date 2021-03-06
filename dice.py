"""
    Module for Classes required for the Dice Game
    Author: Robert
    Date: December 30, 2020 #rip2020

"""

## library imports
import random ## used for random number generation
import pandas as pd ## for data manipulation


## dictionary used to hold score values
scores = {

     1:100
    ,2:0
    ,3:0
    ,4:0
    ,5:50
    ,6:0


}


class Dice(object):
    """
        Dice object which can be used to generate random numbers between 1 and 6

    """
    def roll(self):
        """
            Returns a randomly generated number between 1 and 6

            Args:
                None
            Returns:
                integer between 1 and 6

        """
        return random.randint(1,6)


class Player(object):
    """
        Player object which 'plays' the dice game

    """

    ## ID number for identifying different players
    pid = 1
    def __init__(self,isin=False):
        """
            Initializes a Player object

            Args:
                None

            Returns:
                Instance of the Player class

        """
        ## set the instance pid
        self.pid = Player.pid

        ## isin indicator indicates whether or not the player is 'in' the game or not
        self.isin = isin

        ## current score of the player
        self.score = 0

        ## increment Class variable
        Player.pid +=1


        ## initialize list to keep track of isin status
        self.player_statuses = []

        ## initialize list to keep track of rolls player takes
        self.player_rolls = []

        ## initialize list to keep track of scores player scores each turns
        self.player_scores = []

        ## itialie a list to keep track of the number of turns a player plays
        self.turns_taken = 0

        ## initialize list to keep track of turn scores
        self.turn_scores = []



    def __repr__(self):
        """
            Representation method

            Args:
               None
            Returns:
                string representation of the Player instance

        """
        return "".join(['pid: ',str(self.pid)," score: ",str(self.score)])

    def add_player_status(self):
        """
            Appends the current status of the player to a list

            Args:
                None
            Returns:
                None


        """

        self.player_statuses.append(self.get_player_status())

    def get_player_statuses(self):
        """
            Getter method for returning a player's statuses

            Args:
                None

            Returns:
                List of player statuses

        """

        return self.player_statuses.copy()


    def add_player_rolls_taken(self,rolls:int):
        """
            Appends the number of rolls taken by the player to a list

            Args:
                rolls (int): number of rolls the player took
            Returns:
                None


        """

        self.player_rolls.append(rolls)

    def get_player_rolls_taken(self):
        """
            Getter method for returning number of rolls taken by the player for each turn

            Args:
                None

            Returns:
                List of the rolls taken during each turn


        """

        return self.player_rolls.copy()

    def add_turn_score(self,turn_score:int):
        """
            Appends the score of the current turn to a list

            Args:
                turn_score (int): score of the current turn
            Returns:
                None


        """

        self.turn_scores.append(turn_score)

    def get_turn_scores(self):
        """
            Getter method for player's turn scores

            Args:
                None

            Returns:
                List of player's turn scores

        """

        return self.turn_scores.copy()


    def add_player_score(self):


        """
            Appends the current score of the player to a list

            Args:
                None
            Returns:
                None


        """


        self.player_scores.append(self.get_score())


    def get_player_scores(self):
        """
            Getter method for player's list of scores`

            Args:
                None

            Returns:
                List of player scores


        """

        return self.player_scores.copy()

    def add_turn(self):
        """
            Increments the number of turns the player has taken
            Args:
                None
            Returns:
                None

        """

        self.turns_taken +=1

    def get_turns_taken(self):
        """
            Getter method for the number of turns the player has taken

            Args:
                None

            Returns:
                number of turns the player has taken
        """

        return self.turns_taken


    def get_player_status(self):
        """
            Getter method for obtaining the current status of the player


            Args:
                None

            Returns:
                bool, player status


        """

        return self.isin

    def turn(self):
        """
            Player takes a turn, and adds the score of that turn to their cumulative score through the 'play' method

            Args:
                None

            Returns:
                None

        """
        self.score += self.play() ## increment the player's score
        self.add_player_status() ## mark the player's status
        self.add_player_score() ## mark the player's score
        self.add_turn() ## increment the player's turn count


    def get_pid(self):
        """
            Getter method for returning the pid of a player

            Args:
                None

            Returns
                pid of the player (int)

        """

        return self.pid


    def get_stats(self):
        """
            Get the stats of a player

            Args:
                None

            Returns:
                pandas Dataframe of the player's stats


        """

        stats_dict = {

             "PlayerID": self.get_pid()
            ,"TurnsTaken": [i+1 for i in range(self.get_turns_taken())]
            ,"TurnScores":self.get_turn_scores()
            ,"CumulativeScore": self.get_player_scores()
            ,"PlayerStatus":self.get_player_statuses()
            ,"RollsTaken":self.get_player_rolls_taken()

        }


        return pd.DataFrame(data=stats_dict)

    def get_score(self):
        """
            Getter method for the Player's current score

            Args:
                None

            Returns:
                int, player current score


        """

        return self.score

    def play(self):
        """
            Player rolls die

            Args:
                None

            Returns:
                integer, score of that turn


        """
        ## initialize score of that turn
        temp_score = 0

        ## temp variable for storing the number of rolls taken
        rolls_taken = 0


        ## if the player is 'in' the game, roll the die 3 times
        if self.isin:
            for turn in range(3):
                roll_score = self.check_score(self.rolls())
                rolls_taken +=1
                if roll_score == 0: ## if the player fails to score on a roll, end their turn and return 0
                    self.add_player_rolls_taken(rolls_taken)
                    self.add_turn_score(0)
                    return 0
                else: ## add the roll score to their turn score and continue
                    temp_score += roll_score

            self.add_player_rolls_taken(rolls_taken)
            self.add_turn_score(temp_score)
            return temp_score ## return their cumulated turn score

        ## if the player is not in, roll the die 3 times
        ## difference between rolling while 'in' and 'out' is that scoring a 0 on a roll, doesn't end your turn
        else:
            ## TODO make a 1 liner
            for turn in range(3): ## increment the turn score over 3 rolls
                temp_score += self.check_score(self.rolls())
                rolls_taken +=1

            self.add_player_rolls_taken(rolls_taken)

            ## if the player is able to score 300 or more, they are now 'in' the game
            if temp_score >= 300:
                self.isin = True
                self.add_turn_score(temp_score)
                return temp_score
            else:
                self.add_turn_score(0)
                return 0 ## if the player fails to score 300 or more, their score is 0


    def roll(self):
        """
            Method for player to roll a die

            Args:
                None

            Returns:
                integer, random number between 1 and 6

        """
        return Dice().roll()

    def rolls(self):
        """
            Method for rolling 3 die

            Args:
                None

            Returns:
                list of 3 numbers between 1 and 6

        """
        return [self.roll() for _ in range(3)]

    def check_score(self,rolls):
        """
            Checks the score of a roll

            Args:
                rolls (list[int]): list of length 3 integerss

            Returns:
                integer, result of the rolls

        """
        ## check that the length of the list = 3
        assert len(rolls) == 3, "Didn't roll 3 die"


        ## sorts the rolls in ascending? order (can't remember but doesn't matter)
        sorted_rolls = sorted(rolls)

        ## check if the first number is the same as the second number
        ## if it is, you've rolled a triplet
        if sorted_rolls[0] == sorted_rolls[-1]:
            if sorted_rolls[0] == 1: ## if the number is a 1, return 1x1000
                return sorted_rolls[0] * 1000
            else: ## otherwise, return the number rolled x 100
                return sorted_rolls[0] * 100
        else: ## return the score
            return sum([scores[roll] for roll in rolls])


class TurnBasedPlayer(Player):
    """
        Child of the Player class
        TurnBasedPlayer plays the Dice game based on a specified minimum number of rolls
        E.g. If turns = 5 , player will roll the die 5 times and then accept whatever score they have received

    """

    def __init__(self,turns,isin=False):
        """
            Initialize a TurnBasedPlayer

            Args:
                turns (int): number of turns the player will play before ending their turn

            Returns
                Instance of the TurnBasedPlayer class

        """

        ## intialize instance variables according to parent __init__ method
        super().__init__(isin=isin)

        ## number of rolls player will play before ending their turn
        self.turns = turns


    def get_min_turns(self):
        """
            Getter method for the number of turns

            Args:
                None

            Returns:
                int, number of rolls player will play before ending their turn

        """
        return self.turns

    def play(self):

        """
            Player rolls die

            Args:
                None

            Returns:
                integer, score of that turn


        """

        ## temporary score of that turn
        temp_score = 0

        ## temp variable for storing the number of rolls taken
        rolls_taken = 0


        ## get the number of turns this player will attempt
        turns = self.get_min_turns()

        ## only difference between Player and TurnBasedPlayer is the number of rolls it attemps
        if self.isin:
            for turn in range(turns): ## attempt to roll the die the set number of times
                rolls_taken +=1
                roll_score = self.check_score(self.rolls())
                if roll_score == 0:
                    self.add_turn_score(0)
                    self.add_player_rolls_taken(rolls_taken)
                    return 0
                else:
                    temp_score += roll_score

            self.add_player_rolls_taken(rolls_taken)
            self.add_turn_score(temp_score)
            return temp_score

        else:
            for turn in range(3):
                temp_score += self.check_score(self.rolls())

            self.add_player_rolls_taken(rolls_taken)

            if temp_score >= 300:
                self.isin = True
                self.add_turn_score(temp_score)
                return temp_score
            else:
                self.add_turn_score(0)
                return 0

## TODO comment / work on RandomTurnBasedPlayer
class RandomTurnBasedPlayer(TurnBasedPlayer):
    def __init__(self,max_turns_choice:int=20):
        super().__init__(None)
        self.max_turns_choice = max_turns_choice

    def get_min_turns(self):
        return random.randint(1,self.max_turns_choice)





class ScoreBasedPlayer(Player):
    """
        Child of the Player class
        ScoreBasedPlayer plays the Dice game based on a specified minimum score
        E.g. If score = 300 , player will roll the die until they have a turn score of 300 or more

    """
    def __init__(self,min_score,isin=False):

        """
            Initialize a ScoreBasedPlayer

            Args:
                score (int): score the player will attempt to acheive each turn before ending their turn

            Returns
                Instance of the ScoreBasedPlayer class

        """

        ## initialize instance variables using Parent __init__method
        super().__init__(isin=isin)

        ## set the mininmum score the player will attempt to acheive each turn
        self.min_score = min_score

    def get_min_score(self):
        """
            Getter method for the minimum score

            Args:
                None

            Returns:
                int, minimum score player will attempt to roll each turn before ending their turn

        """
        return self.min_score

    def play(self):
        """
            Player rolls die

            Args:
                None

            Returns:
                integer, score of that turn


        """


        ## set score of turn
        temp_score = 0

        ## temp variable for storing the number of rolls taken
        rolls_taken = 0

        ## get minimum score player will attempt to get on this turn
        min_score = self.get_min_score()
        if self.isin:
            while temp_score < min_score: ## continue rolling until the minimum_score or higher is acheived
                roll_score = self.check_score(self.rolls())
                rolls_taken +=1
                if roll_score == 0:
                    self.add_turn_score(0)
                    self.add_player_rolls_taken(rolls_taken)
                    return 0
                else:
                    temp_score += roll_score


            self.add_player_rolls_taken(rolls_taken)
            self.add_turn_score(temp_score)
            return temp_score


        else:
            for turn in range(3):
                temp_score += self.check_score(self.rolls())


            self.add_player_rolls_taken(rolls_taken)


            if temp_score >= 300:
                self.isin = True

                self.add_turn_score(temp_score)
                return temp_score
            else:
                self.add_turn_score(0)
                return 0


## TODO stuff
class RandomScoreBasedPlayer(ScoreBasedPlayer):
    def __init__(self,max_score_choice:int=500):
        super().__init__(None)
        self.max_score_choice = max_score_choice

    def get_min_score(self):
        return random.randrange(50,self.max_score_choice+50,50)


class Game(object):

    """

        Object for playing the dice game


    """
    def __init__(self,players,final_score):

        """
            Initializes an instance of the Game class

            Args:
                players (list[Player]): list, containing instances of the Player class or it's children who will be playing the game
                final_score int: final score that must be acheived in order to win the game

        """

        ## check that all players have not played the game, or are 'in' a game
        assert all(

                [not player.isin for player in players]



        ), "Player is already 'in' a game"


        ## store players
        self.players = players


        ## store the final score
        self.final_score = final_score

        ## set the winner = nobody
        self.winner = None

        ## set the game as to not being complete
        self.over = False


    def get_player_stats(self):
        """
            Getter method which returns the stats of all the players in the game in a DataFrame

            Args:
                None

            Returns:
                pandas Dataframe of all the player stats


        """


        return pd.concat([player.get_stats() for player in self.players],axis=0,sort=True).reset_index(drop=True)

    def play(self):
        """
            Play the game

            Args:
                None
            Returns:
                None

        """

        ## TODO, add functionality where if someone reaches the final score, the other players are given 1 more turn to reach the target score

        ## keep looping until someone reaches the set score
        while not self.over:
            ## loop through the players
            for player in self.players:
                player.turn() ## play a turn
                if player.score >= self.final_score: ## if a player acheives the target score or higher, end the game
                    self.winner = player ## set the winner equal to that player
                    self.over = True ## set the game as over
                    return  ## finish
