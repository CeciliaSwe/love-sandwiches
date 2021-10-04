import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures from the user
    """
    while True:
        print("Please enter sales data")
        print("Data should be six number, separated by a comma")
        print("For example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
        print(f"The data provided is: {data_str}")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises value error if integers cannot be converted,
    or if there are not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"We are expecting 6 values instead of {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Recevie a list of integers, insert into worksheet
    Update worksheet with provided data
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")



def calculate_surplus_data(sales_row):
    """
    Compares sales with stock and returns positive values for left overs
    And negative values for extra was made fresh
    """
    print("Calculating surplus data...")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to love sandwiches Data Automation")
main()
