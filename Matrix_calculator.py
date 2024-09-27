from fractions import Fraction

def input_matrix():
    row = int(input("Enter the number of rows: "))
    column = int(input("Enter the number of columns: "))
    
    matrix = []
    print("Enter the entries rowwise:")
    
    for i in range(row):
        a = []
        for j in range(column):
            a.append(Fraction(input()))
        matrix.append(a)
    
    identity_matrix = None
    if row == column:
        identity_matrix = [[Fraction(int(i == j)) for j in range(row)] for i in range(row)]
    
    return matrix, identity_matrix

def print_matrices(matrix, identity_matrix, step_number, operation=""):
    print(f"\nStep {step_number}: {operation}")
    for i in range(len(matrix)):
        formatted_row = ' '.join([str(x.limit_denominator()) for x in matrix[i]])
        if identity_matrix:
            formatted_id_row = ' '.join([str(x.limit_denominator()) for x in identity_matrix[i]])
            print(formatted_row + ' | ' + formatted_id_row)
        else:
            print(formatted_row)

def perform_row_operations(matrix, identity_matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    step_number = 1
    elementary_matrices_operations = []

    for col in range(min(num_rows, num_cols)):
        pivot_row = None
        for i in range(col, num_rows):
            if matrix[i][col] != 0:
                pivot_row = i
                break

        if pivot_row is None:
            continue

        if pivot_row != col:
            matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
            if identity_matrix:
                identity_matrix[col], identity_matrix[pivot_row] = identity_matrix[pivot_row], identity_matrix[col]
                elementary_matrices_operations.append(f"R{col+1} <-> R{pivot_row+1}")
            print_matrices(matrix, identity_matrix, step_number, f"R{col+1} <-> R{pivot_row+1}")
            step_number += 1

        pivot = matrix[col][col]
        if pivot != 1:  # Normalize pivot row
            for j in range(num_cols):
                matrix[col][j] /= pivot
                if identity_matrix:
                    identity_matrix[col][j] /= pivot
            elementary_matrices_operations.append(f"R{col+1} -> R{col+1} / {pivot}")
            print_matrices(matrix, identity_matrix, step_number, f"R{col+1} -> R{col+1} / {pivot}")
            step_number += 1

        for i in range(num_rows):
            if i != col and matrix[i][col] != 0:
                factor = matrix[i][col]
                for j in range(num_cols):
                    matrix[i][j] -= factor * matrix[col][j]
                    if identity_matrix:
                        identity_matrix[i][j] -= factor * identity_matrix[col][j]
                elementary_matrices_operations.append(f"R{i+1} -> R{i+1} - ({factor})R{col+1}")
                print_matrices(matrix, identity_matrix, step_number, f"R{i+1} -> R{i+1} - ({factor})R{col+1}")
                step_number += 1
    return elementary_matrices_operations

def display_elementary_matrices(operations):
    print("\nSystem of Elementary Matrices to create A:")
    operation_str = "A = "
    for op in operations:
        operation_str += f"[{op}] "
    print(operation_str)

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

def main():
    matrix, identity_matrix = input_matrix()
    
    print("\nInput Matrix:")
    print_matrices(matrix, identity_matrix, 0)
    
    elementary_matrices_operations = perform_row_operations(matrix, identity_matrix)
    
    find_solutions(matrix)
    
    display_elementary_matrices(elementary_matrices_operations)

main()
