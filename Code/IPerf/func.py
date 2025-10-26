import iperf3

def run_test(rate,size,readout=False):
    client = iperf3.Client()
    client.duration = 5
    client.interval = 0.1
    client.server_hostname = '172.16.10.1'
    client.port = 5201
    client.protocol = 'udp'
    client.blksize = size
    client.bandwidth = rate
    client.reverse = True

    result = client.run()

    if result.error:
        raise Exception(result.error)

    packets_total = 0
    lost_total = 0

    for i in result.json["intervals"][1:]:
        packets_total += i["sum"]["packets"]
        lost_total += i["sum"]["lost_packets"]
    
    loss = lost_total/packets_total

    if readout:
        print("Lost",loss)
        print("pps",result.packets/result.seconds)
        print("L4 rate",(result.packets/result.seconds)*(size)*8)
        print("L3 rate",(result.packets/result.seconds)*(size+8)*8)
        print("L2 rate",(result.packets/result.seconds)*(size+28)*8)
        print("L1 rate",(result.packets/result.seconds)*(size+42)*8)

    return loss