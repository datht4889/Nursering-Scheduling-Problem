from copy import deepcopy

N = 10                           #nurses
D = 2                           #days
S = 4                           #shifts
a = 1                           #min_nurses_per_shift
b = 6                           #max_nurses_per_shift
F= [[] for i in range(N)]       #free_days

#0-1_matrix
matrix = [[[0 for shift in range(S)] for day in range(D)] for nurse in range(N)]

#All solution saved
result = []

#function to check position 
def isSafe(nurse, day, shift):
    #nurse_per_shift <= b
    for day1 in range(D):
        for shift1 in range(S):
            sb=0
            for nurse1 in range(N):
                sb += matrix[nurse1][day1][shift1]
            if sb > b:
                return False

    #night_shift previous day
    if day != 0 and matrix[nurse][day-1][3] == 1:
        return False

    # free_day F
    if day in F[nurse]:
        return False

    return True



#solving function
def solve(nurse, day):
    #when all postition is filled
    
    if nurse == N-1 and day == D:
        # nurse_per_shift >= a
        for day2 in range(D):
            for shift2 in range(S):
                sa=0
                for nurse2 in range(N):
                    sa += matrix[nurse2][day2][shift2]
                if sa < a:
                    return False

        # nurse_per_shift <=b
        for day1 in range(D):
            for shift1 in range(S):
                sb=0
                for nurse1 in range(N):
                    sb += matrix[nurse1][day1][shift1]
                    if sb > b:
                        return False 

        result.append(deepcopy(matrix))
        return True
    

    if day == D:
        day=0
        nurse+=1

    for shift in range(S):
        if isSafe(nurse, day, shift):
            matrix[nurse][day][shift] = 1
            # print(matrix)
        if solve(nurse, day+1):
            return True 
            
        matrix[nurse][day][shift] = 0
    return False



if solve(0,0):
    print('', end = '\t')
    for day in range(D):
        print(f'Day {day+1}', end ='\t')
    print()
    for nurse in range(N):      
        print(f'N {nurse+1}', end= '\t')
        for day in range(D):
            for shift in range(S):
                if matrix[nurse][day][shift] == 1:
                    print(shift+1, end = '\t')
                    break
            else:
                print('0', end = '\t')
        print()
else:
    print('No feasible solution')


