qdels = ["qdel"]
for i in range(187043, 187775 + 1):
    qdels.append(str(i))

with open("qdel.txt", "w") as f:
    for qdel in qdels:
        f.writelines(qdel + " ")
