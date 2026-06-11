#!/usr/bin/env python3

import sys
import numpy as np

tokens = sys.stdin.read().split()
idx = 0

def read_matrix():
    global idx

    rows = int(tokens[idx])
    idx += 1

    cols = int(tokens[idx])
    idx += 1

    data = []
    for _ in range(rows):
        row = [float(tokens[idx + j]) for j in range(cols)]
        idx += cols
        data.append(row)

    return np.array(data, dtype=np.float64)

def main():
    A = read_matrix()
    B = read_matrix()

    if A.shape[1] != B.shape[0]:
        print("Dimension mismatch", file=sys.stderr)
        return 1

    C = A @ B

    for row in C:
        print(*row)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())