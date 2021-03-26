## Load Data:
with open("../Data/communities.data", "r") as f:
    lines = f.readlines()
    data = [line.strip().split(",") for line in lines]

with open("../Data/Attributes.txt", "r") as f:
    attributes = f.readlines()
    attributes = [x.strip("\n") for x in attributes]

with open("../Data/communities.csv", "w") as f:
    f.write(",".join(attributes) + "\n")
    for line in lines:
        f.write(line)
