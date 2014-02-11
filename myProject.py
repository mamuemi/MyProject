# status: 02-10-2014
# obtain from web crawl json, clean data (empty, dup entries, stop words, punctuation), do and visualize word count of job profiles as bar plot

import json
from collections import defaultdict, OrderedDict, Counter
import pandas as pd
import csv
import matplotlib.pyplot as plt

# source
source = ('linkedin/items1.json')
source_json = json.load(open(source))

#delete dictionaries in list where value for description is []
source_json[:] = [d for d in source_json if d.get('description')]

# normalize url field by cutting off string starting ?
# example: http://www.linkedin.com/jobs2/view/11437308?trk=njsrch_hits&goback=%2Efjs_sales+director_*1_*1_Y_*1_*1_*1_2_R_true_*1_*2_*2_*2_*2_*2_*2_*2_*2
for item in source_json:
    s = item.get('url').split('?')[0]
    item['url'] = s

# delete duplicates from source based on url field
url = []
source_json_clean = []

for item in source_json:
    if item.get('url') in url:
        pass
    else:
        url.append(item.get('url'))
        source_json_clean.append(item)

#create data frame
source_df = pd.DataFrame(source_json_clean)

#delete commas in title column
i=0
for item in source_df.title:
    if "," in source_df.title.get_value(i)[0]:
        temp = source_df.title.get_value(i)
        new = temp[0].replace(",", "")
        temp[0] = new
        source_df.title.set_value(i,temp)        
        i += 1
    else:
        i += 1
        pass

#delete bracket ( in title column

i=0
for item in source_df.title:
    if "(" in source_df.title.get_value(i)[0]:
        temp = source_df.title.get_value(i)
        new = temp[0].replace("(", "")
        temp[0] = new
        source_df.title.set_value(i,temp)        
        i += 1
    else:
        i += 1
        pass

#delete bracket ) in title column
i=0
for item in source_df.title:
    if ")" in source_df.title.get_value(i)[0]:
        temp = source_df.title.get_value(i)
        new = temp[0].replace(")", "")
        temp[0] = new
        source_df.title.set_value(i,temp)        
        i += 1
    else:
        i += 1
        pass

#word count for title column
wordcountT = defaultdict(int)

for title in source_df.title:
    for w in title[0].split():
        wordcountT[w] += 1

#create ordered dictionary and list, then  sort by value
dict_orderedWordsTitle = OrderedDict(sorted(wordcountT.items(), key=lambda t: t[1], ))
list_orderedWordsTitle = dict_orderedWordsTitle.items()
list_orderedWordsTitle.reverse()

# delete stop words, etc
stopWords = [ "a", "i", "it", "am", "at", "on", "in", "to", "too", "very", \
                 "of", "from", "here", "even", "the", "but", "and", "is", "my", \
                 "them", "then", "this", "that", "than", "though", "so", "are", \
                 "for", "with", "The", "OR", "or"]
stemEndings = [ "-s", "-es", "-ed", "-er", "-ly" "-ing", "-'s", "-s'" ]
punctuation = [ ".", ",", ":", ";", "!", "?", "-", "--", "&", "/", "\\"]
otherTerms = ["\u2013"]

list_orderedWordsTitleClean = [item for item in list_orderedWordsTitle if item[0] not in otherTerms 
                                          and item[0] not in stopWords
                                          and item[0] not in stemEndings
                                          and item[0] not in punctuation]

#prepare and show bar plot
xvaluesLabelT = [item[0] for item in list_orderedWordsTitleClean]
yvaluesT = [item[1] for item in list_orderedWordsTitleClean]

scope = 15
xvaluesT = range(scope)

plt.bar(xvaluesT[:scope], yvaluesT[:scope], align='center')
plt.xticks(xvaluesT, xvaluesLabelT[:scope])
plt.rcParams['figure.figsize'] = (30.0, 10.0)
plt.title("Word Count in Job Title in source file '%s'" %(source))
plt.xlabel("Words")
plt.ylabel("Counts")
plt.show()


