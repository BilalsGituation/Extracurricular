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


def setup(env, staff, duration, interval):
    call_centre = CallCentre(env, staff, duration)

    for i in range(1,6):
        env.process(customer(env, i, call_centre))

        while True:
            yield env.timeout(random.randint(interval -1, interval+1))
            i+=1
            env.process(customer(env, i, call_centre))

#unsupported = n_waiting - n_supported

print("Starting sim of shift at call centre")
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, MEAN_SUPPORT, BETWEEN_CUSTOMERS))
#print(f"Number of unsupported customers in queue: {name - n_supported}.")
#print(f"Number of customers mid-call: {name - n_supported}.")
env.run(until=END_T)
print(f"Number of customers supported: {n_supported}.")
print(f"Number of customers unsupported: {n_waiting}.")


'''
Terminal:
python BasicCallCentre_sim.py > ./CallCentre_output.txt
tail CallCentre_output.txt

CONDS 1:
NUM_EMPLOYEES=2
MEAN_SUPPORT=5
BETWEEN_CUSTOMERS=2
END_T = 435

CONDS 1 RUN 1:
Number of customers supported: 159.
Number of customers unsupported: 218.

CONDS 1 RUN 2:
Number of customers supported: 165.
Number of customers unsupported: 217.


CONDS 1 RUN 3:
Number of customers supported: 163.
Number of customers unsupported: 222.
# '''
# Looks like this call centre wouldn't be very highly regarded as is. Now that we
# know some basics, let's just change some conditions to play around with this and
# move on, as I would like an efficient way to run a sim many times and get summary
# stats, rather than optimise this much more
'''
Since the two employees were organised, they were able to persuade the employer to
hire more staff, rather than require the employees to work at a rate that would support
more than twice the amount of customers in a shift.
So, the HR department successfully completed their task of recruiting more employees to
work at the same rate for the same pay, and their workspaces had been prepared in the meantime...

CONDS 2:
NUM_EMPLOYEES=7 # changing some names to show I didn't paste this from somewhere
MEAN_SUPPORT=5
BETWEEN_CUSTOMERS=2
END_T = 435

CONDS 2 RUN 1:


CONDS 2 RUN 2


CONDS 2 RUN 3:
'''
