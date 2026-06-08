# Report of Assignment 2

- Name: Yucong Cao
- Github Repo Link: [CaoYucong/CWM-Project](https://github.com/CaoYucong/CWM-project)

## Reading Timestamp Counter

### Question 1

```
ubuntu@ubuntu:~/CWM-project/assignment2$ for i in 1 2 3 4 5 6 7 8 9 10; do python3 rdtime.py; done
CPU time counter: 247367917243279 ns
CPU time diff: 14185 ns
CPU time counter: 247367936143185 ns
CPU time diff: 14889 ns
CPU time counter: 247367955112848 ns
CPU time diff: 14445 ns
CPU time counter: 247367974208514 ns
CPU time diff: 14219 ns
CPU time counter: 247367993318996 ns
CPU time diff: 15268 ns
CPU time counter: 247368012259227 ns
CPU time diff: 14571 ns
CPU time counter: 247368031415901 ns
CPU time diff: 13434 ns
CPU time counter: 247368050476170 ns
CPU time diff: 14435 ns
CPU time counter: 247368069433511 ns
CPU time diff: 13802 ns
CPU time counter: 247368088358195 ns
CPU time diff: 14495 ns
```

### Question 2

```
ubuntu@ubuntu:~/CWM-project/assignment2$ python3 rdtime.py 
CPU time counter: 256050674644392 ns
CPU time diff: 13313 ns
CPU min diff time: 118 ns
```

![](/home/ubuntu/CWM-project/assignment2/one_million_repeat_python.png)

![one_million_repeat_without_first](/home/ubuntu/CWM-project/assignment2/one_million_repeat_python_without_first.png)

![](/home/ubuntu/CWM-project/assignment2/one_million_repeat_python_CDF.png)

### Question 3

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ./rdtime 10
CPU frequency: 0.900 GHz
Minimum consecutive TSC diff: 188 cycles
Approximate time: 208.89 ns
```

### Question 4

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ./rdtime 10
CPU frequency: 3.600 GHz
Minimum consecutive TSC diff: 50 cycles
Approximate time: 13.89 ns
```

### Question 5

![](/home/ubuntu/CWM-project/assignment2/one_million_repeat_c.png)

![](/home/ubuntu/CWM-project/assignment2/one_million_repeat_c_CDF.png)

### Question 6

```
ubuntu@ubuntu:~/CWM-project/assignment2$ taskset -c 1 ./rdtime 1000000
CPU frequency: 3.600 GHz
Minimum consecutive TSC diff: 44 cycles
Approximate time: 12.22 ns
```

![](/home/ubuntu/CWM-project/assignment2/one_million_repeat_c_single_core.png)

![](one_million_repeat_c_single_core_CDF.png)

They should be the same as one single program would only run one core.

### Question 7

|               | Average | Median | $90\%$ | $99\%$ | Max    |
| ------------- | ------- | ------ | ------ | ------ | ------ |
| Python        | 268.54  | 275    | 280    | 310    | 3.5e6  |
| C             | 62.9182 | 52     | 52     | 54     | 1.5e5  |
| C single core | 62.7928 | 52     | 52     | 54     | 1.25e5 |

The time difference of python is bigger than c.

### Question 8

Yes. The Python code takes significantly more time, as python is a higher level language replying on c code, one more layer of translation (compilation) is needed.

### Question 9

The CPU might not be able to work continuously, due to the circuit architecture, there might occur some large time gap between two instructions, due to other activities, or due to some safety regulations that limits CPU from working continuously over a time period.

### Question 10

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ping 8.8.8.8 -c 10 -i 0.2
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=3.30 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=3.27 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=113 time=3.17 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=113 time=3.19 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=113 time=3.17 ms
64 bytes from 8.8.8.8: icmp_seq=6 ttl=113 time=3.18 ms
64 bytes from 8.8.8.8: icmp_seq=7 ttl=113 time=3.18 ms
64 bytes from 8.8.8.8: icmp_seq=8 ttl=113 time=3.28 ms
64 bytes from 8.8.8.8: icmp_seq=9 ttl=113 time=3.20 ms
64 bytes from 8.8.8.8: icmp_seq=10 ttl=113 time=3.27 ms

--- 8.8.8.8 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 1805ms
rtt min/avg/max/mdev = 3.169/3.220/3.304/0.051 ms
```

### Question 11

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ping www.pku.edu.cn -c 10 -i 0.2
PING www.lb.pku.edu.cn (162.105.131.160) 56(84) bytes of data.

--- www.lb.pku.edu.cn ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 1870ms
```

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ping www.titech.ac.jp -c 10 -i 0.2
PING web-a1n.westeurope.cloudapp.azure.com (20.107.116.39) 56(84) bytes of data.

--- web-a1n.westeurope.cloudapp.azure.com ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 1870ms
```

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ping www.mit.edu -c 10 -i 0.2
PING e9566.dscb.akamaiedge.net (23.43.64.242) 56(84) bytes of data.
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=1 ttl=51 time=3.35 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=2 ttl=51 time=3.54 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=3 ttl=51 time=3.27 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=4 ttl=51 time=3.30 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=5 ttl=51 time=3.26 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=6 ttl=51 time=3.30 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=7 ttl=51 time=3.49 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=8 ttl=51 time=3.41 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=9 ttl=51 time=3.39 ms
64 bytes from a23-43-64-242.deploy.static.akamaitechnologies.com (23.43.64.242): icmp_seq=10 ttl=51 time=3.54 ms

--- e9566.dscb.akamaiedge.net ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 1806ms
rtt min/avg/max/mdev = 3.258/3.383/3.536/0.101 ms
```

Both China university and Japan university are not responding within 1.8s, might due to too complexed Internet connections (too many internal transferring servers that made the respond time too long).

### Question 12

```
ubuntu@ubuntu:~/CWM-project/assignment2$ ping 127.0.0.1 -c 10 -i 0.2
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=6 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=7 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=8 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=9 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=10 ttl=64 time=0.017 ms

--- 127.0.0.1 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 1865ms
rtt min/avg/max/mdev = 0.017/0.017/0.019/0.000 ms
```

### Question 13

```
ubuntu@ubuntu:~/CWM-project/assignment2$ sudo ping 127.0.0.1 -c 100 -i 0.01
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.012 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.014 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.009 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.012 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=6 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=7 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=8 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=9 ttl=64 time=0.020 ms
64 bytes from 127.0.0.1: icmp_seq=10 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=11 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=12 ttl=64 time=0.020 ms
64 bytes from 127.0.0.1: icmp_seq=13 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=14 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=15 ttl=64 time=0.020 ms
64 bytes from 127.0.0.1: icmp_seq=16 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=17 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=18 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=19 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=20 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=21 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=22 ttl=64 time=0.014 ms
64 bytes from 127.0.0.1: icmp_seq=23 ttl=64 time=0.014 ms
64 bytes from 127.0.0.1: icmp_seq=24 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=25 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=26 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=27 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=28 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=29 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=30 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=31 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=32 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=33 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=34 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=35 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=36 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=37 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=38 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=39 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=40 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=41 ttl=64 time=0.014 ms
64 bytes from 127.0.0.1: icmp_seq=42 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=43 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=44 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=45 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=46 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=47 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=48 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=49 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=50 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=51 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=52 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=53 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=54 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=55 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=56 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=57 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=58 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=59 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=60 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=61 ttl=64 time=0.021 ms
64 bytes from 127.0.0.1: icmp_seq=62 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=63 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=64 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=65 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=66 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=67 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=68 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=69 ttl=64 time=0.020 ms
64 bytes from 127.0.0.1: icmp_seq=70 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=71 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=72 ttl=64 time=0.010 ms
64 bytes from 127.0.0.1: icmp_seq=73 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=74 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=75 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=76 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=77 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=78 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=79 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=80 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=81 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=82 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=83 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=84 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=85 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=86 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=87 ttl=64 time=0.015 ms
64 bytes from 127.0.0.1: icmp_seq=88 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=89 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=90 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=91 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=92 ttl=64 time=0.014 ms
64 bytes from 127.0.0.1: icmp_seq=93 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=94 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=95 ttl=64 time=0.017 ms
64 bytes from 127.0.0.1: icmp_seq=96 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=97 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=98 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=99 ttl=64 time=0.018 ms
64 bytes from 127.0.0.1: icmp_seq=100 ttl=64 time=0.020 ms

--- 127.0.0.1 ping statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 1096ms
rtt min/avg/max/mdev = 0.009/0.017/0.021/0.002 ms
```

The minimum/max difference is quite small. It might comes from some interference.

### Question 14

```
ubuntu@ubuntu:~/CWM-project/assignment2$ sudo ping 127.0.0.1 -c 10000 -f
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
 
--- 127.0.0.1 ping statistics ---
10000 packets transmitted, 10000 received, 0% packet loss, time 88ms
rtt min/avg/max/mdev = 0.002/0.002/0.012/0.000 ms, ipg/ewma 0.008/0.002 ms
```

