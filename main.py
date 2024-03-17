from datetime import date, datetime
import process
import requests
import os


def get_pricing_data():
    try:
        url = os.environ['URL']
    except KeyError as e:
        print("URL not found")
        url = "http://127.0.0.1:8000/api/repricer/get-pricing-data/"

    # url = "https://oakriver-backend-staging.herokuapp.com/api/repricer/get-pricing-data/"

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
    response_dict = response.json()
    status_code = response.status_code
    return response_dict['result'], status_code




def main():
    sheet = process.connect_sheet()
    worksheet = sheet.get_worksheet(0)

    last_50_rows = process.get_last_50_rows(worksheet)

    price_data, status_code = get_pricing_data()
    curr_bb_winner = process.get_bb_winner_curr(price_data)
    recent_data = process.fetch_recent_data(last_50_rows)
    prev_bb_winner = process.get_bb_winner_prev(recent_data)


    price_data = process.add_event_id(price_data, curr_bb_winner, prev_bb_winner)

    # # Prepare the data for the rows
    rows = [list(row.values()) for row in price_data]

    # Append all rows at once
    worksheet.append_rows(rows)
    process.save_row_number(len(rows))
    print("Data has been written to the Google Sheet")



def first():
    sheet = process.connect_sheet()
    worksheet = sheet.get_worksheet(0)

    price_data, status_code = get_pricing_data()
    for data in price_data:
        data['event_id'] = process.generate_event_id(data['fba_seller_id'], data['fba_date'], data['fba_time'])
    
    rows = [list(row.values()) for row in price_data]

    # Append all rows at once
    worksheet.append_rows(rows)
    process.save_row_number(len(rows))
    print("Data has been written to the Google Sheet")


if __name__ == "__main__":
    main()
