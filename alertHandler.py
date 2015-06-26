__author__ = 'branden'


import time, traceback
import sendSMS, mbtaJsonParse, People
from collections import defaultdict


def main():
    try:
        while True:
            handleCustomAlerts()
            handleDailyAlerts()
            time.sleep(15)
    except:
        print "Error in alertHandler"
        print traceback.print_exc()
        time.sleep(15)
        # main()

########################## CUSTOM ALERTS ##################################

#Handle custom alerts if they exist
def handleCustomAlerts():
    tempDict = defaultdict(list)
    for person in People.allPeople:
        #If person has a pending custom alert
        if person.customAlertInfo != None:
            hrs, mins = person.customAlertInfo.time.split(':')
            hrs = int(hrs)
            mins = int(mins)
            #If the current time is past the alert time
            if (sendSMS.timeCheck(*[hrs, mins, 23, 59])):
                mbtaJsonParse.popDict(tempDict, person.customAlertInfo.station)
                for nextTrain in tempDict[person.customAlertInfo.direction]:
                   #If the next train is at the correct distance
                   if ((person.customAlertInfo.dist * 60) < nextTrain < ((person.customAlertInfo.dist * 60) + 70)):
                        sendSMS.sendCustomSMS(person, nextTrain)
                        person.customAlertInfo = None
                        break


#Checks to see if emailed alerts are properly formatted
def checkAlertFormat(sender, emailInfo):
    if (emailInfo[0] in mbtaJsonParse.stationConverter) and\
            (emailInfo[1] == "Northbound" or emailInfo[1] == "Southbound") and\
            (":" in emailInfo[2]) and (0 < int(emailInfo[3]) < 60):
        return True
    else:
        msg = "Incorrect Alert Format. Please check spelling and try again"
        s = People.personGrab(sender)
        sendSMS.send(msg, s)
        return False

#Make sure station and direction are uppercase for custom alerts
def prepareAlert(emailInfo):
    emailInfo[0] = emailInfo[0].title()
    emailInfo[1] = emailInfo[1].title()
    return emailInfo

########################## DAILY ALERTS ###################################

# Check to see if sms should be sent for Daily Alert
def handleDailyAlerts():
    sendSMS.sendCustom = False
    tempDict = defaultdict(list)
    for person in People.allPeople:
        if eligibleForDaily(person):
            mbtaJsonParse.popDict(tempDict, person.dailyAlertInfo.station)
            for nextTrain in tempDict[person.dailyAlertInfo.direction]:
                if ((person.dailyAlertInfo.dist * 60) < nextTrain < ((person.dailyAlertInfo.dist * 60) + 70)):
                    sendSMS.sendCustom = True
                    sendSMS.runAlert(nextTrain, person)
                    sendSMS.sendCustom = False
                    person.waitingOnDaily = False
                    break


#Determines if all daily alert criteria are met
#is it within the set time, has the person received an alert today yet, is it the right day
def eligibleForDaily(person):
    if (person.dailyAlertInfo != None) and \
                (sendSMS.timeCheck(*person.dailyAlertInfo.time)) and \
                (person.waitingOnDaily) and \
                (sendSMS.dayCheck(person.dailyAlertInfo.days)):
        return True
    else:
        return False



if __name__ == "__main__":
    main()