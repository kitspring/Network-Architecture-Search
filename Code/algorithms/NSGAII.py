'''
[INTRO] a nondominated sorting-based multiobjective EA (MOEA), called nondominated sorting genetic algorithm II (NSGA-II)
[REFERRENCE]: Deb, K., et al. "A fast and elitist multiobjective genetic algorithm: NSGA-II." IEEE Transactions on Evolutionary Computation 6.2(2002):182-197.
[CONTRIBUTOR OF CODE] Severus Peng
'''

import numpy as np
from public import tools

# fast non-dominate sorting
# INPUT: population of solutions
# OUTPUT:
#          Fi with indexs of population
#          population table of relating Fi number


def fast_non_dominated_sort(population_value):
    Sp = dict()
    Np = np.zeros(population_value.shape[0])
    Prank = np.zeros(population_value.shape[0])
    Fi = dict()
    Fi[1] = list()
    for p in range(population_value.shape[0]):
        Sp[p] = list()
        for q in range(population_value.shape[0]):
            if tools.is_dominate(population_value[p], population_value[q]):
                Sp[p].append(q)
            if tools.is_dominate(population_value[q], population_value[p]):
                Np[p] = Np[p] + 1
        if Np[p] == 0:
            Prank[p] = 1
            Fi[1].append(p)
    i = 1
    while Fi[i] != []:
        Q = list()
        for p in Fi[i]:
            for q in Sp[p]:
                Np[q] = Np[q] - 1
                if Np[q] == 0:
                    Prank[q] = i + 1
                    Q.append(q)
        i = i + 1
        Fi[i] = Q
    return Fi, Prank

# crowding distance
# INPUT: solutions with type of ndarray
# OUTPUT: related distance row vector


def crowding_distance(solutions):
    len = solutions.shape[0]
    len_m = solutions.shape[1]
    distance_i = np.zeros(len)
    for i in range(len_m):
        solut_value, rank = tools.sort(tools.normalized_vector(solutions[:, i]))
        distance_i[rank[0]] = np.Inf
        distance_i[rank[-1]] = np.Inf
        for j in [x+1 for x in range(len-2)]:
            distance_i[rank[j]] = distance_i[rank[j]] + (solutions[rank[j+1], i]-solutions[rank[j-1], i])/(
                np.max(solutions[:, i])-np.min(solutions[:, i]))
    return distance_i
