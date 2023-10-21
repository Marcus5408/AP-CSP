from math import floor, log2

def circle_solver(n):
    return (n - (2 ** floor(log2(n)))) * 2 + 1
    return 1 if n & (n - 1) == 0 and n != 0 else (n - 2 ** (n.bit_length() - 1)) * 2 + 1
    # use a ternary operator to return 1 if n is a power of 2, otherwise do the following:
    # find the last power of 2: (2 ** (n.bit_length() - 1))
    # subtract that from n to get the difference between the last power of 2 and n
    # multiply that difference by 2 and add 1
    # return that value
    
# this is the same as the above function, but expanded for readability
def expanded_function(n):
    if n & (n - 1) == 0 and n != 0: return 1 # if n is a power of two, print 1
    else:
        last_power_of_two = 2 ** (n.bit_length() - 1) # find the last power of two
        n = (n - last_power_of_two) * 2 + 1 # find the difference between the last power of two and n, then multiply by 2 and add 1
        return n
    
print("Welcome to the Circular Problem Solver!")
n = int(input("How many numbers are in the circle? (n): "))
print(f"The last number remaining is {circle_solver(n)}")