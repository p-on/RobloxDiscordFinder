import requests, threading, re, sys
discord_regex = r'(.{2,32}([^a-zA-Z0-9_\-\/()\[\]{}])\d{4})'

class c: 
    "Corresponding console colour codes."
    BL = '\033[30m'; R  = '\033[31m'; LR = '\033[1;31m'; G  = '\033[32m'; YE = '\033[93m'; B  = '\033[34m'; LB = '\033[1;34m'; MA = '\033[35m'; CY = '\033[36m'; W  = '\033[37m'; RS = '\033[0m'; EC = '\033[0m'; BD = '\033[1m'; UL = '\033[4m'; X = '\033[0m'; Y = '\033[31m'

class main:
    "Main functions for Roblox Discord Finder."
    def search_ropro(id: str, name: str):
        "Searches RoPro API for a linked Discord."
        response = requests.post("https://api.ropro.io/getUserInfoTest.php?userid=" + id)
        if response.status_code == 200:
            data = response.json()
            if not data["discord"] == "":
                print(f"{c.X}Discord found ({c.YE}{name}{c.X}) {c.G}", data["discord"], c.X)

    def search_description(data: str, name: str):
        "Searches description for Discord tag matches."
        for query in re.findall(discord_regex, data):
            print(f"{c.X}Discord found ({c.YE}{name}{c.X}) {c.G}", str(query).split("(")[1].split("',")[0].split("'")[1], c.X)

    def find_user(id: str):
        "Finds Roblox information."
        response = requests.get("https://users.roblox.com/v1/users/" + id)
        if response.status_code == 200:
            data = response.json()
            return data

    def name_to_id(name: str):
        "Finds Roblox user id from name."
        response = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [name]})
        if response.status_code == 200:
            data = response.json()
            return str(data["data"][0]["id"])

    def query_friends(id: str):
        "Grabs all Roblox friends of user."
        response = requests.get("https://friends.roblox.com/v1/users/" + id + "/friends?userSort=Alphabetical")
        if response.status_code == 200:
            data = response.json()
            return data["data"]

if not len(sys.argv) > 1:
    print(f"{c.R}User not specified, example: {c.YE}py rdf.py 9igeon{c.X}")
else:
    user_input = sys.argv[1]
    print(f"{c.X}Starting search for {user_input}, this could take a while...")
    user_id = main.name_to_id(user_input)
    threads = []

    if user_id:
        user_data = main.find_user(user_id)
        threads.append(threading.Thread(target=main.search_ropro, args=(user_id, user_input)))
        threads.append(threading.Thread(target=main.search_description, args=(user_data["description"], user_input)))

        user_friends = main.query_friends(user_id)
        for friend in user_friends:
            friend_data = main.find_user(str(friend["id"]))
            threads.append(threading.Thread(target=main.search_ropro, args=(str(friend["id"]), friend["name"])))
            threads.append(threading.Thread(target=main.search_description, args=(friend_data["description"], friend["name"])))
    else:
        print(f"{c.R}User not found!{c.X}")

    for thread in threads: thread.start()
    for thread in threads: thread.join()
    print(f"{c.X}Searching done for {user_input}!")
exit()
