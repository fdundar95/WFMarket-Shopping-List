# WFMarket-Shopping-List
This script is a tool for checking the prices of items in Warframe. It uses the Warframe Market API to retrieve pricing information, and allows the user to copy a message to their clipboard to contact the seller directly on Warframe.

## Installation
1. Clone the repository or download the script.
2. Install the required modules by running pip install -r requirements.txt in your terminal.

## Usage

1. Add the items you want to check, one per line, to shopping_list.txt.
- If an item has different ranks, you can specify the rank by adding the rank number at the end of the item name (e.g., "Vitality 10").
![Untitled](https://user-images.githubusercontent.com/79167732/225706024-3ba71c06-6516-42cd-912c-31acdba100f1.png)

2. Run the script.

3. The script will check each item in shopping_list.txt and output the lowest price and seller. If the lowest price is less than or equal to the weighted average, a message will be copied to your clipboard that you can use to contact the seller on Warframe.

4. Paste the message in Warframe chat to contact the seller and purchase the item.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
