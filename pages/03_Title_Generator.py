import numpy as np
import pandas as pd
import requests
import streamlit as st

import random

PRODUCT_CATEGORIES = ['Instant Coffee', 'Ground Coffee', 'Herbal Tea',
       'Dried Mangoes', 'Mixed Nuts', 'Gouda Cheese', 'Candy & Chocolate Bars', 'Sugars',
       'Spiraluna Herbal Supplements',\
        'Pendant Light Fixtures', 'Place Mats', 'Laundry Hampers',\
        'Garden Soil', 'Composition Notebooks', "Women's Tote Handbags"]


PRODUCT_CATEGORY_BRACKET1 = ['Instant Coffee', 'Ground Coffee', 'Herbal Tea', 'Sugars', 'Dried Mangoes', 'Candy & Chocolate Bars', 'Mixed Nuts']
PRODUCT_CATEGORY_BRACKET2 = ['Pendant Light Fixtures', 'Place Mats', 'Laundry Hampers', 'Garden Soil', 'Composition Notebooks', "Women's Tote Handbags"]

def get_packs_str(n_packs, category):
    counter =  ' Tea Bag' if 'Tea' in category else '' if 'Spirulina' in category else ' Pack'
    return str(n_packs)+ counter if n_packs == 1 else str(n_packs)+ counter +'s'

csv_url = "https://docs.google.com/spreadsheets/d/134_9QijNvcPinZLtJYuLOg_r_fQgZUF6vhEvLceUxLM/export?format=csv"
data_df = pd.read_csv(csv_url)

def get_generic_keyword(category):
    src_keywords = data_df[data_df['category']==category]['generic_keywords'].values[0].split(',')
    src_keywords = [s.strip() for s in src_keywords]
    return random.choice(src_keywords)

def get_popular_keyword(category):
    try:
        src_keywords = data_df[data_df['category']==category]['popular_keywords'].values[0].split(',')
        src_keywords = [s.strip() for s in src_keywords]
        return random.choice(src_keywords)
    except:
        return ''

def get_option_keywords(category):
    src_keywords = data_df[data_df['category']==category]['option_keywords'].values[0].split(',')
    src_keywords = [s.strip() for s in src_keywords]
    return src_keywords

####################################

st.title("Title Generator")
st.markdown("---")
product_category = ""
generated_title = ""

st.session_state.disable_get_organic  = False
st.session_state.disable_weight  = False
st.session_state.disable_num_packs = False

st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True) 

st.subheader('Generated title')
logtxtbox = st.empty()
logtxtbox.text_area("Output", generated_title , height = 100, label_visibility='collapsed')

st.write('Answer the following questions to generate the title.')

this_product_category = st.selectbox(
        "What is your product category?",
        PRODUCT_CATEGORIES
    )

this_product_brand_name = st.text_input(
    "What is your brand name? (case-sensitive)" , 'Brand name here')


# if this_product_category in PRODUCT_CATEGORY_BRACKET2:

#     st.session_state.disable_get_organic = True
#     st.session_state.disable_weight = True
#     st.session_state.disable_num_packs = True

#print(st.session_state.disable_get_organic)
this_product_bracket_text =''
if this_product_category in PRODUCT_CATEGORY_BRACKET1:
    this_product_coffee_roast_type = ''
    this_product_spirulina_form = ''

    this_product_weight = st.number_input(
        'What is the weight of your product?',\
        min_value = 0, disabled=st.session_state.disable_weight)

    this_product_weight_unit = st.selectbox(
        'What is the weight unit of your product?',\
        ['g','oz','kg','lb'])

    this_product_num_packs = st.number_input(
        'How many product units/packs do you want to include?',\
        min_value = 1, disabled=st.session_state.disable_num_packs)
    

    # product specific
    if 'Tea' in this_product_category:
        this_product_tea_flavor = st.text_input(       
            "What is the tea flavor?"
        )

    if 'Coffee' in this_product_category:
        this_product_coffee_roast_type = st.selectbox(       
            "What roast level are the coffee beans?",
            ['Light Roast','Medium Roast','Dark Roast']
        )

    if 'Spirulina' in this_product_category:
        print('Coffee detected')
        this_product_spirulina_form = st.selectbox(
            "Is your product in powder or tablet form?",
            ['Powder','Tablet'],
        this_product_spirulina_form = this_product_spirulina_form + 's' if this_product_spirulina_form =='tablet' else this_product_spirulina_form
        )

    this_product_bracket_text = ' '.join([str(this_product_weight),this_product_weight_unit,\
                                 get_packs_str(this_product_num_packs, this_product_category),\
                                 this_product_coffee_roast_type, this_product_spirulina_form]).strip()
    


this_product_option_keywords = st.multiselect(
    'Which of the following apply to your product? (choose all that apply)',\
    get_option_keywords(this_product_category)
    )

random.shuffle(this_product_option_keywords)

this_product_generic_keyword = get_generic_keyword(this_product_category)
this_product_popular_keyword = get_popular_keyword(this_product_category)

###### Generate title 
if st.button('Generate'):
    generated_title = " ".join([this_product_brand_name, this_product_generic_keyword ,\
                     this_product_bracket_text, this_product_popular_keyword])+" "+\
                        " ".join(this_product_option_keywords)

    logtxtbox.text_area("Generated title: ",generated_title , height = 100)

st.markdown("<a href='#linkto_top'>View result</a>", unsafe_allow_html=True)

#######################
# col1, col2 = st.columns(2)

# with col1:
#     st.checkbox("Disable selectbox widget", key="disabled")
#     st.radio(
#         "Set selectbox label visibility 👉",
#         key="visibility",
#         options=["visible", "hidden", "collapsed"],
#     )

# with col2:
#     option = st.selectbox(
#         "How would you like to be contacted?",
#         ("Email", "Home phone", "Mobile phone"),
#         label_visibility=st.session_state.visibility,
#         disabled=st.session_state.disabled,
#     )
