#!/usr/bin/env python3
"""A simple O(n^3) matrix multiplication program for comparison testing."""

import sys
from typing import List

Matrix = List[List[float]]


def matmul_slow(a: Matrix, b: Matrix, c: Matrix, m: int, n: int, p: int) -> None:
    """Simple O(n^3) matrix multiplication.
    
    This loop order is correct but cache-unfriendly for matrix B.
    """
    for i in range(m):
        for j in range(p):
            total = 0.0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total

def main(argv: list[str]) -> int:
    # Read input from stdin
    lines = sys.stdin.read().strip().split('\n')
    
    if len(lines) < 2:
        print("Error: insufficient input", file=sys.stderr)
        return 1
    
    # Parse matrix A dimensions
    m, n = map(int, lines[0].split())
    
    # Read matrix A
    a = []
    for i in range(1, m + 1):
        row = list(map(float, lines[i].split()))
        a.append(row)
    
    # Parse matrix B dimensions
    n_check, p = map(int, lines[m + 1].split())
    if n_check != n:
        print("Error: dimension mismatch", file=sys.stderr)
        return 1
    
    # Read matrix B
    b = []
    for i in range(m + 2, m + 2 + n):
        row = list(map(float, lines[i].split()))
        b.append(row)
    
    # Perform matrix multiplication
    c = [[0.0 for _ in range(p)] for _ in range(m)]
    matmul_slow(a, b, c, m, n, p)
    
    # Print result matrix (flattened to space-separated values)
    result = []
    for row in c:
        for val in row:
            result.append(f"{val:.6f}")
    print(" ".join(result))
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
