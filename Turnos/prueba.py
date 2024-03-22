import sys

x = input("Sentences: ")
count = x.split()
letters = 0
found = 0
for i in x:
    if i.isalpha():
        letters += 1
for i in range(len(count)):
    if count[i] == "website":
        count[i] = "webapp"
        found += 1
    elif count[i] == "website.":
        count[i] = "webapp"
        found += 1
    else:
        continue
separator = ' '
re = separator.join(count)

        
print(f"{re}")
print(f"found: {found}")
print(f"count words: {len(count)}")
print(f"count letters: {letters}")