import ndr

tests = [
    {"size":64},
    {"size":512},
    {"size":1500},
]

with ndr.Tester(user="root",server="localhost") as t:
    for test in tests:
        test["result"] = t.ndr_simplex(packet_size=test["size"],target_ndr=0.05,duration=5,readout=False,pairs=[0,1])

print(tests)