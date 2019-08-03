# -*- coding: utf-8 -*-
from string import Template
import sparql
import pandas as pd
from tabulate import tabulate

endpoint = "https://query.wikidata.org/sparql"

s = sparql.Service(endpoint, "utf-8", "GET")

get_property_values_statement_template = Template ( \
'select ?prop_info_label ?value \n' + \
' where \n' + \
'{ \n' + \
' { \n' + \
' $wd_qualifier ?prop ?value . \n' + \
' ?prop rdf:type owl:DatatypeProperty . \n' + \
' ?prop_info wikibase:directClaim ?prop . \n' + \
' ?prop_info  rdfs:label ?prop_info_label filter (lang(?prop_info_label)="$lang") . \n' + \
' } \n' + \
' union \n' + \
' { \n' + \
'  $wd_qualifier ?prop ?prop_value . \n' + \
'  ?prop rdf:type owl:ObjectProperty . \n' + \
'  ?prop_info wikibase:claim ?prop . \n' + \
'  ?prop_info  rdfs:label ?prop_info_label filter (lang(?prop_info_label)="$lang") . \n' + \
'  ?prop_value ?prop_value_prop ?prop_value_prop_value filter exists {?prop_value_prop rdf:type owl:ObjectProperty} . \n' + \
'  ?prop_value_prop_value rdfs:label ?value filter (lang(?value)="$lang") \n' + \
' } \n' + \
' } ' + \
' order by ?prop_info_label '  \
)
                                                   
get_qualifier_count_statement_template = Template(\
'select    (count(distinct ?s) as ?s) \n' + \
'where \n' + \
'{ \n' + \
'  ?s rdfs:label "$label_value"@$lang . \n' + \
'  ?s p:P31 ?prop_value . \n' + \
'  ?prop_info wikibase:claim p:P31 . \n' + \
'  ?prop_info  rdfs:label ?prop_info_label filter (lang(?prop_info_label)="$lang") \n' +
'  ?prop_value ?prop_value_prop ?prop_value_prop_value filter exists {?prop_value_prop rdf:type owl:ObjectProperty} . \n' + \
'  ?prop_value_prop_value rdfs:label ?value filter (lang(?value)="$lang") \n ' + \
'}' \
)

get_qualifiers_statement_template = Template(\
'select   distinct ?s (group_concat(distinct ?value; separator="; ") as ?instance_of) \n' + \
'where \n' + \
'{ \n' + \
'  ?s rdfs:label "$label_value"@$lang . \n' + \
'  ?s p:P31 ?prop_value . \n' + \
'  ?prop_info wikibase:claim p:P31 . \n' + \
'  ?prop_info  rdfs:label ?prop_info_label filter (lang(?prop_info_label)="$lang") \n' + \
'  ?prop_value ?prop_value_prop ?prop_value_prop_value filter exists {?prop_value_prop rdf:type owl:ObjectProperty} . \n' + \
'  ?prop_value_prop_value rdfs:label ?value filter (lang(?value)="$lang") \n' + \
'} \n' + \
'group by ?s \n'  \
)
                                                  
def get_sparql_result(sparql_query):
    q = s.query(sparql_query)
    r = q.fetchall()
    return r

def get_count_value(sparql_result):
    count_value = sparql_result[0][0].value
    return count_value

def get_literal_values(result_tuple):
    #print result_tuple[0].value
    ret_dict = {}
    key = result_tuple[0].value
    value = result_tuple[1].value
    ret_dict[key]=value
    return key, value
          
def get_qualifiers_count_by_label_and_language(label_value, language):
    get_qualifier_count_statement = get_qualifier_count_statement_template.substitute(label_value=label_value,lang=language)
    #print get_qualifier_count_statement
    qualifier_count_result = get_sparql_result(get_qualifier_count_statement)
    c = get_count_value(qualifier_count_result)
    return "Found " + c + " qualifiers:"

def get_qualifiers_by_label_and_language(label_value, language):                       
    get_qualifiers_statement = get_qualifiers_statement_template.substitute(label_value=label_value,lang=language)
    qualifiers_result = get_sparql_result(get_qualifiers_statement)
    qualifiers_result_dict = map(lambda x: get_literal_values(x), qualifiers_result)
    df_qualifiers_result = pd.DataFrame(qualifiers_result_dict,columns=["qualifier","instance of"])
    #html_table = df_qualifiers_result.to_html(index=False)
    result_table = tabulate(df_qualifiers_result,headers='keys', showindex=False, tablefmt='simple')
    return result_table
