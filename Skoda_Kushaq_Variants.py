#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
import requests
import pandas as pd


url = f"https://www.autocarindia.com/auto-features/skoda-kushaq-new-variants-price-features-explained-431972"

request = requests.get(url)
doc = BeautifulSoup(request.content)


volkswagan_variants = doc.find("div", attrs = {"class" : "news_article_body"})


found_tags = volkswagan_variants.find_all(lambda tag: tag.name in ['p', 'h2', 'h3'] and tag.find('span', attrs = {"style" : "color:#ff0000"}))


variant_names = []
ul_contents_list = []

for tag in found_tags:
     
    next_sibling = tag.find_next_sibling()
    

    if tag.name == 'h2' and next_sibling and next_sibling.name == 'h3':
        next_ul = next_sibling.find_next(lambda t: t.name == 'ul' and not t.attrs)
        variant_names.append(next_sibling.string)
        

    elif next_sibling and next_sibling.name == 'p' :
        next_next_sibling = next_sibling.find_next_sibling()
        
        if next_next_sibling and next_next_sibling.name == 'p' and  'br' in [p_tag.name for p_tag in next_sibling.find_all()] and next_sibling.attrs:
            next_ul = tag.find_next(lambda t: t.name == 'ul' and not t.attrs)

            if next_ul:
                    variant_names.append(tag.string)

        elif not next_next_sibling or next_next_sibling.name != 'p':
            next_ul = tag.find_next(lambda t: t.name == 'ul' and not t.attrs)
            variant_names.append(tag.string)  
            
        else:
            continue
            
    elif next_sibling and next_sibling.name != 'p':
        next_ul = tag.find_next(lambda t: t.name == 'ul' and not t.attrs)
        variant_names.append(tag.string)
        
    if next_ul:
        ul_tags = list(next_ul.strings)
        
        if ul_tags not in ul_contents_list:
            ul_contents_list.append(ul_tags)
        
    else:
        print("No <ul> tag found")
        
variant_names = list(dict.fromkeys(variant_names))


features = {}
for idx, ul_content in enumerate(ul_contents_list):
    features[variant_names[idx]] = ul_content


total_features = list(features.values())
All_Features = [item for sublist in total_features for item in sublist]


base = []

for variant in features:
    original_features = features[variant]
    
    features[variant] = features[variant] + base
    
    base = base + original_features


Car_Features = {
    'Features' : All_Features
}

df = pd.DataFrame(Car_Features)

for variant in features:
    df[variant] = df['Features'].isin(features[variant])


for values in features:
    df[values]= df[values].replace({True : "✔", False : "✘"})


print(df)

