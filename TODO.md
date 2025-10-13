### To do list

* Write a stream profile that does everything I need ✅
  * At least 500 different destinations and sources, address ranges directly configurable ✅
  * Packet size directly configurable ✅
* Put together configurations for the routers I want to test, in the configurations I want to test
  * Routerboard RB951G-2HnD
    * Bridging (w/ and w/out bridge filter rules)
    * Routing
      * Fast path
      * 25 filter rules
      * 25 simple queues
      * PPPoE, with NAT
  * Netcomm NF18AC
    * PPPoE, with NAT
  * Mercku M6A
    * PPPoE, with NAT
* Write a library to iteratively change parameters on a Mikrotik router
* Write a program that iteratively increases traffic on a port while measuring drop rate, either recording the drop rate for all throughputs, or finding the highest throughput that gives a specified drop rate or less
* Write a framework to run tests and update parameters
* Compile report of results
