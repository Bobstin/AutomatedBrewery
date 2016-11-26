import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.BeerSmithImporter import importFromBeersmith





importResults=importFromBeersmith(r'C:\Users\Justin.Kahn\Desktop\testBeerSmithFile.bsmx')
for i in range(0,5): print(importResults[i])