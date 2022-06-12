# Classic cashier/queue example (Call centre) of discrete event simulation

# This will be based off anything I can find using the search term "simpy"
# on YouTube, but uses @NeuralNine's 18-minute video found on the first page

import random
import numpy as np
import simpy

NUM_EMPLOYEES=7 # changing some names to show I didn't paste this from somewhere
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
    print(f"Cumulative total customers supported (Day {i + 1}): {total_supported}.")
    left_waiting = left_waiting + n_waiting
    print(f"Cumulative total customers whose issues were not resolved on day of call (Day {i+1}): {left_waiting}.")


# actually I wanted to run it a proper amount of times (see changes since last commit)
'''
Terminal: (... write file, paths...) Extracurricular/Simulations$ tail CallCentre_output.txt

Customer 224 enters call at 433.00 minutes into shift.
Customer 223 left call at 433.00 minutes into shift.
Customer 225 enters waiting queue at 434.00 minutes into shift.
Customer support concluded for customer 224 at 434.00 minutes into shift.
Customer 225 enters call at 434.00 minutes into shift.
Customer 224 left call at 434.00 minutes into shift.
Number of customers supported in shift 99: 222.
Number of customers unsupported in shift 99: 3.
Cumulative total customers supported (Day 99): 21523.
Cumulative total customers whose issues were not resolved on day of call (Day 99): 240.

Looks like we get roughly 99% of calls resolved on the same day. That should be ok for a while,
but after doing what they can for a year or so, the call centre may get a backlog. Let's see whether
the discrepancy remains in the order of 100:1 resolved:unresolved...
'''
