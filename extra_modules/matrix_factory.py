import numpy as np
from scipy import sparse

class MatrixBuilder:

    def __init__(self, which_matrix, params):

        matrices_available = ['laplace']

        if which_matrix not in matrices_available:
            raise Exception("The requested matrix is not available to build in our framework.")

        self.params = params

        # Unpack params
        self.verbosity = self.params['verbosity']
        self.nx = self.params['nx']
        self.ny = self.params['ny']

        #if self.nx!=self.ny: raise Exception("Cannot construct/invert nonsquare matrices.")

        self.N = self.nx*self.ny

        if which_matrix == 'laplace':
            self.mat_type = 'laplace'
            if self.verbosity == 'FULL':
                print("\nConstructing the matrix of type " + which_matrix + ".")
            elif self.verbosity == 'SILENT':
                pass
            else:
                raise Exception("Specified verbosity not available.")
        else:
            raise Exception("The requested matrix is not available to build for now.")


    def build(self):

        if self.verbosity == 'FULL':
            print("\nBuilding the matrix of type " + self.mat_type + ".")
        elif self.verbosity == 'SILENT':
            pass
        else:
            raise Exception("Specified verbosity not available.")

        if self.mat_type == 'laplace':

            # Diagonals of the laplace matrix
            main_diag = np.ones(self.N)*(-4.0)
            side_diag = np.ones(self.N-1)
            side_diag[np.arange(1,self.N)%4==0] = 0
            up_down_diag = np.ones(self.N-3)
            diagonals = [main_diag,side_diag,side_diag,up_down_diag,up_down_diag]

            # Constructing the matrix through SciPy's sparse
            self.mat = sparse.diags(diagonals, [0, -1, 1,self.nx,-self.nx], format="csr", dtype=float)
            #self.mat = buf_mat.tocsr()

        else:
            raise Exception("The requested matrix is not available to build for now.")


    def return_mat(self):
        return self.mat


    def display(self):
        print(self.mat.toarray())
