import time

from Entities import Vessel, Location
from helper import getRangeOfVessel, getRangeOfVesselWithXY, getAllNode, getVector, getVertexOfHole, getHoles, \
    getPositionAvailable, getLocationVessel, getValidLocationVessel
from GRASP import SortVesselArrivalInc, GreedyRandomizedConstruction, LocalSearch, UpdateSolution
import sys

X = "x"
Y = "y"

# Berth
# TODO: change this to be calculated variable
T = 9999999999
S = 40

# vessel_locations = [
#     ([0, 12], [5, 12], [5, 9], [0, 9]),
#     ([2, 9], [5, 9], [5, 7], [2, 7]),
#     ([5, 12], [8, 12], [8, 10], [5, 10]),
#     ([0, 3], [6, 3], [6, 0], [0, 0]),
#     ([6, 4], [8, 4], [8, 0], [6, 0]),
#     ([8, 10], [11, 10], [11, 0], [8, 0])
# ]
# vessels = [
#     Vessel(1, 10, 10, 10),
#     Vessel(2, 15, 5, 9, 2),
#     Vessel(3, 6, 0, 5),
#     Vessel(4, 20, 2, 10, 3),
#     Vessel(5, 5, 15, 5),
#     Vessel(6, 15, 12, 8),
#     Vessel(7, 4, 1, 3)
# ]
# BREAKS = [20, 32]
vessel_locations = []
vessels = []
BREAKS = []
MAX_ITER = 10


def GRASP(max_iter=50, seed=0):
    best_benefit = None
    sorted_vessels = SortVesselArrivalInc(vessels)
    best_searched_vessels = None
    best_searched_packing_positions = None
    end_time = int(time.time() + 5*60)

    for _ in range(max_iter):
        print(_)
        start_iter_time = time.time()
        constructed_packing_solutions = GreedyRandomizedConstruction(sorted_vessels, S, T, BREAKS)
        searched_vessels, searched_packing_positions, benefit = \
            LocalSearch(sorted_vessels, constructed_packing_solutions, S, T, BREAKS)
        best_searched_vessels, best_searched_packing_positions, best_benefit = \
            UpdateSolution(searched_vessels,
                           searched_packing_positions,
                           benefit,
                           best_searched_vessels,
                           best_searched_packing_positions,
                           best_benefit)
        end_iter_time = time.time()
        step_iter_time = int(end_iter_time - start_iter_time)
        if int(end_time - time.time()) < step_iter_time:
            break

    # print(best_benefit)
    for v, p in zip(best_searched_vessels, best_searched_packing_positions):
        v.u, v.v = p[3]['x'], p[3]['y']
    return tuple(sorted(best_searched_vessels, key=lambda ves: ves.index, reverse=False))


if __name__ == "__main__":
    step = 0
    # sys.argv[1]
    filename = sys.argv[1]
    start_time = time.time()
    with open(filename) as file:
        for line in file:
            if "length" in line:
                step = 1
                continue
            elif "breaks" in line:
                step = 2
                continue
            elif "weight" in line:
                step = 3
                continue
            elif line.strip() == "":
                continue

            if step == 1 and line.strip() != "":
                S = int(line.strip())
            elif step == 2 and line.strip() != "":
                BREAKS.append(int(line.strip()))
            elif step == 3:
                raw_vessels = line.strip().split()
                vessels.append(Vessel(int(raw_vessels[0]), int(raw_vessels[1]), int(raw_vessels[2]),
                                      1 if len(raw_vessels) == 4 else int(raw_vessels[3])))

        output = open("out" + filename[2:], 'w')
        L = ["% Vessel index, mooring time $u_i$, starting berth position occupied $v_i$\n"]

        for v in GRASP(MAX_ITER):
            L.append(f"{v.index}\t{v.u}\t{v.v}\n")
        output.writelines(L)
        output.close()
    print(time.time()-start_time)
