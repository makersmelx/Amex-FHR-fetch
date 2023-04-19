PAGE_SIZE = 10
HEAD = "\n====================================================\n"


def isYes(input):
    return input in ["Yes", "yes", "Y", "y"]


def displayHotel(hotel, properties, graph):
    intro = HEAD
    intro += f'{hotel["name"]}\n'

    intro += f'Brand: {hotel["brand"]}\n'
    intro += f'City: {hotel["city"]}\n'
    intro += "\n"
    intro += f'{hotel["description"]["title"]}\n'
    intro += "\n"
    intro += f'{hotel["location"]}\n'
    intro += "\n"
    intro += f'{hotel["description"]["introduction"]}\n'
    print(intro)

    while True:
        choice = input(
            f"{HEAD}1. Check hotel details and activies\n2. Check FHR benefits.\n3. Find a related hotel.\n4. Quit (or type q).\n")
        if choice == "1":
            display = HEAD
            for item in hotel["details"]:
                display += f'{item}:\n'
                display += hotel["details"][item]
                display += "\n\n"
            print(display)
        elif choice == "2":
            display = HEAD
            for _index, item in enumerate(hotel["benefits"]):
                display += f"{_index+1}: {item}\n"
            print(display)
        elif choice == "3":
            displayByBrandAndCity(properties, graph, [
                                  hotel["brand"], hotel["city"]])
            print(intro)
        elif choice == "4" or choice == "q":
            return


def keywordMatchHotel(keyword, hotel):
    def containsLower(a, b):
        return a.lower() in b.lower()
    checkList = [hotel["name"], hotel["brand"],
                 hotel["city"], hotel["location"]]
    for c in checkList:
        if containsLower(keyword, c):
            return True
    for value in hotel["description"].values():
        if containsLower(keyword, value):
            return True
    for value in hotel["details"].values():
        if containsLower(keyword, value):
            return True
    return False


def paginationAndInput(source):
    page = 0
    while True:
        print(HEAD)
        for i in range(page*PAGE_SIZE, (page+1)*PAGE_SIZE):
            if i < len(source):
                print(f"{'{:0>2}'.format(i+1)}: {source[i]}")
        hasNext = (page+1)*PAGE_SIZE <= len(source)
        todo = input(
            f"Input the number to check details. {'n for next page.' if hasNext else ''}q to quit.\n")
        if todo == "q":
            return -1
        elif todo == "n":
            page += 1
            continue
        elif todo.isdigit() and 0 < int(todo) <= len(source):
            return int(todo) - 1


def displayByBrandAndCity(properties, graph, mode=None):
    indexList = []
    # display related hotels
    if mode and isinstance(mode, list):
        indexList = sorted(graph["brand"][mode[0]] + graph["city"][mode[1]])
    else:
        # display all brands
        mode = "brand" if (mode and mode == "brand") else "city"
        # select a brand/city to display
        source = sorted(graph[mode].keys())
        choice = paginationAndInput(source)
        if choice == -1:
            return
        # select a hotel to display
        indexList = graph[mode][source[choice]]

    nameOnly = [properties[i]["name"] for i in indexList]

    while True:
        choice = paginationAndInput(nameOnly)
        if choice == -1:
            return

        hotel = properties[indexList[choice]]
        displayHotel(hotel, properties, graph)


def searchByKeywords(properties, graph):
    keywords = input(
        f"{HEAD}Please input one or more keywords. seperate by \",\"\n").split(",")
    result = []
    for index, hotel in enumerate(properties):
        match = True
        for word in keywords:
            match = keywordMatchHotel(word, hotel)
            if not match:
                break
        if match:
            result.append(index)
    while True:
        choice = paginationAndInput([properties[i]["name"] for i in result])
        if choice == -1:
            return
        displayHotel(properties[result[choice]], properties, graph)


def mainInteraction(properties, graph):
    while True:
        choice = input(
            f"{HEAD}Please choose an option.\n1. List all brands of FHR hotels.\n2. List all cities that have an FHR hotel\n3. Seach an FHR hotel by keyword(s).\n4. Quit (or type q)\n")
        if choice == "1":
            displayByBrandAndCity(properties, graph, "brand")
        elif choice == "2":
            displayByBrandAndCity(properties, graph, "city")
        elif choice == "3":
            searchByKeywords(properties, graph)
        elif choice == "4" or choice == "q":
            return
