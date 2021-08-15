import math
from math import sqrt
import numbers


def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

    
def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

    
def dot_product(vector_one, vector_two):
    if len(vector_one) != len(vector_two):
        print("error! Vectors must have same length")
    result = 0
    for i in range(len(vector_one)):
        result += vector_one[i] * vector_two[i]
    return result
    
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            return self.g[0][0]

        elif self.h ==  2:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]
            determinant = (a * d) - (b * c)
            return determinant

        return None

    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        sum = 0
        for i in range(len(self.g)):
            for j in range(len(self.g)):
                if i == j:
                    sum += self.g[i][j]
        return sum
    

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        inverse = identity(self.h)

        if len(self.g) == 1:
            inverse[0][0] = 1 / self.g[0][0]

        elif len(self.g) == 2:
            determinant = self.determinant()
            if determinant == 0:
                raise ValueError('A non-invertible')
            else:
                a = self.g[0][0]
                b = self.g[0][1]
                c = self.g[1][0]
                d = self.g[1][1]
                inverse[0][0] = (1 / determinant) * d
                inverse[0][1] = (-1 / determinant) * b
                inverse[1][0] = (-1 / determinant) * c
                inverse[1][1] = (1 / determinant) * a
        return inverse

    
    def T(self):
        matrix_transpose = []
        row = []

        for i in range(len(self.g[0])):
            for j in range(len(self.g)):
                row.append(self.g[j][i])
            matrix_transpose.append(row)
            row = []

        return Matrix(matrix_transpose)

    
    def is_square(self):
        return self.h == self.w

    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
            
        matrixSum = []
        row = []

        for i in range(len(self.g)):
            for j in range(len(self.g[0])):
                row.append(self.g[i][j] + other[i][j])
            matrixSum.append(row)
            row = []
            
        return Matrix(matrixSum)

    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        
        result = []
        row = []
        for i in range(len(self.g)):
            for j in range(len(self.g[0])):
                row.append(- self.g[i][j])
            result.append(row)
            row = []

        return Matrix(result)

    
    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        
        if (self.h != other.h) or (self.w != other.w):
            raise ValueError('Dimensions must be same')

        matrixSub = []
        row = []
        for i in range(len(self.g)):
            for j in range(len(self.g[0])):
                row.append(self.g[i][j] - other[i][j])
            matrixSub.append(row)
            row = []

        return Matrix(matrixSub)

    
    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        product = []
        matrixB_T = other.T()
        row = []
        for i in range(len(self.g)):
            for j in range(len(matrixB_T.g)):
                rowA = self.g[i]
                rowB = matrixB_T[j]
                row.append(dot_product(rowA, rowB))
            product.append(row)
            row = []

        return Matrix(product)

    
    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            r = []
            for i in range(len(self.g)):
                row = []
                for j in range(len(self.g[0])):
                    row.append(self.g[i][j] * other)
                r.append(row)

            return Matrix(r)
            