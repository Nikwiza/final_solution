import numpy as np
import math

def hungerian(cost_matrix):
    # Konstruisemo matricu i oduzimamo najmanji element u svakoj vrsti od cele vrste

    row_min_vals = np.min(cost_matrix, axis=1)
    reduced_matrix = cost_matrix - row_min_vals[:, None]
    col_min_vals = np.min(reduced_matrix, axis=0)
    reduced_matrix = reduced_matrix - col_min_vals[None, :]

    num_rows, num_cols = reduced_matrix.shape

    # Iterativni korak

    while True:
        assigned_rows = []
        assigned_cols = []

        # Trazenje nezavisnih nula

        for i in range(num_rows):
            zero_count = 0
            for j in range(num_cols):
                if j not in assigned_cols:
                    if reduced_matrix[i, j] == 0:
                        zero_count += 1
                        temp_j = j
            if zero_count == 1:
                assigned_rows.append(i)
                assigned_cols.append(temp_j)

        # Trazenje nezavisnih nula posle eliminacije vec izabranih
                
        for i in range(num_rows):
            for j in range(num_cols):
                if i not in assigned_rows and j not in assigned_cols:
                    if reduced_matrix[i, j] == 0:
                        assigned_rows.append(i)
                        assigned_cols.append(j)

        assigned_row_col_dict = dict(zip(assigned_rows, assigned_cols))

        if len(assigned_rows) == num_rows:
            break

        marked_rows = []
        crossed_rows = []
        crossed_cols = []

        # Oznacavamo redove koji nemaju jedinstvene 0 i precrtavamo sve kolone sa 0 u tim redovima
        for i in range(num_rows):
            if i not in assigned_rows:
                marked_rows.append(i)
            if i in marked_rows:
                for j in range(num_cols):
                    if j not in crossed_cols and reduced_matrix[i, j] == 0:
                        crossed_cols.append(j)

        # Oznacujemo redove sa 0 u toj precrtanim kolonama i precrtavamo sve ostale
        for i in range(num_rows):
            for j in range(num_cols):
                if i in assigned_row_col_dict and j == assigned_row_col_dict[i] and j in crossed_cols:
                    marked_rows.append(i)
            if i not in marked_rows:
                crossed_rows.append(i)

        # Odredjujemo najmanju vrednost koja nije precrtana
        min_val = math.inf
        for i in range(num_rows):
            if i not in crossed_rows:
                for j in range(num_cols):
                    if j not in crossed_cols:
                        if reduced_matrix[i, j] < min_val:
                            min_val = reduced_matrix[i, j]

        # Oduzimamo tu vrednost od elemenata koji nisu precrtani, a dodajemo onima sto su dva puta precrtani
        for i in range(num_rows):
            for j in range(num_cols):
                if i not in crossed_rows and j not in crossed_cols:
                    reduced_matrix[i, j] -= min_val
                elif i in crossed_rows and j in crossed_cols:
                    reduced_matrix[i, j] += min_val

    # Uzimamo izabrane poslove i racunamo po staroj matrici cenu poslova
    total_cost = 0
    print('Radnik: posao/cena')
    for key, value in assigned_row_col_dict.items():
        print(key, ':', value, '/', cost_matrix[key, value])
        total_cost += cost_matrix[key, value]
    print('Optimalna cena: ', total_cost)

    return total_cost, assigned_row_col_dict

# Primer sa vezbi
cost_matrix = np.array([[14, 9, 12, 8, 16],
                       [8, 7, 9, 9, 14],
                       [9, 11, 10, 10, 12],
                       [11, 8, 8, 6, 14],
                       [11, 9, 10, 7, 13]])

hungerian(cost_matrix)
