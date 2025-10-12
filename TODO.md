### To do list

* Write a stream profile that does everything I need
  * Addresses directly configurable
  * Many different IP addresses (500 destinations and sources)
* Put together configurations for the routers I want to test, in the configurations I want to test
  * Routerboard RB951G-2HnD
    * Bridging (w/ and w/out bridge filter rules)
    * Routing
      * Fast path
      * 25 filter rules
      * 25 simple queues
      * PPPoE
  * Netcomm NF18AC
    * PPPoE
  * Mercku M6A
    * PPPoE
* Write a library to iteratively change parameters on a Mikrotik router
* Write a program that iteratively increases traffic on a port while measuring drop rate, either recording the drop rate for all throughputs, or finding the highest throughput that gives a specified drop rate or less
* Write a framework to run tests and update parameters
