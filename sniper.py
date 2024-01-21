# ethfavcoin.xyz

try:
    import requests
    import browser_cookie3
    from browser_cookie3 import BrowserCookieError
    import time
except ModuleNotFoundError as e:
    module = str(e).split("'")[1]
    print(f'{module} not found. PLease install it using: pip install {module}')

def get_roblox_cookie(browser):
    match browser:
        case 1:
            try:
                cookies = browser_cookie3.chrome(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Chrome not installed')
        case 2:
            try:
                cookies = browser_cookie3.firefox(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('FireFox not installed')
        case 3:
            try:
                cookies = browser_cookie3.librewolf(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('LibreWolf not installed')
        case 4:
            try:
                cookies = browser_cookie3.opera(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Opera not installed')
        case 5:
            try:
                cookies = browser_cookie3.opera_gx(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Opera GX not installed')
        case 6:
            try:
                cookies = browser_cookie3.edge(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Edge not installed')
        case 7:
            try:
                cookies = browser_cookie3.chromium(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Chromium not installed')
        case 8:
            try:
                cookies = browser_cookie3.brave(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Brave not installed')
        case 9:
            try:
                cookies = browser_cookie3.vivaldi(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Vivaldi not installed')
        case 10:
            try:
                cookies = browser_cookie3.safari(domain_name='roblox.com')
            except BrowserCookieError:
                raise BrowserCookieError('Safari not installed')
        case default:
            raise ValueError('Please, enter a number between 1 and 10.')
    assert len(cookies) > 0, 'Couldnt find any cookies, be sure to be logged in roblox'
    for cookie in cookies:
        if cookie.name == '.ROBLOSECURITY':
            roblox_cookie = cookie.value.split('_')[2]
    return roblox_cookie

def get_x_token(cookie_code):
    global x_token
    x_token = requests.post("https://auth.roblox.com/v2/logout",
                         headers={'cookie': ".ROBLOSECURITY=" + cookie_code}).headers["x-csrf-token"]
    return x_token

def get_item_data(id, asset_type, cookie_code, x_token):
    url = 'https://catalog.roblox.com/v1/catalog/items/details'
    params = {"items": [{"itemType": asset_type,"id": id}]}
    header = {'X-CSRF-TOKEN': x_token}
    cookie = {'.ROBLOSECURITY': cookie_code}
    products = requests.post(url,json=params ,headers=header,cookies=cookie)
    return products

def buy_item(products, cookie_code, x_token):
    product_id = products['productId']
    price = products['price']
    seller_id = products['creatorTargetId']
    url_2 = f'https://economy.roblox.com/v1/purchases/products/{product_id}'
    headers = {'X-CSRF-TOKEN':x_token, 'Cookie':'.ROBLOSECURITY=' + cookie_code,'Content-Type':'application/json'}
    data = {'expectedCurrency':1,'expectedPrice':price,'expectedSellerId':seller_id}
    response = requests.post(url_2,headers=headers,json=data)
    return response

def main():
    with open('limiteds.txt', 'r') as file:
        limiteds = list(map(int,file.read().split(",")))


    browser = int(input(''' Enter your Browser (pay attention that Opera and Opera GX are different numbers):
    1 - Chrome,
    2 - Firefox,
    3 - LibreWolf,
    4 - Opera,
    5 - Opera GX,
    6 - Edge,
    7 - Chromium,
    8 - Brave,
    9 - Vivaldi,
    10 - Safari.
    '''))


    
    roblox_cookie = get_roblox_cookie(browser)
    x_token = get_x_token(roblox_cookie)
    for limited_id in limiteds:
        product_data = get_item_data(limited_id, 1, roblox_cookie, x_token)


        if product_data.status_code == 200 and product_data.json()['data']:
            response = buy_item(product_data.json()['data'][0], roblox_cookie, x_token)
        else:
            print(f'There was a problem accessing {limited_id} data.')
            print(f'Information: {product_data.reason}')


        if response.ok:
            print(f'Bought {limited_id}')
        else:
            print(f'There was an error buying the item {limited_id}. Information: {response.reason}')

main()
