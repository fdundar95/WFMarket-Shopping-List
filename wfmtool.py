import requests
import json
import pyperclip
import os

class WFMTool:
    def __init__(self):
        self.api_url = "https://api.warframe.market/v1/items/"
        self.item_link = "https://warframe.market/items/"
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.shopping_list = os.path.join(self.dir_path, "shopping_list.txt")

    def priceChecker(self):
        # Open the shopping list file and loop through its items
        with open (self.shopping_list, "r", encoding="UTF-8") as file:
            for item in file.readlines(): 
                # Removing numeric characters, converting spaces to underscores and lowercasing the item name to create the correct item URL
                item_url = ''.join(c for c in item if not c.isnumeric()).replace(" ","_").lower().strip().rstrip("_")
                # Getting the orders and statistics for the current item
                orders_response = requests.get(self.api_url +  item_url + "/orders").text
                orders = json.loads(orders_response)
                statistics_response = requests.get(self.api_url +  item_url + "/statistics").text
                statistics = json.loads(statistics_response)

                # Initializing a dictionary to store online sellers for the current item
                online_sellers = {}

                # Checking if the item has a rank
                if True in [char.isdigit() for char in item]:
                    # Extracting the mod rank from the item name
                    mod_rank = int(''.join(c for c in item if c.isnumeric()).strip())
                    ranked_mod_list = []
                    # Looping through the orders for the current item and adding the online sellers to the online_sellers dictionary
                    for listing in orders['payload']['orders']:
                        if (listing['order_type'] == 'sell' and listing['user']['status'] == 'ingame') and (listing['mod_rank'] == mod_rank):
                            online_sellers[listing['user']['ingame_name']] = listing['platinum']  
                    # Looping through the statistics for the current item and adding the stats for the current mod rank to the ranked_mod_list 
                    for i in statistics['payload']['statistics_closed']['48hours']:
                        if i['mod_rank'] == mod_rank:
                            ranked_mod_list.append(i)
                    # Looping through the statistics for the current item and adding the stats for the current mod rank to the ranked_mod_list 
                    avg = ranked_mod_list[-1]['wa_price']
                    median = ranked_mod_list[-1]['median']            
                else:
                    # Looping through the orders for the current item and adding the online sellers to the online_sellers dictionary
                    for listing in orders['payload']['orders']:
                        if listing['order_type'] == 'sell' and listing['user']['status'] == 'ingame':
                            online_sellers[listing['user']['ingame_name']] = listing['platinum'] 
                            # Getting the average and median prices for the current item
                            avg = statistics['payload']['statistics_closed']['48hours'][-1]['wa_price']
                            median = statistics['payload']['statistics_closed']['48hours'][-1]['median']

                # Sorting the online sellers by price
                sort_sellers = sorted(online_sellers.items(), key=lambda x: x[1])
                seller = sort_sellers[0][0]
                lowest = sort_sellers[0][1]  

                # Creating the item link for the current item
                link = self.item_link + item_url

                # Checking if the lowest price is below the weighted average and median prices
                if lowest <= (avg) and (median):
                    # If the condition is True, it prints the details of the item, seller, and prices and copies the order message to the clipboard.
                    print(f"✔️ Item:{item.title().rstrip()} - Seller:{seller} - Price:{lowest} - Weighted Average:{avg}\n{link}\n")                
                    if "set".title() not in item.title():
                        pyperclip.copy(f"/w {seller} Hi! I want to buy: [{''.join(c for c in item if not c.isdigit()).title().rstrip()}] for {lowest} platinum. (warframe.market)")
                    else:
                        pyperclip.copy(f"/w {seller} Hi! I want to buy: {''.join(c for c in item if not c.isdigit()).title().rstrip()} for {lowest} platinum. (warframe.market)")
                else:
                    # If the condition is False, it prints the details of the item, seller, and prices without copying the message to the clipboard.
                    print(f"❌ Item:{item.title().rstrip()} - Seller:{seller} - Price:{lowest} - Weighted Average:{avg}\n{link}\n")
        
        print("Last eligible listing copied.\n")
        input("Press Enter to Exit...")

wfmtool = WFMTool()
wfmtool.priceChecker()