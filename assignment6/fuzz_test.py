#!/usr/bin/env python3

import argparse
import random
import subprocess
import sys

import numpy as np


def gen_matrix(rows: int, cols: int, low: float = -10.0, high: float = 10.0) -> np.ndarray:
    return np.array(
        [[random.uniform(low, high) for _ in range(cols)] for _ in range(rows)],
        dtype=np.float64,
    )


def build_input_text(a: np.ndarray, b: np.ndarray) -> str:
    lines = []
    lines.append(f"{a.shape[0]} {a.shape[1]}")
    for row in a:
        lines.append(" ".join(f"{x:.6f}" for x in row))

    lines.append(f"{b.shape[0]} {b.shape[1]}")
    for row in b:
        lines.append(" ".join(f"{x:.6f}" for x in row))

    return "\n".join(lines) + "\n"


def parse_matrix_output(text: str, rows: int, cols: int) -> np.ndarray:
    tokens = text.strip().split()
    values = list(map(float, tokens))

    expected = rows * cols
    if len(values) != expected:
        raise ValueError(f"Expected {expected} numbers, got {len(values)}")

    return np.array(values, dtype=np.float64).reshape(rows, cols)


def run_script(script: str, input_text: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, script],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=5,
    )
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", default="matmul_fast.py", help="Fast implementation")
    parser.add_argument("--oracle", default="matmul_np.py", help="NumPy implementation")
    parser.add_argument("--cases", type=int, default=100, help="Number of test cases")
    parser.add_argument("--max-dim", type=int, default=5, help="Maximum matrix dimension")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    for case_id in range(1, args.cases + 1):
        m = random.randint(1, args.max_dim)
        n = random.randint(1, args.max_dim)
        p = random.randint(1, args.max_dim)

        a = gen_matrix(m, n)
        b = gen_matrix(n, p)
        input_text = build_input_text(a, b)

        try:
            fast_rc, fast_out, fast_err = run_script(args.fast, input_text)
            np_rc, np_out, np_err = run_script(args.oracle, input_text)
        except subprocess.TimeoutExpired:
            print(f"[FAIL] case {case_id}: timeout")
            print(input_text)
            return 1

        if fast_rc != 0:
            print(f"[FAIL] case {case_id}: {args.fast} exited with {fast_rc}")
            print("stderr:")
            print(fast_err)
            print("input:")
            print(input_text)
            return 1

        if np_rc != 0:
            print(f"[FAIL] case {case_id}: {args.oracle} exited with {np_rc}")
            print("stderr:")
            print(np_err)
            print("input:")
            print(input_text)
            return 1

        try:
            fast_mat = parse_matrix_output(fast_out, m, p)
            np_mat = parse_matrix_output(np_out, m, p)
        except Exception as e:
            print(f"[FAIL] case {case_id}: output parse error: {e}")
            print("input:")
            print(input_text)
            print("fast stdout:")
            print(fast_out)
            print("np stdout:")
            print(np_out)
            return 1

        if not np.allclose(fast_mat, np_mat, atol=1e-6, rtol=1e-6):
            print(f"[FAIL] case {case_id}: mismatch")
            print("input:")
            print(input_text)
            print("fast result:")
            print(fast_mat)
            print("numpy result:")
            print(np_mat)
            return 1

        print(f"[OK] case {case_id}: {m}x{n} * {n}x{p}")

    print("All fuzz cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())