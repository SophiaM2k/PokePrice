import requests, collections
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from collections import defaultdict
import customtkinter
import pandas as pd
from CTkListbox import *
from PIL import Image
from urllib.request import urlopen
from io import BytesIO
import webbrowser
#To Do:
#Change Shiny Vault data to correct set in csv
#allow user to remove certain listings from average calculation
#show last sold for price instead of just average
#make it so card number is  in this format (11/13) instead of just 11

data= pd.read_csv("C:\\Users\\utbea\Desktop\\Python\\TCG Price Tracker\\TCG-Price\\cards.csv", usecols=['set', 'name', 'set_num'])
#customtkinter.set_appearance_mode('dark')
#customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('1280x720')
data.set_index('name', inplace=True)
buttons=customtkinter.CTkFrame(root, bg_color='red')
buttons.pack()
display=customtkinter.CTkFrame(root, bg_color='green' )
display.pack()

def callback(link):
    webbrowser.open_new(link)
def set_select(self):
    card_names=data[(data['set'] == self)].loc[:, 'set_num' ].to_dict()
    sorted_card_names=[]
    for k,v in card_names.items():
        card= ' '.join([k,v])
        sorted_card_names.append(card)
    sorted_card_names.sort()
    select_card.configure(values=sorted_card_names, state='normal')
    
    
set_names=data['set'].tolist()
set_names=list(set(set_names))
set_names.sort()


def keyword():
    keywords=f'{select_set.get()} {select_card.get()}'.replace(' ','+').replace('/', '%2F')
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keywords}&_sacat=0&LH_TitleDesc=0&Graded={check()}&_dcat=183454&rt=nc&LH_Sold=1&LH_Complete=1'
    return url



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
            images=item.find('div', {'class': 's-item__image'}).find_all('img')
            for image in images:
                cards[item.find('div', {'class': 's-item__title'}).text]['images'].append(image['src'])
            
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
                d = today - timedelta(days=14)

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

def search():
    url = keyword()
    print(url)
    soup = get_data(url)
    #print(parse(soup))
    card_results=parse(soup)
    sorted_cards=sort_cards(card_results)
    average_price=get_average(sorted_cards)
    load_list(sorted_cards)
    
def load_list(sc):
    search_listbox.delete('0', 'end')
    for k,v in sc.items():
        for img in sc[k]['images']:
            image_url=img
        i_url = urlopen(image_url)
        raw_data=i_url.read()
        i_url.close()
        im=Image.open(BytesIO(raw_data))

        card_image=customtkinter.CTkImage(dark_image=im, size=(100,100))
        card_label=customtkinter.CTkLabel(display, text='', image=card_image)
        search_listbox.insert('END', f'{k} Date Sold {v["date"]} Price: {v["price"]}', image=card_image)


    

#card_label.pack(pady=10)

select_set = customtkinter.CTkOptionMenu(buttons, values=set_names, command=set_select)
select_set.pack(pady=12, padx=10, side='left')
select_set.set('Select Set')

select_card = customtkinter.CTkOptionMenu(buttons, values=None, state='disabled', command=None )
select_card.pack(pady=12, padx=10, side='left')
select_card.set('Select Card')

check_var = customtkinter.StringVar(value='off')
card_grade= customtkinter.CTkCheckBox(buttons, text='Graded', variable=check_var, onvalue='on', offvalue='off')
card_grade.pack(pady=12, padx=10, side='left')

def check():
    grade = ''
    if card_grade.get() == 'on':
        grade = 'Yes'
    else:
        grade = 'No'
    return grade

search_button=customtkinter.CTkButton(buttons, text='Search', command=search) #get_average(sorted_cards)
search_button.pack(pady=12, padx=10, side='left')

search_listbox=CTkListbox(display, width=1280, height=720)
search_listbox.pack(fill='both',expand=True, pady=12, padx=10)
search_listbox.configure(font=('Helvetica', 15))

root.mainloop()
#print(f'Average Sell Price: {round(average_price, 2)}')
#print(f'Sorted Card Results: Keys: {sorted_cards.keys()}  Values: {sorted_cards.values()}')
#print(f'Average Sell Price: {average_price}')
#print(sorted_cards)
#print(len(sorted_cards))
#print(len(parse(soup)))
#Test Card: charizard gx hidden fates sv49/sv94
