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
 - `large-scale` test limits the dimensions at 

```
Running negative-dimension tests: (count=20)
Testing negative dimension scenarios, should be rejected by both implementations.
Negative-dimension [###---------------------------] 2/20 rejected
[FAIL] test 2: expected negative-dimension failure
fast exit: 0
oracle exit: 0
```bash