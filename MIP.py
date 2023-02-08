from ortools.linear_solver import pywraplp
from random import *
import math

# random instance
N = randint(5, 20)                                #nurses
D = randint(1, 10)                                #days
S = 4                                             #shifts
a = randint(1, int(N/S))                          #min_nurses_per_shift
b = randint(math.ceil(N/S), math.ceil(1.5*N/S))   #max_nurses_per_shift
F = [[] for i in range(N)]                        #free_days


for i in range(randint(0, N)):
    ran_nurse = randint(0, N-1)
    ran_day = randint(0, D)
    if randint(0, 1) == 1 and ran_day not in F[ran_nurse]:
            F[ran_nurse].append(ran_day)

# N, D, S, a, b, F = 18, 10, 4, 3, 7, [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1], [0], []]

solver = pywraplp.Solver.CreateSolver('SCIP')

x = {}
for nurse in range(N):
    for day in range(D):
        for shift in range(S+1):
            x[(nurse, day, shift)] = solver.IntVar(0, 1, f"x[{nurse}, {day}, {shift}]")

#constraints for feasible solution 

#nurse work at most 1 shift each day
for nurse in range(N):
    for day in range(D):
        constraint = solver.Constraint(1, 1)
        for shift in range(S+1):
            constraint.SetCoefficient(x[(nurse, day, shift)], 1)
            

#lower and upper bound for nurse per shift
for day in range(D):
    for shift in range(S):
        constraint = solver.Constraint(a, b)
        for nurse in range(N):
            constraint.SetCoefficient(x[(nurse, day, shift)], 1)

# night shift
for nurse in range(N):
    for day in range(1, D):
        constraint = solver.Constraint(0, 1)
        constraint.SetCoefficient(x[(nurse, day-1, S-1)], -1)
        constraint.SetCoefficient(x[(nurse, day, S)], 1)

# rest day
# for nurse in range(N):
#     for day in F[nurse]:
#         constraint = solver.Constraint(1, 1)
#         constraint.SetCoefficient(x[(nurse, day, S)], 1)


#max night shift
max_shift = solver.IntVar(0, 100,'max_shift')
for nurse in range(N):
    # for day in range(D):
    solver.Add(max_shift >= sum(x[(nurse, day, 3)] for day in range(D)))

#objective function
solver.Minimize(max_shift) 

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    optimal = [[[0 for shift in range(S+1)] for day in range(D)] for nurse in range(N)]
    for nurse in range(N):
        for day in range(D):
            for shift in range(S+1):
                optimal[nurse][day][shift] = int(x[(nurse, day, shift)].solution_value())
            

    # for i in optimal:
    #     print(i)
         
    print('', end = '\t')
    for day in range(D):
        print(f'Day {day+1}', end ='\t')
    print()
    for nurse in range(N):
        print(f'N {nurse+1}', end= '\t')
        for day in range(D):
            for shift in range(S):
                if optimal[nurse][day][shift] == 1:
                    print(shift+1, end = '\t')
                    break
            else:
                print('0', end = '\t')
        print()

    
    max_night_shift = 0
    for nurse in range(N):
        temp = 0
        for day in range(D):
            temp += optimal[nurse][day][3] 
        if max_night_shift < temp:
            max_night_shift = temp 
    
    print('\nMaximum night shift in the solution is' ,max_night_shift)


else:
    print('No feasible solution')


