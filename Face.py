# -----------------------------------------------------------
# class for storing information regarding a specific face
#
# 2021 Jeremiah Plauche, Texas, US
# email jeremiah.plauche@gmail.com
# -----------------------------------------------------------

class Face:
	"""
		attributes every instance of Face will have:
			layout 		- possible values: normal, split, flip, transform, modal_dfc, meld, leveler, saga, adventure
			layout_face	- 0 for primary face, 1 for secondary face
			name
			mana_cost
			type_line
			oracle_text
			colors
			frame_color
		attributes only some instances of Face will have:
			power
			toughness
			loyalty
			frame_effects
	"""
	scryfallKeys = {'layout', 'name', 'mana_cost', 'type_line', 'oracle_text', 'colors', 'power', 'toughness', 'loyalty'}

	def __init__(self, parentDict, layout_face):
		# parentDict is the Scryfall dictionary for the whole magic card, not the face
		self.layout = parentDict['layout']	
		self.layout_face = layout_face	 

		# Check if multi-faced, i.e. split, flip, transform, modial_dfc, adventure all have 'card_faces', others do not
		if 'card_faces' in parentDict.keys():
			for key in Face.scryfallKeys:
				faceDict = parentDict['card_faces'][layout_face]
				if key in faceDict.keys():
					self.__dict__[key] = faceDict[key]
				else:
					# print_keyError('faceDict', key)
		else:
			for key in Face.scryfallKeys:
				if key in parentDict.keys():
					self.__dict__[key] = parentDict[key]
				else:
					# print_keyError('parentDict', key)

		self.frame_color = self.determineFrameColor(parentDict)
		# if "Legendary" in self.type_line: self.frame_effect = "legendary"
		# if "Miracle" in self.type_line: self.frame_effect = "miracle"


	def determineFrameColor(self, parentDict):
		if "Land" in self.type_line:
			tempColors = []
			# This handles colors for the two color fetch lands
			if "Plains" in self.oracle_text: tempColors.append("W")
			if "Island" in self.oracle_text: tempColors.append("U")
			if "Swamp" in self.oracle_text: tempColors.append("B")
			if "Mountain" in self.oracle_text: tempColors.append("R")
			if "Forest" in self.oracle_text: tempColors.append("G")

			# attribute for mana produced by this land
			if "produced_mana" in parentDict: tempColors.extend(parentDict["produced_mana"])
		else:
			tempColors = self.colors

		tempColors = list(set(tempColors)) #remove duplicates

		if len(tempColors) == 0: return "Colorless"
		elif len(tempColors) == 1: return tempColors[0]
		elif len(tempColors) == 2: return tempColors[0] + tempColors[1]
		else: return "Gold"

	def print_face(self):
		for key in Face.__dict__:
			if "__" not in key:
				print_line(key, str(self.__dict__[key]))

def print_keyError(dictName, keyName):
	print("KeyCustomError: '" + dictName + "' did not have key '" + keyName + "'")
	pass

def print_line(keyName, dictContent):
	print("key '" + keyName + "' has content '" + dictContent + "'")