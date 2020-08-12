#!/usr/bin/env python
#Learn how this works here: http://youtu.be/pxofwuWTs7c
 
import requests
import json

#https://api.scryfall.com/cards/named?exact=island
 
def card_search(card_name):
    url = 'https://api.scryfall.com/cards/named?exact=!"'	#Base URL
    card_name = card_name.replace(' ', '%20')				#Replace spaces
    final_url = url + card_name + '"'						#Final URL

    req = requests.get(url=final_url).json()
    #print(req)

    print(req['name'])
    print(req['colors'])
    print(req['color_identity'])	
    print(req['mana_cost'])
    print(req['oracle_text'])
    print(req['type_line'])
    if 'creature' in req['type_line']:
   		print(req['power'] + "/" + req['toughness'])
    print(" − ")

    #data = json.load(json_obj)
   
    #for item in data['objects']:
    #    print item['name'], item['phone']

card_search("Chandra, Torch of Defiance")