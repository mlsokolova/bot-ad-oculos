# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import pymorphy2
import codecs
import random

def file_to_dictionary(filename):
    dictionary = {}
    with codecs.open(filename, encoding="utf-8") as f:
        for line in f:
            #print line
            (key,val)=line.split("|")
            #print key + " " + val
            dictionary[key]=val.replace("\n","")
    return dictionary;

dict_ADJF = file_to_dictionary("dicts/ADJF.txt")
dict_INFN = file_to_dictionary("dicts/INFN.txt")
dict_VERB = file_to_dictionary("dicts/INFN.txt")
dict_ADVB = file_to_dictionary("dicts/ADVB.txt")
dict_NOUN = file_to_dictionary("dicts/NOUN.txt")
dict_CONJ = file_to_dictionary("dicts/CONJ.txt")

main_dict={}
main_dict["ADJF"]=dict_ADJF
main_dict["INFN"]=dict_INFN
main_dict["VERB"]=dict_INFN
main_dict["VERB"]=dict_INFN
main_dict["ADVB"]=dict_ADVB
main_dict["NOUN"]=dict_NOUN
main_dict["CONJ"]=dict_CONJ

interjections = [l.rstrip('\n') for l in codecs.open("dicts/bunch.txt","r","utf-8")]

punc = [u".",u",",u":",u";",u"!",u"?",u"...",u"(",u")"]

morph = pymorphy2.MorphAnalyzer()

def morph_parse(word):
    parse = morph.parse(word)[0]
    return parse

def get_replaced_words_with_interjections(word_list):
    phrase_size = len(word_list)
    #print(phrase_size)
    interjection_frequency=int(round(10*((phrase_size*2)/(phrase_size*7))))
    #print(interjection_frequency)
    positions = list(range(0,phrase_size))
    positions_for_interjection = [random.choice(positions) for i in range(interjection_frequency)]
    result = word_list
    result.append(".")
    for p in positions_for_interjection:
        if result[p+1] not in punc and result[p] not in punc and result[p-1] not in punc: 
            result[p] = result[p] + ',' + random.choice(interjections) + ','
        else:
            if result[p] in punc:
                result[p] = result[p] + random.choice(interjections) + ','
            if result[p+1] in punc:
                result[p] = result[p] + ',' + random.choice(interjections)
            if result[p-1] in punc:
                result[p] = result[p] + ',' + random.choice(interjections) + ","
    return result

def get_VERB(parsed_verb, replaced_value):
    ret_parsed_verb = morph.parse(replaced_value)[0]
    #print(ret_parsed_verb)
    #gender = parsed_verb.tag.gender
    #print(parsed_verb)
    #print(replaced_value)
    tense = parsed_verb.tag.tense
    number = parsed_verb.tag.number
    if tense == "past" and number == "plur":
        ret_parsed_verb = ret_parsed_verb.inflect({"past"}).inflect({"plur"})
        #print(ret_parsed_verb)
    else: 
        #print(ret_parsed_verb)
        person = parsed_verb.tag.person
        if (person == "3per" and tense == "past" and number == "sing"):
            gender = parsed_verb.tag.gender
            ret_parsed_verb = ret_parsed_verb.inflect({"3per"}).inflect({"past"}).inflect("sing").inflect({gender})
            #print(ret_parsed_verb)
        elif (tense=="pres"):
            ret_parsed_verb = ret_parsed_verb.inflect({number}).inflect({person})
            #print(ret_parsed_verb)
    return ret_parsed_verb

def get_ADJF(parsed_adjf, replaced_value):
    ret_parsed_adjf = morph.parse(replaced_value)[0]
    #print(ret_parsed_adjf)
    gender = parsed_adjf.tag.gender
    case = parsed_adjf.tag.case
    number = parsed_adjf.tag.number
    ret_parsed_adjf = ret_parsed_adjf.inflect({gender,case,number})
    return ret_parsed_adjf

def get_NOUN(parsed_noun, replaced_value):
    ret_parsed_noun = morph.parse(replaced_value)[0]
    number = parsed_noun.tag.number
    case = parsed_noun.tag.case
    ret_parsed_noun = ret_parsed_noun.inflect({case,number})
    return ret_parsed_noun

def get_parsed_replased(parsed_word):
    ret_parsed_word = parsed_word
    pos = parsed_word.tag.POS
    normal_form = parsed_word.normal_form
    dict4replacing = main_dict.get(pos)
    #print(dict4replacing)
    if dict4replacing != None:
        replaced_value = dict4replacing.get(normal_form)
        if replaced_value != None:
            if pos == "ADJF":
                ret_parsed_word = get_ADJF(parsed_word, replaced_value)
            if pos == "INFN":
                ret_parsed_word = morph.parse(replaced_value)[0]
            if pos == "VERB":
                ret_parsed_word = get_VERB(parsed_word,replaced_value)
            if pos == "ADVB":
                ret_parsed_word = morph.parse(replaced_value)[0]
            if pos == "CONJ":
                ret_parsed_word = morph.parse(replaced_value)[0]
            if pos == "NOUN":
                ret_parsed_word = get_NOUN(parsed_word,replaced_value)
    return ret_parsed_word

def get_enrich_phrase(txt):
    #morph = pymorphy2.MorphAnalyzer()
    txt_words = nltk.word_tokenize(txt)
    parsed_words = list(map(lambda x: morph_parse(x), txt_words))
    parsed_replased_words = list(map(lambda x: get_parsed_replased(x), parsed_words))
    replaced_words = list(map(lambda x: x.word, parsed_replased_words))
    replaced_words_with_interjections = get_replaced_words_with_interjections(replaced_words)
    enriched_phrase = ' '.join(replaced_words_with_interjections)
    return enriched_phrase
    

