# Classic cashier/queue example (Call centre) of discrete event simulation

# This will be based off anything I can find using the search term "simpy"
# on YouTube, but uses @NeuralNine's 18-minute video found on the first page

import random
import numpy as np
import simpy

NUM_EMPLOYEES=2 # changing some names to show I didn't paste this from somewhere
MEAN_SUPPORT=5
BETWEEN_CUSTOMERS=2
END_T = 435 # 120 in the tutorial but 2-hour shifts unrealistic, no?
# So we have an 8h day with 45m employee break seamlessly included

n_supported = 0 # i don't want to write my vars in caps, lesson learned

class CallCentre:

    def __init__(self, env, staff, duration):
        self.env = env
        self.staff = simpy.Resource(env,staff)
        self.duration = duration

    def support(self, customer):
        random_time = max(1, np.random.normal(self.duration, 4))
        yield self.env.timeout(random_time) # generator
        print(f"Customer support concluded for customer {customer} at minute {self.env.now:.2f} of the shift.")

def customer(env, name, call_centre):
    global n_supported
    print(f"Customer {name} enters waiting queue at minute {env.now:.2f} of the shift.")
    with call_centre.staff.request() as request:
        yield request
        print(f"Customer {name} enters call centre at minute {env.now:.2f} of the shift.")
        yield env.process(call_centre.support(name))
        print(f"Customer {name} left call at minute {env.now:.2f} of the shift.")
        n_supported+=1

def setup(env, staff, duration, interval):
    call_centre = CallCentre(env, staff, duration)

    for i in range(1,6):
        env.process(customer(env, staff, call_centre))

        while True:
            yield env.timeout(random.randint(interval -1, interval+1))
            i+=1
            env.process(customer(env, i, call_centre))

print("Starting sim of shift at call centre")
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, MEAN_SUPPORT, BETWEEN_CUSTOMERS))
env.run(until=END_T)
