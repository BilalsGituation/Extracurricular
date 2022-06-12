# Classic cashier/queue example (Call centre) of discrete event simulation

# This will be based off anything I can find using the search term "simpy"
# on YouTube, but uses @NeuralNine's 18-minute video found on the first page
# as jumpoff

import random
import numpy as np
import simpy
import statistics

#Resource count
NUM_EMPLOYEES=5
#Simpy clock runs in minutes
MEAN_SUPPORT=5
BETWEEN_CUSTOMERS=2 # time between customers
END_T = 435 # 120 in the tutorial but 2-hour shifts unrealistic, no?
# So we have an 8h day with 45m employee break seamlessly included

# counter placeholders
n_supported = 0
n_waiting = 0
total_supported = 0
left_waiting = 0

# class
class CallCentre:
# initial state
    def __init__(self, env, staff, duration):
        self.env = env # simulation needs an environment
        self.staff = simpy.Resource(env,staff) # employee is a simulation resource
        self.duration = duration # call duration is called in downstream function

    def support(self, customer):
        random_time = max(1, np.random.normal(self.duration, 4))
        yield self.env.timeout(random_time) # generator
        print(f"Customer support concluded for customer {customer} at {self.env.now:.2f} minutes into shift.")


# The function that happens
def customer(env, name, call_centre):
    global n_supported, n_waiting
    n_waiting+=1
    print(f"Customer {name} enters waiting queue at {env.now:.2f} minutes into shift.")
    with call_centre.staff.request() as request:
        yield request
        print(f"Customer {name} enters call at {env.now:.2f} minutes into shift.")
        yield env.process(call_centre.support(name))
        print(f"Customer {name} left call at {env.now:.2f} minutes into shift.")
        n_supported+=1
        n_waiting-=1

# the function that connects a customer to the employee and decides its duration
# based on yields from customer(?)
def setup(env, staff, duration, interval):
    call_centre = CallCentre(env, staff, duration)

    for i in range(1,6):
        env.process(customer(env, i, call_centre))

        while True:
            yield env.timeout(random.randint(interval -1, interval+1))
            i+=1
            env.process(customer(env, i, call_centre))

#placeholder for our sample
sample_supported = []
sample_unsupported = []

#Run the shift several times
for i in range(100):
    # counters for customer state at end of day
    n_supported=0
    n_waiting=0
    print(f"Starting sim {i+1} of shift at call centre")
    #run the simulation once
    env = simpy.Environment()
    env.process(setup(env, NUM_EMPLOYEES, MEAN_SUPPORT, BETWEEN_CUSTOMERS))
    env.run(until=END_T)
    #description at end of shift
    print(f"Number of customers supported in shift {i + 1}: {n_supported}.")
    print(f"Number of customers unsupported in shift {i + 1}: {n_waiting}.")
    #feed generated data into variables and report/do mild stats at end of day
    total_supported = total_supported + n_supported
    sample_supported.append(n_supported)
    mean_sd_supported = f"Mean daily total customers supported ({i + 1} days) = {total_supported/(i+1)}, S.D. = {np.std(sample_supported)}"
    print(f"Cumulative total customers supported (Day {i + 1}): {total_supported}.")
    print(f"{mean_sd_supported}")
    left_waiting = left_waiting + n_waiting
    sample_unsupported.append(n_waiting)
    mean_sd_unsupported = f"Mean daily total customers left unsupported ({i + 1} days) = {left_waiting/(i+1)}, S.D. = {np.std(sample_unsupported)}"
    print(f"Cumulative total customers whose issues were not resolved on day of call (Day {i+1}): {left_waiting}.")
    print(f"{mean_sd_unsupported}")
