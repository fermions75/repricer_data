import os



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





# def get_last_50_rows(worksheet):
#     last_row = get_last_row_number()
#     start_row = max(last_row - 50 + 1, 2)  # 2 is the first row after the headers
#     # Fetch the last 50 rows
#     range_str = f"A{start_row}:L{last_row}"  
#     last_50_rows = worksheet.get(range_str)
#     return last_50_rows



# def generate_event_id(seller_id, date_str, time_str):
#     return f"{seller_id}_{date_str}_{time_str}"



# def add_event_id(price_data, curr_bb_winner, prev_bb_winner):
#     for data in price_data:
#         asin = data['ASIN']
#         bb_winner_now = curr_bb_winner.get(asin)
#         bb_winner_prev = prev_bb_winner.get(asin).get('seller_id')
#         event_id_prev = prev_bb_winner.get(asin).get('event_id')
#         date_str = data['fba_date']
#         time_str = data['fba_time']
#         if bb_winner_now == bb_winner_prev:
#             data['event_id'] = event_id_prev
#         else:
#             data['event_id'] = generate_event_id(bb_winner_now, date_str, time_str)
#     return price_data




# def get_bb_winner_curr(pricing_data):
#     bb_data = {}
#     asin_list = []
#     for data in pricing_data:
#         seller_id = data['fba_seller_id']
#         is_bb_winner = data['fba_is_buybox_winner']
#         asin = data['ASIN']
#         asin_list.append(asin)
#         if is_bb_winner:
#             bb_data[asin] = seller_id
#     for asin in asin_list:
#         if asin not in bb_data:
#             bb_data[asin] = None

#     # print("this is bb data curr ----> ", bb_data)
#     return bb_data




# def get_bb_winner_prev(recent_data):
#     bb_data = {}
#     for key, value in recent_data.items():
#         asin = key
#         asin_data = value
#         found_bb_winner = False
#         for data in asin_data:
#             seller_id = data[5]
#             event_id = data[0]
#             is_bb_winner = data[11]
#             if is_bb_winner == 'TRUE':
#                 bb_data[asin] = {
#                     "seller_id": seller_id,
#                     "event_id": event_id
#                 }
#                 found_bb_winner = True
#                 break
#         if not found_bb_winner:
#             # print("bb not found for asin -------> ", asin)
#             bb_data[asin] = {
#                 "seller_id": None,
#                 "event_id": None
#             }
#     # print("this is bb data prev ----> ", bb_data)
#     return bb_data
        