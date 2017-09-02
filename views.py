# -*- coding: utf-8 -*-

from tabulate import tabulate

def resultsView( exams, credit, course ):
    stab = "----------------------------------------------------------"
    examsInfo = exams.items()
    creditInfo = credit.items()
    courseInfo = course.items()
    
    examStr = ''
    for i in range( 0, len( exams ) ):
        examStr += examsInfo[i][0].decode( "utf-8" )

        examStr += " (" + examsInfo[i][1].decode( "utf-8" ) + ")"
        examStr += "\n"
    examStr = "Экзамены:\n" + examStr
    
    creditStr = ''
    for i in range( 0, len( credit ) ):
        creditStr += creditInfo[i][0].decode(" utf-8" )
        creditStr += " (" + creditInfo[i][1].decode( "utf-8" ) + ")"
        creditStr += "\n"
    creditStr = stab + "\nЗачеты:\n" + creditStr
    
    courseStr = ''
    for i in range( 0, len( course ) ):
        courseStr += courseInfo[i][0].decode("utf-8").replace( "Курсовая работа", '' )
        courseStr += " (" + courseInfo[i][1].decode( "utf-8" ) + ")"
        courseStr += "\n"
    courseStr = stab + "\nКурсовые работы:\n" + courseStr
    
    print examStr + creditStr + courseStr
    return examStr + creditStr + courseStr

def schedulePrint(list):
    for each in list:
        print each
