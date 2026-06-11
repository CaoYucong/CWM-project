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


def build_mismatch_input_text(
    a: np.ndarray,
    b: np.ndarray,
    declared_a: tuple[int, int],
    declared_b: tuple[int, int],
) -> str:
    lines = []
    lines.append(f"{declared_a[0]} {declared_a[1]}")
    for row in a:
        lines.append(" ".join(f"{x:.6f}" for x in row))

    lines.append(f"{declared_b[0]} {declared_b[1]}")
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


def print_progress(test_id: int, total: int, mode: str, status: str = "") -> None:
    bar_width = 30
    filled = int(bar_width * test_id / total)
    bar = "#" * filled + "-" * (bar_width - filled)
    if mode == "mismatch":
        mode_label = "Mismatch"
    elif mode == "large":
        mode_label = "Large"
    elif mode == "large-scale":
        mode_label = "Large-scale"
    else:
        mode_label = "Simple"
    status_text = f" {status}" if status else ""
    print(f"\r{mode_label} [{bar}] {test_id}/{total}{status_text}", end="", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", default="matmul_fast.py", help="Fast implementation")
    parser.add_argument("--oracle", default="matmul_np.py", help="NumPy implementation")
    parser.add_argument("--tests", "--cases", type=int, default=20, help="Number of tests per mode")
    parser.add_argument(
        "--mode",
        choices=["simple", "mismatch", "large-number", "large-scale", "all"],
        default="all",
        help="Test mode",
    )
    parser.add_argument("--max-dim", type=int, default=20, help="Maximum matrix dimension")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    modes_to_run = ["simple", "mismatch", "large-number", "large-scale"] if args.mode == "all" else [args.mode]

    for mode in modes_to_run:
        print(f"\nRunning {mode} tests:")
        if mode == "simple":
            print("Testing correct multiplication, dimension limited by max_dim.")
        if mode == "mismatch":
            print("Testing dimension mismatch scenarios, should be rejected by both implementations.")
        if mode == "large-number":
            print("Testing large-number values with dimensions limited to 10 and input values from 1e7 to 1e9.")
        if mode == "large-scale":
            print("Testing large-scale matrices with values under 1e5 and work scale between 1e3 and 1e4.")
        for test_id in range(1, args.tests + 1):
            max_dim = args.max_dim
            if mode == "mismatch":
                max_dim = min(max_dim, 10)
            elif mode == "large-number":
                max_dim = min(max_dim, 10)
            elif mode == "large-scale":
                max_dim = min(max_dim, 1e4)

            if mode == "large-scale":
                m = int(1e3 + random.randint(0, 9) * 1e3)
                n = int(1e3 + random.randint(0, 9) * 1e3)
                p = int(1e3 + random.randint(0, 9) * 1e3)
            else:
                m = random.randint(1, max_dim)
                n = random.randint(1, max_dim)
                p = random.randint(1, max_dim)

            if mode == "simple":
                a = gen_matrix(m, n)
                b = gen_matrix(n, p)
                input_text = build_input_text(a, b)
                expect_failure = False
            elif mode == "large-number":
                a = gen_matrix(m, n, low=1e7, high=1e9)
                b = gen_matrix(n, p, low=1e7, high=1e9)
                input_text = build_input_text(a, b)
                expect_failure = False
            elif mode == "large-scale":
                a = gen_matrix(m, n, low=0.0, high=1e5)
                b = gen_matrix(n, p, low=0.0, high=1e5)
                input_text = build_input_text(a, b)
                expect_failure = False
            elif mode == "mismatch":
                a = gen_matrix(m, n)
                b = gen_matrix(n, p)
                declared_a = (m, n + random.randint(1, max_dim))
                declared_b = (n, p + random.randint(1, max_dim))
                input_text = build_mismatch_input_text(a, b, declared_a, declared_b)
                expect_failure = True

            print_progress(test_id, args.tests, mode)

            try:
                fast_rc, fast_out, fast_err = run_script(args.fast, input_text)
                np_rc, np_out, np_err = run_script(args.oracle, input_text)
            except subprocess.TimeoutExpired:
                print()
                print(f"[FAIL] test {test_id}: timeout")
                print(input_text)
                return 1

            if mode == "mismatch":
                if fast_rc == 0 or np_rc == 0:
                    print()
                    print(f"[FAIL] test {test_id}: expected mismatch failure")
                    print("fast exit:", fast_rc)
                    print("oracle exit:", np_rc)
                    print("input:")
                    print(input_text)
                    return 1

                print_progress(test_id, args.tests, mode, "rejected")
                continue

            if fast_rc != 0:
                print()
                print(f"[FAIL] test {test_id}: {args.fast} exited with {fast_rc}")
                print("stderr:")
                print(fast_err)
                print("input:")
                print(input_text)
                return 1

            if np_rc != 0:
                print()
                print(f"[FAIL] test {test_id}: {args.oracle} exited with {np_rc}")
                print("stderr:")
                print(np_err)
                print("input:")
                print(input_text)
                return 1

            try:
                fast_mat = parse_matrix_output(fast_out, m, p)
                np_mat = parse_matrix_output(np_out, m, p)
            except Exception as e:
                print()
                print(f"[FAIL] test {test_id}: output parse error: {e}")
                print("input:")
                print(input_text)
                print("fast stdout:")
                print(fast_out)
                print("np stdout:")
                print(np_out)
                return 1

            if not np.allclose(fast_mat, np_mat, atol=1e-6, rtol=1e-6):
                print()
                print(f"[FAIL] test {test_id}: mismatch")
                print("input:")
                print(input_text)
                print("fast result:")
                print(fast_mat)
                print("numpy result:")
                print(np_mat)
                return 1

            print_progress(test_id, args.tests, mode, "passed")
        print()


    print()
    print("All fuzz cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())