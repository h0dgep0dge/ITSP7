import iperf3

packet_size = 400

def run_test(rate):
    global packet_size
    client = iperf3.Client()
    client.duration = 20
    client.server_hostname = '172.16.10.1'
    client.port = 5201
    client.protocol = 'udp'
    client.blksize = packet_size
    client.bandwidth = rate
    client.reverse = True

    result = client.run()

    if result.error:
        return result.error
    return result

low  =  8_000_000
high = 12_000_000

while True:
    target = (low+high)/2
    print("Trying",target)
    result = run_test(int(target))
    percent = result.lost_percent
    print("Lost",percent)
    print("pps",result.packets/result.seconds)
    print("L4 rate",(result.packets/result.seconds)*(packet_size)*8)
    print("L3 rate",(result.packets/result.seconds)*(packet_size+8)*8)
    print("L2 rate",(result.packets/result.seconds)*(packet_size+28)*8)
    print("L1 rate",(result.packets/result.seconds)*(packet_size+42)*8)
    if percent > 0:
        high = target
    else:
        low = target
    print()
