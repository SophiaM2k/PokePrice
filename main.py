import requests, json, collections
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from datetime import date, datetime, timedelta
from collections import defaultdict

keywords=input('Enter card name, set and number: ').replace(' ','+').replace('/', '%2F')
url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keywords}&_sacat=0&LH_TitleDesc=0&Graded=No&_dcat=183454&rt=nc&LH_Sold=1&LH_Complete=1'
print(url)


card_list = []
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    results = soup.find('div', {'class': 'srp-river-results clearfix'}).find_all('li',{'class':'s-item s-item__pl-on-bottom'}, limit=20)
    cards=dict()
   
    try:
        for item in results:
            cards.setdefault(item.find('div', {'class': 's-item__title'}).text, defaultdict(list))
            cards[item.find('div', {'class': 's-item__title'}).text]['price'].append(float(item.find('span', {'class':'s-item__price' }).text.replace('$', '').replace(',', '').strip()))
            cards[item.find('div', {'class': 's-item__title'}).text]['date'].append(item.find('span', {'class': 'POSITIVE'}).text)
            cards[item.find('div', {'class': 's-item__title'}).text]['sold_type'].append(item.find('span', {'class' : 's-item__purchase-options s-item__purchaseOptions'}))
            
    except (KeyError, ValueError):
        print('KeyError accepted!')
    return cards

    
        

def sort_cards(d_cards):
    words=['Metal', 'Fan', 'Gold', 'METAL']
    #print(f'BEFORE DELETION: {d_cards}')
    for k,v in list(d_cards.items()):
        for x in range(len(v['sold_type'])):
            try:
                if 'Best offer accepted' in v['sold_type'][x]: #Removes items sold by best offer
                    if len(v['sold_type']) <=1:
                        #print(k, v['sold_type'], 'Deleted!')
                        del d_cards[k]
                    if len(v['sold_type']) > 1:
                        #print(k, v['sold_type'], 'Deleted (multiple value)')
                        del d_cards[k]['sold_type'][x]
                        del d_cards[k]['price'][x]
                        del d_cards[k]['date'][x]

            except (TypeError, IndexError):
                ''
        for word in words:
            if word in k: #Removes fan made cards
                try:
                    del d_cards[k]
                except KeyError:
                    ''
        try:
            for x in range(len(v['date'])):
                today=date.today()
                sold_date = v['date'][x][6:]
                new_sold_date = datetime.strptime(sold_date, '%b %d, %Y').date()
                d = today - timedelta(days=7)

                if new_sold_date < d:
                    if len(v['date']) <=1:
                        #print(k, 'deleted')
                        del d_cards[k]
                    if len(v['date']) > 1:
                        #print(k, 'deleted')
                        del d_cards[k]['sold_type'][x]
                        del d_cards[k]['price'][x]
                        del d_cards[k]['date'][x]
        except (KeyError, IndexError):
                ''
                    

                
    return d_cards

average=0
def get_average(s_cards): #Calculates average price of card
    prices=list()
    for k,v in s_cards.items():
        for x in v['price']:
            prices.append(x)
    print(prices)
    return sum(prices)/len(prices)
  
soup = get_data(url)
card_results=parse(soup)
sorted_cards=sort_cards(card_results)
average_price=get_average(sorted_cards)
print(round(average_price, 2))
#print(f'Sorted Card Results: Keys: {sorted_cards.keys()}  Values: {sorted_cards.values()}')
#print(f'Average Sell Price: {average_price}')
#print(sorted_cards)
print(len(sorted_cards))
#print(len(parse(soup)))
#Make it so the card number needs to be in title
#Test Card: charizard gx hidden fates sv49/sv94
