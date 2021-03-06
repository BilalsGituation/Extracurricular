# Classic cashier/queue example (Call centre) of discrete event simulation

# This will be based off anything I can find using the search term "simpy"
# on YouTube, but uses @NeuralNine's 18-minute video found on the first page
# as jumpoff

# I then changed it to generate a story about singing birds queuing to wake
# me in the morning (with a capacity of 5 birds singing simultaneously)

'''
Credit to GitHub@fitosky1 for starting the line of joking that led to this script!

please see history files in this repo "BasicCallCentre.py" and its output
"CallCentre_output.txt"
'''

import random
import numpy as np
import simpy
import statistics

#Resource count
Songbird_capacity=2 # changed to 2 perches on tree
#Simpy clock runs in minutes
MEAN_SING=5
BETWEEN_BIRDS=2 # time between customers
END_T = 60 # 5am

# counter placeholders
n_finished_song = 0
n_waiting = 0
total_sung = 0
left_waiting = 0

# class
class TreeNearWindow:
# initial state
    def __init__(self, env, perch, duration):
        self.env = env # simulation needs an environment
        self.staff = simpy.Resource(env,perch) # space for bird to sing is a simulation resource
        self.duration = duration # song duration is called in downstream function

    def song(self, bird):
        random_time = max(1, np.random.normal(self.duration, 4))
        yield self.env.timeout(random_time) # generator
        if self.env.now > 10:
            print(f"Bird {bird} finished singing at 4:{self.env.now:.2f}AM, flew off somewhere.\n")
        else:
            print(f"Bird {bird} finished singing at {self.env.now:.2f} minutes after 4:00AM, flew off somewhere.\n")

# The function that
#  causes generation of birds, to go through the singing queue in setup function
def bird(env, name, nearby_tree):
    global n_finished_song, n_waiting
    n_waiting+=1
    if env.now > 10:
        print(f"Bird {name} starts hovering around tree perch at 4:{env.now:.2f}AM.\n")
    else:
        print(f"Bird {name} starts hovering around tree perch at {env.now:.2f} minutes after 4:00AM.\n")
    with nearby_tree.staff.request() as request:
        yield request
        if env.now > 10:
            print(f"Bird {name} is able to sit and starts singing at 4:{env.now:.2f}.\n")
        else:
            print(f"Bird {name} is able to sit and starts singing at {env.now:.2f} minutes after 4:00AM.\n")
        yield env.process(nearby_tree.song(name))
        n_finished_song+=1
        n_waiting-=1

# the function that connects a bird to a perch and decides its song duration
# after receiving yields from bird function(?)
def setup(env, perch, duration, interval):
    nearby_tree = TreeNearWindow(env, perch, duration)

    for i in range(1,6):
        env.process(bird(env, i, nearby_tree))

        while True:
            yield env.timeout(random.randint(interval -1, interval+1))
            i+=1
            env.process(bird(env, i, nearby_tree))

#placeholder for our sample
sample_sung = []
sample_LeftWaiting = []

#Run the shift several times
for i in range(50):
    # counters for bird state at end of day
    n_finished_song=0
    n_waiting=0
    print(f"\nIT IS 4AM (Day {i+1})\n(minute decimals signify hundredths for now)")
    #run the simulation once
    env = simpy.Environment()
    env.process(setup(env, Songbird_capacity, MEAN_SING, BETWEEN_BIRDS))
    env.run(until=END_T)
    #description at end of hour
    print(f"Number of birds finished singing at 5:00AM on day {i + 1}: {n_finished_song}.\n")
    print(f"Number of birds not finished singing at 5:00AM on day {i + 1}: {n_waiting}.\n")
    #feed generated data into variables and report/do mild stats at end of day
    total_sung = total_sung + n_finished_song
    sample_sung.append(n_finished_song)
    mean_sd_sung = f"Mean daily total birds who finished their song by 5:00AM ({i + 1} days) = {total_sung/(i+1)}, S.D. = {np.std(sample_sung)}.\n"
    print(f"Cumulative total birds finished singing at 5:00AM (Day {i + 1}): {total_sung}.\n")
    print(f"{mean_sd_sung}")
    left_waiting = left_waiting + n_waiting
    sample_LeftWaiting.append(n_waiting)
    mean_sd_LeftWaiting = f"Mean daily total birds who did not finish singing by 5:00AM ({i + 1} days) = {left_waiting/(i+1)}, S.D. = {np.std(sample_LeftWaiting)}.\n"
    print(f"Cumulative total birds not finished singing at 5:00AM (Day {i+1}): {left_waiting}.\n")
    print(f"{mean_sd_LeftWaiting}")
    print(f"@BilalsGituation got {random.uniform(2.0,6.0)} hours sleep this morning") # don't worry, I'm exaggerating
