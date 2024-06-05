qdels = ["qdel"]
for i in range(20099, 20397 + 1):
    qdels.append(str(i))

with open("qdel.txt", "w") as f:
    for qdel in qdels:
        f.writelines(qdel + " ")
