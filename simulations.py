"""
    Module for simulating Dice games
    Author: Robert Currie
    Date: December 30, 2020 #rip2020

"""


## library imports 
from collections import defaultdict ## holds results
from typing import List ## for type hinting 

## for shuffling 
import random 

## dice game imports 
from dice import ScoreBasedPlayer, TurnBasedPlayer ,Game


def score_based_simulation(player_of_interest_score:int,num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_scores:int=500,score_step:int=50):
    """
        Runs a simulation of Dice games where the players are all ScoreBased 
        
        Args:
            player_of_interest_score (int): score of player you'd like to simulate in the games
            e.g. 300 = player who rolls till 300
            
            num_players (int): number of players including the player of interest who will participate in the game
            
            num_games (int): number of games to be played
            
            score_goal (int) : final_score of the game object
            
            max_player_scores (int): maximum possible value the other players will try and roll to
            e.g. 500 = maximum score another random player will roll till is 500
            
            score_step (int): step for creating the possible choices that the other players will use 
            
       Returns:
           tuple of win pct of player of interest and the average min_score the other players had 
    
    
    """
    
    ## check there are atleast two players in the game 
    
    assert num_players > 1, "Insufficient number of players"
    
    ## setting the wins of the player of interest
    wins = 0
    
    ## list for holding the minimum scores of the other players 
    player_avg_scores = []
    
    ## generate list of possible scores the other players will attempt to roll to 
    possible_scores = [i for i in range(50,max_player_scores,score_step)]

    
    ## play the games
    for i in range(num_games):
        
        ## generate a player object which we are inteested in
        player_of_interest = ScoreBasedPlayer(player_of_interest_score) 
        ## generate the other players
        players = [ScoreBasedPlayer(random.choice(possible_scores)) for _ in range(num_players-1)] 
        ## note the minimum scores of the other players 
        player_avg_scores.append(sum([player.min_score for player in players])/len(players))
        ## append the player of interest
        players.append(player_of_interest)
        ## shuffle the players
        random.shuffle(players)
        ## create the game
        game = Game(players,score_goal)
        ## play the game
        game.play()

        ## if the winner is the player of interest, increment the number of wins by 1
        if game.winner == player_of_interest:
            wins += 1

    # return the results 
    return wins / num_games,sum(player_avg_scores)/len(player_avg_scores)


def score_based_simulations(scores_to_be_examined:List[int],num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_scores:int=500,score_step:int=50):
    """
        Runs multiple simulations of the Dice game for ScoreBasedPlayer 
        Args:
            scores_to_be_examined (list[int]): scores of player you'd like to simulate in the games
            e.g. [50,100,150] simulates games for ScoreBasedPlayers who roll till 50, 100, 150 respectively 
            
            num_players (int): number of players including the player of interest who will participate in the game
            
            num_games (int): number of games to be played
            
            score_goal (int) : final_score of the game object
            
            max_player_scores (int): maximum possible value the other players will try and roll to
            e.g. 500 = maximum score another random player will roll till is 500
            
            score_step (int): step for creating the possible choices that the other players will use 
            
       Returns:
           dictionary with key, value pairing of score of the player of interest and win pct of player of interest and the average min_score the other players had, respectively 
    
    """
    
    
    ## create the dictionary to hold the results
    wins = defaultdict(int)
    
    ## loop through the scores and run the simulations 
    for score in scores_to_be_examined:
        wins[score] = score_based_simulation(score,num_players=num_players,num_games=num_games,score_goal=score_goal,max_player_scores=max_player_scores,score_step=score_step)
        
    
    return wins
    
def turn_based_simulation(player_of_interest_turns:int,num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_turns:int=10):
    
    """
        Runs a simulation of Dice games where the players are all Turnbased 
        
        Args:
            player_of_interest_turns (int): turns of the player you'd like to simulate in the games
            e.g. 3 = player who rolls till 300
            
            num_players (int): number of players including the player of interest who will participate in the game
            
            num_games (int): number of games to be played
            
            score_goal (int) : final_score of the game object
            
            max_player_scores (int): maximum possible value the other players will try and roll to
            e.g. 500 = maximum score another random player will roll till is 500
            
            score_step (int): step for creating the possible choices that the other players will use 
            
       Returns:
           tuple of win pct of player of interest and the average min_turns the other players had 
    
    
    """
    assert num_players > 1, "Invalid # of players"
    
    ## setting the # of wins of the player of interest
    wins = 0
    
    ## list for holding the min_turns of the other players
    player_avg_turns = []

    ## simulating the games
    for i in range(num_games):
        ## making the player of interest
        player_of_interest = TurnBasedPlayer(player_of_interest_turns)  
        ## making the other players
        players = [TurnBasedPlayer(random.randint(1,max_player_turns)) for _ in range(num_players-1)] 
        ## saving the other players
        player_avg_turns.append(sum([player.turns for player in players])/len(players))
        
        ## adding the player of interest to the players list
        players.append(player_of_interest)
        
        ## shuffling 
        random.shuffle(players)
        
        ## playing the game
        game = Game(players,score_goal)
        game.play()

        ## if the winner is the player of interest increment the number of wins by 1
        if game.winner == player_of_interest:
            wins += 1


            
    ## return the result 
    return wins / num_games,sum(player_avg_turns)/len(player_avg_turns)


def turn_based_simulations(turns_to_be_examined:List[int],num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_turns:int=10):
    """
        Runs multiple simulations of the Dice game for TurnBasedPlayer 
        Args:
            turns_to_be_examined (list[int]): turns of the player you'd like to simulate in the games
            e.g. [1,2,3] simulates games for TurnBasedPlayers who roll till 1, 2, 3 rolls respectively 
            
            num_players (int): number of players including the player of interest who will participate in the game
            
            num_games (int): number of games to be played
            
            score_goal (int) : final_score of the game object
            
            max_player_scores (int): maximum possible value the other players will try and roll to
            e.g. 500 = maximum score another random player will roll till is 500
            
            score_step (int): step for creating the possible choices that the other players will use 
            
       Returns:
           dictionary with key, value pairing of score of the player of interest and win pct of player of interest and the average min_turns the other players had, respectively 
    
    """
    
    ## dictionary for holding the results
    wins = defaultdict(int)
    
    ## looping through the turns to be examined 
    for turn in turns_to_be_examined:
        wins[turn] = turn_based_simulation(turn,num_players=num_players,num_games=num_games,score_goal=score_goal,max_player_turns=max_player_turns)
        
    
    return wins
    