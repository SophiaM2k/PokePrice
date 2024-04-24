import customtkinter
import pandas as pd


#To Do:
#Change Shiny Vault data to correct set in csv
#TURN INTO WEB APP INSTEAD OF GUI APPLICATION :)
#Change state of card drop down to false until set is picked
#make Graded or Not Graded option
data= pd.read_csv("C:\\Users\\utbea\Desktop\\Python\\TCG Price Tracker\\TCG-Price\\cards.csv", usecols=['set', 'name', 'set_num'])
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('1280x720')
data.set_index('name', inplace=True)

def set_select(self):
    #print(data[(data['set'] == self)])
    card_names=data[(data['set'] == self)].loc[:, 'set_num' ].to_dict()
    sorted_card_names=[]
    for k,v in card_names.items():
        card= ' '.join([k,v])
        sorted_card_names.append(card)
    sorted_card_names.sort()
    select_card.configure(values=sorted_card_names)
    
    #TURN ROW DATA INTO LIST VALUE EX: [pokemon setnum, pokemon2 setum2, etc.]

set_names=data['set'].tolist()
set_names=list(set(set_names))
set_names.sort()

select_set = customtkinter.CTkOptionMenu(master=root, values=set_names, command=set_select)
select_set.pack(pady=12, padx=10)
select_set.set('Select Set')

select_card = customtkinter.CTkOptionMenu(master=root, values=None, command=None )
select_card.pack(pady=12, padx=10)
select_card.set('Select Card')



root.mainloop()

