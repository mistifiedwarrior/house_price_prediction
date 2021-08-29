import re
from re import match

from core import get_training_data, predict_price, train_model

def print_separator():
    print("----------------------------------------------------")

def get_user_option():
    print_separator()
    print("Enter 'P' to Predict Price\nEnter 'H' to help\nEnter 'Q' to Quit")
    option = input("Enter Option: ").strip().upper()
    if option != 'Q' and option != 'H' and option != 'P':
        print("Invalid Option, Please enter a valid option")
        return get_user_option()
    print_separator()
    return option

def print_help():
    print("""___HELP DOCUMENTATION___""")

def print_possible_locations(possible_locations):
    print_separator()
    for index in range(0, len(possible_locations)):
        print(f"{index + 1}. => {possible_locations[index]}")
    print_separator()

def get_location(locations):
    print_separator()
    location = input("Enter Location: ").strip()
    possible_locations = list(filter(lambda v: match(f".*{location}.*", v, flags=re.I), locations))
    if len(possible_locations) == 0:
        print("No location found, Try again!!")
        return get_location(locations)
    return select_location_number(locations, possible_locations)

def select_location_number(X, possible_locations):
    print_possible_locations(possible_locations)
    location_index = int(input("Select location (-1 to enter location again): "))
    if location_index == -1:
        return get_location(X)
    if 1 <= location_index <= len(possible_locations):
        return possible_locations[location_index - 1]
    print("Invalid Location number, Select location again")
    return select_location_number(X, possible_locations)

def get_bhk():
    print_separator()
    bhk = int(input("Enter size (in BHK) [Valid size: 1 - 50]: "))
    if 0 < bhk <= 50:
        return bhk
    print("Invalid Bhk, Please enter a valid bhk")
    return get_bhk()

def get_total_sqft(bhk):
    print_separator()
    area = int(input(f"Enter area (in sqft) [valid area: {bhk * 300}-{bhk * 600}]: "))
    if (bhk * 300) <= area <= (bhk * 600):
        return area
    print("Invalid Area, Please enter a valid area")
    return get_total_sqft(bhk)

def get_bath(bhk):
    print_separator()
    bath = int(input(f"Enter Bath [valid range: 1-{bhk}]: "))
    if 0 <= bath <= bhk:
        return bath
    print("Invalid Bath, Please enter a valid bath")
    return get_bath(bhk)

def loop(X, regression):
    while True:
        print_separator()
        option = get_user_option()
        if option == 'H':
            print_help()
        if option == 'Q':
            return
        if option == 'P':
            location = get_location(list(X.columns[3:]))
            print(f"Selected Location: {location}")
            bhk = get_bhk()
            total_sqft = get_total_sqft(bhk)
            bath = get_bath(bhk)
            price = predict_price(regression, X, location, bhk, total_sqft, bath)
            print()
            print_separator()
            print("-                      ANSWER                      -")
            print_separator()
            print(f"""You selected\nLocation: {location}, {bhk} BHK, {total_sqft} sqft, {bath} bath""")
            print(f"Predicted Price: {'{:.2f}'.format(price)} (in Lakhs)")
            print_separator()
            print()

if __name__ == '__main__':
    print("Training Model ...")
    X, Y = get_training_data()
    regression = train_model(X, Y)
    print("Training Completed")
    loop(X, regression)
