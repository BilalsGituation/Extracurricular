# Classic cashier/queue example (Call centre) of discrete event simulation

# This will be based off anything I can find using the search term "simpy"
# on YouTube, but uses @NeuralNine's 18-minute video found on the first page

import random
import numpy as np
import simpy
import statistics

NUM_EMPLOYEES=5 # changing some names to show I didn't paste this from somewhere
MEAN_SUPPORT=5
BETWEEN_CUSTOMERS=2
END_T = 435 # 120 in the tutorial but 2-hour shifts unrealistic, no?
# So we have an 8h day with 45m employee break seamlessly included

n_supported = 0 # i don't want to write my vars in caps, lesson learned
n_waiting = 0
total_supported = 0
left_waiting = 0

class CallCentre:

    def __init__(self, env, staff, duration):
        self.env = env
        self.staff = simpy.Resource(env,staff)
        self.duration = duration

    def support(self, customer):
        random_time = max(1, np.random.normal(self.duration, 4))
        yield self.env.timeout(random_time) # generator
        print(f"Customer support concluded for customer {customer} at {self.env.now:.2f} minutes into shift.")


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


def setup(env, staff, duration, interval):
    call_centre = CallCentre(env, staff, duration)

    for i in range(1,6):
        env.process(customer(env, i, call_centre))

        while True:
            yield env.timeout(random.randint(interval -1, interval+1))
            i+=1
            env.process(customer(env, i, call_centre))

sample_supported = []
sample_unsupported = []

#unsupported = n_waiting - n_supported
for i in range(100):
    n_supported=0
    n_waiting=0
    print(f"Starting sim {i+1} of shift at call centre")
    env = simpy.Environment()
    env.process(setup(env, NUM_EMPLOYEES, MEAN_SUPPORT, BETWEEN_CUSTOMERS))
#print(f"Number of unsupported customers in queue: {name - n_supported}.")
#print(f"Number of customers mid-call: {name - n_supported}.")
    env.run(until=END_T)
    print(f"Number of customers supported in shift {i + 1}: {n_supported}.")
    print(f"Number of customers unsupported in shift {i + 1}: {n_waiting}.")
    total_supported = total_supported + n_supported
    sample_supported.append(n_supported)
    #print(sample_supported)
    mean_sd_supported = f"Mean daily total customers supported ({i + 1} days) = {total_supported/(i+1)}, S.D. = {np.std(sample_supported)}"
    print(f"Cumulative total customers supported (Day {i + 1}): {total_supported}.")
    print(f"{mean_sd_supported}")
    left_waiting = left_waiting + n_waiting
    sample_unsupported.append(n_waiting)
    mean_sd_unsupported = f"Mean daily total customers left unsupported ({i + 1} days) = {left_waiting/(i+1)}, S.D. = {np.std(sample_unsupported)}"
    print(f"Cumulative total customers whose issues were not resolved on day of call (Day {i+1}): {left_waiting}.")
    print(f"{mean_sd_unsupported}")
