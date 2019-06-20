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
matType = "laplace"
params_matrix = dict()
# nx and ny represent dimensions of the lattice corresponding to this laplace matrix
params_matrix['nx'] = 64
params_matrix['ny'] = 64
A = MatrixBuilder(matType, params_matrix)
A.build()

# Build right hand sides, B_ysize corresponds to the number of right hand sides to be block-solved against
B_xsize = A.getDimsY()
B_ysize = 10
B = np.random.rand(B_xsize, B_ysize)

# Initial solution for the solves
x0 = np.zeros(A.getDimsX(), dtype=float)

# Use the different block krylov solvers

#py_impls = ["nonblocked", "blocked_classic", "blocked_li"]
pyImpls = ["classical", "li"]

use_py_modules = dict()
use_py_modules['classical'] = True
use_py_modules['li'] = True

for solverType in pyImpls:

    print("\n------------\nSolving the " + matType + " matrix using the " + solverType + " solver\n------------\n")

    # Build solver
    params_solver = dict()
    params_solver['maxiters'] = 100
    params_solver['verbosity'] = overall_verbosity
    params_solver['tol'] = 1e-6
    params_solver['test_after_solve'] = True
    params_solver['use_py_modules'] = use_py_modules[solverType]
    params_solver['block_krylov_type'] = solverType
    kSolver = Solver.create('krylov', solverType, params_solver)

    sol,execTime = kSolver.solve(A,B,x0)

    print("Execution time for the <" + solverType + "> solver: " + str(execTime))

#-------------------------------------------------------------

# TODO
# Call all the cpp implementation
