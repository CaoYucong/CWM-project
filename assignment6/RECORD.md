```
(cwm-project) ubuntu@ubuntu:~/CWM-project$ python3 assignment6/fuzz_test.py 

Running simple tests:
Testing correct multiplication, dimension limited by max_dim.
Simple [#-----------------------------] 1/20
[FAIL] test 1: matmul_fast.py exited with 2
stderr:
/home/ubuntu/CWM-project/.venv/bin/python3: can't open file '/home/ubuntu/CWM-project/matmul_fast.py': [Errno 2] No such file or directory

input:
8 2
5.828481 -9.499508
-6.016678 -6.789954
-2.972300 6.877014
-8.715731 -1.707489
-1.878373 4.656078
9.161088 -5.083764
1.873474 -5.596344
2.284667 -0.681382
2 11
-0.194138 -5.343009 -4.579012 1.550763 9.035783 2.320284 7.506371 -6.023688 -4.069042 -2.310642 -6.841907
2.086145 9.884510 -7.103007 7.274354 -5.167221 -7.766452 0.249947 2.282485 -0.011083 -4.253598 -2.210417
```

