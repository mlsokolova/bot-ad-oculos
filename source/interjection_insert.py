# -*- coding: utf-8 -*-

import codecs

dictionary = {}

def file_to_dictionary(filename):
    with codecs.open(filename, encoding="utf-8") as f:
        for line in f:
            #print line
            (key,val)=line.split("|")
            #print key + " " + val
            dictionary[key]=val
    #return dictionary;

def subst_with_interjection(key):
        #print key
        subst_val = dictionary.get(key)
        if subst_val is None: subst_val=key
        #print subst_val
        return subst_val

def phrase_processing(phrase):
    if phrase.endswith(".")==False:
        phrase += "|."
    phrase=phrase.lower()
    #print "phrase=" + phrase
    words=phrase.split("|")
    #print words;
    return words;
    
def interjection_insert(phrase, filename):
    file_to_dictionary(filename)
    enriched_words = map(lambda x: subst_with_interjection(x), phrase_processing(phrase))
    #print enriched_words 
    enriched_phrase = " ".join(enriched_words)
    return enriched_phrase
    #return enriched_phrase;
    #for w in enriched_words:
    #    print  enriched_phrase + w;
    #    enriched_phrase = enriched_phrase + w
    #    print enriched_phrase
