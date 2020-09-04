# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:47:44 2020

@author: Kamil
"""

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from time import time
import random
import pandas as pd

def run_simulations(max_simulation_number=2000, variant='Monty Hall', change=True, keep_log=False, fname='simulation.png' ):
    """Function runs number of simulation for different variants of Monty Hall problem to evaluate what is the optimal strategy
        for the Contenstant. It runs 'simulation_number' of simulation where for each of them different number of simulated games
        is conducted. Thanks to that we can see how probability value for specific variant and strategy converge to a specific value. 
        
    Parameters:
    - max_simulation_number (int): Maximum number of simulation with increasing number of iterations
    - variant (str): What variant of the problem to simulate: 'Monty Hall', 'Monty Fall'
    - change (bool): Player's strategy to tackle the problem: True - Chnage, False - Stay
    - keep_log (bool): if to create simulation log, not recommended for huge number of simulations
    
    Returns:
    list: mean probabilities for number of simulation. 
    Data Frame: simulation_log

   """

    columns =  ['simulation_id','game_no','prize_door','players_initial_choice','monty_elimination','players_final_choice','result'] 
    simulation_log = []
    
    # results of simulations
    winning_probability_means = []
    # ids of simulation
    simulation_ids = []
    # to calculate simulation time
    start_time = time()

    # double loop construction let us to see how the probabilities are converging at a specific value for seperate experiments
    for no_of_games in range(1, max_simulation_number+1):
        
        score = []
        door_set = {1,2,3} 
        for game_no in range(0,no_of_games): # sub loop that simulates from 1 to no_of_games games
            game_log = []
            game_log.append(no_of_games)
            game_log.append(game_no)
            
            # 0. initial settings:
            not_to_open_doors = set()
            host_doors = door_set.copy()
            player_doors = door_set.copy()
            
            # 1. Randomly choose prize door
            prize_door = random.choice(tuple(host_doors))
            game_log.append(prize_door)
            if variant == 'Monty Hall':
                not_to_open_doors.add(prize_door) # Host knows not to open prize door 
            #elif variant == 'Monty Fall':
                # do nothing as Host does not know where is the prize
                
            # 2. Randomly choose Contestant selection
            players_choice = random.choice(tuple(player_doors))
            game_log.append(players_choice)
            # Host knows not to open these doors 
            not_to_open_doors.add(players_choice) 
            host_doors.difference_update(not_to_open_doors)
        
            # 3. if host has a choice, pick one at random and remove from available choice for the Contestant
            host_elimination = random.choice(tuple(host_doors))
            game_log.append(host_elimination)
            # Contestant cannot pick open door
            player_doors.remove(host_elimination)
                # if Host has chosen prize door - trial void
            if host_elimination == prize_door:
                # Contestant does not get to choose
                game_log.append('--')
                # trial considered as VOID
                game_log.append('VOID')
                # update simulation log
                if keep_log:
                    simulation_log.append(game_log)
                # skip to another game iteration
                continue
            
            # 4. Depending on the strategy Contestant may keep or change initial selection !!!! implement different solution
            if change:
                # remove players previous choice
                player_doors.remove(players_choice)
                #unpack player's final selection
                (final_choice,) = player_doors 
            else:
                # player keeps initial choice
                final_choice = players_choice
                
            game_log.append(final_choice)
        

            if final_choice == prize_door:
                score.append(1)
                game_log.append('WIN')
            else:
                score.append(0)
                game_log.append('LOSE')

            if keep_log:
                simulation_log.append(game_log)
  
        if len(score)==0:
            score.append(0)
        winning_probability_means.append(np.mean(score))
        simulation_ids.append(no_of_games)
            
    end_time = time()
    print ("Total time :", end_time - start_time )
    
    # plotting a figure  
    plt.figure()
    
    #Set a title
    if change:
        strategy = 'switching'
    else:
        strategy = 'keeping'
        
    label = 'Probability convergence graph for {} problem\n with {} initial choice strategy'.format(variant,strategy)
    plt.title(label)
    plt.xlabel('number of independant simulations with increasing number of trials')
    plt.ylabel('probability of winning a prize')
    # Display results of symulation
    plt.plot(simulation_ids,winning_probability_means)
    #plt.show()
    plt.savefig(fname, dpi=400)
    
    print('Show probabilities of 10 latest simulation:')
    print(winning_probability_means[-10:])
    
    if keep_log:
        simulation_log = pd.DataFrame(data=simulation_log, columns=columns)
        
    return winning_probability_means , simulation_log

#Producing 4 convergence graphs for 2 different variant for both strategies
sim_no = 2000
# simulation of Monty Hall problem with switching initial choice strategy
print('Start simulation of Monty Hall problem with switching initial choice strategy') 
probabilities, simulation_log = run_simulations(max_simulation_number=sim_no, variant='Monty Hall', change=True, keep_log=True, fname='sim-MH-switching.png' )

# simulation of Monty Hall problem with keeping initial choice strategy
print('Start simulation of Monty Hall problem with keeping initial choice strategy') 
probabilities, simulation_log = run_simulations(max_simulation_number=sim_no, variant='Monty Hall', change=False, keep_log=True, fname='sim-MH-keeping.png' )

# simulation of Monty Fall variant with switching initial choice strategy
print('Start simulation of Monty Fall variant with switching initial choice strategy') 
probabilities, simulation_log = run_simulations(max_simulation_number=sim_no, variant='Monty Fall', change=True, keep_log=True, fname='sim-MF-switching.png' )

# simulation of Monty Fall variant with keeping initial choice strategy
print('Start simulation of Monty Fall variant with keeping initial choice strategy') 
probabilities, simulation_log = run_simulations(max_simulation_number=sim_no, variant='Monty Fall', change=False, keep_log=True, fname='sim-MF-keeping.png' )

