from random import *
from copy import deepcopy
import math
import time

# #random variable
N = randint(5, 30)                                #nurses
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

N, D, S, a, b, F = 18, 10, 4, 3, 7, [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1], [0], []]


#function to get neighbors of a feasible solution
def neighbor(ma):
    neighbors = []
    for i in range(50):
        temp_matrix = deepcopy(ma)
        nurse1 = randint(0, N-1)
        day1 = randint(0, D-1)
        shift1 = randint(0, S-1)
        temp_matrix[nurse1][day1] = [0 for i in range(S)]
        temp_matrix[nurse1][day1][shift1] = 1

        if feasible(temp_matrix) and temp_matrix not in neighbors:
            neighbors.append(temp_matrix)


        temp_matrix = deepcopy(ma)
        nurse2 = randint(0, N-1)
        day2 = randint(0, D-1)
        nurse3 = randint(0, N-1)
        day3 = randint(0, D-1)
        temp = temp_matrix[nurse2][day2]
        temp_matrix[nurse2][day2] = temp_matrix[nurse3][day3]
        temp_matrix[nurse3][day3] = temp
        if feasible(temp_matrix) and temp_matrix not in neighbors:
            neighbors.append(temp_matrix)

    return neighbors


#constraints for feasible solution 
def feasible(temp):
    #nurse work at most 1 shift each day
    for nurse in range(N):
        for day in range(D):
            num_shift = 0
            for shift in range(S):
                num_shift += temp[nurse][day][shift]
            if num_shift > 1:
                return False

    #lower bound for nurse per shift
    for day2 in range(D):
        for shift2 in range(S):
            sa=0
            for nurse2 in range(N):
                sa += temp[nurse2][day2][shift2]
            if sa < a:
                return False
    
    #upper bound for nurse per shift
    for day1 in range(D):
        for shift1 in range(S):
            sb=0
            for nurse1 in range(N):
                sb += temp[nurse1][day1][shift1]
            if sb > b:
                return False
    
    #rest day or night shift
    for day in range(D):
        for nurse in range(N):
            if day !=0 and temp[nurse][day-1][S-1] == 1 and 1 in temp[nurse][day]:
                return False
            if day in F[nurse] and 1 in temp[nurse][day]:
                return False

    return True


#function to get the maximum night shift of a nurse
def max_night_shift(temp_matrix):
    if temp_matrix == 'Cannot generate feasible solution in acceptable time':
        return
    max_night_shift = 0
    for nurse in range(N):
        temp = 0
        for day in range(D):
            temp += temp_matrix[nurse][day][3] 
        if max_night_shift < temp:
            max_night_shift = temp 
    return max_night_shift


#function to generate a feasible solution
lim = 0
def generate():
    global lim
    lim += 1

    #0-1_matrix
    matrix = [[[0 for shift in range(S)] for day in range(D)] for nurse in range(N)]

    for day in range(D):
        Nurse = list(range(N))
        temp = Nurse.copy()
        for nurse in range(N):
            if day != 0 and matrix[nurse][day-1][S-1] == 1:
                temp[nurse] = -1
            if day in F[nurse]:
                temp[nurse] = -1
        

        Nurse = []
        for i in temp:
            if i != -1:
                Nurse.append(i)
        

        for shift in range(S):
            # x = randint(a, b)
            for i in range(a):
                if Nurse != []:
                    random_num = randint(0, len(Nurse)-1)
                    random_nurse = Nurse.pop(random_num)
                    # Nurse.pop(random_num)
                    matrix[random_nurse][day][shift] = 1
                else:
                    break
    #limit the max depth recursion          
    if lim <= 900:
        if feasible(matrix):
            return matrix
        return generate()
    return 'Cannot generate feasible solution in acceptable time'

#function to print solution
def print_solution(solution):
    if solution == 'Cannot generate feasible solution in acceptable time':
        print(solution)
        return 
    print('', end = '\t')
    for day in range(D):
        print(f'Day {day+1}', end ='\t')
    print()
    for nurse in range(N):
        print(f'N {nurse+1}', end= '\t')
        for day in range(D):
            for shift in range(S):
                if solution[nurse][day][shift] == 1:
                    print(shift+1, end = '\t')
                    break
            else:
                print('0', end = '\t')
        print()


#function to find local optimization
def LocalSearch(solution):
    if solution == 'Cannot generate feasible solution in acceptable time':
        return solution
    while True:
        for neighbor1 in neighbor(solution):
            if max_night_shift(neighbor1) < max_night_shift(solution):
                solution = neighbor1
                break
            
        else:
            break
    
    return solution
    
start_time=time.time()
Local_solution = generate()
LocalSearch(Local_solution)
end_time=time.time()
print('Solution of Local Search:')
print_solution(Local_solution)
print('\nMaximum night shift in the solution is' ,max_night_shift(Local_solution))
print('Running time:', round((end_time-start_time),2), 's')
print()


#Iterated Local Search
def Iterated():
    solution = generate()
    if solution == 'Cannot generate feasible solution in acceptable time':
        return solution
    for i in range(200):
        temp = LocalSearch(solution)
        if max_night_shift(temp) < max_night_shift(solution):
            solution = temp
    return solution



start_time=time.time()
Iterated_solution = Iterated()
end_time=time.time()
print('Solution using Iterated Local Search:')
# print_solution(Iterated_solution)
print('\nMaximum night shift in the solution is' ,max_night_shift(Iterated_solution))
print('Running time:', round((end_time-start_time),2), 's')
print() 

#Simulated Annealing
def Anealing():
    solution = generate()
    # print(max_night_shift(solution))
    if solution == 'Cannot generate feasible solution in acceptable time':
        return solution
    T = 1000
    while T > 0.001:
        neighbor1 = choice(neighbor(solution))
        if max_night_shift(neighbor1) < max_night_shift(solution):
            solution = neighbor1
        elif math.exp((max_night_shift(solution) - max_night_shift(neighbor1))/T) > random():
            solution = neighbor1
        T *= 0.9

    return solution

start_time=time.time()
Anealing_solution = Anealing()
end_time=time.time()
print('Solution using Simulated Anealing:')
# print_solution(Anealing_solution)
print('\nMaximum night shift in the solution is' ,max_night_shift(Anealing_solution))
print('Running time:', round((end_time-start_time),2), 's')
print()


#Tabu Search
def Tabu():
    solution = generate()
    if solution == 'Cannot generate feasible solution in acceptable time':
        return solution
    solution = LocalSearch(solution)
    temp = LocalSearch(solution)
    visited = [temp]
    for i in range(100):
        neighbors = neighbor(temp)
        neighbors.sort(key = max_night_shift)
        for index in range(len(neighbors)):
            if neighbors[index] not in visited:
                temp = neighbors[index]
                visited.append(temp)
                break
        
        if i > 10:
            visited.pop(0)
    if visited != []:
        if max_night_shift(visited[-1]) < max_night_shift(solution):
            return visited[-1]
    return solution

start_time=time.time()
Tabu_solution = Tabu()
end_time=time.time()
print('Solution using Tabu Search:')
# print_solution(Tabu_solution)
print('\nMaximum night shift in the solution is' ,max_night_shift(Tabu_solution))
print('Running time:', round((end_time-start_time),2), 's')


