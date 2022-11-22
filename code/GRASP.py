import random
import time

import numpy as np
from helper import GetPossibleLocations
from functools import reduce
from sympy import symbols

x, y = symbols('x y')


def SortVesselArrivalInc(vessels):
    return tuple(sorted(vessels, key=lambda ves: ves.arrival_time, reverse=False))


def GetPossibleLocationCosts(vessels, possible_locations):
    # def Cost(vessel, location):
    # max_x = 0
    # for i in location:
    #     if i['x'] > max_x:
    #         max_x = i['x']
    # return vessel.w * (location[1]['x'] - vessel.a)

    return list(map(lambda pl: pl[0].w * (pl[1][1]['x'] - pl[0].a), zip(vessels, possible_locations)))


def ScreenPossibleLocations(possible_locations, possible_location_costs):
    possible_location_screened = []
    possible_location_screened_costs = []
    min_cost = min(possible_location_costs)

    def isSatisfy(cost_k):
        r = random.random()
        return (1 / cost_k) < (r / min_cost)

    for index, cost in enumerate(possible_location_costs):
        if not isSatisfy(cost):
            possible_location_screened.append(possible_locations[index])
            possible_location_screened_costs.append(cost)

    return possible_location_screened, possible_location_screened_costs


def GetPossibleLocationProbabilities(possible_location_screened_costs):
    sum_inverse_cost = sum(map(lambda c: 1 / c, possible_location_screened_costs))
    possible_location_screened_probabilities = list(map(lambda cost: (1 / cost) / sum_inverse_cost,
                                                        possible_location_screened_costs))
    possible_location_probabilities = np.asarray(possible_location_screened_probabilities).astype('float64')
    possible_location_probabilities = possible_location_probabilities / np.sum(possible_location_probabilities)

    return possible_location_probabilities


def GreedyRandomizedConstruction(vessels, S, T, breaks, seed=0):
    # random.seed(seed)
    packing_positions = []
    vessel_locations = tuple()

    for index, vessel in enumerate(vessels):
        possible_locations = GetPossibleLocations(vessel, vessel_locations, S, T, breaks)
        possible_location_costs = GetPossibleLocationCosts(vessels[:index + 1], possible_locations)
        possible_location_screened, possible_location_screened_costs \
            = ScreenPossibleLocations(possible_locations, possible_location_costs)
        possible_location_probabilities = GetPossibleLocationProbabilities(possible_location_screened_costs)
        index_location = np.random.choice(len(possible_location_screened), p=possible_location_probabilities)
        possible_location = possible_location_screened[index_location]
        packing_positions.append(possible_location)
        vessel_locations = vessel_locations + ConvertListDictToListList(possible_location)

    return packing_positions


def ConvertListDictToListList(possible_location):
    return ((
                (possible_location[0]['x'], possible_location[0]['y']),
                (possible_location[1]['x'], possible_location[1]['y']),
                (possible_location[2]['x'], possible_location[2]['y']),
                (possible_location[3]['x'], possible_location[3]['y']),
            ),)


def GreedyHeuristicForTheRest(possible_locations):
    return possible_locations[3]['y'] + possible_locations[3]['y']


def GetBenefit(vessels, packing_positions):
    return sum(v.w * (p[1]['x'] - v.a) for v, p in zip(vessels, packing_positions))


def LocalSearch(vessels, packing_positions, S, T, breaks, l1=10):
    """l1: loop times to choose the best insertion list"""
    benefit = GetBenefit(vessels, packing_positions)
    packing_positions_list = list(map(lambda p: ConvertListDictToListList(p)[0], packing_positions))

    for _ in range(l1):
        for i in range(len(vessels) - 1):
            copy_vessels = list(vessels)
            copy_packing_positions = packing_positions[:]
            copy_packing_positions_list = packing_positions_list[:]

            copy_vessels[i], copy_vessels[i + 1] = copy_vessels[i + 1], copy_vessels[i]
            copy_packing_positions[i], copy_packing_positions[i + 1] = \
                copy_packing_positions[i + 1], copy_packing_positions[i]
            copy_packing_positions_list[i], copy_packing_positions_list[i + 1] = \
                copy_packing_positions_list[i + 1], copy_packing_positions_list[i]
            copy_packing_positions_list = tuple(copy_packing_positions_list)

            for j in range(i, len(copy_vessels)):
                # Split into 2 parts and repack all vessels after i
                possible_locations = GetPossibleLocations(copy_vessels[j], copy_packing_positions_list[:j + 1], S, T, breaks)
                possible_location_benefits = [GreedyHeuristicForTheRest(pl) for pl in possible_locations]
                best_location = possible_locations[np.argmin(possible_location_benefits)]
                copy_packing_positions[j] = best_location

            copy_benefit = GetBenefit(copy_vessels, copy_packing_positions)
            if copy_benefit < benefit:
                vessels = copy_vessels
                packing_positions = copy_packing_positions
                benefit = copy_benefit

    return vessels, packing_positions, benefit


def UpdateSolution(searched_vessels, searched_packing_positions, benefit, best_searched_vessels,
                   best_searched_packing_positions, best_benefit):
    if best_benefit is None:
        return searched_vessels, searched_packing_positions, benefit
    return (searched_vessels, searched_packing_positions, benefit) if benefit < best_benefit \
        else (best_searched_vessels, best_searched_packing_positions, best_benefit)
