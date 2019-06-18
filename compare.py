# Enforce Python3 usage
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# Local dir
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += '/'

import numpy as np

# Append local modules necessary for the tests
sys.path.append(dir_path + 'Python/')
sys.path.append(dir_path + 'extra_modules/')

# Imports associated to sys.path.append
from solvers import Solver
from matrix_factory import MatrixBuilder

#------------------------------------------------------------


# Tests

# Fixing seed for tests
np.random.seed(12347)

overall_verbosity = "FULL"

# First, build the matrix to invert
mat_type = "laplace"
params_matrix = dict()
# nx and ny represent dimensions of the lattice corresponding to this laplace matrix
params_matrix['nx'] = 4
params_matrix['ny'] = 4
params_matrix['verbosity'] = overall_verbosity
A = MatrixBuilder(mat_type, params_matrix)
A.build()

# Build rhs
# TODO: change the following for an apropriate general build
b = np.random.rand(A.N)

# Initial solution for the solves
x0 = np.zeros(A.N, dtype=float)

# Use the different solvers

#py_impls = ["nonblocked", "blocked_classic", "blocked_li"]
py_impls = ["nonblocked", "blocked_li"]

use_py_modules = dict()
use_py_modules['nonblocked'] = True
use_py_modules['blocked_li'] = True

for solver_type in py_impls:

    print("\n------------\nSolving the " + mat_type + " matrix using the " + solver_type + " solver\n------------\n")

    # Build solver
    params_solver = dict()
    params_solver['maxiters'] = 100
    params_solver['verbosity'] = overall_verbosity
    params_solver['tol'] = 1e-6
    params_solver['test_after_solve'] = True
    params_solver['use_py_modules'] = use_py_modules[solver_type]
    k_solver = Solver('krylov', solver_type, params_solver)

    sol = k_solver.solve(A,b,x0)

#-------------------------------------------------------------

# TODO
# Call all the cpp implementation
