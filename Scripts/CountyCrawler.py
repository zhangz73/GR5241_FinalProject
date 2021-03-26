import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

state_code_map = pd.read_csv("../Data/StateCode.csv")
county_code_map = pd.read_csv("../Data/CountyCode.csv")

def get_communities():
    with open("../Data/communities.data", "r") as f:
        lines = f.readlines()
    communities = [line.strip().split(",")[3] for line in lines]
    state_code = [line.strip().split(",")[0] for line in lines]
    return communities, state_code

def crawl_from_wiki(state_code, community):
    url = "https://www.google.com/search?q=fips+code+for+"
    state_name = state_code_map[state_code_map.FIPS == int(state_code)]["StateName"].iloc[0]
    url += community + " " + state_name
    url = url.strip().replace(" ", "+")
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
        
    divs = soup.findAll("div", {"class": "BNeawe s3v9rd AP7Wnd"}) #Z0LcW XcVN5d AZCkJd
    #print([divs[i].getText() for i in range(len(divs))])
    info = [divs[i].getText().strip() for i in range(len(divs))]
    zip, fips = " ", " "
    for i in range(len(info) - 1):
        if info[i].lower() == "zip code":
            zip = info[i + 1]
        elif info[i].lower() == "fips code":
            fips = info[i + 1]
#    zip = divs[1].getText().strip()
#    fips = divs[5].getText().strip()
    print(zip, fips)
    fips = fips.replace("-", "")
    if len(fips) == 10:
        county_code = fips[2:5]
        county_name = county_code_map[county_code_map.FIPS == int(county_code)]["CountyName"].iloc[0]
    else:
        county_name = ""
    return zip, fips, county_name, state_name

communities, state_code = get_communities()

zip_arr = []
fips_arr = []
county_code_arr = []
county_name_arr = []
community_name_arr = []
community_code_arr = []
state_code_arr = []
state_name_arr = []

for i in tqdm(range(len(communities))):
    zip, fips, county_name, state_name = crawl_from_wiki(state_code[i], communities[i])
    zip_arr.append(zip)
    fips_arr.append(fips)
    county_name_arr.append(county_name)
    state_name_arr.append(state_name)
    state_code_arr.append(" " + fips[:2])
    community_code_arr.append(" " + fips[-5:])
    community_name_arr.append(communities[i])
    if len(fips) == 10:
        county_code_arr.append(" " + fips[2:5])
    else:
        county_code_arr.append(" ")

df = pd.DataFrame.from_dict({"ZipCode": zip_arr, "FIPS": fips_arr, "CountyName": county_name_arr, "CountyCode": county_code_arr, "CommunityName": community_name_arr, "CommunityCode": community_code_arr, "StateName": state_name_arr, "StateCode": state_code_arr})
df.to_csv("../Locations.csv", index=False)
