import customtkinter
import pandas as pd
from CTkListbox import *


#To Do:
#Change Shiny Vault data to correct set in csv
#Change state of card drop down to false until set is picked
#make Graded or Not Graded option
data= pd.read_csv("C:\\Users\\utbea\Desktop\\Python\\TCG Price Tracker\\TCG-Price\\cards.csv", usecols=['set', 'name', 'set_num'])
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('1280x720')
data.set_index('name', inplace=True)
buttons=customtkinter.CTkFrame(root, bg_color='red')
buttons.pack()
display=customtkinter.CTkFrame(root, bg_color='green',  )
display.pack()

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

select_set = customtkinter.CTkOptionMenu(buttons, values=set_names, command=set_select)
select_set.pack(pady=12, padx=10, side='left')
select_set.set('Select Set')

select_card = customtkinter.CTkOptionMenu(buttons, values=None, state='disabled', command=None )
select_card.pack(pady=12, padx=10, side='left')
select_card.set('Select Card')

card_grade= customtkinter.CTkCheckBox(buttons, text='Graded')
card_grade.pack(pady=12, padx=10, side='left')

search_button=customtkinter.CTkButton(buttons, text='Search', command=None)
search_button.pack(pady=12, padx=10, side='left')

search_listbox=CTkListbox(display)
search_listbox.pack(expand=True, pady=12, padx=10)


root.mainloop()

