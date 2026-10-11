import pathlib

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    matrix, sol = [], []
    symbols, numbers = ['+', '-'], [i for i in range(10)]

    content = path.read_text().split("\n")
    #print(content)
    
    for line in content:
        equation = []
        if line == '':
            continue

        coef_x = None
        sgn = 1
        for char in line:
            if char in " +=":
                continue

            if char == '-':
                sgn = -1
                continue

            if char == 'x' or char == 'y' or char == 'z':
                if coef_x is None:
                    coef_x = 1

                equation.append(float(coef_x) * sgn)
                coef_x, sgn = None, 1
                continue

            if coef_x is None:
                coef_x = char
            else:
                coef_x += char
        
        matrix.append(equation)
        sol.append(float(coef_x) * sgn)

    return matrix, sol
    #return [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0, 0]

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")

def determinant(matrix: list[list[float]]) -> float:
    #return 0.0
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - \
            matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) + \
            matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    #return 0.0
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    #return 0.0
    import math 
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    #return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    result = []
    for idx in range(len(matrix)):
        new_row = []
        for row in matrix:
            new_row.append(row[idx])
        result.append(new_row)

    return result

print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    #return [0, 0, 0]
    result, length = [], len(vector)
    for row in matrix:
        sum = 0
        for idx in range(length):
            sum += row[idx] * vector[idx]
        result.append(sum)
    
    return result
print(f"{multiply(A, B)=}")

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    #return [0.0, 0.0, 0.0]
    
    def replace_col(matrix: list[list[float]], vector: list[float],
                    index: int) -> list[list[float]]:

        new_matr, leng = [], len(matrix)
        for idx in range(leng):
            line = []
            for col in range(leng):
                if col == index:
                    line.append(vector[idx])
                else:
                    line.append(matrix[idx][col])
            new_matr.append(line)

        return new_matr

    matrix_det, length = determinant(matrix), len(matrix)
    
    x_matr = replace_col(matrix, vector, 0)
    x_det = determinant(x_matr)
    #print(x_matr)

    y_matr = replace_col(matrix, vector, 1)
    y_det = determinant(y_matr)
    #print(y_matr)

    z_matr = replace_col(matrix, vector, 2)
    z_det = determinant(z_matr)
    #print(z_matr)

    return [x_det / matrix_det, y_det / matrix_det, z_det / matrix_det]

print(f"{solve_cramer(A, B)=}")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    #return [[0, 0], [0, 0]]
    minor, length = [], len(matrix)
    for idx in range(length):
        line = []
        if idx == i:
            continue
        for col in range(length):
            if col == j:
                continue
            line.append(matrix[idx][col])

        minor.append(line)

    return minor

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    #return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    cofactor_matrix, length = [], len(A)
    for idx in range(length):
        line = []
        for col in range(length):
            minr = minor(matrix, idx, col)
            det = minr[0][0] * minr[1][1] - minr[0][1] * minr[1][0]
            det *= (-1)**(idx + col)
            line.append(det)
        cofactor_matrix.append(line)

    return cofactor_matrix


def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    #return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return transpose(matrix)

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    #return [0, 0, 0]
    inverse_matrix = adjoint(cofactor(matrix))
    det, length = determinant(matrix), len(matrix)
    for idx in range(length):
        for col in range(length):
            inverse_matrix[idx][col] *= 1/det
    #print(inverse_matrix)
    return multiply(inverse_matrix, vector)

print(f"{solve(A, B)=}")
