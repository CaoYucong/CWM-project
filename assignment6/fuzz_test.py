#!/usr/bin/env python3

import argparse
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


def gen_matrix(rows: int, cols: int, low: float = -10.0, high: float = 10.0) -> np.ndarray:
    return np.array(
        [[random.uniform(low, high) for _ in range(cols)] for _ in range(rows)],
        dtype=np.float64,
    )


def gen_int_matrix(rows: int, cols: int, low: int = 1, high: int = 100) -> np.ndarray:
    return np.array(
        [[random.randint(low, high) for _ in range(cols)] for _ in range(rows)],
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
        timeout=60,
    )
    return p.returncode, p.stdout, p.stderr


def write_fail_testcase(input_text: str) -> None:
    path = Path(__file__).resolve().parent / "fail_testcase.txt"
    path.write_text(input_text)
    print(f"Failing testcase saved to: {path}")


def print_progress(test_id: int, total: int, mode: str, status: str = "") -> None:
    bar_width = 30
    filled = int(bar_width * float(test_id) / float(total))
    bar = "#" * filled + "-" * (bar_width - filled)
    if mode == "mismatch":
        mode_label = "Mismatch"
    elif mode == "negative-dimension":
        mode_label = "Negative-dimension"
    elif mode == "large-number":
        mode_label = "Large-number"
    elif mode == "large-scale":
        mode_label = "Large-scale"
    elif mode == "large-number-and-scale":
        mode_label = "Large-number-scale"
    elif mode == "float":
        mode_label = "Float"
    else:
        mode_label = "Simple"
    status_text = f" {status}" if status else ""
    print(f"\r{mode_label} [{bar}] {test_id}/{total}{status_text}", end="", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", default="matmul_fast.py", help="Fast implementation")
    parser.add_argument("--oracle", default="matmul_np.py", help="NumPy implementation")
    parser.add_argument("--tests", "--cases", type=int, default=None, help="Number of tests per mode; uses mode-specific defaults when omitted")
    parser.add_argument(
        "--mode",
        choices=["simple", "mismatch", "negative-dimension", "large-number", "large-scale", "large-number-and-scale", "float", "all"],
        default="all",
        help="Test mode",
    )
    parser.add_argument("--max-dim", type=int, default=20, help="Maximum matrix dimension")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    modes_to_run = ["simple", "mismatch", "negative-dimension", "large-number", "float", "large-scale", "large-number-and-scale"] if args.mode == "all" else [args.mode]

    default_tests = {
        "simple": 20,
        "mismatch": 20,
        "negative-dimension": 20,
        "large-number": 20,
        "large-scale": 1,
        "large-number-and-scale": 1,
        "float": 20,
    }

    for mode in modes_to_run:
        tests = args.tests if args.tests is not None else default_tests.get(mode, 1)
        print(f"\nRunning {mode} tests: (count={tests})")
        if mode == "simple":
            print("Testing correct multiplication, dimension limited by max_dim.")
        if mode == "mismatch":
            print("Testing dimension mismatch scenarios, should be rejected by both implementations.")
        if mode == "negative-dimension":
            print("Testing negative dimension scenarios, should be rejected by both implementations.")
        if mode == "large-number":
            print("Testing large-number values with dimensions limited to 10 and input values from 1e7 to 1e9.")
        if mode == "large-scale":
            print("Testing large-scale matrices with values under 1e5 and work scaled 1000 by 1000")
        if mode == "large-number-and-scale":
            print("Testing large-number-and-scale matrices with values from 1e7 to 1e9 and work scaled 1000 by 1000.")
        if mode == "float":
            print("Testing float matrices with dimensions limited to 100 and values under 1e5.")

        fast_times: list[float] = []
        np_times: list[float] = []
        for test_id in range(1, tests + 1):
            max_dim = args.max_dim
            if mode == "mismatch" or mode == "negative-dimension":
                max_dim = min(max_dim, 100)
            elif mode == "large-number":
                max_dim = min(max_dim, 100)
            elif mode == "large-scale":
                max_dim = min(max_dim, 1e4)
            elif mode == "large-number-and-scale":
                max_dim = min(max_dim, 1e4)
            elif mode == "float":
                max_dim = min(max_dim, 100)

            if mode == "large-scale" or mode == "large-number-and-scale":
                m = 1000
                n = 1000
                p = 1000
            else:
                m = random.randint(1, max_dim)
                n = random.randint(1, max_dim)
                p = random.randint(1, max_dim)

            if mode == "simple":
                a = gen_int_matrix(m, n)
                b = gen_int_matrix(n, p)
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
            elif mode == "large-number-and-scale":
                a = gen_matrix(m, n, low=1e7, high=1e9)
                b = gen_matrix(n, p, low=1e7, high=1e9)
                input_text = build_input_text(a, b)
                expect_failure = False
            elif mode == "float":
                a = gen_matrix(m, n, low=0.0, high=1e5)
                b = gen_matrix(n, p, low=0.0, high=1e5)
                input_text = build_input_text(a, b)
                expect_failure = False
            elif mode == "mismatch":
                a = gen_int_matrix(m, n)
                b = gen_int_matrix(n, p)
                declared_a = (m, n + random.randint(1, max_dim))
                declared_b = (n, p + random.randint(1, max_dim))
                input_text = build_mismatch_input_text(a, b, declared_a, declared_b)
                expect_failure = True
            elif mode == "negative-dimension":
                a = gen_int_matrix(m, n)
                b = gen_int_matrix(n, p)
                # Randomly choose which dimension to make negative
                declared_a = (m, n)
                declared_b = (n, p)
                choice = random.randint(0, 3)
                if choice == 0:
                    declared_a = (-m, n)
                elif choice == 1:
                    declared_a = (m, -n)
                elif choice == 2:
                    declared_b = (-n, p)
                else:
                    declared_b = (n, -p)
                input_text = build_mismatch_input_text(a, b, declared_a, declared_b)
                expect_failure = True
            
            if mode == "mismatch" or mode == "negative-dimension":
                print_progress(test_id - 1, tests, mode, "rejected")
            else:
                print_progress(test_id - 1, tests, mode, "passed")

            try:
                start_time = time.perf_counter()
                fast_rc, fast_out, fast_err = run_script(args.fast, input_text)
                fast_duration = time.perf_counter() - start_time

                start_time = time.perf_counter()
                np_rc, np_out, np_err = run_script(args.oracle, input_text)
                np_duration = time.perf_counter() - start_time
            except subprocess.TimeoutExpired:
                print()
                print(f"[FAIL] test {test_id}: timeout")
                write_fail_testcase(input_text)
                return 1
            
            if mode == "mismatch" or mode == "negative-dimension":
                print_progress(test_id, tests, mode, "rejected")
            else:
                print_progress(test_id, tests, mode, "passed")

            fast_times.append(fast_duration)
            np_times.append(np_duration)

            if mode == "mismatch" or mode == "negative-dimension":
                if fast_rc == 0 or np_rc == 0:
                    print()
                    print(f"[FAIL] test {test_id}: expected {mode} failure")
                    print("fast exit:", fast_rc)
                    print("oracle exit:", np_rc)
                    write_fail_testcase(input_text)
                    return 1

                print_progress(test_id, tests, mode, "rejected")
                continue

            if fast_rc != 0:
                print()
                print(f"[FAIL] test {test_id}: {args.fast} exited with {fast_rc}")
                print("stderr:")
                print(fast_err)
                write_fail_testcase(input_text)
                return 1

            if np_rc != 0:
                print()
                print(f"[FAIL] test {test_id}: {args.oracle} exited with {np_rc}")
                print("stderr:")
                print(np_err)
                write_fail_testcase(input_text)
                return 1

            try:
                fast_mat = parse_matrix_output(fast_out, m, p)
                np_mat = parse_matrix_output(np_out, m, p)
            except Exception as e:
                print()
                print(f"[FAIL] test {test_id}: output parse error: {e}")
                write_fail_testcase(input_text)
                print("fast stdout:")
                print(fast_out)
                print("np stdout:")
                print(np_out)
                return 1

            if not np.allclose(fast_mat, np_mat, atol=1e-6, rtol=1e-6):
                print()
                print(f"[FAIL] test {test_id}: mismatch")
                write_fail_testcase(input_text)
                print("fast result:")
                print(fast_mat)
                print("numpy result:")
                print(np_mat)
                return 1

            print_progress(test_id, tests, mode, "passed")
        print()

        if fast_times or np_times:
            print(f"\n{mode.capitalize()} timing summary:")
            print(f"  fast   : {len(fast_times)} runs")
            print(f"    mean   = {statistics.mean(fast_times):.6f} s")
            print(f"    median = {statistics.median(fast_times):.6f} s")
            print(f"    min    = {min(fast_times):.6f} s")
            print(f"    max    = {max(fast_times):.6f} s")
            print(f"  np     : {len(np_times)} runs")
            print(f"    mean   = {statistics.mean(np_times):.6f} s")
            print(f"    median = {statistics.median(np_times):.6f} s")
            print(f"    min    = {min(np_times):.6f} s")
            print(f"    max    = {max(np_times):.6f} s")


    print()
    print("All fuzz cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())