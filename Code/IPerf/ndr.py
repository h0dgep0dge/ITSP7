from func import *

tests = [
    {"size":64-iperf_overhead},
    {"size":512-iperf_overhead},
    {"size":1500-iperf_overhead},
]

for test in tests:
    test["result"] = run_ndr("172.16.10.1",500-iperf_overhead,readout=True)
    print(tests)