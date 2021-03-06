import module
import tutor
import ReaderWriter
import timetable
import random
import math
import copy

class Scheduler:

	def __init__(self,tutorList, moduleList, moduleLabList):
		self.tutorList = tutorList
		self.moduleList = moduleList
		self.moduleLabList = moduleLabList
		self.minTtList = [[], 1000000]
		
	#Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
	#This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith. 
	#Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
	#Every module needs one "module" and one "lab" session type. 
	
	#moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
	# m.name  - the name of the module
	# m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

	#tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
	# t.name - the name of the tutor
	# t.expertise - a list of strings, describing the expertise of the tutor. 

	#For Task 1:
	#Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise. 
	#Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
	#There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
	#In some problems, modules will cover 2 topics and in others, 3.
	#A tutor will have between 3-8 different expertise fields. 

	#For Task 2 and 3:
	#A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
	#Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
	#A tutor can not teach more than 2 credits per day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)
		
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.backTrackModSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	def createLabSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.		
		self.backTrackModLabSchedule(timetableObj)


		#Do not change this line
		return timetableObj

	#It costs £500 to hire a tutor for a single module.
	#If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
	#If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

	#It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
	#If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here. 
	def createMinCostSchedule(self): 
		#Do not change this line
		timetableObj = timetable.Timetable(3) 

		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.backTrackTask3(timetableObj)
		#Do not change this line
		return self.minTtList[0]


	#This simplistic approach merely assigns each module to a random tutor, iterating through the timetable. 
	def randomModSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#The first educated approach to this problem  
	def backTrackModSchedule(self, timetableObj, dayNumber = 0, sessionNumber = 1, tutorSessions = {}, ):
		#If all days and sessions are filled return True
		if dayNumber == 5:
			return True
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		#Consider the session of a particular day and try assigning each tutor for the session one by one
		for tut in self.tutorList:
			if self.isValidTask1(timetableObj, tut, dayNumber, sessionNumber, tutorSessions):
			#tutorSessions is a len(tutorList)x5 sized list with number of sessions per day per tutor encoded in it 

				#assign the tutor for this session
				timetableObj.addSession(days[dayNumber], sessionNumber, tut, self.moduleList[dayNumber*5 + sessionNumber - 1], "module")
				self.addTutorSessions(tutorSessions, tut, dayNumber)

				[nextSessionNumber, nextDayNumber] = self.updateSessionDayNumber(sessionNumber, dayNumber, 1)
				if self.backTrackModSchedule(timetableObj, nextDayNumber, nextSessionNumber, tutorSessions):
					return True
					
				#Since this assignment has no further solutions we deallocate the tutor from that session
				tutorSessions[tut][dayNumber] = tutorSessions[tut][dayNumber] - 1
			
		#If no tutors can be assigned to this sessionNumber on days[dayNumber] then return False
		return False

	def isValidTask1(self, timetableObj, tut, dayNumber, sessionNumber, tutorSessions):
		heCanTeach = timetableObj.canTeach(tut, self.moduleList[dayNumber*5 + sessionNumber - 1], False)
		if tut in tutorSessions:
			isTeachingToday = (tutorSessions[tut][dayNumber] > 0)
			isTeachingTwiceThisWeek = (sum(tutorSessions[tut]) >= 2)
		else:
			isTeachingToday = False
			isTeachingTwiceThisWeek = False
			
		return (heCanTeach and not isTeachingToday and not isTeachingTwiceThisWeek)

	def addTutorSessions(self, tutorSessions, tut, dayNumber):
		if tut not in tutorSessions:
			tutorSessions[tut] = [0,0,0,0,0]
		tutorSessions[tut][dayNumber] = tutorSessions[tut][dayNumber] + 1
	
	def updateSessionDayNumber(self, sessionNumber, dayNumber, taskNumber):
		if taskNumber == 1:
			sessionNumber = sessionNumber + 1
			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1
			return [sessionNumber, dayNumber]
		if taskNumber == 2:
			sessionNumber = sessionNumber + 1
			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
			return [sessionNumber, dayNumber] 
	
	#This simplistic approach merely assigns each module and lab to a random tutor, iterating through the timetable.
	def randomModAndLabSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "lab")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	def backTrackModLabSchedule(self, timetableObj, dayNumber = 0, sessionNumber = 1, tutorCredits = {}):
		#If all days and sessions are filled return True
		if dayNumber == 5:
			return True
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		#Consider the session of a particular day and try assigning each tutor to it one by one
		for tut in self.tutorList:
			moduleOrLab = "module" if (dayNumber*10 + sessionNumber -1) < 25 else "lab" 
			if self.isValidTask2(timetableObj, tut, dayNumber, sessionNumber, tutorCredits, moduleOrLab):
			#tutorCredits is len(tutorList)x5 sized list with number of credits per day per tutor encoded in it
				#First 25 sessions are modules and the next 25 are labs
				
				timetableObj.addSession(days[dayNumber], sessionNumber, tut, self.moduleLabList[dayNumber*10 + sessionNumber - 1], moduleOrLab)
				self.addTutorCredits(tutorCredits, tut, dayNumber, moduleOrLab)

				[nextSessionNumber, nextDayNumber] = self.updateSessionDayNumber(sessionNumber, dayNumber, 2)
				if self.backTrackModLabSchedule(timetableObj, nextDayNumber, nextSessionNumber, tutorCredits):
					return True
				
				self.removeTutorCredits(tutorCredits, tut, dayNumber, moduleOrLab)
		
		#If no tutor can be assigned to this session on days[dayNumber] then return False
		return False

	def backTrackTask3(self, timetableObj, tutorCredits = {}, level = 1):
		#If all days and sessions are filled return True
		if level == 51:
			timetableObj.scheduleChecker(self.tutorList, self.moduleList)
			print("minCost:"+ str(self.minTtList[1]) + " timeTableObjCost:" + str(timetableObj.cost)) 
			if timetableObj.cost < self.minTtList[1]:
				self.minTtList[0] = copy.deepcopy(timetableObj)
				self.minTtList[1] = timetableObj.cost
			return
			
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		#Consider the session of a particular day and try assigning each tutor to it one by one
		for tut in self.tutorList:
			[dayNumber, sessionNumber] = self.levelToDaySessionNumber(level) 
			#print(str(dayNumber) + str(sessionNumber))

			moduleOrLab = "module" if (dayNumber*10 + sessionNumber -1) < 25 else "lab" 
			if self.isValidTask2(timetableObj, tut, dayNumber, sessionNumber, tutorCredits, moduleOrLab):
			#tutorCredits is len(tutorList)x5 sized list with number of credits per day per tutor encoded in it
				#First 25 sessions are modules and the next 25 are labs
				
				timetableObj.addSession(days[dayNumber], sessionNumber, tut, self.moduleLabList[dayNumber*10 + sessionNumber - 1], moduleOrLab)
				self.addTutorCredits(tutorCredits, tut, dayNumber, moduleOrLab)

				self.backTrackTask3(timetableObj, tutorCredits, level + 1)
				
				self.removeTutorCredits(tutorCredits, tut, dayNumber, moduleOrLab)
		
		#If no tutor can be assigned to this session on days[dayNumber] then return False
		#return False

	def isValidTask2(self, timetableObj, tut, dayNumber, sessionNumber, tutorCredits, moduleOrLab):
		isLab = False if moduleOrLab == "module" else True
		heCanTeach = timetableObj.canTeach(tut,self.moduleLabList[dayNumber*10 + sessionNumber -1], isLab)
		if tut in tutorCredits:
			has2CreditsToday = tutorCredits[tut][dayNumber] >= 2
			has4CreditsThisWeek = (sum(tutorCredits[tut]) >= 4)
		else:
			has2CreditsToday = False
			has4CreditsThisWeek = False
		
		return (heCanTeach and not has2CreditsToday and not has4CreditsThisWeek)

	def addTutorCredits(self, tutorCredits, tut, dayNumber, moduleOrLab):
		credit = 2 if moduleOrLab == "module" else 1
		if tut not in tutorCredits:
			tutorCredits[tut] = [0,0,0,0,0,0,0,0,0,0]
		tutorCredits[tut][dayNumber] = tutorCredits[tut][dayNumber] + credit
	
	def removeTutorCredits(self, tutorCredits, tut, dayNumber, moduleOrLab):
		credit = 2 if moduleOrLab == "module" else 1
		tutorCredits[tut][dayNumber] = tutorCredits[tut][dayNumber] - credit
	
	def levelToDaySessionNumber(self, level):
		if level%10 != 0:
			sessionNumber = level%10
		else:
			sessionNumber = 10
		dayNumber = (int)((level - sessionNumber)/10)

		return [dayNumber, sessionNumber]


				
























