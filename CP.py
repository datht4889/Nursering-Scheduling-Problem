from ortools.sat.python import cp_model
from random import *
import math
import time

# random instance
N = randint(20, 100)                              #nurses
D = randint(15, 30)                               #days
S = 4                                             #shifts
a = randint(1, int(N/S))                          #min_nurses_per_shift
b = randint(math.ceil(N/S), math.ceil(1.5*N/S))   #max_nurses_per_shift
F = [[] for i in range(N)]                        #free_days


for i in range(randint(0, N)):
    ran_nurse = randint(0, N-1)
    ran_day = randint(0, D)
    if randint(0, 1) == 1 and ran_day not in F[ran_nurse]:
            F[ran_nurse].append(ran_day)


start_time = time. time()

model = cp_model.CpModel()


x = {}
for nurse in range(N):
    for day in range(D):
        for shift in range(S):
            x[(nurse, day, shift)] = model.NewBoolVar(f"x[{nurse}, {day}, {shift}]")


#nurse work at most 1 shift each day
for nurse in range(N):
    for day in range(D):
        model.AddAtMostOne(x[(nurse, day, shift)] for shift in range(S))

#lower and upper bound for nurse per shift
for day in range(D):
    for shift in range(S):
        model.Add(sum(x[(nurse, day, shift)] for nurse in range(N)) <= b)
        model.Add(sum(x[(nurse, day, shift)] for nurse in range(N)) >= a)


# night shift
for nurse in range(N):
    for day in range(D-1):
        for shift in range(S):
            m=model.NewBoolVar('m')
            model.Add(x[(nurse, day, 3)]==1).OnlyEnforceIf(m)
            model.Add(x[(nurse, day, 3)]==0).OnlyEnforceIf(m.Not())
            model.Add(x[(nurse, day+1, shift)]==0).OnlyEnforceIf(m)


# rest day
for nurse in range(N):
    for day in range(D):
        if day in F[nurse]:
            for shift in range(S):
                model.Add(x[(nurse, day, shift)]==0)


#max night shift
max_shift3 = model.NewIntVar(0, 100,'max_shift3')
for nurse in range(N):
    # for day in range(D):
    model.Add(max_shift3 >= sum(x[(nurse, day, 3)] for day in range(D)))
      
#objective function
model.Minimize(max_shift3) 

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    optimal = [[[0 for shift in range(S)] for day in range(D)] for nurse in range(N)]
    for nurse in range(N):
        for day in range(D):
            for shift in range(S):
                optimal[nurse][day][shift] = (solver.Value(x[(nurse, day, shift)]))
            

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

    end_time = time.time()
    print('Running time:', round(end_time - start_time, 2), 's')

else:
    print('No feasible solution')

