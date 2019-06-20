# Local dir
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += '/'

import sys
import warnings
import numpy as np

class Solver:

    # Attributes - to be inherited by the actual solvers
    measureExecTime = True

    def __init__(self, params):

        # Dict with all params
        self.params = params

        self.verbosity = self.params['verbosity']
        self.tol = self.params['tol']
        self.maxiters = self.params['maxiters']
        self.test_after_solve = self.params['test_after_solve']
        self.use_py_modules = self.params['use_py_modules']

        self.blockKrylovType = self.params['block_krylov_type']

        # TODO: check all the params (and of the correct type) were passed


    def create(solver_type, solver_subtype, params):

        if solver_type != 'krylov':
            raise Exception("Only krylov methods implemented for now.")

        # Check if the chosen krylov method is implemented
        types_of_kr = ["classical", "li"]
        type_of_kr = solver_subtype

        if type_of_kr not in types_of_kr:
            raise Exception("The chosen krylov method is not implemented for now.")

        if type_of_kr == 'classical':

            sys.path.append(dir_path + 'krylov_solvers/blocked_classical')
            from solver_krylov_blocked_classical import SolverKrylovBlockedClassical
            return SolverKrylovBlockedClassical(params)

        elif type_of_kr == 'li':

            warnings.warn("Solver <" + type_of_kr + "> is under construction. This solver will return a zero vector.")
            sys.path.append(dir_path + 'krylov_solvers/blocked_li')
            from solver_krylov_blocked_li import SolverKrylovBlockedLi
            return SolverKrylovBlockedLi(params)

        else:
            raise Exception("Solver <" + type_of_kr + "> is under construction.")


    def test_solution(self, A, B):


        sol_is_correct = True
        for i in range(B.shape[1]):
            sol_is_correct = np.allclose(A.returnMat().dot(self.last_solve_result[:,i]), B[:,i])

        if self.verbosity == 'FULL':
            if sol_is_correct:
                print("\nSolution agrees with Ax=b.")
            else:
                print("\nSolution doesn't agree with Ax=b.")
        elif self.verbosity == 'SILENT':
            pass
        else:
            raise Exception("Specified verbosity not available.")
