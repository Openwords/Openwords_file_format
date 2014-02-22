#Dalimil Hajek
#often words are categorized in more then one category
#like http://en.wiktionary.org/wiki/%D0%B0%D2%99%D0%B0%D2%A1#Bashkir - that's ok I only count it once

import re
import sys
from urllib.request import *
import urllib.parse as urlp

if(len(sys.argv) < 3):   #program_name quite/verbose language
    print("not enough arguments")
    sys.exit()
    
name = sys.argv[2]
URLold = {}
URLfresh = {"/wiki/Category:"+name+"_parts_of_speech": 1} #1 - follow links, 0 -don't
hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
#links on the wiktionary are always relative

def save():
    if(sys.argv[1] == "quiet"):
        counting = 0
        for i in URLold:
            if(not i.startswith("/w/") and not i.startswith("/wiki/Category")):
                counting += 1
        print("unique links in subcategories: "+str(counting)+"\n")
    else: #verbose
        for i in URLold:
            if(not i.startswith("/w/") and not i.startswith("/wiki/Category")):
                print("https://en.wiktionary.org"+urlp.unquote_plus(i)+"\n")
    
while len(URLfresh) != 0:
    nex = URLfresh.popitem();
    URLold[nex[0]] = nex[1]
    url = "https://en.wiktionary.org"+nex[0];
    #print(urlp.unquote_plus(url))
    if(nex[1] == 0): #word page - don't follow
        continue

    #else follow
    ok = Request(url, None, hdr)
    html = urlopen(ok).read()
    t = str(html.decode('utf-8'))
            
    starting = t.find("Subcategories")
    if(starting == -1):
        starting = t.find("Pages in category")
    t = t[starting:]
    stop = t.find("<noscript>")
    t = t[:stop]
    
    z = re.findall(r'href="/w[^"]*', t) #get urls
    print(len(z)) #number of links with categories, may not be all unique yet
    for i in range(len(z)): #remove href
        z[i] = z[i][6:]
                          
    for i in z: #links from this page
        if (i not in URLold) and (i not in URLfresh):
            #print(urlp.unquote_plus(i)+"---")
            if(i.startswith("/w/ind")):
                if(i.find("pageuntil") == -1 and i.find("pagefrom") != -1):
                    x = i.split("amp;")
                    addit = ""
                    for val in x:
                        addit += val
                    URLfresh[addit] = 1
            elif((i[6:]).startswith("Categ")):
                URLfresh[i] = 1
            else:
                URLfresh[i] = 0
                
save()    


      
    
