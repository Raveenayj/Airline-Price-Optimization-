import sys
import numpy as np
sys.path.append("C:/Users/dell/Downloads/mysim.py")
from mysim import sim_rev, my_score


n_dls = 11
min_dl = 100               #setting minimum value for range of demand level
max_dl = 200               #setting maximum value for range of demand level
demand_levels = np.linspace(min_dl, max_dl, n_dls)

max_tickets = 200          #setting value for maximum no. of tickets
max_days = 150              # setting value for maximun no. of days

#Indices of Q are: n_sold in day, tickets_left to start day, demand level, days left
Q = np.zeros([max_tickets, max_tickets, n_dls, max_days])
#Indices of V are: n_left and n_days;tickets left and days left
V = np.zeros([max_tickets, max_days])

#The base case in which we have to sell with only one day left
for tickets_left in range(max_tickets):
    for sold_tickets in range(tickets_left+1): # add 1 to offset 0 indexing. Allowing all tickets to sell
        for demand_index, dem_lev in enumerate(demand_levels):
            # We do not want prices to be negative
            price = max(dem_lev - sold_tickets, 0)
            Q[sold_tickets, tickets_left, demand_index, 0] = price * sold_tickets
    # Choosing the optimum number to sell,for each demand level. Output of this is array .of size n_demand_levels
    revenue_from_best_quantity_at_each_demand_level = Q[:, tickets_left, :, 0].max(axis=0)
    # As demand level values are unknown, we will take average as all values are possible
    V[tickets_left, 0] = revenue_from_best_quantity_at_each_demand_level.mean()
	
	
#The general case :considering for other time horizons; iteratively calculating Q and V values periodically	further back
for days_left in range(1, max_days):
    for tickets_left in range(max_tickets):
        for sold_tickets in range(tickets_left):
            for demand_index, dem_lev in enumerate(demand_levels):
                price = max(dem_lev - sold_tickets, 0)
                rev_today = price * sold_tickets
                ##Q calculates current revenue from above function but also adds V value from leftover tickets
                Q[sold_tickets, tickets_left, demand_index, days_left] = rev_today + V[tickets_left-sold_tickets, days_left-1]  
        expected_total_rev_from_best_quantity_at_each_demand_level = Q[:, tickets_left, :, days_left].max(axis=0)
        V[tickets_left, days_left] = expected_total_rev_from_best_quantity_at_each_demand_level.mean()
		
		
def pricing_func(days_left, tickets_left, dem_lev):
    dem_lev_index = np.abs(dem_lev - demand_levels).argmin()
    day_index = days_left - 1 # arrays are 0 indexed
    tickets_index = int(tickets_left)  # in case, it comes in as float, but need to index with it
    Q_vals = Q[:, tickets_index, dem_lev_index, day_index]
    desired_quantity = Q_vals.argmax()# offset 0 indexing
    price = dem_lev - desired_quantity
    return price




my_score(pricing_func)	