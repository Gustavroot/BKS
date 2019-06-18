import scipy.sparse.linalg as spla
import numpy as np
import warnings

class SolverKrylovNonblocked:

    def __init__(self, params):

        # Dict with all params
        self.params = params

        self.verbosity = self.params['verbosity']
        self.tol = self.params['tol']
        self.maxiters = self.params['maxiters']
        self.test_after_solve = self.params['test_after_solve']
        self.use_py_modules = self.params['use_py_modules']

        # TODO: check all the params (and of the correct type) were passed


    def solve(self, A, b, x0):

        if self.use_py_modules:
            solution, exit_code = spla.gmres(A.return_mat(), b, x0, tol=self.tol, maxiter=self.maxiters)
        else:
            warnings.warn("Own version of nonblocked GMRES not implemented yet. Returning a zero vector.")
            solution, exit_code = np.zeros(A.N), 0

        if exit_code==0:
            self.last_solve_result = solution
            if self.test_after_solve: self.test_solution(A,b)
            return solution
        elif exit_code:
            raise Exception("Tolerance not achieved !")
        else:
            raise Exception("Bad input params - or breakdown !")


    def test_solution(self, A, b):
        sol_is_correct = np.allclose(A.return_mat().dot(self.last_solve_result), b)

        if self.verbosity == 'FULL':
            if sol_is_correct:
                print("\nSolution agrees with Ax=b.")
            else:
                print("\nSolution doesn't agree with Ax=b.")
        elif self.verbosity == 'SILENT':
            pass
        else:
            raise Exception("Specified verbosity not available.")
