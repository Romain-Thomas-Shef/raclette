"""
This file is part of the raclette project
It codes the function that converts cff files
to bibtex

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-

Used a lot this documentation: https://bibtex.eu/
"""

###Python standard library
import textwrap

##Third party
import yaml

##Local imports
from . import hardcoded

def cff_to_bibtex(filecontent):
    '''
    Parameters
    -----------

    Returns
    -------
    '''
    ###load the data as a YAML file
    yamlconf = yaml.safe_load(''.join(filecontent))

    ###check in there is a "preferred-citation" in it
    if 'preferred-citation' in yamlconf:
        bibtex = preferred_citation_to_bibtex(yamlconf['preferred-citation'])
        construction = 'preferred-citation'
    else:
        bibtex = build_bibtex_from_cff(yamlconf)
        construction = 'built'
 
    return bibtex, construction
    

def preferred_citation_to_bibtex(cffdata):
    '''
    This builds the bibtex entry from a
    preferred citation block of a CFF file

    Parameters:
    ----------

    Return
    ------
    bibtex : str
             bibtex entry
    '''
    available_data = {}
    for i in hardcoded.bibtex_fields:
        if i in cffdata:
            ###For authors we make small checks (number and format)
            if i == 'authors': 
                authors_list = ''
                
                final_list_authors = cffdata[i]

                ##check format 
                for person in final_list_authors:
                    if 'name' in person or ('given-names' in person and 'family-names' in person):
                        if 'name' in person:
                            authors_list += f"{person['name']} and "
                        else: 
                            authors_list += f"{person['family-names']}, {person['given-names']} and "
                
                

                #clean up the end and cut lines to 60 characters
                authors_list = textwrap.fill(authors_list.strip('and '), 60,
                                             break_long_words=False).replace('\n', '\n\t\t\t')

                ###add to the final dictionary
                available_data[i] = authors_list
            
            elif i == 'type':
                available_data[i] = hardcoded.cff_type_to_bibtex_type[cffdata[i].lower()]
                
            elif isinstance(cffdata[i], dict):
                list_string = [f'{cffdata[i][j]}' for j in cffdata[i] ]
                available_data[i] = list_string[0]

            else:
                available_data[i] = cffdata[i]

    
    ###Tune pages number
    if 'start' in available_data and 'end' in available_data and 'pages' not in available_data:
        if available_data['start'] is not None and available_data['end'] is not None:
            available_data['pages'] = '%s--%s'%(available_data['start'], available_data['end'])
            available_data.pop('start')
            available_data.pop('end')

    elif 'pages' in available_data and 'start' in available_data and 'end' in available_data:
            available_data.pop('start')
            available_data.pop('end')
            
    ###this is an arbitrary format, just the identifier to refer to the bibtex entry
    if 'year' in cffdata:
        if 'and' in authors_list:
            citekey = authors_list.split('and')[0].split(',')[0].strip().replace(" ", "") + str(cffdata['year']) 
        else:
            citekey = authors_list.split(', ')[0].strip().replace(" ", "") + str(cffdata['year'])
    else:
        if 'and' in authors_list:
            citekey = authors_list.split('and')[0].split(',')[0].strip()
        else:
            citekey = authors_list.split(', ')[0].split(',')[0]

    ##and return the final bibtex assembled    
    return assemble_bibtex(available_data, citekey)

def build_bibtex_from_cff(cffdata):
    '''
    This builds the bibtex entry from a
    preferred citation block of a CFF file

    Parameters:
    ----------

    Return
    ------
    bibtex : str
             bibtex entry
    '''
    available_data = {}
    for i in hardcoded.cff_fields:
        if i in cffdata:
            ###For authors we make small checks (number and format)
            if i == 'authors': 
                authors_list = ''
                
                final_list_authors = cffdata[i]

                ##check format 
                for person in final_list_authors:
                    if 'name' in person or ('given-names' in person and 'family-names' in person):
                        if 'name' in person:
                            authors_list += f"{person['name']} and "
                        else: 
                            authors_list += f"{person['family-names']}, {person['given-names']} and "
 

                #clean up the end and cut lines to 60 characters
                authors_list = textwrap.fill(authors_list.strip('and '), 60,
                                             break_long_words=False).replace('\n', '\n\t\t\t')
                ##save it
                available_data[i] = authors_list


            elif i == 'type':
                available_data[i] = hardcoded.cff_type_to_bibtex_type[cffdata[i].lower()]
            else:
                available_data[i] = cffdata[i]

    ###sometimes 'type' is not part of the cff (for some F*** reason)
    if 'type' not in available_data:
        available_data['type'] = 'software'

    ##Now cross match with the bibtex list
    keys_for_bibtex = {}
    for key in hardcoded.cff_keywords_to_bibtex:
        ###some are lists in priority order so we must check for this
        key_to_check = key
        if isinstance(hardcoded.cff_keywords_to_bibtex[key], list):
            for subkey in hardcoded.cff_keywords_to_bibtex[key]:
                if subkey in available_data:
                    key_to_check = subkey
                    break
        elif key == 'author':
            key_to_check = 'authors'
        else:
            key_to_check = key
        ##dates
        if 'date' in key_to_check and key == 'year':
            ##cff dates are a string YYYY-MM-DD 
            keys_for_bibtex[key] = str(available_data[key_to_check]).split('-')[0]
        elif 'date' in key_to_check and key == 'month':
            ##cff dates are a string YYYY-MM-DD 
            keys_for_bibtex[key] = str(available_data[key_to_check]).split('-')[1]
        elif key_to_check in available_data:
            keys_for_bibtex[key] = available_data[key_to_check] 

    ###if type is misc, we must remove version number (based on observation in github)
    if keys_for_bibtex['type'] == 'misc' and 'version' in keys_for_bibtex:
        keys_for_bibtex.pop('version')

    ###this is an arbitrary format, just the identifier to refer to the bibtex entry
    if 'year' in keys_for_bibtex:
        citekey = authors_list.split(', ')[0] + str(keys_for_bibtex['year']) 
    else:
        citekey = authors_list.split(', ')[0]
 
    ##and return the final bibtex assembled    
    return assemble_bibtex(keys_for_bibtex, citekey)


def assemble_bibtex(data, citekey):
    '''
    This function assemble the final bibtex entry

    it takes a dictionary as entry. The dictionary must have at least
    the 'type' keyword
    

    Parameter
    ---------
    data    :   dict
                entry dictionary with data for the bibtex
    citekey :   str
                string to identify the bibtex entry
    Return 
    ------
    bibtex :    str
                final bibtex
    '''
    ###assemble the bibtex
    bibtex_start = "@%s{%s,\n"%(data['type'], citekey)
    bibtex_middle = ""
    for d in data:
        if d not in ['type', 'authors']:
            bibtex_middle += f'\t{d}'+' = {%s},\n'%data[d]
        if d == 'authors':
            bibtex_middle += '\tauthor = {%s},\n'%data[d]
    bibtex_end = "}"

    bibtex = bibtex_start + bibtex_middle + bibtex_end

    return bibtex
