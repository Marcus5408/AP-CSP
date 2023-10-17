# stores prices of items. pound_of_bananas is the price per pound.
prices = {
    "apple": 0.60,
    "pineapple": 2.50,
    "pound_of_bananas": 0.35,
}

# customer data is stored in a dict
# purchases is a dict of items and their quantities
customer_data = {
    "name": "Stacey",
    "purchases": {
        "apple": 12,
        "pineapple": 2,
        "pound_of_bananas": 5,
    },
    "amount_tendered": 20.00,
}

# function can be reused for any customer as long as the customer
# doesn't buy anything that isn't in the prices dict
def print_receipt(customer):
    number_of_items = 0
    total_cost = 0

    # if it wasn't for the pound_of_bananas, this would be a two-liner :(
    for item, quantity in customer['purchases'].items():
        if item == 'pound_of_bananas':
            number_of_items += 1
        else:
            number_of_items += quantity
        
        total_cost += prices[item] * quantity

    average_cost_per_item = total_cost / number_of_items
    change = customer['amount_tendered'] - total_cost

    # the actual printing of the receipt
    print("-----------")
    print(f"Customer: {customer['name']}\n")
    print(f"Number of Items: {number_of_items}")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Average Cost Per Item: ${average_cost_per_item:.2f}\n")
    print(f"Amount Tendered: ${customer['amount_tendered']:.2f}")
    print(f"Change: ${change:.2f}")
    print("-----------")

print_receipt(customer_data)