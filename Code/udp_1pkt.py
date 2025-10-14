from trex_stl_lib.api import *
import argparse


class STLS1(object):

    def get_streams (self, direction, tunables, **kwargs):
        parser = argparse.ArgumentParser(description='Argparser for {}'.format(os.path.basename(__file__)), 
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-c','--client', type=str, default='16.0.0.0', help='Template for the client IP addresses')
        parser.add_argument('-s','--server', type=str, default='48.0.0.0', help='Template for the server IP addresses')
        parser.add_argument('-l','--length', type=int, default=512, help='Target L3 packet length')
        args = parser.parse_args(tunables)
        
        print(args,direction)

        if direction==0:
            src_ip=args.client
            dst_ip=args.server
            src_port=31337
            dst_port=12
        else:
            src_ip=args.server
            dst_ip=args.client
            src_port=12
            dst_port=31337

        pkt = Ether()/IP(src=src_ip,dst=dst_ip)/UDP(sport=src_port,dport=dst_port)
        padding = max(args.length-len(pkt.payload),0)*'x'

        instructions = STLScVmRaw( [ 
                                     STLVmFlowVar ( "ip_src", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_src", pkt_offset= "IP.src", offset_fixup=2 ),
                                     STLVmFlowVar ( "ip_dst", min_value=1,max_value=511,size=2,op="random"),
                                     STLVmWrFlowVar (fv_name="ip_dst", pkt_offset= "IP.dst", offset_fixup=2 ),
                                     STLVmFixIpv4(offset = "IP")
                         ]
                      )

        stlpkt = STLPktBuilder( pkt = pkt/padding , vm = instructions )

        return [ STLStream( packet = stlpkt,mode = STLTXCont()) ]


# dynamic load - used for trex console or simulator
def register():
    return STLS1()



