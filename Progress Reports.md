# Progress reports

## Week 5-6

### Progress

I’m slightly behind the plan in terms of documents written, I’ve completed a document with my requirements and my proposed solutions, and completed some research on the packet generator I would like to use, TRex.

### Meeting with Graham

I met with Graham on the 26th of August, and I caught him up on my plan for the project, and we discussed the challenges i’m anticipating going forward with the project.

### Challenges

TRex has a great depth of flexibility and configurability, and just understanding how it works on a core level is very difficult. I’ve been reading as much as I can find about it but the documentation isn’t very helpful to someone just getting started.

### Results

After the research I’ve done, I’m convinced that TRex will be a good solution, if I can overcome the challenge of understanding how it works and how to properly use it.

### Going Forward

I’m going to continue working with my mentors both at EIT and at my job at Inspire Net, and continue researching how to leverage these tools to achieve my goals.

## Weeks 7-8

### Progress

In week 7 I started working on running the TRex software on real hardware. The first obstacle was getting an operating system installed on the machine, with no graphical output.

The first operating system I tried was CentOS 7.6, the OS and version recommended by the TRex documentation, however the outdated packages didn't work with the most recent version of TRex.

In week 8 I tried installing the latest version of Debian, which is working reasonably well.
I've successfully run TRex in kernel mode, but still having some glitches with DPDK mode.
I've started documenting the process of installing Debian on my firebox in the file Installation.md

### Challenges

Finding a way to install a linux distribution on a computer with no graphical output was a big challenge.
I solved it by generating a custom install image that can be controlled over serial.
I'm also still struggling with the lack of good documentation for TRex, but making progress nonetheless.

### Palmerston North Linux User Group

In week 8 I gave a presentation to the Palmerson North Linux User Group on the topic of OpenWRT, a Linux distro for routers.
After my presentation I spoke with a few of the attendees about networking and particularly driver support enabling hardware acceleration for routing.
I'm hoping this knowledge will help me with completing this project.

## Weeks 9-10

### Milestones

* Got TRex working on the firebox in DPDK mode, by moving to CentOS Stream 9
* Ran first benchmarks on a Mikrotik router running in bridge mode
* Developed a simple routing configuration for the Mikrotik router that supports running route mode benchmarks

### Documentation

* Extended Install.md to cover installing CentOS Stream 9 on the Firebox

## Weeks 11-12


Learning Python API, first automated tests
Issue, router has degraded performance when starting test using pytohn API, found this is because using the `start --total` command from the console runs the test equally on all available interfaces, while the particular way I've been starting the test via python is biasing towards one interface, creating a bottleneck.
