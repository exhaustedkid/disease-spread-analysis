import dataclasses

import cvxpy as cp
import numpy as np

from input_processing import *

@dataclasses.dataclass
class OptimizingSolver:
    def __init__(self, tree, colors, N):
        self.tree = tree
        self.colors = colors
        self.N = N

        color_to_node = get_colors(colors)
        node_to_color = colors_to_dict(colors)

        self.C = len(color_to_node)
        self.L = len(node_to_color)


    def solve(self) -> int: # TODO: change in to solver output struct        
        d, x_lb, x_ub = self.preprocess_input()      

        constraints, objective = self.get_problem_statement(d, x_lb, x_ub)

        print("obj = ", objective)
        print("co = ", constraints)
        print("solvers = ", cp.installed_solvers())
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.SCIPY)

        print("Solved = ", 0.5 * problem.value)
        return 0.5 * problem.value


    def preprocess_input(self):
        N = self.N
        C = self.C

        d = np.zeros((N, N), dtype=int)
        for edge in self.tree.split(sep=','):
            i, j = edge.split("->")
            d[int(i) - 1][int(j) - 1] = 1

        x_lb = np.zeros((N, C), dtype=int)
        x_ub = np.ones((N, C), dtype=int)
        for leave in self.colors.split(sep=','):
            num, color = leave.split(':')
            x_lb[int(num) - 1][int(color) - 1] = 1
            for i in range(C):
                if i != int(color) - 1:
                    x_ub[int(num) - 1][i] = 0

        return (d, x_lb, x_ub)


    def get_problem_statement(self, d, x_lb, x_ub):
        N = self.N
        C = self.C
        L = self.L
        constraints = []

        x = cp.Variable((N, C), boolean=True, name='x')
        for i in range(N):
            for k in range(C):
                constraints.append(x_lb[i][k] <= x[i, k])
                constraints.append(x[i, k] <= x_ub[i][k])

        for i in range(N):
            constraints.append(eval('1 == ' +' + '.join(f'x[{i},{j}]' for j in range(C))))

        for i in range(N - L):
            for k in range(C):
                constraints.append(eval(f'x[{i},{k}] <= ' + ' + '.join(f'{d[i][j]} * x[{j},{k}]' for j in range(N))))


        y = cp.Variable((N * C, N * C), boolean=True, name='y')
        for i in range(N):
            for j in range(N):
                for p in range(C):
                    for q in range(C):
                        constraints.append(eval(f'y[{i * C + p},{j * C + q}] <= x[{i},{p}]'))

        for i in range(N):
            for j in range(N):
                for p in range(C):
                    for q in range(C):
                        constraints.append(eval(f'y[{i * C + p},{j * C + q}] <= x[{j},{q}]'))

        for i in range(N):
            for j in range(N):
                for p in range(C):
                    for q in range(C):
                        constraints.append(eval(f'y[{i * C + p},{j * C + q}] >= x[{i},{p}] + x[{j},{q}] - 1'))



        e = cp.Variable((C, C), boolean=True, name='e')

        for p in range(C):
            constraints.append(eval(f'e[{p},{p}] == {0}'))

        for i in range(N):
            for j in range(N):
                for p in range(C):
                    for q in range(C):
                        if p == q:
                            continue
                        constraints.append(eval(f'e[{p},{q}] >= {d[i][j] + d[j][i]} * y[{i * C + p},{j * C + q}]'))

        for p in range(C):
            for q in range(C):
                if p == q:
                    continue
                constraints.append(eval(f'e[{p},{q}] <= ' + ' + '.join(f'{d[i][j] + d[j][i]} * y[{i * C + p},{j * C + q}]' for i in range(N) for j in range(N))))

        deg = cp.Variable(C, integer=True, name='deg')
        for k in range(C):
            constraints.append(deg[k] >= 0)
            constraints.append(deg[k] <= C - 1)

        for i in range(C):
            constraints.append(eval(f'deg[{i}]' + ' == ' +' + '.join(f'e[{i},{j}]' for j in range(C))))

        c_bits = 1
        if C > 1:
            c_bits = int(np.floor(np.log2(C - 1))) + 1  # + 1 because not to add it everywhere below


        deg_b = cp.Variable((C, c_bits), boolean=True, name='deg_b')
        for i in range(C):
            constraints.append(eval(f'deg[{i}] == ' + ' + '.join(f'deg_b[{i},{k}] * {2**k}' for k in range(c_bits))))

        t = cp.Variable((C * c_bits, C * c_bits), boolean=True, name='t')
        for i in range(C):
            for j in range(C):
                for k in range (c_bits):
                    for l in range (c_bits):
                        constraints.append(eval(f't[{i * c_bits + k},{j * c_bits + l}] <= deg_b[{i, k}]'))
                        constraints.append(eval(f't[{i * c_bits + k},{j * c_bits + l}] <= deg_b[{j, l}]'))
                        constraints.append(eval(f't[{i * c_bits + k},{j * c_bits + l}] >= deg_b[{i, k}] + deg_b[{j, l}] - 1'))
            

        h = cp.Variable((C, C), integer=True, name='h')
        for i in range(C):
            for j in range(C):
                constraints.append(h[i, j] >= 0)
                constraints.append(h[i, j] <= (C - 1)*(C - 1))
                constraints.append(eval(f'h[{i},{j}] == ' + ' + '.join(f't[{i * c_bits + k},{j * c_bits + l}] * {2**(k + l)}' for k in range(c_bits) for l in range(c_bits))))


        m = cp.Variable((C, C), integer=True, name='m')
        for i in range(C):
            for j in range(C):
                constraints.append(m[i, j] >= 0)
                constraints.append(m[i, j] <= (C - 1)*(C - 1) * e[i,j])

        for i in range(C):
            for j in range(C):
                if (i == j):
                    continue
                constraints.append(eval(f'0 <= h[{i},{j}] - m[{i},{j}]'))

        for i in range(C):
            for j in range(C):
                if (i == j):
                    continue
                constraints.append(eval(f'h[{i},{j}] - m[{i},{j}] <= {(C - 1)*(C - 1)} * (1 - e[{i},{j}])'))

        objective = ''
        for i in range(C):
            for j in range(C):
                objective += f'm[{i}][{j}]'
                if i + 1 < C or j + 1 < C:
                    objective += ' + '

        return (constraints, cp.Maximize(eval(objective)))