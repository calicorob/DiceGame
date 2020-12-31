from collections import defaultdict
from typing import List


import random 

from dice import ScoreBasedPlayer,Game


def score_based_simulation(player_of_interest_score:int,num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_scores:int=500,score_step:int=50)->float:
    wins = 0
    player_avg_scores = []
    possible_scores = [i for i in range(50,max_player_scores,score_step)]

    for i in range(num_games):
        player_of_interest = ScoreBasedPlayer(player_of_interest_score)  
        players = [ScoreBasedPlayer(random.choice(possible_scores)) for _ in range(num_players-1)] 
        player_avg_scores.append(sum([player.min_score for player in players])/len(players))
        players.append(player_of_interest)
        random.shuffle(players)
        game = Game(players,score_goal)
        game.play()

        if game.winner == player_of_interest:
            wins += 1


    return wins / num_games,sum(player_avg_scores)/len(player_avg_scores)


def turn_based_simulations(scores_to_be_examined:List[int],num_players:int=6,num_games:int=10000,score_goal:int=5000,max_player_scores:int=500,score_step:int=50):
    wins = defaultdict(int)
    
    for score in scores_to_be_examined:
        wins[score] = score_based_simulation(score,num_players=num_players,num_games=num_games,score_goal=score_goal,max_player_scores=max_player_scores,score_step=score_step)
        
    
    return wins
    