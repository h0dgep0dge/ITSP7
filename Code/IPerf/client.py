import iperf3


client = iperf3.Client()
client.duration = 5
client.server_hostname = '172.16.10.1'
client.port = 5201
client.protocol = 'udp'
client.blksize = 200
client.bandwidth = 1000000
client.reverse = True
result = client.run()

if result.error:
    print(result.error)
else:
    print(result)
