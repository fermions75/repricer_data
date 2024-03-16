import requests

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
print("Status Code:", response.status_code)
print("Response:", response.json())