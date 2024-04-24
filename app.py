from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField

data= pd.read_csv("C:\\Users\\utbea\Desktop\\Python\\TCG Price Tracker\\TCG-Price\\cards.csv", usecols=['set', 'name', 'set_num'])
app = Flask(__name__)
app.config['SECRET_KEY']='urmom'

set_names=data['set'].tolist()
set_names=list(set(set_names))
set_names.sort()

class CardForm(FlaskForm):
    set_list=SelectField(choices=set_names)
    card=SelectField(choices='')

@app.route('/', methods=['POST', 'GET'])
def index():
    form=CardForm()
    return render_template('index.html', form=form)


@app.route('/get_names', methods=['POST', 'GET'])
def get_names():
    set_id=request.args.get('set_list')
    card_names=data[(data['set'] == set_id)].loc[:, 'set_num' ].to_dict()
    sorted_card_names=[]
    for k,v in card_names.items():
        card= ' '.join([k,v])
        sorted_card_names.append(card)
    sorted_card_names.sort()
    return render_template('card_options.html', sorted_card_names=sorted_card_names)



if __name__ == '__main__':
    app.run(debug=True)