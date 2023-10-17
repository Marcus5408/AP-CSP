age = 15
is_adult = False

if age >= 16 and is_adult:
    print("can drive and an adult!")
else:
    if age > 16 or is_adult:
        if age > 16:
            print("can drive")
        if is_adult:
            print("adult")
    else:
        print("can't drive and not an adult")


print("the end")