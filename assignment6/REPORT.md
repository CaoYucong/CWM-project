# Report of Assignment 6

- Name: Yucong Cao
- Github Repo Link: [CaoYucong/CWM-Project](https://github.com/CaoYucong/CWM-project)

## Fuzz Test

### Target

The fuzz test is targeting at the `matmul_fast.py` from assignment 1. The porpuse of the test is to verify the correctness and to find any bugs and volnerailities that emerges during the test.

### Test Method

The correctness test is conducted by cross-checking another standard matrix multiplication script with numpy, by giving the same input to both the scripts, and compare whether their outputs are the same.

The standatd input is in this form: `rowA colB` is given first, and the matrix `A` is input next, following is the same input for matrix `B`. For example:

Example Input:

```
2 3
1.5 2.0 1.9
4.0 5.5 6.0

3 2
7.0 8.0
9.0 1.0
11.0 12.0
```

This means the input matrices are :

$$
A = 
\begin{bmatrix}
1.5 & 2.0 & 1.9 \\
4.0 & 5.5 & 6.0
\end{bmatrix}, 
B = 
\begin{bmatrix}
7.0 & 8.0\\
9.0 & 1.0\\
11.0& 12.0
\end{bmatrix}, 
$$

Example Output:

```
49.4 36.8
143.5 109.5
```

which corresponds to the product of $A$ and $B$.

Data range: $rows, cols \leq 100$, $|{A_{ij}}| \leq 10$, $A_{ij} \in  ℤ$ unless stated otherwise.

Different kinds of invalid inputs are also tested to find any buds or vulnerabilities including :
 - `mismatch` test refers to the case when the dimension declared does not match with the actual matrix input, rejection (raising an error) is expected from the script.
 - `negative-dimension` test refers to the case when the leading dimension information are given negative, rejection (raising an error) is expected from the script.

Different extreme inputs are also tested, including:
 - `float` test sets all the emelents in matrix a float number.
 - `large-number` test limits all the elements in matrix in the range of $10^7 ~ 10^9$.
 - `large-scale` tests large-scale matrices with values under 1e5 and work scaled 1000 by 1000
 - `large-number-and-scale` tests large-number-and-scale matrices with values from 1e7 to 1e9 and work scaled 1000 by 1000

### Result

```
ubuntu@ubuntu:~/CWM-project/assignment6$ python3 '/home/ubuntu/CWM-project/assignment6/fuzz_test.py'

Running simple tests: (count=20)
Testing correct multiplication, dimension limited by max_dim.
Simple [##############################] 20/20 passed

Simple timing summary:
  fast   : 20 runs
    mean   = 0.031106 s
    median = 0.030808 s
    min    = 0.030356 s
    max    = 0.033202 s
  np     : 20 runs
    mean   = 0.108059 s
    median = 0.107698 s
    min    = 0.104649 s
    max    = 0.117116 s

Running mismatch tests: (count=20)
Testing dimension mismatch scenarios, should be rejected by both implementations.
Mismatch [##############################] 20/20 rejected

Mismatch timing summary:
  fast   : 20 runs
    mean   = 0.114654 s
    median = 0.113533 s
    min    = 0.112762 s
    max    = 0.127931 s
  np     : 20 runs
    mean   = 0.169088 s
    median = 0.168505 s
    min    = 0.167643 s
    max    = 0.172433 s

Running negative-dimension tests: (count=20)
Testing negative dimension scenarios, should be rejected by both implementations.
Negative-dimension [##############################] 20/20 rejected

Negative-dimension timing summary:
  fast   : 20 runs
    mean   = 0.117723 s
    median = 0.117018 s
    min    = 0.111903 s
    max    = 0.131128 s
  np     : 20 runs
    mean   = 0.175980 s
    median = 0.175632 s
    min    = 0.167533 s
    max    = 0.184200 s

Running large-number tests: (count=20)
Testing large-number values with dimensions limited to 10 and input values from 1e7 to 1e9.
Large-number [##############################] 20/20 passed

Large-number timing summary:
  fast   : 20 runs
    mean   = 0.033221 s
    median = 0.031171 s
    min    = 0.030230 s
    max    = 0.072315 s
  np     : 20 runs
    mean   = 0.108751 s
    median = 0.108678 s
    min    = 0.105807 s
    max    = 0.114626 s

Running float tests: (count=20)
Testing float matrices with dimensions limited to 100 and values under 1e5.
Float [##############################] 20/20 passed

Float timing summary:
  fast   : 20 runs
    mean   = 0.031356 s
    median = 0.031219 s
    min    = 0.030550 s
    max    = 0.033317 s
  np     : 20 runs
    mean   = 0.108920 s
    median = 0.108195 s
    min    = 0.105229 s
    max    = 0.118843 s

Running large-scale tests: (count=1)
Testing large-scale matrices with values under 1e5 and work scaled 1000 by 1000
Large-scale [##############################] 1/1 passed

Large-scale timing summary:
  fast   : 1 runs
    mean   = 51.400527 s
    median = 51.400527 s
    min    = 51.400527 s
    max    = 51.400527 s
  np     : 1 runs
    mean   = 2.264707 s
    median = 2.264707 s
    min    = 2.264707 s
    max    = 2.264707 s

Running large-number-and-scale tests: (count=1)
Testing large-number-and-scale matrices with values from 1e7 to 1e9 and work scaled 1000 by 1000.
Large-number-scale [##############################] 1/1 passed

Large-number-and-scale timing summary:
  fast   : 1 runs
    mean   = 52.011891 s
    median = 52.011891 s
    min    = 52.011891 s
    max    = 52.011891 s
  np     : 1 runs
    mean   = 2.359002 s
    median = 2.359002 s
    min    = 2.359002 s
    max    = 2.359002 s

All fuzz cases passed.
```

#### Bugs and volnerailities found

 - Missing Negetive Error

 ```bash
Running negative-dimension tests: (count=20)
Testing negative dimension scenarios, should be rejected by both implementations.
Negative-dimension [###---------------------------] 2/20 rejected
[FAIL] test 2: expected negative-dimension failure
fast exit: 0
oracle exit: 0
```

Fixed by adding a condition at input:

```python
    if rows < 0 or cols < 0:
        raise ValueError("matrix dimensions must be non-negative")
```

 - Long Execution Time under large scale:

```
Running large-scale tests: (count=1)
Testing large-scale matrices with values under 1e5 and work scaled 1000 by 1000
Large-scale [##############################] 1/1 passed

Large-scale timing summary:
  fast   : 1 runs
    mean   = 51.400527 s
    median = 51.400527 s
    min    = 51.400527 s
    max    = 51.400527 s
  np     : 1 runs
    mean   = 2.264707 s
    median = 2.264707 s
    min    = 2.264707 s
    max    = 2.264707 s

Running large-number-and-scale tests: (count=1)
Testing large-number-and-scale matrices with values from 1e7 to 1e9 and work scaled 1000 by 1000.
Large-number-scale [##############################] 1/1 passed

Large-number-and-scale timing summary:
  fast   : 1 runs
    mean   = 52.011891 s
    median = 52.011891 s
    min    = 52.011891 s
    max    = 52.011891 s
  np     : 1 runs
    mean   = 2.359002 s
    median = 2.359002 s
    min    = 2.359002 s
    max    = 2.359002 s
```

For large scales inputs, the computation time is very long on `matmul_fast.py`, which will cauce problems if this script is implemented on a server with large scale inquries.