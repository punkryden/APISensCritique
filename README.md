# APISensCritique
Scripts for collecting datas from SensCritique

## api_bib.py : extract the collection of a user into a csv file

Input:
- User
- Firt page of the collection to extract
- Last page of the collection to extract
Output :
- bibNote_<date>.csv
 
 The script appends rows to output file. You can restart the script from a specific page if something go wrong...

## api_critique.py : extract the reviews of a user into a csv file
  
Input:
- User
- Firt page of the reviews to extract
- Last page of the reviews to extract
Output :
- bibCritique_<date>.csv
