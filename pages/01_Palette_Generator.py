import pandas as pd
import numpy as np
import requests

import matplotlib.pyplot as plt

import streamlit as st

st.set_page_config(page_title = 'Color Palette Generator')

########## DATASET ##########
csv_url = 'https://docs.google.com/spreadsheets/d/1QT7ovgrCVEFQul3fTylSqKwbwHDMgeGV_Zue8xtEVro/export?format=csv&id=1QT7ovgrCVEFQul3fTylSqKwbwHDMgeGV_Zue8xtEVro&gid=696560758'
#res = requests.get(csv_url)
#open('color_dataset.csv', 'wb').write(res.content)

df = pd.read_csv(csv_url)


########## DROPDOWN MENU ##########
st.title("Palette Generator")
st.markdown("---")
PRODUCT_CATEGORIES = ['Choose a category', 'Candy & Chocolate Bars', 'Composition Notebooks', 'Dried Mangoes', 
              'Garden Soil', 'Gouda Cheese', 'Ground Coffee', 'Herbal Tea',
             'Instant Coffee', 'Laundry Hampers', 'Mixed Nuts', 
             'Pendant Light Fixtures', 'Place Mats', 'Spirulina Herbal Supplements',
             'Sugars', "Women's Tote Handbags"]

this_product_category = st.selectbox('Category:', PRODUCT_CATEGORIES)

st.markdown('')

if this_product_category == 'Candy & Chocolate Bars':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Milk', 'Dark']
elif this_product_category == 'Composition Notebooks':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Kraft', 'Marble']
elif this_product_category == 'Dried Mangoes':
    SUBCATEGORIES = ['Choose a subcategory', 'General']
elif this_product_category == 'Garden Soil':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Peat Moss', 'Coco Coir']
elif this_product_category == 'Gouda Cheese':
    SUBCATEGORIES = ['Choose a subcategory', 'General']
elif this_product_category == 'Ground Coffee':
    SUBCATEGORIES = ['Choose a subcategory', 'Dark', 'Medium']
elif this_product_category == 'Herbal Tea':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Ginger', 'Hibiscus', 'Chamomile']
elif this_product_category == 'Instant Coffee':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Dark', 'Medium', 'Mushroom']
elif this_product_category == 'Laundry Hampers':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Fabric', 'Rattan']
elif this_product_category == 'Mixed Nuts':
    SUBCATEGORIES = ['Choose a subcategory', 'General']
elif this_product_category == 'Pendant Light Fixtures':
    SUBCATEGORIES = ['Choose a subcategory', 'General']
elif this_product_category == 'Place Mats':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Kraft', 'Marble']
elif this_product_category == 'Spirulina Herbal Supplements':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Blue', 'Green']
elif this_product_category == 'Sugars':
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Coconut', 'White', 'Brown']
elif this_product_category == "Women's Tote Handbags":
    SUBCATEGORIES = ['Choose a subcategory', 'General', 'Shoulder', 'Purse', 'Canvas']
else:
    SUBCATEGORIES = ['Choose a subcategory']

this_product_subcat = st.selectbox('Subcategory:', SUBCATEGORIES)


########## FUNCTIONS ##########
def hex2rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

def generate_colors(category, subcategory, df=df):
    
    filtered_df = df[(df['category']==category) & (df['subcategory']==subcategory)]

    color_tags = ['accent', 'secondary', 'primary']
    
    a = []
    df_ = []
    color_palette = []
    
    for tag in color_tags:
        
        a = filtered_df[filtered_df['tag']==tag]
        
        if len(a)<1:
            pass
        elif len(a)==1:
            df_.append(a.sample(n=1))
        else:
            df_.append(a.sample(n=2))

    color_palette = pd.concat(df_, ignore_index=True)  
    color_palette['RGB'] = color_palette.apply(lambda x: hex2rgb(x['hex']), axis=1)
    
    return color_palette

def print_hex(color_palette):
    
    hex_val = color_palette[['tag', 'hex']]
    
    arr = []
    for tag, color in hex_val.values:
        color_arr = '#'+color+' ('+tag+')'
        arr.append(color_arr)
        
        sentence = '; '.join(arr)
        
    return sentence

def show_palette(color_palette):
    
    fig = plt.figure(figsize=(20, 5))

    for i in range(len(color_palette['RGB'])):
        plt.subplot(1, 6, i+1)
        plt.imshow([[color_palette['RGB'][i]]])
        plt.title('#'+ str(color_palette['hex'][i]) + ' ' + '(' + color_palette['tag'][i] + ')', fontsize=14, y=-0.15)
        plt.tick_params(
        axis='both',         
        which='both',     
        left=False,     
        bottom=False,         
        labelleft=False,
        labelbottom=False)
        plt.axis('off')

    st.pyplot(fig)

########## GENERATE PALETTE ########## 
st.markdown("---")
if st.button("Generate color palette!"):
    if (this_product_category == 'Choose a category') | (this_product_subcat == 'Choose a subcategory'):
        st.write('')
        st.error('Please choose a **category** and a **subcategory** from the dropdowns.')
    
    else:
        st.subheader("Color Palette for %s (%s):" % (this_product_category, this_product_subcat))
        palette_ = generate_colors(this_product_category.lower(), this_product_subcat.lower())
        show_palette(palette_)

        st.write("Color Hex:")
        st.success(print_hex(palette_))
        
        