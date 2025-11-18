from iperf_lib import *

tests = [
    {"size":64-iperf_overhead},
    {"size":512-iperf_overhead},
    {"size":1500-iperf_overhead},
]

for test in tests:
    test["result"] = run_ndr("4.4.4.4",test["size"],readout=True,target_ndr=0.05,duration=30)
    print(tests)

print(tests)
