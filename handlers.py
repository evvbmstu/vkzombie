# -*- coding: utf-8 -*-

import re
from controller import *
from settings import *
import sys
import MySQLdb
import schedule
import nltk
from views import dayView
reload(sys)
sys.setdefaultencoding("utf-8")

#Handling all messages.
def handler( string, vkId ):
    if " " in string:
        parts = string.split( " " )
        command = parts[0]
	
    	# Exam's result's 
        if check( command, commands['session'] ):
            try:
                group, surname = formatter( parts )
            except ValueError:
                return formatter( parts )
            results = getResults( group, surname )
            return results
    	# Registration block
        elif check( command, commands['registration'] ): 
            if len( parts ) != 4:
                return " Неправильно введена команда. Проверь ещё раз."
            try:
                group, surname = formatter( parts )
            except ValueError:
                return formatter( parts )
            results =  checkIn ( vkId, surname, group )
            return results
    	# Schdedule command's block.

        elif check( command, commands['today'] ):
            try:
                group, surname = formatter( parts )
            except ValueError:
                return formatter( parts )
            return daySchedule( group )
        elif check( command, commands['tomorrow'] ):
            try:
                group, surname = formatter( parts )
            except ValueError:
                return formatter( parts )
            return tomorrowSchedule( group )
        elif check( command, commands['week'] ):
            try:
                group, surname = formatter( parts )
            except ValueError:
                return formatter( parts )
            return dayView( weekSchedule( group ) )
        else:
            return "Команда не найдена "
    else:
        if check( string, commands['session'] ):
	    group, surname = getFromDb( vkId )
	    results = getResults( group, surname )
	    return results
	elif check( string, commands['commandsInfo'] ):
	    return commandsInfoList
	elif check( string, commands['today'] ):
	    group, surname = getFromDb( vkId )
	    return daySchedule( group )
	elif check( string, commands['tomorrow'] ):
             group, surname = getFromDb( vkId )
             return tomorrowSchedule( group )
        elif check( string, commands['week'] ):
             group, surname = getFromDb( vkId )
             return dayView( weekSchedule( group ) )
	else:
	    return " Неверная команда " 

# Format input text ( group, name )
def formatter( parts ):
        try:
            surname = unicode( parts[2], 'utf-8' ).lower().capitalize()
        except IndexError:
                return "Команда введена не полностью, правильный вариант можно посмотреть по запросу <команды>"
        if '-' not in parts[1]:
            try:
                digits = re.search(r'\d+', parts[1]).group()
            except AttributeError:
                return "Неправильно введена команда. Возможно, ты перепутал фамилию/форму обучения и группу местами. Попробуй еще раз!"
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
            else:
                return " Неправильно указана группа, стоит быть внимательнее ) "

	if unicode( parts[-1], 'utf-8' ).upper() == u'БАКАЛАВР':
            digits += 'Б'
        elif unicode( parts[-1], 'utf-8' ).upper() == u'МАГИСТР':
            digits += 'М'

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

def check ( string, commands ):
	string = unicode( string, "utf-8" ).upper()
	if string in commands:
	    return True
	else:
	    dist = nltk.edit_distance( string, commands[0] )
	    if dist <= 2:
	        return True
	    else:
	        return False

