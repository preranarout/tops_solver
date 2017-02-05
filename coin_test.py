import numpy as np
from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray

def test1():
    s = CyClpSimplex()

    # Add variables
    x = s.addVariable('x', 3)
    y = s.addVariable('y', 2)

    # Create coefficients and bounds
    A = np.matrix([[1., 2., 0], [1., 0, 1.]])
    B = np.matrix([[1., 0, 0], [0, 0, 1.]])
    D = np.matrix([[1., 2.], [0, 1]])
    a = CyLPArray([5, 2.5])
    b = CyLPArray([4.2, 3])
    x_u = CyLPArray([2., 3.5])

    # Add constraints
    s += A * x <= a
    s += 2 <= B * x + D * y <= b
    s += y >= 0
    s += 1.1 <= x[1:3] <= x_u

    # Set the objective function
    c = CyLPArray([1., -2., 3.])
    s.objective = c * x + 2 * y.sum()

    # Solve using primal Simplex
    s.primal()
    print s.primalVariableSolution['x']

def mps_test():
    s = CyClpSimplex()
    s.readMps("/home/nbanerjee/gurobi605/linux64/examples/data/stein9.mps")
    s.primal()
    # print s.primalVariableSolution('x')

def main():
    test1()
    print "\n\n==========================="
    mps_test()

if __name__ == "__main__":
    main()