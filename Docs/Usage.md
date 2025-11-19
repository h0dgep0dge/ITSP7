## Using IPerf for testing in direct mode

IPerf is recommended for tests where the client is required to be directly attached to the router, on the same LAN. For simulating clients behind a router, use TRex for indirect testing.

The iperf_lib.py file has 2 functions, `run_test()` for running a one-off test, and `run_ndr()` for running a "non drop rate" test.

~~~
run_test(hostname,rate,size,readout=False,port=5201,duration=5)
    run_test() executes a single test run at the prescribed packet rate, duration,
    and size, and returns a dict containing the number of packets sent and the
    number of packets lost.

    hostname: the target hostname as a string
    rate: the target bitrate to send per second as an integer
    size: the size of the packet to be transmitted, not including overhead for IPerf, UDP, IP, or Ethernet. Integer
    readout: Print possibly useful information about connections, boolean, default false
    port: The port of the server listening on the target host, default 5201
    duration: The number of seconds to run the test, default 5
~~~

~~~
run_ndr(hostname, packet_size, bottom_rate=1_000_000, top_rate=1_000_000_000, target_ndr=0, max_iterations=10, target_delta=1000, readout=True, port=5201, duration=5)
    run_ndr() runs a series of tests with run_test(), finding the highest
    possible transmission rate resulting in a drop rate of target_ndr at most.
    This rate is found by way or successive bisection of the search space, a
    binary search.

    hostname: the target hostname as a string
    packet_size: the size of the packet to be transmitted, not including overhead for IPerf, UDP, IP, or Ethernet. Integer
    bottom_rate: the lowest possible rate to check, one megabit by default
    top_rate: the highest possible rate to check, one gigabit by default
    target_ndr: the drop rate the algorithm targets
    max_iterations: the maximum number of tests that can be run
    target_delta: sets a target delta between the top and bottom of the remaining search space, ending the test if this point is reached
    readout: Print possibly useful information about connections, boolean, default false
    port: The port of the server listening on the target host, default 5201
    duration: The number of seconds to run the test, default 5
~~~

## Using TRex for testing in indirect mode

ndr.py provides a Tester class for configuring and running tests through TRex. Streams can be configured and customized, and then run at a target rate with `run_test()` or run a series of tests to calculate the NDR with `ndr_simplex()` and `ndr_duplex()`

class Tester:
    def __init__(self,user,server,verbose_level='error')
    def get_active_ports(self):
    def add_stream_multi(self,pair,src_msb=16,dst_msb=48,size=512,direction=0):
    def add_stream(self,pair,src_msb=16,dst_msb=48,size=512,direction=0,instructions=None,pps=1000):
    def wait(self):
    def run_test(self,rate,duration=5,readout=False)
    def ndr_simplex(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5,pairs=[0])
    def ndr_duplex_acks(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5,pairs=[0])
    def run_ndr(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5):