# 	Author: Vince Verdadero (19009246)
#   Created: 27 / 01 / 21
#   Last edited: 10 / 02 / 21
#   Description: A program to show the shopping schedule and delivery schedule
#  	This program will:
# 					Show the day of the week that you visited per store for week 3 and 4
#                   List the items per store that you should buy and any substitutions that could be available.
#                   Delivery Schedule for the items that should be delivered per day.
#  	User advice: None


# This import is used to read csv files
import csv


# classes to construct objects to show the available items
class Store:

    # constructor for the store class
    def __init__(self, tag, stockitem, numberofweeks):
        self.Tag = tag
        self.StockItem = stockitem
        self.Itemsbought = []
        self.alternatives = []
        self.dayVisited = 0

        for i in range(numberofweeks):
            self.Itemsbought.append([])
            self.alternatives.append([])

    # This checks the item of the store if that Item is available.
    # Having a boolean will make sure whether there is an item or not.
    def availableitemsinstock(self, item):
        if item in self.StockItem:
            return True
        else:
            return False


class Item:
    # constructor for the Item class
    def __init__(self, nameofitem, price):
        self.NameofItem = nameofitem
        self.Price = price


class House:
    # constructor for the House class
    def __init__(self, housenumber, itemsrequired, numberofweeks):
        self.HouseNumber = housenumber
        self.ItemsRequired = itemsrequired
        self.DayofDelivery = []
        for i in range(numberofweeks):
            self.DayofDelivery.append([])


# These are different global variables that will be used for a variety of functions
Stores = []
Houses = []
Items = []

Number_of_weeks = 0
Number_of_Houses = 0


# Reads csv file using the file path.
# This will Read the data from the csv file from the filepath used and it delivers it to an array.
def readcsv(filepath):
    list_of_data = []

    with open(filepath, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            list_of_data.append(row)  # Adds the row to a list

        return list_of_data


# # This is a def function and a Days list to show the different days of the week
# This will print out the items that the Danny/Carla should go to on that day
# and when they should deliver on the day listed
def daynames():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return days


# This will set the global variables, and will hold the data about the number of weeks and houses on the file.
def getnumberweeksandhouses():
    global Number_of_weeks, Number_of_Houses
    filepath = "DATA CWK SHOPPING DATA WEEK 4 FILE B.csv"
    data_of_houses = readcsv(filepath)

    # This will check and confirm houses are in the file
    number_of_houses_confirmed = []

    # Changed to start at 2 due to the extra column added for task 2.
    for number_of_Houses in range(2, (len(data_of_houses[0]) - 1)):
        if not (data_of_houses[0][number_of_Houses] in number_of_houses_confirmed):
            number_of_houses_confirmed.append(data_of_houses[0][number_of_Houses])
            Number_of_Houses += 1

    # This will check and confirm the number of weeks are in the file
    for header in data_of_houses[1]:
        if "WEEK" in header:
            Number_of_weeks += 1


# This holds data about each store and the items they have in available

def dataofshoppinglist():
    global Number_of_weeks
    filepath = "DATA CWK SHOPPING DATA WEEK 4 FILE A.csv"
    shopping_data_list = readcsv(filepath)
    for item, Item_of_product in enumerate(
            shopping_data_list):  # Loop through each row in store and the item of product
        if item != 0:  # This will skip the row and create the item with the data from the shoppinglist data
            Items.append(Item(Item_of_product[1], Item_of_product[2]))
    for item, header in enumerate(shopping_data_list[0]):
        if "STORE" in header:
            items_stocked = []
            for i, Item_of_product in enumerate(shopping_data_list):
                if i != 0 and Item_of_product[item].lower() == "y":  # the item containing 'Y'
                    items_stocked.append(Items[i - 1])
            Stores.append(Store(header, items_stocked, Number_of_weeks))


#  This will get the data on each house and the Items they require
def getdataofhouses():
    global Number_of_weeks, Number_of_Houses
    filepath = "DATA CWK SHOPPING DATA WEEK 4 FILE B.csv"
    data_of_houses = readcsv(filepath)

    # Changed to start at 2 due to the extra column added for task 2.
    for house in range(2, (Number_of_Houses + 2)):
        house_number = data_of_houses[0][house]  # Gets house number
        required_item_for_house = [[] for x in range(Number_of_weeks)]
        for num in range(Number_of_weeks):  # This will loop for the number of weeks
            for i, Item_of_product in enumerate(data_of_houses):
                if i > 1:
                    if Item_of_product[house + (num * Number_of_Houses)] != "":
                        for itemProductOb in Items:
                            if itemProductOb.NameofItem == Item_of_product[0]:
                                required_item_for_house[num].append(
                                    [itemProductOb, int(Item_of_product[house + (num * Number_of_Houses)])])

        # house list
        Houses.append(House(house_number, required_item_for_house, Number_of_weeks))


# This will discover what is the best store to buy the most items which are required
# By getting the top number/most items in the list, this will show what the best shop from also getting its index.

def discoverbeststore(product_of_items):
    store_points = [0] * len(Stores)

    for item in product_of_items:
        for i, store in enumerate(Stores):
            listed = store.availableitemsinstock(item[0])  # This will loop through the stores
            if listed:
                store_points[i] += 1

    best_store = store_points.index(max(store_points))

    return best_store


# BuyingItemOfProducts to be added to the BoughtItem list, if not it will be on the MissedItems list

def buyingitemofproducts(products_of_items, storeindex, week):
    missed_items = []
    store = Stores[storeindex]

    for Item_of_product in products_of_items:
        listed = store.availableitemsinstock(
            Item_of_product[0])  # This checks if the available items are in stock in the store
        if listed:
            available_of_item = False
            for j, BoughtItem in enumerate(store.Itemsbought[week]):
                if Item_of_product[0] == BoughtItem[0]:
                    available_of_item = True
                    store.Itemsbought[week][j][1] += Item_of_product[1]  # Increment the quantity of the item

            if not available_of_item:
                store.Itemsbought[week].append(Item_of_product)

        else:

            missed_items.append(Item_of_product)

    return missed_items


# This will show the alternatives which deal with the constraints

def buyingalternatives(product_of_items, storeindex, week):
    store = Stores[storeindex]
    alternatives_missed = product_of_items

    for item in product_of_items:
        listed = store.availableitemsinstock(item[0])  # This checks if the available items are in stock in the store

        if listed:
            item_paid = False
            for i, BoughtItem in enumerate(store.Itemsbought[week]):
                if item[0] == BoughtItem[0]:
                    item_paid = True
                    store.Itemsbought[week][i][1] += item[1][1]

            if not item_paid:
                store.Itemsbought[week].append([item[0], item[1][1]])

            item_alternatives = False  # Look through if the item is already in the alternatives list
            for j, AlternativeItem in enumerate(store.alternatives[week]):
                if item[0] == AlternativeItem[0]:
                    item_alternatives = True
                    store.alternatives[week][j][1][1] += item[1][1]
            if not item_alternatives:
                store.alternatives[week].append(item)

            alternatives_missed.remove(item)

    return alternatives_missed


# This is to enable to buy the best alternative and the right item to substitute/alternate
# By having alternatives/substitutions, these are decided by which other item has the most similar words
# in its name and replace it.
# If there are no word matches we find the item with the most similar price.
# Once a Alternative has been found it is added to the AlternativeItems list
# along with the item that it will replace(missedItem).

def bestalternativesatstore(missed_product_of_items, storeindex):
    alternative_items = []
    best_alternative = ""

    store = Stores[storeindex]

    for Missed_product_of_item in missed_product_of_items:
        top_word_matches = 0
        for Product_of_items in store.StockItem:
            missed_product_name_list = Missed_product_of_item[0].NameofItem.split(" ")
            list_item_name = Product_of_items.NameofItem.split(" ")
            matched_word = list(set(missed_product_name_list) & set(list_item_name))
            if len(matched_word) > top_word_matches and Missed_product_of_item[0] != Product_of_items:
                top_word_matches = len(matched_word)
                best_alternative = Product_of_items

        # If no Alternatives found
        if top_word_matches == 0:
            smallest_price_difference = 99.99
            for Product_of_items in store.StockItem:
                # Difference of price - return the absolute value of missed product of item - product of items
                difference_of_price = abs(
                    float(Missed_product_of_item[0].Price[1:]) - float(Product_of_items.Price[1:]))
                if difference_of_price < smallest_price_difference:
                    smallest_price_difference = difference_of_price
                    best_alternative = Product_of_items

        alternative_items.append([best_alternative, Missed_product_of_item])

    return alternative_items


# This is the main shopping algorithm and there are a variety of rules to be followed

def shoppingalgo():
    global day_week_counter
    maximum_days_between_deliveries = 1
    last_possible_day = 3

    for n in range(Number_of_weeks):
        visit = 0
        stores_visited = []
        for house in Houses:
            count = 0
            day_week_counter = 0
            # This will get the items required for the current house and for the current week.
            items_required = house.ItemsRequired[n]
            store = discoverbeststore(items_required)
            if not (store in stores_visited):
                stores_visited.append(store)
                Stores[store].dayVisited = visit
                visit += 1

            Missed_items = buyingitemofproducts(items_required, store, n)

            # Loop until we are not missing any items
            while len(Missed_items) != 0:
                if (count < maximum_days_between_deliveries) and ((visit + 1) < last_possible_day):
                    store = discoverbeststore(Missed_items)
                    Missed_items = buyingitemofproducts(Missed_items, store, n)
                    # if we've shopped at a new store so increment the visit counter
                    if not (store in stores_visited):
                        stores_visited.append(store)
                        Stores[store].dayVisited = visit
                        visit += 1  # A visit count will be incremented when you shopped at the store.

                    count += 1
                else:  # If they can't visit all the stores, find the best alternatives for the items
                    Alternatives = bestalternativesatstore(Missed_items, store)
                    Missed_items = buyingalternatives(Alternatives, store, n)
                    if not (store in stores_visited):
                        Stores[store].dayVisited = visit
                    break

            # can now set its delivery visit
            house.DayofDelivery[n] = (visit - 1)

    # This will print out each item in each store

    print("Here is the Shopping Schedule: ")

    for w in range(Number_of_weeks):
        print("\n")
        print(f"For Week {w + 1}: ")
        for store in Stores:
            if len(store.Itemsbought[w]) != 0:
                print(f" \n The visit of the store you should visit is: {daynames()[day_week_counter]}")
                print("\n")
                print(f"{store.Tag}")
                for item in store.Itemsbought[w]:
                    print(f" {item[1]} X {item[0].Price} of {item[0].NameofItem}  ")

                for item in store.alternatives[w]:
                    print(
                        f"\n  Alternatives Made: {item[1][1]}  X {item[1][0].NameofItem}  can be exchanged to "
                        f" {item[1][1]} X {item[0].NameofItem}  ")
                day_week_counter += 1
        day_week_counter = 0

    # This will print out the delivery schedule
    print("\n")
    print("Here is the Delivery Schedule: ")
    for Num in range(Number_of_weeks):
        print("\n")
        print(f" For week {Num + 1}: ")
        print("\n")
        for c in range(7):
            print(f" {daynames()[day_week_counter]}  ")
            message = ""
            for house in Houses:
                if house.DayofDelivery[Num] == c:
                    message += f"{house.HouseNumber}, "

            if len(message) != 0:
                message = message[:-2]
                print(f"Item are ready to be delivered in: "
                      f"\n HOUSE NUMBERS: {message}")
                print("\n")
            else:
                print("No need to deliver today!")
                print("\n")

            day_week_counter += 1
        day_week_counter = 0


# This is calling all the functions
getnumberweeksandhouses()
dataofshoppinglist()
getdataofhouses()
shoppingalgo()
