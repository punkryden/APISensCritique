# APISensCritique
Scripts for collecting datas from SensCritique

## api_bib.py : extract the collection of a user into a csv file

Input:
- User
- First page of the collection to extract
- Last page of the collection to extract
Output :
- bibNote_<date>.csv
 Title : the name of the item
 Artist : first occurence of directors for movies, developers for video game, authors for books/comics, creators for series, artists for music
 Year : production year or release date
 Category : precise category (Court-Métrage, Moyen-Métrage) or universe (Film)
 * to fix : some items without category...*
 Note : user evaluation or in progress flag or wish flag
  * to fix : UTF8 issue when open in Excel, ok in NotePad*
 
 The script appends rows to output file. You can restart the script from a specific page if something go wrong...

## api_critique.py : extract the reviews of a user into a csv file
  
Input:
- User
- First page of the reviews to extract
- Last page of the reviews to extract
Output :
- bibCritique_<date>.csv
 Title : the title of the review
 Link : the link in SensCritique
 Review : the body of the full review
