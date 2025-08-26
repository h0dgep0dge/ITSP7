# Project Bitstream Requirements and Proposed Solution

## Requirements

### Functional

* The platform shall carry out network performance tests on routing and switching devices attached to its ports
* The platform shall be able to carry out a series of these tests automatically
* The platform shall be able to apply configuration changes on the device-under-test automatically between tests
* The platform shall generate reports showing changes in performance against changes in configuration

### Non-functional

* The platform may use a text based or command line based interface, but should be easy to use for a technical user, and give output that is easy to understand

## Proposed Solution

### Packet generation - TRex

TRex is an open source high performance packet generation software developed by Cisco. It is highly configurable and allows for very deep and nuanced testing. I think it would be very well suited to be the traffic generation and measurement component of this system, however the depth of configurability is going to be a challenge to master.

### Configuration deployment - Custom software

There are standardized protocols for deploying configuration to a networking device, such as TR-069. Although using a standardized protocol like this would give more flexibility in the devices that could be tested while varying configuration, I decided implementing TR-069 or trying to use an OTS TR-069 solution would be too complex for the scale of this project. Instead I plan to write a simple custom solution to target Mikrotik RouterOS devices, as most of the devices I have to test are Mikrotik routers.

### Test automation - Further research needed

Some tools for iteratively running TRex tests already exist, but it’s not currently clear to me if these tools are generally applicable or only useful for narrow use-cases. This will require further investigation, and may require a custom solution.
