from test_sympy import symbols, Eq, nsolve, exp
import numpy as np
from scipy.optimize import fsolve

def get_param(epsilon, delta, epochs):
    delta_u = delta / (epochs + 1)
    epsilon_u = symbols('epsilon_u')
    equation = Eq(np.sqrt(2 * epochs * np.log(1 / delta_u)) * epsilon_u + epochs * epsilon_u * (exp(epsilon_u) - 1), epsilon)
    result = nsolve(equation, epsilon_u, 0)
    return result, delta_u

epsilon_u, delta_u = get_param(0.1, 1e-3, 100)
print(epsilon_u, delta_u)


