


# def get_area_square_footage(link):
    

# import requests
# from bs4 import BeautifulSoup

# def get_class_data(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
    
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     elements = soup.find_all(class_="_3vyydJK3KMwn7-s2BEXJAf")
    
#     return [el.get_text(strip=True) for el in elements]



# url = "https://www.rightmove.co.uk/properties/167743766#/?channel=RES_BUY"
# print(get_class_data(url))


import requests
from bs4 import BeautifulSoup

def get_area_footage_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    element = soup.find(class_="_3vyydJK3KMwn7-s2BEXJAf")
    
    return element.get_text(strip=True) if element else None


# url = "https://www.rightmove.co.uk/properties/167743766#/?channel=RES_BUY"
# print(get_area_footage_data(url))