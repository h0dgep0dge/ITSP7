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

    def add_stream_multi(self,pair,src_msb=16,dst_msb=48,size=512,direction=0):
        instructions = STLScVmRaw( [ 
                                     STLVmFlowVar ( "ip_src", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_src", pkt_offset= "IP.src", offset_fixup=2 ),
                                     STLVmFlowVar ( "ip_dst", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_dst", pkt_offset= "IP.dst", offset_fixup=2 ),
                                     
                                     STLVmFixIpv4(offset = "IP"),
                         ]
                      )
        self.add_stream(pair,src_msb,dst_msb,size,direction,instructions)

    def add_stream(self,pair,src_msb=16,dst_msb=48,size=512,direction=0,instructions=None,pps=1000):
        port = pair*2+direction
        src = f"{src_msb+port}.0.0.1"
        dst = f"{dst_msb+port}.0.0.1"
        pkt = Ether()/IP(src=src,dst=dst)/UDP(sport=31337,dport=31337)
        padding = max(size-len(pkt),0)*'x'

        stlpkt = STLPktBuilder( pkt = pkt/padding , vm = instructions )
        self.handle.add_streams(STLStream(packet = stlpkt,mode = STLTXCont(pps=1000)),ports=[port])
        self.active_ports[port] = True

    def wait(self):
        self.handle.wait_on_traffic()

    def run_test(self,rate,duration=5,readout=False):
        self.handle.clear_stats()
        self.handle.start(mult=f"{rate}%",duration=duration,ports=self.get_active_ports())
        self.wait()
        time.sleep(1)
        stats = self.handle.get_stats()
        if readout:
            print(stats["total"])
        return {"sent":stats["total"]["opackets"],"lost":stats["total"]["opackets"]-self.handle.get_stats()["total"]["ipackets"]}
    
    def ndr_simplex(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5,pairs=[0]):
        self.handle.reset() # make sure there are no lingering streams on the ports
        for pair in pairs:
            self.add_stream(pair,size=packet_size)
        return self.run_ndr(packet_size,bottom_rate,top_rate,target_ndr,max_iterations,readout,duration)
    
    def ndr_duplex_acks(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5,pairs=[0]):
        self.handle.reset()
        for pair in pairs:
            self.add_stream(pair,size=packet_size,direction=0,pps=1000)
            self.add_stream(pair,size=packet_size,direction=1,pps=50)
        return self.run_ndr(packet_size,bottom_rate,top_rate,target_ndr,max_iterations,readout,duration)

    def run_ndr(self,packet_size=512,bottom_rate=0,top_rate=100,target_ndr=0,max_iterations=10,readout=False,duration=5):
        low  =  bottom_rate
        high = top_rate
        best_bw = bottom_rate
        best_pps = 0
        iterations = 0

        while iterations < max_iterations:
            target = (low+high)/2
            iterations += 1
            if readout:
                print(f"Iteration {iterations}, trying {target}%")
            results = self.run_test(rate=target,duration=duration,readout=readout)
            loss = results["lost"]/results["sent"]
            if loss > target_ndr:
                high = target
            else:
                low = target
                best_pps = results["sent"]/duration
                best_bw = best_pps*(packet_size)*8
        return {"bw":best_bw,"pps":best_pps}



