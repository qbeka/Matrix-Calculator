#Augmented to REF Matrix to RREF Matrix
#WORKING

from fractions import Fraction

def input_matrix(): #complete
    row = int(input("Enter the number of rows: "))
    column = int(input("Enter the number of columns: "))
     
    matrix = []
    print("Enter the entries rowwise:")
     
    for i in range(row):
        a =[]
        for j in range(column):
            a.append(int(input()))
        matrix.append(a)
        
    return matrix
    


def matrix_to_RREF(matrix): #complete
    def eliminate_above(matrix, row, col):
        for i in range(row - 1, -1, -1):
            factor = matrix[i][col]
            for j in range(len(matrix[0])):
                matrix[i][j] -= factor * matrix[row][j]
            if factor != 0:
                print(f"Operation: R{i+1} -> R{i+1} - ({factor})R{row+1}:")

    print("\nTransforming to RREF:")
    num_rows = len(matrix)
    num_cols = len(matrix[0])    
    step_number = 1

    for i in range(num_rows - 1, -1, -1):
        pivot_col = None
        for j in range(num_cols):
            if matrix[i][j] == 1:
                pivot_col = j
                print(f"\nStep {step_number}: Eliminating entries above the leading 1 in column {pivot_col + 1}")
                eliminate_above(matrix, i, pivot_col)
                print_matrix(matrix)
                step_number += 1
                break

    return matrix


def matrix_to_REF(matrix): #complete
    def swap_rows(matrix, row1, row2):
        matrix[row1], matrix[row2] = matrix[row2], matrix[row1]

    def find_best_row(matrix, col, start_row):
        best_row = start_row
        min_fraction_count = float('inf')

        for i in range(start_row, len(matrix)):
            if matrix[i][col] != 0:
                temp_row = [Fraction(x) / matrix[i][col] for x in matrix[i]]
                fraction_count = sum(1 for x in temp_row if x.denominator != 1)

                if fraction_count < min_fraction_count:
                    min_fraction_count = fraction_count
                    best_row = i

                if fraction_count == 0:
                    break

        return best_row

    def make_first_entry_one(matrix, row, col):
        divisor = matrix[row][col]
        if divisor != 0:
            for j in range(len(matrix[0])):
                matrix[row][j] = Fraction(matrix[row][j]) / divisor

    def eliminate_below(matrix, row, col):
        for i in range(row + 1, len(matrix)):
            factor = matrix[i][col]
            for j in range(len(matrix[0])):
                matrix[i][j] -= factor * matrix[row][j]
            if factor != 0:
                print(f"Operation: R{i+1} -> R{i+1} - ({factor})R{row+1}:")

    print("\nTransforming to REF:")
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    step_number = 1

    for step in range(min(num_rows, num_cols)):
        pivot_row = find_best_row(matrix, step, step)

        if matrix[pivot_row][step] == 0:
            print(f"\nStep {step_number}: No non-zero entries found in column {step + 1}")
            step_number += 1
            continue

        if pivot_row != step:
            swap_rows(matrix, step, pivot_row)
            print(f"\nStep {step_number}: Swapping row {step + 1} with row {pivot_row + 1}")
            print_matrix(matrix)
            step_number += 1

        divisor = matrix[step][step]
        make_first_entry_one(matrix, step, step)
        print(f"\nStep {step_number}: Making the first entry of row {step + 1} a 1 by dividing with {divisor}")
        print_matrix(matrix)
        step_number += 1

        for i in range(step + 1, len(matrix)):
            factor = matrix[i][step]
            if factor != 0:
                print(f"\nStep {step_number}: Making entry in row {i + 1}, column {step + 1} zero by subtracting {factor} times row {step + 1}")
                eliminate_below(matrix, step, step)
                print_matrix(matrix)
                step_number += 1

    return matrix

def print_matrix(matrix): #complete
    for row in matrix:
        formatted_row = [' '.join([str(Fraction(x).limit_denominator()) for x in row])]
        print(' '.join(formatted_row))
        
        
def find_rank(matrix):
    
    rank = 0
    
    num_rows = len(matrix)
    num_cols = len(matrix[0]) - 1

    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i][j] == 1:
                rank += 1
            
    print(f"Your rank is {rank}")
         
        
def find_solutions(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0]) - 1

    pivot_cols = set()
    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i][j] == 1:
                pivot_cols.add(j)
                break

    free_vars = [j for j in range(num_cols) if j not in pivot_cols and any(matrix[i][j] != 0 for i in range(num_rows))]

    inconsistent = any(all(matrix[i][j] == 0 for j in range(num_cols)) and matrix[i][num_cols] != 0 for i in range(num_rows))
    if inconsistent:
        print("\nThe system has no solutions.")
        return
    
    if free_vars:
        print("\nThe system has infinitely many solutions:")
        for i in range(num_rows):
            equation = []
            for j in range(num_cols):
                coeff = matrix[i][j]
                if j in free_vars:
                    var = f"s"
                    if coeff == -1:
                        equation.append(f"-{var}")
                    elif coeff == 1:
                        equation.append(var)
                    elif coeff != 0:
                        equation.append(f"{Fraction(-coeff).limit_denominator()}*{var}")

            constant = matrix[i][num_cols]
            if constant != 0:
                equation.append(f"{Fraction(constant).limit_denominator()}")

            print(f"x{i+1} = {' + '.join(equation)}" if equation else f"x{i+1} = 0")

        print(f"Where x{j+1} represents {' and '.join(f's' for j in free_vars)} and is of the real numbers.")
    else:
        print("\nThe system has a unique solution:")
        for i in range(num_rows):
            print(f"x{i+1} = {Fraction(matrix[i][num_cols]).limit_denominator()}")

def main(): #complete
    
    matrix = input_matrix()
    print("\nAugmented Matrix:")
    print_matrix(matrix)
    
    ref_matrix = matrix_to_REF(matrix)
    print("\nMatrix in REF:")
    print_matrix(ref_matrix)

    rref_matrix = matrix_to_RREF(matrix)
    print("\nMatrix in RREF:")
    print_matrix(rref_matrix)
    
    find_solutions(rref_matrix)
    
    find_rank(rref_matrix)
    

main()
    