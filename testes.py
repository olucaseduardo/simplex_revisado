from numpy.ma.core import shape

from src.simplex.reviewed_simplex import ReviewedSimplex
from src.simplex.simplex_methods import SimplexMethods
from src.simplex.standard_form import StandardForm
import numpy as np

from src.utils.matrix_util import remove_last_columns, get_two_phase_c

# c = [2, 3]
# A = [[1, 1], [1, 0], [1, 0], [0, 1], [0, 1]]
# b = [10000, 1500, 6000, 2500, 5000]
# D = ["<=", ">=", "<=", ">=", "<="]

c = [2,1]
A = [[-2,3],[3,2]]
b = [9,12]
D = [">=",">="]

c = [7,10]
A = [[2,1],[2,6]]
b = [6,15]
D = [">=",">="]
# #
# c = [1,-2   ]
# A = [[1,1],[-1,1],[0,1]]
# b = [2,1,3]
# D = [">=",">=","<="]

# c = [2, 3, 4]
# A = [[1, 2, -3], [-2, 0, 3], [1, 1, 0]]
# b = [10, 15, 8]
# D = ["<=", ">=", "="]

# c = [1,1]
# A = [[2,-1],[-1,2]]
# b = [6,6]
# D = [">=", ">="]

# c = [1,-2,2]
# A = [[1,1,1], [2,-1,3]]
# b = [3,4]
# D = ["=", "<="]

c = [1,1]
A = [[1,4], [3,1]]
b = [4,1]
D = [">=", "="]

# c = [4,8]
# A = [[3,2], [1,1],[1,0]]
# b = [18,5,4]
# D = ["<=", ">=", "<="]
#
# c = [2,3,4]
# A = [[1,2,-3], [-2,0,3],[1,1,0]]
# b = [10,15,8]
# D = ["<=", ">=", "="]

#
# c = [12,8]
# A = [[4,2], [3,4]]
# b = [3,4]
# D = ["<=", "<="]

artificial_count = D.count(">=") + D.count("=")

objective = "Minimizar"

standard_form = StandardForm.execute({
    "A": A,
    "b": b,
    "D": D,
    "c": c,
    "objective": objective,
    "method":"Big M"
})

print(standard_form)

simplex_methods = SimplexMethods(standard_form)
result = (simplex_methods.execute())
if result == 1:
    print("INFINITO")
    exit(1)
print(result[4]())

print(np.array([1,2,3]).shape[0])