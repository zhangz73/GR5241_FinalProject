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

data = pd.read_csv("../Data/communities.csv")
to_delete = []
for col in data.columns:
    if np.sum(data[col] == "?") > 0:
        to_delete.append(col)
data[[x for x in data.columns if x not in to_delete]].to_csv("../Data/communities_rmMissing.csv", index=False)
