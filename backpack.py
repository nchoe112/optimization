import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

np.random.seed(0)

weights = np.random.randint(1, 11, 20).tolist()
prices = np.random.randint(1, 11, 20).tolist()
cap = 20

print(weights)
print(prices)

init_weight = 0 

def min_weight(weights):
    global init_weight
    global cap
    copied_weights = weights.copy()

    sorted_weights = sorted(weights)
    lightest_fit = []

    for i in sorted_weights:
        if i + init_weight < cap:
            index = copied_weights.index(i)
            lightest_fit.append(index)

            init_weight += i
            copied_weights[index] = None
        else:
            break

    print(lightest_fit)
    print(init_weight)
        
#min_weight(weights)

init_price_weight = 0 

def max_price(prices):
    global init_price_weight
    global cap
    global weights

    copied_price = prices.copy()

    price_weight_indices = sorted(
    enumerate(zip(prices, weights)), 
    key=lambda x: (-x[1][0], x[1][1])  # Sort by price descending, then by weight ascending
    )

    cost_fit = []

    for index, (price, weight) in price_weight_indices:
        
        if weight + init_price_weight < cap:
            cost_fit.append(index)
            init_price_weight += weight  
            copied_price[index] = None
        else:
            break

    #print(cost_fit)
    #print(init_price_weight)

max_price(prices)

def knapsack(weights, prices):

    items = list(range(len(weights)))
    possible = []
    pass_weight = []
    high_price = []
    max_price = 0

    for i in range(1, len(items) + 1):
        possible.extend(combinations(items, i))

    for i in possible:
        curr_weight = sum(weights[ii] for ii in i)
        if curr_weight < cap:
            pass_weight.append(i)

    for i in pass_weight:
        curr_price = sum(prices[ii] for ii in i)
        if curr_price > max_price:
            max_price = curr_price
            high_price = i
    
    print(high_price)
    print(len(possible))


knapsack(weights, prices)




