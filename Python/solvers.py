# Local dir
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += '/'

import sys
import warnings

class Solver:

    def __init__(self, solver_type, solver_subtype, params):

        if solver_type != 'krylov':
            raise Exception("Only krylov methods implemented for now.")

        # Check if the chosen krylov method is implemented
        self.types_of_kr = ["nonblocked", "blocked_classic", "blocked_li"]
        self.type_of_kr = solver_subtype
        if self.type_of_kr not in self.types_of_kr:
            raise Exception("The chosen krylov method is not implemented for now.")

        if self.type_of_kr == 'nonblocked':

            sys.path.append(dir_path + 'krylov_solvers/nonblocked')

            from solver_krylov_nonblocked import SolverKrylovNonblocked

            self.solver = SolverKrylovNonblocked(params)

        elif self.type_of_kr == 'blocked_li':
            warnings.warn("Solver <" + self.type_of_kr + "> is under construction. This solver will return a zero vector.")

            sys.path.append(dir_path + 'krylov_solvers/blocked_li')

            from solver_krylov_blocked_li import SolverKrylovBlockedLi

            self.solver = SolverKrylovBlockedLi(params)

        else:
            raise Exception("Solver <" + self.type_of_kr + "> is under construction.")
            


    def solve(self, A, b, x0):

        return self.solver.solve(A,b,x0)
