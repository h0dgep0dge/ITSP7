## Using IPerf for testing in direct mode

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