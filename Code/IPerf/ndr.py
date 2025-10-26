from func import run_test

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
