import gspread
from google.oauth2.service_account import Credentials

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

    print("Please enter sales data")
    print("Data should be six number, separated by a comma")
    print("For example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here:")
    print(f"The data provided is: {data_str}")

    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises value error if integers cannot be converted,
    or if there are not exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"We are expecting 6 values instead of {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")




get_sales_data()
