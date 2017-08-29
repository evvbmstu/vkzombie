# -*- coding: utf-8 -*-

import re
from controller import getResults,checkIn
from settings import *
import sys
import MySQLdb
import nltk
reload(sys)
sys.setdefaultencoding("utf-8")

#Handling all messages.
def handler( string, vkId ):
    if " " in string:
        parts = string.split( " " )
        command = unicode( parts[0], 'utf-8' ).upper()
        
	if command in commands['session']:
            group, surname = formatter( parts )
	    results = getResults( group, surname )
	    return results
	elif command in commands['registration']: 
	    group, surname = formatter( parts )
	    results =  checkIn ( vkId, surname, group )
	    return results
        else:
            return "Команда не найдена "
    else:
        if unicode( string, 'utf-8' ).upper()  in commands['session']:
	    group, surname = getFromDb( vkId )
	    results = getResults( group, surname )
	    return results
	elif unicode( string, 'utf-8' ).upper() in commands['commandsInfo']:
	    return commandsInfoList

# Format input text ( group, name )
def formatter( parts ):
        surname = unicode( parts[2], 'utf-8' ).lower().capitalize()
            
        if '-' not in parts[1]:
            digits = re.search(r'\d+', parts[1]).group()
            index = unicode(re.search(r'\D+',parts[1]).group(),'utf-8').upper()
        else:
            group  = unicode( parts[1], "utf-8" ).upper()
            return group, surname
            
            
        if str(index) == "ЮР" or str(index[0]) == "Т":
            digits = '-' + digits

        elif str(index) == "ИУ" and digits[:2] == "10":
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        elif str(index) == "МТ" and digits[:2] == "10":
            digits = digits[0:2] + '-' + digits[2:len(digits)]
                
        elif str(index) == "СМ" and digits[:2] == "10":
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        elif str(index) == "Э" and digits[:2] == "10":
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        elif str(index) == "МТ" and len(digits) == 4 and (digits[:2] == "12" or digits[:2] == "13") :
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        elif str(index) == "СМ" and len(digits) == 4 and (digits[:2] == "12" or digits[:2] == "13") :
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        elif str(index) == "ФН" and len(digits) == 4:
            digits = digits[0:2] + '-' + digits[2:len(digits)]
            
        else:
            if len( digits ) == 3:
                digits = digits[:1] + '-' + digits[1:4]
            elif len( digits ) == 4:
                digits = digits[:1] + '-' + digits[1:5]
            elif len( digits ) == 5:
                digits = digits[:2] + '-' + digits[2:5]

        return str(index + digits), surname

def getFromDb( vkId ):
    connection = MySQLdb.connect( MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, charset='utf8',use_unicode = True)
    cursor = connection.cursor()
    cursor.execute( "SELECT surname FROM user WHERE vk_id =" + str( vkId ) + ";" )
    surname = cursor.fetchone()[0]
    cursor.execute( "SELECT UID from user WHERE vk_id = " + str( vkId ) + ";" )
    group = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return group, surname
