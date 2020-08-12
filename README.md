# MTG-Proxy-Generator
My MTG Proxy Generator does two things that makes it unique among any other proxy generator that is available online. 

1: it takes two deck lists (of card names) and splices them together into a single proxy list using the ScryFall API to search for the card information. 

2: it uses colored borders instead of black and white, and mana symbols instead of of {R}. 

The idea of this proxy generator is essentially to cut the art out of a card, which cuts the card in half, and then glue two halfs (from different decks) together into a single proxy. That way you can play one deck right side up or a second deck upside down.

Part of my goal was to help with dyslexic players such as myself since nearly all proxy generators that scrape information with an API are just walls of text that are difficult to parse at a glance. The addition of colors and the correct symbols greatly helps with readability. 

Proxies still contain all relavent information (cost, typeline, oracle text), as well as optionally provided information like the deckname.

This is a work in progress, with the end-goal of the project being hosted online for public use.
