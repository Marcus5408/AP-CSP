from bus import Bus

bus = Bus(2)

for i in range(10):
    print(bus.current_stop)
    bus.move()
