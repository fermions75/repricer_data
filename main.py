import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import date, datetime

def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1rwdptDXi7VfUWEp-EDfHY_qzTjrscPCFsj2y6fVTFE4"
    sheet = client.open_by_key(sheet_id)
    return sheet

def get_pricing_data():
    url = "https://oakriver-backend-staging.herokuapp.com/api/repricer/get-pricing-data/"

    # Assuming you're sending a JSON payload
    data = {
        "asin_list": [
            "B0B4FB4G8N",
            "B0BR8D79QX",
            "B08R6DMVHH",
            "B0CLZH9RM4",
            "B098QMD9LV"
        ]
    }

    response = requests.get(url, json=data)

    # Print the status code and returned data
    # print("Status Code:", response.status_code)
    # print("Response:", response.json())
    response_dict = response.json()
    status_code = response.status_code
    return response_dict['result'], status_code

def add_event_id(price_data):
    for data in price_data:
        curr_date = date.today().strftime("%Y-%m-%d")
        curr_time = datetime.now().strftime("%H:%M:%S")
        data['curr_date'] = curr_date
        data['curr_time'] = curr_time
    return price_data


# Connect to the Google Sheet
sheet = connect_sheet()
worksheet = sheet.get_worksheet(0)
price_data, status_code = get_pricing_data()
price_data = add_event_id(price_data)

# # Write the values in the subsequent rows
# for index, row in enumerate(price_data, start=2):
#     worksheet.insert_row(list(row.values()), index)

# Prepare the data for the rows
rows = [list(row.values()) for row in price_data]

# Append all rows at once
worksheet.append_rows(rows)
    

print("Data has been written to the Google Sheet")