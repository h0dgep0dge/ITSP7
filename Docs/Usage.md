## Using IPerf for testing in direct mode

The iperf_lib.py file has 2 functions, `run_test()` for running a one-off test, and `run_ndr()` for running a "non drop rate" test.

~~~
run_test(hostname,rate,size,readout=False,port=5201,duration=5)
    run_test executes a single test run at the prescribed packet rate, duration,
    and size, and returns a dict containing the number of packets sent and the
    number of packets lost.

    hostname: the target hostname as a string
    rate: the number of packets to send per second as an integer
    size: the size of the packet to be transmitted, not including
          overhead for IPerf, UDP, IP, or Ethernet. Integer
    readout: Print possibly useful information about connections, boolean, default false
    port: The port of the server listening on the target host, default 5201
    duration: The number of seconds to run the test, default 5
~~~

~~~

~~~

## Using TRex for testing in indirect mode