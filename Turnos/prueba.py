from itertools import count

yourcounter = count()

next_counted_value = next(yourcounter)
next_counted_value = yourcounter()
print(next_counted_value)
if next_counted_value == 99:
    yourcounter = count(0)
    