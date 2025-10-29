import iperf3

iperf_overhead = 42

def run_test(hostname,rate,size,readout=False,port=5201,duration=5):
    client = iperf3.Client()
    client.duration = duration+1
    client.server_hostname = hostname
    client.port = port
    client.protocol = 'udp'
    client.blksize = size
    client.bandwidth = int(rate)
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
        print()

    return {"sent":packets_total,"lost":lost_total}

def run_ndr(hostname,packet_size,bottom_rate=1_000_000,top_rate=1_000_000_000,target_ndr=0,max_iterations=10,target_delta=1000,readout=True,port=5201,duration=5):
    low  =  bottom_rate
    high = top_rate
    best_bw = bottom_rate
    best_pps = 0
    iterations = 0

    while iterations < max_iterations:
        target = (low+high)/2
        iterations += 1
        if readout:
            print(f"Iteration {iterations}, trying {target}")
        results = run_test(hostname,target,packet_size,readout=readout,port=port,duration=duration)
        loss = results["lost"]/results["sent"]
        if loss > target_ndr:
            high = target
        else:
            low = target
            best_pps = results["sent"]/duration
            best_bw = best_pps*packet_size
    return {"bw":best_bw,"pps":best_pps}

