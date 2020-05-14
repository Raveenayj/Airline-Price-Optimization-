from IPython.display import display, Javascript
import json
from numpy.random import uniform, seed
from numpy import floor
from collections import namedtuple


#This file works as a simulation environment containing the main function's definitions used in the main optimization code
#This function is used to calculate the no. of tickets sold
def _sold_tickets(p, dem_lev, max_qty):
        quantity_wanted = floor(max(0, p - dem_lev))
        return min(quantity_wanted, max_qty)

# This is to calculate total revenue 
def sim_rev(days_left, tickets_left, pricing_func, rev_to_date=0, min_dem_lev=100, max_dem_lev=200, verbose=False):
    if (days_left == 0) or (tickets_left == 0):
        if verbose:
            if (days_left == 0):
                print("Today, flight took off. ")
            if (tickets_left == 0):
                print("Flight is fully booked.")
            print("Total Revenue: ${:.0f}".format(rev_to_date))
        return rev_to_date
    else:
        dem_lev = uniform(min_dem_lev, max_dem_lev)             #demand level 
        p = pricing_func(days_left, tickets_left, dem_lev)       #pricing function depends on 3 parameters:days left,tickets left and demand level
        q = _sold_tickets(dem_lev, p, tickets_left)              #tickets sold function based on demand level, price and tickets left
        if verbose:
            print("{:.0f} days before flight: "
                  "Started with {:.0f} seats. "
                  "Demand level: {:.0f}. "
                  "Price set to ${:.0f}. "
                  "Sold {:.0f} tickets. "
                  "Daily revenue is {:.0f}. Total revenue-to-date is {:.0f}. "
                  "{:.0f} seats remaining".format(days_left, tickets_left, dem_lev, p, q, p*q, p*q+rev_to_date, tickets_left-q))
        return sim_rev(days_left = days_left-1,
                              tickets_left = tickets_left-q,
                              pricing_func=pricing_func,
                              rev_to_date=rev_to_date + p * q,
                              min_dem_lev=min_dem_lev,
                              max_dem_lev=max_dem_lev,
                              verbose=verbose)

def _save_score(score):
    message = {
        'jupyterEvent': 'custom.exercise_interaction',
        'data': {
            'learnTutorialId': 117,
            'interactionType': "check",
            'questionId': 'Aug31OptimizationChallenge',
            'outcomeType': 'Pass',
            'valueTowardsCompletion': score/10000,
            'failureMessage': None,
            'learnToolsVersion': "Testing"
        }
    }
    js = 'parent.postMessage(%s, "*")' % json.dumps(message)
    display(Javascript(js))

# This is to print all the information regarding flights and calculate revenue in those cases and also, calculate the average revenue from all flights 
def my_score(pricing_func, sims_per_case=200):
    seed(0)
    Case = namedtuple('Case', 'n_days n_tickets')
    cases = [Case(n_days=100, n_tickets=100),                           #considering different cases with different number of days and tickets
                 Case(n_days=14, n_tickets=50),
                 Case(n_days=2, n_tickets=20),
                Case(n_days=1, n_tickets=3),
                 ]
    case_scores = []
    for c in cases:
        case_score = sum(sim_rev(c.n_days, c.n_tickets, pricing_func)
                                     for _ in range(sims_per_case)) / sims_per_case
        print("Ran {:.0f} flights starting {:.0f} days before flight with {:.0f} tickets. "
              "Average revenue: ${:.0f}".format(sims_per_case,
                                                c.n_days,
                                                c.n_tickets,
                                                case_score))
        case_scores.append(case_score)
    score = sum(case_scores) / len(case_scores)
    try:
        _save_score(score)
    except:
        pass
    print("Average revenue across all flights is ${:.0f}".format(score))
