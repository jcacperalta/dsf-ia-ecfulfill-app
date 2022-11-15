#import libraries
import streamlit as st
import numpy as np
import pandas as pd
import re

from fuzzywuzzy import fuzz

#title
st.title("Description Recommender")
st.markdown("---")
#load dataset from GSheet
csv_url1 = 'https://docs.google.com/spreadsheets/d/1bVFT4xXYUoa5WYxxMfhoTcfcwE3k3---_uKqHIKeZVQ/export?format=csv&id=1bVFT4xXYUoa5WYxxMfhoTcfcwE3k3---_uKqHIKeZVQ&gid=1404104541'
csv_url2 = 'https://docs.google.com/spreadsheets/d/16uXyAlWvroi6TyaG_MhpSFoZAUM1N3zDbG_Nei-SZjg/export?format=csv&id=16uXyAlWvroi6TyaG_MhpSFoZAUM1N3zDbG_Nei-SZjg&gid=1860382666'

df = pd.read_csv(csv_url1)
df_words = pd.read_csv(csv_url2)

# string to array
def str_to_arr(text):
    '''Input: string. Output: array of sentences split based on a given pattern'''
    pattern = '\|remove'
    return re.split(pattern, text)

# array to string
def arr_to_str(text_array):
    '''Input: array. Output: string containing combined elements of array'''
    return " ".join([w for w in text_array])

# remove blanks and nan
def clean_desc(array):
    '''Input: array. Output: array without blanks or nan values and with lower cased text'''
    desc_arr = []
    for text in array:
        if (text == "") | (text == 'nan'):
            pass
        else:
            desc_arr.append(text.lower())
    return desc_arr

# assign levels by page_num (top:1-3 others:4--)
def get_level(page):
    '''Input: number. Output: assigned level based on the product page number in query search'''
    if page < 4:
        return 'top'
    else:
        return 'others'

# apply functions
df['level'] = df.apply(lambda x: get_level(x['page_num']), axis=1)
df['description'] = df.apply((lambda x: str_to_arr(str(x['desc_text']))), axis = 1)
df['desc_arr_'] = df.apply((lambda x: clean_desc(x['description'])), axis = 1)
df['desc_text_'] = df.apply((lambda x: arr_to_str(x['desc_arr_'])), axis = 1)

# get relevant data from dataframe and drop duplicates
df = df[df['desc_text_'] != ''].drop(['title', 'description', 'desc_text','rating', 'rating_num', 'rank', 'video', 'image_count',\
                                      'image'],axis=1)
df = df.drop_duplicates(['desc_text_']).reset_index(drop=True)

def fuzzy_ratio(word, keyword):
    '''Input: 2 words to be compared. Output: similarity score of these words from fuzzywuzzy'''
    return fuzz.ratio(word, keyword)

def fuzzy_search(keyword):
    '''Input: keywords. Output: Most similar words to keywords based on word database'''
    words = re.split(' ', keyword)
    words_clean = [w for w in words if len(w) > 1]
    
    keywords = []
    for word in words_clean:
        df_words['ratio'] = df_words.apply((lambda x: fuzzy_ratio(x['words'], word)), axis=1)
        closest_word = df_words.sort_values(by=['ratio'], ascending=False)['words'].iloc[0]
        keywords.append(closest_word)
    return keywords

def desc_clean(category, keyword):
    '''Input: category and keywords. Output: array of phrases based on the chosen category and keywords'''
    # find closest words to keywords from database
    words = fuzzy_search(keyword)
    
    # get data of specific category and make these a list
    df_cat = df[(df['category']==category)]
    descriptions = df_cat.desc_arr_.tolist()
    
    key_bullets = []
    for sentences in descriptions:
        for sent in sentences:
            for word in words:    # check if word in sentence
                if (word in sent) & (sent not in key_bullets):
                    key_bullets.append(sent)
                else:
                    pass
            
    clean_phrases = []
    for bullet in key_bullets:
        # split bullet points into phrases
        phrases = re.split('[\,\.\;\!\?]', bullet)
        
        for phrase in phrases:
            phrase = re.sub('-', ' ', phrase)
            phrase = re.sub('[0-9]', '*', phrase)
            
            # remove initial blank space from phrases
            if (phrase == ""):
                continue
            elif phrase[0] == " ":
                phrase = phrase[1:]
                clean_phrases.append(phrase)
            else:
                clean_phrases.append(phrase)
    return clean_phrases, words

def randomize_index_array(n):
    '''Input: n number of values. Output: array of randomly sorted numbers from 0 to n'''
    array = np.random.rand(1,n).argsort(axis=-1)
    return array[0]

def desc_kw(category, keyword, n):
    '''Input: category, keywords, and n number of phrases. 
        Outputs: 1. if input n is larger than the available phrases, returns all values
                 2. if there are no available phrases, returns an empty array
                 3. else returns an array of n number of random phrases
                    '''
    category = category.lower().strip()
    keyword = keyword.lower().strip()
    phrases, words = desc_clean(category, keyword)
    k = len(words)
    word_num_min = 5
    
    key_phrases = []
    
    # if both words in keywords are in the phrase, append phrase
    for phrase in phrases:
        checker = []
        for word in words:
            if word in phrase:
                checker.append(True)
            else:
                checker.append(False)
        if False in checker:
            pass
        else:
            word_num = len(re.split('[\ ]', phrase))
            if (phrase not in key_phrases)&(word_num >= word_num_min): # get unique phrases with specific word count
                key_phrases.append(phrase)
            else:
                pass
    
    # sort values alphabetically
    df_desc = pd.DataFrame({'key_desc':key_phrases})
    key_phrases = df_desc.sort_values(['key_desc'], ascending=True)['key_desc'].tolist()
    
    if (n == 'all')|(n >= len(key_phrases)):
        return key_phrases
    elif len(key_phrases) == n:
        return []
    else:
        random_ind = randomize_index_array(len(key_phrases))
        random_phrases = []
        for i in range(0, n):
            rand_phrase = key_phrases[random_ind[i]]
            random_phrases.append(rand_phrase)
        return random_phrases

PRODUCT_CATEGORIES = ['', 'Instant Coffee', 'Ground Coffee', 'Herbal Tea',\
                      'Dried Mangoes', 'Mixed Nuts', 'Gouda Cheese', 'Candy & Chocolate Bars', 'Sugars',\
                      'Spirulina Herbal Supplements','Pendant Light Fixtures', 'Place Mats', 'Laundry Hampers',\
                      'Garden Soil', 'Composition Notebooks', "Women's Tote Handbags"]

category = st.selectbox(
        "What is your category?",
        PRODUCT_CATEGORIES
    )

KEYWORDS_PER_CATEGORY = {'':[],\
                         'Instant Coffee':['add hot water', 'premium', 'quality', 'organic'], \
                         'Ground Coffee':['dark roast', 'medium roast', 'premium'], \
                         'Herbal Tea':['sweet', 'caffeine free', 'organic', 'gluten free'],\
                         'Dried Mangoes':['snack', 'organic', 'natural'],\
                         'Mixed Nuts':['sea salt', 'non gmo'],\
                         'Gouda Cheese':['insulated package', 'package ensure freshness'],\
                         'Candy & Chocolate Bars':['milk chocolate', 'dark chocolate', 'perfect anytime'],\
                         'Sugars':['non gmo', 'gluten free', 'organic', 'gmo project verified'],\
                         'Spirulina Herbal Supplements':['non gmo', 'certified organic', 'gluten free', 'essential amino acids'],\
                         'Pendant Light Fixtures':['high quality', 'easy install'],\
                         'Place Mats':['protect table', 'daily use', 'non slip', 'easy clean', 'high quality'],\
                         'Laundry Hampers':['high quality', 'large capacity', 'dirty clothes'],\
                         'Garden Soil':['plant food', 'easy use', 'high quality', 'root growth'],\
                         'Composition Notebooks':['wide ruled', 'sewn binding', 'ruled sheets'],\
                         "Women's Tote Handbags":['tote bag', 'zipper pockets', 'snap closure']}

if category != '':
    suggested_keywords = ", ".join([w for w in KEYWORDS_PER_CATEGORY[category]])
    st.write('Suggested Keywords: ', suggested_keywords)    
    
    keywords = st.text_input("Word Search: ")
    search_words = ", ".join([w for w in fuzzy_search(keywords)])

    n = st.number_input('Number of Phrases: ', step=1) # number of phrases
    phrases = desc_kw(str(category), str(keywords), n)
    if st.button("Search"):
        
        if (keywords == '')|(category == '')|(n == 0):
            st.write('')
            st.error('Please choose a **category**, input **keywords**, and number of phrases')
        else:            
            st.write('Keywords: ', search_words)
            if n == 0:
                st.write('')
            elif len(phrases) == 0:
                st.write('No phrases found in database. Please input another keyword')
            elif n > len(phrases):
                st.write("Sample Phrases (" + str(len(phrases)) + "):")
            else:
                st.write("Sample Phrases (" + str(n)+ "):")

            for i, phrase in zip(range(1, n+1), phrases):
                st.write(i, phrase)
            