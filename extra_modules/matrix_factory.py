import numpy as np
from scipy import sparse
from math import sqrt

class MatrixBuilder:

    def __init__(self, whichMatrix, params):

        matrices_available = ['laplace']

        if whichMatrix not in matrices_available:
            raise Exception("The requested matrix is not available to build in our framework.")

        self.params = params

        if ('nx' not in self.params) or ('ny' not in self.params):
            raise Exception("Dimensions of the matrix needed.")

        # Default params
        self.verbosity = "FULL"

        # Unpack params
        if 'verbosity' in params:
            self.verbosity = self.params['verbosity']
        self.nx = self.params['nx']
        self.ny = self.params['ny']

        # Some checks on self.nx and self.ny
        if self.nx!=self.ny: raise Exception("Cannot construct/invert nonsquare matrices.")
        if ((int(sqrt(self.nx)+0.5)**2)!=self.nx): raise Exception("We need nx and ny to be perfect squares.")

        #self.N = self.nx*self.ny

        if whichMatrix == 'laplace':
            self.mat_type = 'laplace'
            if self.verbosity == 'FULL':
                print("\nConstructing the matrix of type " + whichMatrix + ".")
        else:
            raise Exception("The requested matrix is not available to build for now.")


    def build(self):

        if self.verbosity == 'FULL':
            print("\nBuilding the matrix of type " + self.mat_type + ".")

        if self.mat_type == 'laplace':
            self.laplaceBuilder()
        else:
            raise Exception("The requested matrix is not available to build for now.")


    def laplaceBuilder(self):
        # Diagonals of the laplace matrix
        main_diag = np.ones(self.nx)*(-4.0)
        side_diag = np.ones(self.nx-1)
        side_diag[np.arange(1,self.nx)%4==0] = 0
        up_down_diag = np.ones(self.nx-3)
        diagonals = [main_diag,side_diag,side_diag,up_down_diag,up_down_diag]

        # Constructing the matrix through SciPy's sparse
        self.mat = sparse.diags(diagonals, [0, -1, 1,int(sqrt(self.nx)),-int(sqrt(self.nx))], format="csr", dtype=float)
        #self.mat = buf_mat.tocsr()


    def getDimsX(self):
        return self.nx


    def getDimsY(self):
        return self.ny


    def returnMat(self):
        return self.mat


    def display(self):
        print(self.mat.toarray())
