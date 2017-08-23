# -*- coding: utf-8 -*-

from tabulate import tabulate

def resultsView( exams, credit, course ):
    examsInfo = exams.items()
    creditInfo = credit.items()
    courseInfo = course.items()
    outList = []

    for i in range(0, len(exams)):
        tmpList = []
        tmpList.append(examsInfo[i][0].decode("utf-8"))
        tmpList.append(examsInfo[i][1].decode("utf-8"))
        outList.append(tmpList)
    examStr = "Экзамены \n" + tabulate(outList)

    outList = []
    for i in range(0, len(credit)):
        tmpList = []
        tmpList.append(creditInfo[i][0].decode("utf-8"))
        tmpList.append(creditInfo[i][1].decode("utf-8"))
        outList.append(tmpList)
    creditStr = "\nЗачеты \n" + tabulate(outList)

    outList = []
    for i in range(0, len(course)):
        tmpList = []
        tmpList.append(courseInfo[i][0].decode("utf-8"))
        tmpList.append(courseInfo[i][1].decode("utf-8"))
        outList.append(tmpList)
    courseStr = "\nКурсовые \n" + tabulate(outList)
    sumStr = examStr + creditStr + courseStr
    return sumStr
