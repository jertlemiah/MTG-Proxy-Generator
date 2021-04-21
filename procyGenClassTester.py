from Face import Face
from Card import Card
import os.path
from os import path
import requests
import json

def testFace():

  a = dict({
    "object": "card",
    "name": "Extus, Oriq Overlord // Awaken the Blood Avatar",
    "layout": "modal_dfc",
    "cmc": 4.0,
    "type_line": "Legendary Creature — Human Warlock // Sorcery",
    "color_identity": [
      "B",
      "R",
      "W"
    ],
    "keywords": [
      "Magecraft",
      "Double strike"
    ],
    "card_faces": [
      {
        "object": "card_face",
        "name": "Extus, Oriq Overlord",
        "mana_cost": "{1}{W}{B}{B}",
        "type_line": "Legendary Creature — Human Warlock",
        "oracle_text": "Double strike\nMagecraft — Whenever you cast or copy an instant or sorcery spell, return target nonlegendary creature card from your graveyard to your hand.",
        "colors": [
          "B",
          "W"
        ],
        "power": "2",
        "toughness": "4",
      },
      {
        "object": "card_face",
        "name": "Awaken the Blood Avatar",
        "mana_cost": "{6}{B}{R}",
        "type_line": "Sorcery",
        "oracle_text": "As an additional cost to cast this spell, you may sacrifice any number of creatures. This spell costs {2} less to cast for each creature sacrificed this way.\nEach opponent sacrifices a creature. Create a 3/6 black and red Avatar creature token with haste and \"Whenever this creature attacks, it deals 3 damage to each opponent.\"",
        "colors": [
          "B",
          "R"
        ],
      }
    ],
    "all_parts": [
      {
        "object": "related_card",
        "id": "ba09360a-067e-48a5-bdc5-a19fd066a785",
        "component": "combo_piece",
        "name": "Extus, Oriq Overlord // Awaken the Blood Avatar",
        "type_line": "Legendary Creature — Human Warlock // Sorcery",
        "uri": "https://api.scryfall.com/cards/ba09360a-067e-48a5-bdc5-a19fd066a785"
      },
      {
        "object": "related_card",
        "id": "94a50acd-ac2d-47bf-b331-0bcf5edd9c75",
        "component": "token",
        "name": "Avatar",
        "type_line": "Token Creature — Avatar",
        "uri": "https://api.scryfall.com/cards/94a50acd-ac2d-47bf-b331-0bcf5edd9c75"
      }
    ]
  })
  testFace = Face(a, 0)
  #testFace.print_face()
  print(testFace.__dict__)
  #print(Face.__dict__)

  testFace = Face(a, 1)
  #testFace.print_face()
  print(testFace.__dict__)

  b = dict({
    "name": "Conflux",
    "layout": "normal",
    "mana_cost": "{3}{W}{U}{B}{R}{G}",
    "cmc": 8.0,
    "type_line": "Sorcery",
    "oracle_text": "Search your library for a white card, a blue card, a black card, a red card, and a green card. Reveal those cards, put them into your hand, then shuffle.",
    "colors": [
      "B",
      "G",
      "R",
      "U",
      "W"
    ],
    "color_identity": [
      "B",
      "G",
      "R",
      "U",
      "W"
    ],
    "keywords": [

    ]
  })

  testFace = Face(b, 0)
  #testFace.print_face()
  print(testFace.__dict__)

def testCard():
 carda = dict({
    "object": "card",
    "name": "Extus, Oriq Overlord // Awaken the Blood Avatar",
    "layout": "modal_dfc",
    "cmc": 4.0,
    "type_line": "Legendary Creature — Human Warlock // Sorcery",
    "color_identity": [
      "B",
      "R",
      "W"
    ],
    "keywords": [
      "Magecraft",
      "Double strike"
    ],
    "card_faces": [
      {
        "object": "card_face",
        "name": "Extus, Oriq Overlord",
        "mana_cost": "{1}{W}{B}{B}",
        "type_line": "Legendary Creature — Human Warlock",
        "oracle_text": "Double strike\nMagecraft — Whenever you cast or copy an instant or sorcery spell, return target nonlegendary creature card from your graveyard to your hand.",
        "colors": [
          "B",
          "W"
        ],
        "power": "2",
        "toughness": "4",
      },
      {
        "object": "card_face",
        "name": "Awaken the Blood Avatar",
        "mana_cost": "{6}{B}{R}",
        "type_line": "Sorcery",
        "oracle_text": "As an additional cost to cast this spell, you may sacrifice any number of creatures. This spell costs {2} less to cast for each creature sacrificed this way.\nEach opponent sacrifices a creature. Create a 3/6 black and red Avatar creature token with haste and \"Whenever this creature attacks, it deals 3 damage to each opponent.\"",
        "colors": [
          "B",
          "R"
        ],
      }
    ],
    "all_parts": [
      {
        "object": "related_card",
        "id": "ba09360a-067e-48a5-bdc5-a19fd066a785",
        "component": "combo_piece",
        "name": "Extus, Oriq Overlord // Awaken the Blood Avatar",
        "type_line": "Legendary Creature — Human Warlock // Sorcery",
        "uri": "https://api.scryfall.com/cards/ba09360a-067e-48a5-bdc5-a19fd066a785"
      },
      {
        "object": "related_card",
        "id": "94a50acd-ac2d-47bf-b331-0bcf5edd9c75",
        "component": "token",
        "name": "Avatar",
        "type_line": "Token Creature — Avatar",
        "uri": "https://api.scryfall.com/cards/94a50acd-ac2d-47bf-b331-0bcf5edd9c75"
      }
    ]
  })

 cardb = dict({
    "name": "Conflux",
    "layout": "normal",
    "mana_cost": "{3}{W}{U}{B}{R}{G}",
    "cmc": 8.0,
    "type_line": "Sorcery",
    "oracle_text": "Search your library for a white card, a blue card, a black card, a red card, and a green card. Reveal those cards, put them into your hand, then shuffle.",
    "colors": [
      "B",
      "G",
      "R",
      "U",
      "W"
    ],
    "color_identity": [
      "B",
      "G",
      "R",
      "U",
      "W"
    ],
    "keywords": [

    ]
  })

 testCard = Card("main", "WU Spirits", carda, "BR hollow one", cardb)
 testCard.printCard(simple = True)
 testCard.printCard(simple = False)

def textFace2():
  urborg = {
    "tcgplayer_id": 234275,
    "cardmarket_id": 548301,
    "name": "Urborg, Tomb of Yawgmoth",
    "layout": "normal",
    "mana_cost": "",
    "cmc": 0.0,
    "type_line": "Legendary Land",
    "oracle_text": "Each land is a Swamp in addition to its other land types.",
    "colors": [

    ],
    "color_identity": [

    ],
    "keywords": [

    ],
   "frame_effects": [
    "legendary"
  ]
  }

  testFace = Face(urborg, 0)
  print(testFace.__dict__)

# def requestScryfallLibrary():
#   cardName = card_name.replace(' ', '%20')  #Replace spaces    
#     #base_url = 'https://api.scryfall.com/cards/named?exact=!'  #Base URL
#     #final_url = base_url + card_name       #Final URL
#     url = 'https://api.scryfall.com/cards/named?exact=!"%s"' %(card_name) 
#     cardDict = requests.get(url=url).json()
#     return cardDict


# def checkIfOracleCardsAvailable():
#   path.exists()

#testFace()
testCard()
# textFace2()
# scryFallLibrary = requestScryfallLibrary()
# print(scryFallLibrary[])