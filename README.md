# MTG-Proxy-Generator
This is going to be difficult to explain if you don't know anything about Magic the Gathering, but in short this project: 
takes a list of card names, 
does a batch request to the Scryfall API, 
draws a bunch of cards based on the parsed information, 
outputs a PDF with all the info drawn

The end goal is have this accessible through a website.

Further info that won't make sense without MTG knowledge:
My MTG Proxy Generator does two things that makes it unique among any other proxy generator that is available online. 

1: it takes TWO deck lists (of card names) and splices them together into a single proxy list using the ScryFall API to search for the card information. It kinda looks like a Kamigawa flip card, except on opposite sides (if that makes any sense at all).
Nearly all other proxy generators take a single deck as an input, which is painfully inefficient and a waste of space. The exception to this is too efficient Metadeck which can take up to 8 decks, but only lists the names of cards and expects you to know them instinctively 

2: This proxy gen uses colored borders instead of black and white ones like most other, mana symbols instead of of {R}, and even the correct font. This is to help with dyslexic players, such as myself, know what a card is at a glance, much the way you would with a real card.

Proxies made from this proxygen still contain all relavent information (cost, typeline, oracle text), as well as optionally provided information like the deckname.

A lot of this will immediately make sense if you check the Sample Outputs folder.

***Operation***

Run the "ProxyGen.py" file to run the current menu version.

The current menu will intake 2 MTG decks and splice them together into an output. I have included sample decks that outfill into all of the releveant fields.

The parsing currently has issues with a few unique case cards since there are so many that I have to manually fix. 
For example, did you know that Urborg, Tomb of Yawgmoth has a black border? It doesn't have a color or a color identity since it is a land, and it doesn't have the tap for mana ability before it is on the battlefield, so it's difficult to parse in such a way that it would automatically assume the card is black-bordered. But clearly, it is still a black card. Well there's like 50 cards like this, just weird cases that take time to fix.

The generator is RIDICULOUSLY slow and I know why, but fixing it is something I have not found the time and effort to do.
