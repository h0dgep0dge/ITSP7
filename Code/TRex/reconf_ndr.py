import ndr
import copy
import ros_api
import random

def o():
    return random.randint(1,254)

tests = [64,512,1500]

points = []
router = ros_api.Api('192.168.88.5', user='admin', password='tinykite04')

with ndr.Tester(user="root",server="localhost") as t:
    for i in range(0,11):
        for size in tests:
            point = t.run_ndr(packet_size=size,target_ndr=0.05,duration=10,readout=True,ports=[0,2])
            point["size"] = size
            point["rules"] = i
            #print(i,point)
            points.append(point)
        router.talk(('/ip/firewall/filter/add', '=action=drop' ,'=chain=forward', f"=dst-address={o()}.{o()}.{o()}.{o()}", f"=src-address={o()}.{o()}.{o()}.{o()}"))
        print(i)

print(points)

rows = []

for i in range(0,11):
    rows.append({})

for point in points:
    rows[point["rules"]][point["size"]] = point

print("rule,pps_64,bps_64,pps_512,bps_512,pps_1500,bps_1500")
for row in enumerate(rows):
    rule = row[0]
    pps_64 = row[1][64]["pps"]
    bps_64 = row[1][64]["bw"]
    pps_512 = row[1][512]["pps"]
    bps_512 = row[1][512]["bw"]
    pps_1500 = row[1][1500]["pps"]
    bps_1500 = row[1][1500]["bw"]
    
    print(rule,pps_64,bps_64,pps_512,bps_512,pps_1500,bps_1500,sep=",")
