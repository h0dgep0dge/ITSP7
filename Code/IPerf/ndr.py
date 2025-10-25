import iperf3


def run_test(rate,size,readout=False):
    client = iperf3.Client()
    client.duration = 4
    client.server_hostname = '172.16.10.1'
    client.port = 5201
    client.protocol = 'udp'
    client.blksize = size
    client.bandwidth = rate
    client.reverse = True

    result = client.run()

    if result.error:
        return result.error



    best_loss = 100
    for i in result.json["intervals"]:
        best_loss = min(i["sum"]["lost_percent"],best_loss)
    
    if readout:
        print("Lost",best_loss)
        print("pps",result.packets/result.seconds)
        print("L4 rate",(result.packets/result.seconds)*(size)*8)
        print("L3 rate",(result.packets/result.seconds)*(size+8)*8)
        print("L2 rate",(result.packets/result.seconds)*(size+28)*8)
        print("L1 rate",(result.packets/result.seconds)*(size+42)*8)

    return best_loss

low  =  8_000_000
high = 12_000_000

while True:
    target = (low+high)/2
    print("Trying",target)
    result = run_test(int(target),400,True)
    
    if result > 0:
        high = target
    else:
        low = target
    print()
