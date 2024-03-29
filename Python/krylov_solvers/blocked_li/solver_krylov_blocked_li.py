import scipy.sparse.linalg as spla
import numpy as np
import warnings
import sys
import time

# Local dir
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += '/'

sys.path.append(dir_path + '../../')
from solvers import Solver

class SolverKrylovBlockedLi(Solver):

    def solve(self, A, B, x0):

        execTime = 0

        if self.measureExecTime:
            execTime = time.time()

        warnings.warn("Solver <blocked_li> not implemented yet. Returning a zero vector.")
        #solution, exit_code = np.zeros(A.getDimsX()), 0
        solution, exit_code = np.zeros(B.shape), 0

        #if self.use_py_modules:
        #    solution, exit_code = spla.gmres(A.returnMat(), b, x0, tol=self.tol, maxiter=self.maxiters)
        #else:
        #    warnings.warn("Own version of nonblocked GMRES not implemented yet. Returning a zero vector.")
        #    solution, exit_code = np.zeros(A.N), 0

        if self.measureExecTime:
            execTime = time.time() - execTime

        if exit_code==0:
            self.last_solve_result = solution
            if self.test_after_solve: self.test_solution(A,B)
            return (solution,execTime)
        elif exit_code:
            raise Exception("Tolerance not achieved !")
        else:
            raise Exception("Bad input params - or breakdown !")
