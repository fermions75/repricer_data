import requests
import gspread
from google.oauth2.service_account import Credentials
import os

def fetch_recent_data(pricing_data):
    data_map = {}
    for data in reversed(pricing_data):
        asin = data[1]
        if asin in data_map:
            data_map[asin].append(data)
        else:
            data_map[asin] = []
            data_map[asin].append(data)
        
        if len(data_map) == 5:
            break
    return data_map



def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    
    try:
        is_local = os.environ['IS_LOCAL']
        is_local = True
    except KeyError as e:
        print("in local server")
        is_local = False

    if is_local:
        credentials_info = {
            "type": os.environ['TYPE'],
            "project_id": os.environ['PROJECT_ID'],
            "private_key_id": os.environ['PRIVATE_KEY_ID'],
            "private_key": os.environ['PRIVATE_KEY'].replace('\\n', '\n'),
            "client_email": os.environ['CLIENT_EMAIL'],
            "client_id": os.environ['CLIENT_ID'],
            "auth_uri": os.environ['AUTH_URI'],
            "token_uri": os.environ['TOKEN_URI'],
            "auth_provider_x509_cert_url": os.environ['AUTH_PROVIDER_X509_CERT_URL'],
            "client_x509_cert_url": os.environ['CLIENT_X509_CERT_URL']
        }
        creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    else:
        print("I am in local server!")
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)

    client = gspread.authorize(creds)
    sheet_id = "1rwdptDXi7VfUWEp-EDfHY_qzTjrscPCFsj2y6fVTFE4"
    sheet = client.open_by_key(sheet_id)
    return sheet


def process_existing_data(pricing_data):
    data_map = fetch_recent_data(pricing_data)
    print(data_map)
    print("len is ", len(data_map))




def save_row_number(row_number):
    with open('rows.txt', 'r') as f:
        last_row = int(f.read())
    
    row_number += last_row

    with open("rows.txt", "w") as file:
        file.write(str(row_number))


def get_last_row_number():
    with open('rows.txt', 'r') as f:
        last_row = int(f.read())
    return last_row





def get_last_50_rows(worksheet):
    last_row = get_last_row_number()
    start_row = max(last_row - 50 + 1, 2)  # 2 is the first row after the headers
    # Fetch the last 50 rows
    range_str = f"A{start_row}:L{last_row}"  
    last_50_rows = worksheet.get(range_str)
    return last_50_rows



def generate_event_id(seller_id, date_str, time_str):
    return f"{seller_id}_{date_str}_{time_str}"



def add_event_id(price_data, curr_bb_winner, prev_bb_winner):
    for data in price_data:
        asin = data['ASIN']
        bb_winner_now = curr_bb_winner.get(asin)
        bb_winner_prev = prev_bb_winner.get(asin).get('seller_id')
        event_id_prev = prev_bb_winner.get(asin).get('event_id')
        date_str = data['fba_date']
        time_str = data['fba_time']
        if bb_winner_now == bb_winner_prev:
            data['event_id'] = event_id_prev
        else:
            data['event_id'] = generate_event_id(bb_winner_now, date_str, time_str)
    return price_data




def get_bb_winner_curr(pricing_data):
    bb_data = {}
    for data in pricing_data:
        seller_id = data['fba_seller_id']
        is_bb_winner = data['fba_is_buybox_winner']
        asin = data['ASIN']
        if is_bb_winner:
            bb_data[asin] = seller_id
    return bb_data




def get_bb_winner_prev(recent_data):
    bb_data = {}
    for key, value in recent_data.items():
        asin = key
        asin_data = value
        for data in asin_data:
            seller_id = data[5]
            event_id = data[0]
            is_bb_winner = data[11]
            if is_bb_winner == 'TRUE':
                bb_data[asin] = {
                    "seller_id": seller_id,
                    "event_id": event_id
                }
                break
    return bb_data
        