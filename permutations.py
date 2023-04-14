"""
Code for generating conditional permutations.

Written April 2022 for EE 5393 (Circuits, Computation, and Biology) at the Univeristy of Minnesota.

Author: Brett Duncan
Email: dunca384@umn.edu

Example Usage:
x = Var('x')
y = Var('y')
exp = Nand(x, y)
seq = build_seq(exp)

for item in seq:
    print(item)
"""


class Var:
    """
    Class to define a variable that can be used in later operations.
    """
    def __init__(self, sym):
        self.sym = sym
    def __repr__(self):
        return self.sym


class Not:
    def __init__(self, exp):
        self.exp = exp
    def __repr__(self):
        return f'Not({self.exp})'


class And:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'And({self.exp0}, {self.exp1})'


class Nand:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'Nand({self.exp0}, {self.exp1})'


class Or:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'Or({self.exp0}, {self.exp1})'


class Nor:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'Nor({self.exp0}, {self.exp1})'


class Xor:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'Xor({self.exp0}, {self.exp1})'


class Xnor:
    def __init__(self, exp0, exp1):
        self.exp0 = exp0
        self.exp1 = exp1
    def __repr__(self):
        return f'Xnor({self.exp0}, {self.exp1})'


def decompose(exp, indent=0):
    """
    Print an expression tree using a depth first search.
    """
    t = type(exp)
    if t == Var:
        print(' '*indent, exp)
    elif t == Not:
        print(' '*indent, 'Not')
        decompose(exp.exp, indent+1)
    elif t == And:
        print(' '*indent, 'And')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)
    elif t == Nand:
        print(' '*indent, 'Nand')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)
    elif t == Or:
        print(' '*indent, 'Or')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)
    elif t == Nor:
        print(' '*indent, 'Nor')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)
    elif t == Xor:
        print(' '*indent, 'Xor')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)
    elif t == Xnor:
        print(' '*indent, 'Xnor')
        decompose(exp.exp0, indent+1)
        decompose(exp.exp1, indent+1)


# permuations given for the homework
# (this could be generated dynamically)
permuations = {
    "A": [1, 4, 3, 5, 2],
    "B": [1, 4, 5, 2, 3],
    "C": [1, 3, 4, 2, 5],
    "D": [1, 2, 4, 5, 3],
    "E": [1, 4, 2, 3, 5],
}

# lookup table of permutation definitions
lookup = {
    "A": ["C", "B", "C'", "B'"],
    "A'": ["B", "C", "B'", "C'"],
    "B": ["C", "D", "C'", "D'"],
    "B'": ["D", "C", "D'", "C'"],
    "C": ["D", "E", "D'", "E'"],
    "C'": ["E", "D", "E'", "D'"],
    "D": ["E", "B", "E'", "B'"],
    "D'": ["B", "E", "B'", "E'"],
    "E": ["D", "A", "D'", "A'"],
    "E'": ["A", "D", "A'", "D'"]
}


def build_exp(exp):
    """
    Build an expression using Nand, And, and Not.
    """
    t = type(exp)
    if t == Var:
        return exp
    elif t == Not:
        ex = exp.exp
        tt = type(ex)
        if tt == Var:
            return Not(ex)
        elif tt == Not:
            return build_exp(ex.exp)
        elif tt == And:
            # And -> Nand
            return build_exp(Nand(ex.exp0, ex.exp1))
        elif tt == Nand:
            # Nand -> And
            return build_exp(And(ex.exp0, ex.exp1))
        elif tt == Or:
            # Or -> Nor
            return build_exp(Nor(ex.exp0, ex.exp1))
        elif tt == Nor:
            # Nor -> Or
            return build_exp(Or(ex.exp0, ex.exp1))
        elif tt == Xor:
            # Xor -> Xnor
            return build_exp(Xnor(ex.exp0, ex.exp1))
        elif tt == Xnor:
            # Xnor -> Xor
            return build_exp(Xor(ex.exp0, ex.exp1))
    elif t == And:
        return And(build_exp(exp.exp0), build_exp(exp.exp1))
    elif t == Nand:
        return Nand(build_exp(exp.exp0), build_exp(exp.exp1))
    elif t == Or:
        return build_exp(Nand(Not(exp.exp0), Not(exp.exp1)))
    elif t == Nor:
        return build_exp(And(Not(exp.exp0), Not(exp.exp1)))
    elif t == Xor:
        return build_exp(And(Nand(Not(exp.exp0), Not(exp.exp1)), Nand(exp.exp0, exp.exp1)))
    elif t == Xnor:
        return build_exp(Nand(Nand(Not(exp.exp0), Not(exp.exp1)), Nand(exp.exp0, exp.exp1)))


def build_seq(exp, perm='A'):
    """
    Build a sequence of conditional permutations given an expression containing only the following:
    - variables
    - nots of variables
    - and
    - nand

    perm is the permutation to start with.
    """
    t = type(exp)
    p = lookup[perm]
    if t == Var:
        return [(exp, (perm, '*'))]
    elif t == Not:
        ex = exp.exp
        tt = type(ex)
        if tt == Var:
            return [(ex, ('*', perm))]
        else:
            # Not(expression) is not valid here
            raise TypeError()
    elif t == And:
        return build_seq(exp.exp0, p[0]) + \
                    build_seq(exp.exp1, p[1]) + \
                    build_seq(exp.exp0, p[2]) + \
                    build_seq(exp.exp1, p[3])
    elif t == Nand:
        return build_seq(exp.exp0, p[1]) + \
                    build_seq(exp.exp1, p[0]) + \
                    build_seq(exp.exp0, p[3]) + \
                    build_seq(exp.exp1, p[2]) + \
                    [('*', (perm, perm))]
    else:
        # raise an error if we run into some other type
        raise TypeError('Type must be one of Var, Not, And, or Nand')
