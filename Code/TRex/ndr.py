from trex.stl.api import *

import time
import json
from pprint import pprint
import argparse
import sys
import os
from enum import Enum

class Tester:
    def __init__(self,user,server,verbose_level='error'):
        self.handle = STLClient(username=user, server=server, verbose_level=verbose_level)
        self.active_ports = {}
    
    def __enter__(self):
        self.handle.connect()
        self.handle.reset()
        return self

    def __exit__(self,type,value,traceback):
        self.handle.disconnect()

    def get_active_ports(self):
        ports = []
        for port in self.active_ports:
            ports.append(port)
        return ports

    def add_stream(self,port,src="16.0.0.0",dst="48.0.0.0",size=512):
        pkt = Ether()/IP(src=src,dst=dst)/UDP(sport=31337,dport=31337)
        padding = max(size-len(pkt),0)*'x'


        instructions = STLScVmRaw( [ 
                                     STLVmFlowVar ( "ip_src", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_src", pkt_offset= "IP.src", offset_fixup=2 ),
                                     STLVmFlowVar ( "ip_dst", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_dst", pkt_offset= "IP.dst", offset_fixup=2 ),
                                     
                                     STLVmFixIpv4(offset = "IP"),
                         ]
                      )

        stlpkt = STLPktBuilder( pkt = pkt/padding , vm = instructions )
        self.handle.add_streams(STLStream(packet = stlpkt,mode = STLTXCont()),ports=[port])
        self.active_ports[port] = True

    def wait(self):
        self.handle.wait_on_traffic()

    def run_test(self,rate,duration=5):
        self.handle.clear_stats()
        self.handle.start(mult=f"{int(rate)}bpsl1",total=True,duration=duration,ports=self.get_active_ports())
        self.wait()
        time.sleep(1)
        stats = self.handle.get_stats()
        #print(stats["total"])
        return {"sent":stats["total"]["opackets"],"lost":stats["total"]["opackets"]-self.handle.get_stats()["total"]["ipackets"]}
    
    def run_ndr(self,packet_size=512,bottom_rate=1_000_000,top_rate=1_000_000_000,target_ndr=0,max_iterations=10,readout=True,duration=5,ports=[0]):
        low  =  bottom_rate
        high = top_rate
        best_bw = bottom_rate
        best_pps = 0
        iterations = 0

        for port in ports:
            self.add_stream(port,size=packet_size)

        while iterations < max_iterations:
            target = (low+high)/2
            iterations += 1
            if readout:
                print(f"Iteration {iterations}, trying {target}")
            results = self.run_test(rate=target,duration=duration)
            loss = results["lost"]/results["sent"]
            if loss > target_ndr:
                high = target
            else:
                low = target
                best_pps = results["sent"]/duration
                best_bw = best_pps*packet_size*8
        return {"bw":best_bw,"pps":best_pps}

tests = [
    {"size":64},
    {"size":512},
    {"size":1500},
]

with Tester(user="root",server="localhost") as t:
    for test in tests:
        test["result"] = t.run_ndr(packet_size=test["size"],target_ndr=0.05,duration=5)
        print(tests)

print(tests)
