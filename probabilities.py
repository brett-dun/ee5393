"""
Code for computing with probabilities.

Written May 2022 for EE 5393 (Circuits, Computation, and Biology) at the Univeristy of Minnesota.

Author: Brett Duncan
Email: dunca384@umn.edu

For an understanding of the fundamentals behind the calculations found here take a look at
"Synthesizing Logical Computation on Stochastic Bit Streams" by Weikang Qian and Marc Riedel.

Link to Paper:
https://cctbio.ece.umn.edu/wiki/images/6/64/Qian_Riedel_Synthesizing_Logical_Computation_on_Stochastic_Bit_Streams.pdf
"""

import random

class P:
    """
    Probability class that implements basic behaviors for computing with probabilities.
    """
    def __init__(self, p=None, len=None, bits=None) -> None:
        if p is not None and len is not None:
            bits = [i < p * len for i in range(len)]
            random.shuffle(bits)
        self.bits = bits

    @property
    def prob(self) -> float:
        """
        Probability stored by this object. Defined as the number of bits equal to 1 divided by the
        total number of bits.
        """
        count = 0
        for b in self.bits:
            if b:
                count += 1
        return count / len(self.bits)

    def __and__(self, other):
        if len(self.bits) != len(other.bits):
            raise ValueError('Probability objects must have the same number of bits.')
        return P(bits=[a&b for a,b in zip(self.bits, other.bits)])

    def __or__(self, other):
        if len(self.bits) != len(other.bits):
            raise ValueError('Probability objects must have the same number of bits.')
        return P(bits=[a|b for a,b in zip(self.bits, other.bits)])

    def __xor__(self, other):
        if len(self.bits) != len(other.bits):
            raise ValueError('Probability objects must have the same number of bits.')
        return P(bits=[a^b for a,b in zip(self.bits, other.bits)])
    
    def __invert__(self):
        return P(bits=[not b for b in self.bits])


def mux(a, b, s):
    """
    Returns the resulting Probability object resulting from selector probability s selecting
    between probability a and b.
    """
    if len(a.bits) != len(b.bits) or len(b.bits) != len(s.bits):
        raise ValueError('Probability objects must have the same number of bits.')
    return P(bits=[x if z else y for (x,y,z) in zip(a.bits, b.bits, s.bits)])


def f1(x):
    len = 64
    return P(x, len) & ~(P(x, len) & P(0.25, len))


def f2(x, y, z):
    len = 64
    return (P(x, len) ^ P(y, len)) ^ P(z, len)


def f3(x):
    len = 64
    j = P(7/9, len)
    i = P(5/7, len) & ~((P(x, len) & P(x, len)) & j)  # i = 5/7 * (1 - x**2 * j)
    h = P(3/5, len) & ~((P(x, len) & P(x, len)) & i)  # h = 3/5 * (1 - x**2 * i)
    g = P(1/3, len) & ~((P(x, len) & P(x, len)) & h)  # g = 1/3 * (1 - x**2 * h)
    f = ~((P(x, len) & P(x, len)) & g)  # f = 1 - x**2 * g
    return P(x, len) & f  # f3 = x * f
