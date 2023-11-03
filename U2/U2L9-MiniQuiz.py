data = [150, -121, 43, 44, 92, 91, -14, 161, 73, 64, 19, -71, -61]

total_sum, average,  = 0, 0

for index, number in enumerate(data):
    if number % 2 == 0 or number >= 100:
        print(f"Skipping data: {number}")
        data[index] = 0
    else:
        total_sum += number

while 0 in data:
    data.remove(0)

print(f"Total sum of valid data: {total_sum}")
print(f"Average of valid data: {round((total_sum / len(data)), 2)}")