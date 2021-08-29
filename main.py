from core import get_training_data, predict_price, train_model

def print_separator():
    print("-------------------------")

def get_user_option():
    print("Enter 'P' to Predict Price\nEnter 'H' to help\nEnter 'Q' to Quit")
    option = input("Enter Option: ").strip()
    if option != 'Q' and option != 'H' and option != 'P':
        print("Invalid Option, Please enter a valid option")
        return get_user_option()
    print_separator()
    return option

def print_help():
    print("""___HELP DOCUMENTATION___""")

def loop(X, regression):
    while True:
        print_separator()
        option = get_user_option()
        if option == 'H':
            print_help()
        if option == 'Q':
            return
        if option == 'P':
            price = predict_price(regression, X, "Koramangala", 2, 1000, 1)
            print(price)

def main():
    print("Training Model ...")
    X, Y = get_training_data()
    regression = train_model(X, Y)
    print("Training Completed")
    loop(X, regression)

main()
