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
for i in range(1000):
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

Running the simulation 10000 times gives us the following at the tail (no extra stats for now, 3 repeats)
1)
Number of customers supported in shift 10000: 229.
Number of customers unsupported in shift 10000: 2.
Cumulative total customers supported (Day 10000): 2154079.
Cumulative total customers whose issues were not resolved on day of call (Day 10000): 24705.
2)
Cumulative total customers supported (Day 10000): 2153627.
Cumulative total customers whose issues were not resolved on day of call (Day 10000): 24775.
3)
Cumulative total customers supported (Day 10000): 2155113.
Cumulative total customers whose issues were not resolved on day of call (Day 10000): 24604.

Well, of course the discrepancy remains the same magnitude. If you don't keep tracking the customers,
you're just running day 1 over and over again. Should sort this concept out.

Running the simulation 1000 times gives us the following at the tail (with extra stats, 3 repeats)

Cumulative total customers supported (Day 1000): 215208.
Mean daily total customers supported (1000 days) = 215.208, S.D. = 5.946825707888201
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2461.
Mean daily total customers left unsupported (1000 days) = 2.461, S.D. = 1.102941068235289


Cumulative total customers supported (Day 1000): 215576.
Mean daily total customers supported (1000 days) = 215.576, S.D. = 5.913900912257492
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2451.
Mean daily total customers left unsupported (1000 days) = 2.451, S.D. = 1.1007265782200408

Cumulative total customers supported (Day 1000): 215472.
Mean daily total customers supported (1000 days) = 215.472, S.D. = 5.882959799284711
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2444.
Mean daily total customers left unsupported (1000 days) = 2.444, S.D. = 1.0994835151106177

# Someone left their post after something like 40000 shifts was enough
(so 6 employees rather than the 7 up to this point)

Cumulative total customers supported (Day 1000): 215647.
Mean daily total customers supported (1000 days) = 215.647, S.D. = 6.134035457999897
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2458.
Mean daily total customers left unsupported (1000 days) = 2.458, S.D. = 1.1705708009343134

Cumulative total customers supported (Day 1000): 215227.
Mean daily total customers supported (1000 days) = 215.227, S.D. = 5.8999551693212045
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2486.
Mean daily total customers left unsupported (1000 days) = 2.486, S.D. = 1.1374550540570822

Cumulative total customers supported (Day 1000): 215138.
Mean daily total customers supported (1000 days) = 215.138, S.D. = 6.273671652230455
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2454.
Mean daily total customers left unsupported (1000 days) = 2.454, S.D. = 1.1008560305507709

Since our output difference is in terms of decimal points of people, let's see what happens
after someone else leaves

Cumulative total customers supported (Day 1000): 215394.
Mean daily total customers supported (1000 days) = 215.394, S.D. = 5.982705408090892
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2431.
Mean daily total customers left unsupported (1000 days) = 2.431, S.D. = 1.135446608167905

Cumulative total customers supported (Day 1000): 215120.
Mean daily total customers supported (1000 days) = 215.12, S.D. = 5.936295140910701
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2467.
Mean daily total customers left unsupported (1000 days) = 2.467, S.D. = 1.1725659896142306

Cumulative total customers supported (Day 1000): 215149.
Mean daily total customers supported (1000 days) = 215.149, S.D. = 5.931003203506132
Cumulative total customers whose issues were not resolved on day of call (Day 1000): 2517.
Mean daily total customers left unsupported (1000 days) = 2.517, S.D. = 1.1487867513163614

Again, a marginal increase in standard deviation that would practically be not significant
in a call centre, just from knowing what mean and sd signify
'''
