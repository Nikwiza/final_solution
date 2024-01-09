import numpy as np
from itertools import combinations
'''
z - Koeficijenti glavne jednacine
o - Koeficijenti ogranicenja tipa jednakosti
b - Slobodni clanovi ogranicenja

'''

def pivot(tableau, num_constraints, pivot_row):
    tableau[pivot_row, :] /= tableau[pivot_row, -1]
    for i in range(num_constraints + 1):
        if i != pivot_row:
             tableau[i, :] -= tableau[i, -1] * tableau[pivot_row, :]

def find_pivot(tableau):
    second_last_column = tableau[1:, -2]
    last_column = tableau[1:, -1]
    result = np.divide(second_last_column, last_column, out=np.inf * np.ones_like(second_last_column), where=last_column != 0)
    result[result < 0] = np.inf
    return np.argmin(result[result > 0])+1

def check_basic_variables(B, b):
    try:
        inverse_matrix = np.linalg.inv(B)
        return np.all(np.dot(inverse_matrix, b)>=0) 
    except np.linalg.LinAlgError:
        return False

def revised_simplex(C, A, b):
    # Trazenje baznih promenljivih
    num_constraints, num_variables = A.shape
    found_basic_vars = False
    # Prvo proveravamo da li poslednjih num_variables mogu biti bazne (Cesto su to parazitske promenljive)
    B = A[:, -num_constraints:]
    base_index = list(range(num_variables-num_constraints, num_variables))

    if not check_basic_variables(B, b):
        # Ako ne mogu te variable, isprobaj sve kombinacije
        potential_bases = np.array(list(combinations([i for i in range(num_variables)], num_constraints)), dtype=np.ndarray)
        for base in potential_bases:
            base_index = np.array(base, dtype=int)
            B = A[:, base_index]
            if check_basic_variables(B, b):
                found_basic_vars = True
                break
        if not found_basic_vars:
            print('Error: Base not found')
            quit()
        

    # Prva iteracija
    # Konstrukcija tabele
    tableau = np.zeros((num_constraints + 1, num_constraints + 2))
    Bi = np.linalg.inv(B)
    tableau[1:num_constraints+1, :num_constraints] = Bi
        # Iterativni korak
    optimal_solution = None
    solution_values = np.zeros(num_variables)
    while True:
        W = C[base_index] @ Bi
        b_ = Bi@b
        tableau[1:num_constraints+1, num_constraints:num_constraints+1] = b_.reshape(-1, 1)
        tableau[0, :num_constraints] = W
        tableau[0, num_constraints] = C[base_index]@b_

        non_base_index = np.array([i for i in range(len(C)) if i not in base_index], dtype=int)

        coefficients_matrix = A[:, non_base_index].T

        J = [W@j-C[i] for j, i in zip(coefficients_matrix, non_base_index)]
        if all(x >= 0 for x in J):
            optimal_solution = tableau[0, -2]
            for index, value in zip(base_index, tableau[1:, -2]):
                solution_values[index] = value
            break

        min_index_in_J = np.argmin(J)
        min_index_in_non_base = non_base_index[min_index_in_J]
        tableau[0,-1] = J[min_index_in_J]
        tableau[1:, -1] = Bi@coefficients_matrix[min_index_in_J]
        
        pivot_row = find_pivot(tableau)
        pivot(tableau, num_constraints, pivot_row)

        # Menjamo bazne promen.
        base_index[pivot_row-1], non_base_index[min_index_in_J] = non_base_index[min_index_in_J], base_index[pivot_row-1]
        Bi = tableau[1:, :num_constraints]

    print(optimal_solution, solution_values)
        



# Primer sa vezbi
C = np.array([3.8, 4.25, 0, 0, 0, 0])
A = np.array([[1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [3, 5, 0, 0, 1, 0], [20, 10, 0, 0, 0, 1]])
b = np.array([28, 30, 180, 640])
revised_simplex(C, A, b)