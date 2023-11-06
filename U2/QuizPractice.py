def sum_ignore_markers(numbers:list, marker:int, delimiter:int):
  sum = 0
  ignored = False
  for number in numbers:
    if number != marker:
      if not ignored:
        sum += number
      else:
        if number == delimiter:
          ignored = False
    else:
      ignored = True
  return sum

numbers = [1, 2, 2, 6, 99, 99, 7]
print(sum_ignore_markers(numbers, 6, 7))