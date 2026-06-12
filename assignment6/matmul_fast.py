#!/usr/bin/env python3
"""A simple matrix multiplication program for Linux measurement lab.

It computes a simple O(n^3) multiplication with a checksum at the end
so the computation has an observable result.

"""

import sys
from typing import List

Matrix = List[List[float]]

#The matrix entries are initialized deterministically so that every run uses
#the same data. The exact constants are not important; they only create 
#non-uniform values that vary by row and column.
def init_matrix(n: int, seed: float) -> Matrix:
    return [
        [seed + ((i * 131 + j * 17) % 100) / 100.0 for j in range(n)]
        for i in range(n)
    ]

#Zero out output entries.
def zero_matrix(rows: int, cols: int) -> Matrix:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]

#Reorder loops to improve locality
def matmul_fast1(a: Matrix, b: Matrix, c: Matrix, m: int, k: int, n: int) -> None:
    for i in range(m):
        row_ai = a[i]
        row_ci = c[i]
        for j in range(n):
            total = 0.0
            for kk in range(k):
                total += row_ai[kk] * b[kk][j]
            row_ci[j] = total

#Reorder loops to reduce inner loops
def matmul_fast2(a: Matrix, b: Matrix, c: Matrix, m: int, k: int, n: int) -> None:
    for i in range(m):
        row_ai = a[i]
        row_ci = c[i]
        for j in range(n):
            row_ci[j] = 0.0
        for kk in range(k):
            aik = row_ai[kk]
            row_bk = b[kk]
            for j in range(n):
                row_ci[j] += aik * row_bk[j]

def transpose(m: Matrix) -> Matrix:
    rows = len(m)
    cols = len(m[0]) if rows else 0
    return [[m[i][j] for i in range(rows)] for j in range(cols)]

#Matrix transpose method
def matmul_fast3(a: Matrix, b: Matrix, c: Matrix, m: int, k: int, n: int) -> Matrix:
    bt = transpose(b)

    for i in range(m):
        row_ai = a[i]
        row_ci = c[i]
        for j in range(n):
            total = 0.0
            row_btj = bt[j]
            for kk in range(k):
                total += row_ai[kk] * row_btj[kk]
            row_ci[j] = total

    return c


def checksum(m: Matrix, rows: int, cols: int) -> float:
    total = 0.0
    step = (min(rows, cols) // 16) + 1
    for i in range(0, rows, step):
        for j in range(0, cols, step):
            total += m[i][j]
    return total


def usage(prog: str) -> None:
    print(
        f"Usage: {prog} [repetitions]\n"
        "  repetitions  : number of repeated multiplies (default: 1)",
        file=sys.stderr,
    )


def parse_args(argv: list[str]) -> int:
    reps = 1

    if len(argv) > 2:
        usage(argv[0])
        raise SystemExit(1)
    if len(argv) == 2:
        reps = int(argv[1])
    if reps <= 0:
        usage(argv[0])
        raise SystemExit(1)

    return reps

import time

def get_cpu_time_counter() -> int:
    return time.perf_counter_ns()


def read_matrix(tokens: list[str], position: int) -> tuple[Matrix, int]:
    if position + 2 > len(tokens):
        raise ValueError("unexpected end of input while reading matrix dimensions")

    rows = int(tokens[position])
    cols = int(tokens[position + 1])
    
    if rows < 0 or cols < 0:
        raise ValueError("matrix dimensions must be non-negative")
    
    position += 2

    matrix: Matrix = []
    for _ in range(rows):
        row: list[float] = []
        for _ in range(cols):
            if position >= len(tokens):
                raise ValueError("unexpected end of input while reading matrix values")
            row.append(float(tokens[position]))
            position += 1
        matrix.append(row)

    return matrix, position


def main(argv: list[str]) -> int:
    reps = parse_args(argv)

    tokens = sys.stdin.read().strip().split()
    a, pos = read_matrix(tokens, 0)
    b, pos = read_matrix(tokens, pos)

    if not a or not b:
        print("Error: empty matrix input", file=sys.stderr)
        return 1

    m = len(a)
    k = len(a[0])
    if any(len(row) != k for row in a):
        print("Error: inconsistent row length in matrix A", file=sys.stderr)
        return 1

    if len(b) == 0 or any(len(row) != len(b[0]) for row in b):
        print("Error: inconsistent row length in matrix B", file=sys.stderr)
        return 1

    if len(b) != k:
        print(
            f"Error: matrix dimensions incompatible for multiplication: "
            f"A is {m}x{k}, B is {len(b)}x{len(b[0])}",
            file=sys.stderr,
        )
        return 1

    n = len(b[0])
    c = zero_matrix(m, n)

    for i in range(reps):
        time1 = time.perf_counter()
        c = matmul_fast3(a, b, c, m, k, n)
        time2 = time.perf_counter()
        # print(f"matmul_fast3 function :: The {i} th run time = {time2 - time1:.6f} seconds")

    # print(
    #     f"m={m} k={k} n={n} reps={reps} checksum={checksum(c, m, n):.6f}"
    # )

    for row in c:
        print(*row)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
