import random
import time
import numpy as np
import sys

class pool:
    def __init__(self, private_chain, honest_chain, stubborn_blocks, honest_blocks, stubborn_orphans, honest_orphans, unpublished_blocks):
        self.private_chain = private_chain #length of selfish miners private chain
        self.honest_chain = honest_chain  #length of the public chain
        self.stubborn_blocks = stubborn_blocks #number of published blocks mined by selfish miners
        self.honest_blocks = honest_blocks #number of blocks mined by honest miners
        self.bribery_counter = 0

        # may not be used
        self.stubborn_orphans = stubborn_orphans
        self.honest_orphans = honest_orphans
        self.unpublished_blocks = unpublished_blocks

def selfish_mining_simulator(iteration, alpha, gamma):
    P = pool(0, 0, 0, 0, 0, 0, 0)
    state = 0
    # state o.1 indicates state 0'

    for i in range(iteration):
        r = random.uniform(0, 1)
        if state == 0:
            if r <= alpha:
                state = 1
                P.private_chain += 1
            else:
                state = 0
                P.honest_chain += 1
                P.honest_blocks += P.honest_chain
                P.private_chain, P.honest_chain = 0, 0
        elif state == 1:
            if r<=alpha:
                state = 2
                P.private_chain += 1
            else:
                state = 0.1
                P.honest_chain += 1
        elif state == 0.1:
            if r>(1-alpha)*gamma+alpha:
                state = 0
                P.honest_chain += 1
                P.honest_blocks += P.honest_chain
                P.private_chain, P.honest_chain = 0, 0
            elif r>alpha:
                state = 0
                # revenue calculation 
                P.stubborn_blocks += P.private_chain
                P.honest_blocks += 1
                P.private_chain, P.honest_chain = 0, 0
            else:
                state = 0
                P.private_chain += 1
                P.stubborn_blocks += P.private_chain
                P.private_chain, P.honest_chain = 0, 0
        elif state == 2:
            if r<=alpha:
                state = 3
                P.private_chain += 1
            else:
                state = 0
                P.honest_chain += 1
                P.stubborn_blocks += P.private_chain
                P.private_chain, P.honest_chain = 0, 0
        elif state> 2:
            if r<=alpha:
                state += 1
                P.private_chain += 1
            else:
                state -= 1
                P.honest_chain += 1
        else:
            raise ValueError
    return P


def lead_stubborn_mining(iteration, alpha, gamma):
    P = pool(0, 0, 0, 0, 0, 0, 0)
    state = 0
    # state with x.1 represents the state x'

    for i in range(iteration):
        r = random.uniform(0, 1)
        if state == 0:
            if r<=alpha:
                state = 1
                P.private_chain += 1
            else:
                state = 0
                P.honest_chain += 1
                P.honest_blocks += P.honest_chain
                P.honest_chain, P.private_chain = 0, 0
            state = round(state, 1)
        elif state == 1:
            if r<=alpha:
                state = 2
                P.private_chain += 1
            else:
                state = 0.1
                P.honest_chain += 1    
            state = round(state, 1)  
        elif state >=2 and state == int(state):
            # print(state)
            if r<=alpha:
                state += 1
                P.private_chain += 1
            else:
                state = state - 1 + 0.1
                P.honest_chain += 1
            state = round(state, 1)
            
        elif state > 1 and state == int(state) + 0.1:
            if r<=alpha:
                state += 1
                P.private_chain += 1
            elif r<alpha+(1-alpha)*gamma:
                state -= 1
                P.stubborn_blocks += P.honest_chain
                P.private_chain -= P.honest_chain
                # print(P.honest_chain)
                P.honest_chain = 1
            else:
                state -= 1
                P.honest_chain += 1
            state = round(state, 1)
            # print(state)
        elif state == 0.1:
            if r<= alpha:
                state = 0
                P.private_chain += 1
                P.stubborn_blocks += P.private_chain
                P.honest_chain, P.private_chain = 0, 0
            elif r<alpha+(1-alpha)*gamma:
                state = 0
                P.honest_blocks += 1
                P.stubborn_blocks += P.private_chain
                P.honest_chain, P.private_chain = 0, 0
            else:
                state = 0
                P.honest_chain += 1
                P.honest_blocks += P.honest_chain
                P.honest_chain, P.private_chain = 0, 0
            state = round(state, 1)
        else:
            raise ValueError
    return P

def lead_stubborn_mining_with_bribery(iteration, alpha, gamma, bribery_ratio=0.1, start_len=2, end_len=3, penalty=1.2):
    P = pool(0, 0, 0, 0, 0, 0, 0)
    beta = alpha*bribery_ratio
    state = 0
    # state with x.1 represents the state x'

    for i in range(iteration):
        r = random.uniform(0, 1)
        # print(state)
        if state == 0:
            if r<=alpha:
                state = 1
                P.private_chain += 1
            else:
                state = 0
                P.honest_chain += 1
                P.honest_blocks += P.honest_chain
                P.honest_chain, P.private_chain = 0, 0
            state = round(state, 1)
        elif state == 1:
            if r<=alpha:
                state = 2
                P.private_chain += 1
            else:
                state = 0.1
                P.honest_chain += 1    
            state = round(state, 1)  
        elif state >=2 and state == int(state):
            # print(state)
            if r<=alpha:
                state += 1
                P.private_chain += 1
            else:
                state = state - 1 + 0.1
                P.honest_chain += 1
            state = round(state, 1)
            
        elif state > 1 and state == int(state) + 0.1:
            if r<=alpha:
                state += 1
                P.private_chain += 1
            elif r<alpha+(1-alpha)*gamma:
                state -= 1
                P.stubborn_blocks += P.honest_chain
                P.private_chain -= P.honest_chain
                # print(P.honest_chain)
                P.honest_chain = 1
            else:
                state -= 1
                P.honest_chain += 1
            state = round(state, 1)
            # print(state)
        elif state == 0.1:
            if r<= alpha:
                state = 0
                P.private_chain += 1
                P.stubborn_blocks += P.private_chain
                P.honest_chain, P.private_chain = 0, 0
            elif r<alpha+(1-alpha)*gamma:
                state = 0
                P.honest_blocks += 1
                P.stubborn_blocks += P.private_chain
                P.honest_chain, P.private_chain = 0, 0
            else:           
                if P.private_chain<start_len:
                    state = 0
                    P.honest_chain += 1
                    P.honest_blocks += P.honest_chain
                    P.honest_chain, P.private_chain = 0, 0
                else:
                    state = -1
                    P.honest_chain += 1
            state = round(state, 1)
        elif state == -1:
            P.bribery_counter += 1
            if r<=alpha+beta:
                state = -0.1
                P.private_chain += 1
            else:
                state -= 1
                P.honest_chain += 1
            # state = round(state, 1)
        elif state == -0.1:
            P.bribery_counter += 1
            if r<=alpha +beta:
                state = 0
                P.private_chain += 1
                P.stubborn_blocks += P.private_chain
                P.private_chain, P.honest_chain = 0, 0
            else:
                state = -1
                P.honest_chain += 1
            # state = round(state, 1)
        elif state < -1:
            P.bribery_counter += 1
            if r<=alpha+beta:
                state += 1
                P.private_chain += 1
            else:
                # decide whether abandon the whole private chain
                if end_len + state>0:
                    state -= 1
                    P.honest_chain += 1
                else:
                    print('abandon')
                    state = 0
                    P.honest_chain += 1
                    P.honest_blocks += P.honest_chain
                    P.private_chain, P.honest_chain = 0, 0
            # state = round(state, 1)
        else:
            raise ValueError
    return P

# 效果比较微弱，各种参数还需调一调
if __name__ == "__main__":
    iteration = 200000
    alpha = 0.45
    gamma = 0.9
    bribery_ratio=0.2
    start_len=5
    end_len=20
    penalty=1

    res_ratio = []

    res = lead_stubborn_mining_with_bribery(iteration, alpha, gamma, bribery_ratio, start_len, end_len, penalty)
    print("Number of simulation iteration:{}\talpha:{}\tgamma:{}".format(iteration, alpha, gamma))
    print("Number of valid blocks:{}".format(res.honest_blocks + res.stubborn_blocks))
    print("Number of honest blocks:{}".format(res.honest_blocks))
    print("Number of selfish mining blocks:{}".format(res.stubborn_blocks))
    print("Revenue ratio:{}".format(res.stubborn_blocks/(res.honest_blocks + res.stubborn_blocks)))
    print("bribery count blocks:{}".format(alpha*bribery_ratio*penalty*res.bribery_counter))
    print((res.stubborn_blocks-alpha*bribery_ratio*penalty*res.bribery_counter)/(res.honest_blocks + res.stubborn_blocks))
    print("-"*30)

    print("Lead stubborn mining:")
    res = lead_stubborn_mining(iteration, alpha, gamma)
    print("Number of simulation iteration:{}\talpha:{}\tgamma:{}".format(iteration, alpha, gamma))
    print("Number of valid blocks:{}".format(res.honest_blocks + res.stubborn_blocks))
    print("Number of honest blocks:{}".format(res.honest_blocks))
    print("Number of selfish mining blocks:{}".format(res.stubborn_blocks))
    print("Revenue ratio:{}".format(res.stubborn_blocks/(res.honest_blocks + res.stubborn_blocks)))
    print("-"*30)
    print("selfish mining:")
    res = selfish_mining_simulator(iteration, alpha, gamma)
    print("Number of simulation iteration:{}\talpha:{}\tgamma:{}".format(iteration, alpha, gamma))
    print("Number of valid blocks:{}".format(res.honest_blocks + res.stubborn_blocks))
    print("Number of honest blocks:{}".format(res.honest_blocks))
    print("Number of selfish mining blocks:{}".format(res.stubborn_blocks))
    print("Revenue ratio:{}".format(res.stubborn_blocks/(res.honest_blocks + res.stubborn_blocks)))