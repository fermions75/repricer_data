from datetime import date, datetime
import process
import requests
import os



def write_msg_to_file(msg):
    with open('logger.txt', 'a') as f:
        f.write('\n' + msg)


def main():
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
            "B098QMD9LV",
            "B00099E7AG",
            "B00099E79W",
            
        ],
        "last_row_number": process.get_last_row_number()
    }

    response = requests.get(url, json=data)
    response_dict = response.json()
    status_code = response.status_code
    msg = response_dict.get('message')
    if status_code != 200:
        print(f"Error: {msg}")
        write_msg_to_file(f"{datetime.now()} - Error: {msg}")
    else:
        print(f"Success: {msg}")
        write_msg_to_file(f"{datetime.now()} - Success: {msg}")
        row_number = response_dict.get('rows_written')
        process.save_row_number(row_number)
    



if __name__ == "__main__":
    main()