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

class SolverKrylovBlockedClassical(Solver):


    def solve(self, A, B, x0):

        # TODO: fix the way of processing/using <exit_code>

        X = np.empty(B.shape)

        execTime = 0

        if self.measureExecTime:
            execTime = time.time()

        if self.use_py_modules:

            exit_code = 0
            for i in range(B.shape[1]):
                X[:,i],exit_code_x = spla.gmres(A.returnMat(), B[:,i], x0, tol=self.tol, maxiter=self.maxiters)
                exit_code = (exit_code or exit_code_x)

        else:
            warnings.warn("Own version of nonblocked GMRES not implemented yet. Returning a zero vector.")
            solution, exit_code = np.zeros(A.N), 0

        if self.measureExecTime:
            execTime = time.time() - execTime

        if exit_code==0:
            self.last_solve_result = X
            if self.test_after_solve: self.test_solution(A,B)
            return (X,execTime)
        elif exit_code:
            raise Exception("Tolerance not achieved !")
        else:
            raise Exception("Bad input params - or breakdown !")
