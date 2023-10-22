total_people = int(input("How many total people are there? "))
people_per_group = int(input("How many people do you want in each group? "))

num_groups = total_people // people_per_group
people_leftover = total_people % people_per_group

print(f"There are {num_groups} groups with {people_leftover} left over.")