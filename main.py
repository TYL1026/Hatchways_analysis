
import sys
import json
from copy import deepcopy
from json import JSONEncoder
class encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
class Mark:
	def __init__(self,test_id,student_id,mark):
		self.test_id = test_id
		self.student_id = student_id
		self.mark = mark

	def weightedMark(self,weight):
		return round(float(self.mark)*weight,2)

	def __str__ (self):
		return f"test_id:{self.test_id} student_id:{self.student_id} mark:{self.mark} "

class Test:
	def __init__(self,id,course_id,weight):
		self.id = id
		self.course_id = course_id
		self.weight = weight
	def __str__ (self):
		return f"id:{self.id} course_id:{self.course_id} weight:{self.weight} "

class Courses:
	def __init__(self,id,name,teacher,courseAverage):
		self.id = id
		self.name = name
		self.teacher = teacher
		self.courseAverage = courseAverage

	def updateAverage (self,newcourseAverage):
		new = round(self.courseAverage + newcourseAverage,2)
		self.courseAverage = new

	def __str__ (self):
		return f"id:{self.id} name:{self.name} teacher:{self.teacher} courseAverage:{self.courseAverage}"

class Student:
	def __init__(self,id,name,totalAverage,courses):
		self.id = id
		self.name = name
		self.totalAverage = totalAverage
		self.courses = courses

	def updateCourse(self,newCourse,weightedMark):
		#if we already appened this course, just update the average
		for course in self.courses:
			if newCourse.id == course.id:
				course.updateAverage(weightedMark)
				return
		#if not, append it 
		newCourse.updateAverage(weightedMark)
		self.courses.append(newCourse)
	def updateTotal(self):
		result = 0
		index = 0
		for course in self.courses:
			result += course.courseAverage
			index +=1
		self.totalAverage = round(result/index,2)
	def __str__ (self):
		return f"id:{self.id} name:{self.name} totalAverage:{self.totalAverage} courses:{self.courses}"

##class creation end here

def getMarkInfo(fileList):
	markFile = open(fileList[4])
	markInfo = []
	# 1.reading the test lit in courses.csv  
	# 2.put info in the Test class then into a list
	for line in markFile:
		line = line.rstrip().split(",")
		markInfo.append(Mark(line[0],line[1],line[2]))
	#pop the first line since it does not contain test information
	markInfo.pop(0)
	return markInfo


def getCourseInfo(fileList):
	courseFile = open(fileList[1])
	# 1.reading the course lit in courses.csv  
	# 2.put info in the Courses class then into a list
	courseInfo = []
	index = 0
	for line in courseFile:
		line = line.rstrip().split(",")
		courseInfo.append(Courses(line[0],line[1],line[2],0))
	#pop the first line since it does not contain course information

	courseInfo.pop(0)
	return courseInfo

def getTestInfo(fileList):
	testFile = open(fileList[3])
	testInfo = []
	for line in testFile:
		line = line.rstrip().split(",")
		testInfo.append(Test(line[0],line[1],line[2]))
	testInfo.pop(0)
	return testInfo

def getStudentInfo(fileList):
	stdentFile = open(fileList[2])
	stdentInfo = []
	for line in stdentFile:
		line = line.rstrip().split(",")
		stdentInfo.append(Student(line[0],line[1],0,[]))
	stdentInfo.pop(0)
	return stdentInfo

def updateStudent(markInfo,courseInfo,testInfo,studentInfo):
	id = 1
	#loop number is equal to the total number of marks
	# for every mark on the record
	for mark in markInfo:
		#find cooresponding student using the student_id
		student = studentInfo[int(mark.student_id)-1]
		#find cooresponding test using the test_id
		test = testInfo[int(mark.test_id)-1]
		#find course info using the course_id from test
		course = courseInfo[int(test.course_id)-1]
		#all 3 information is found
		#now calculate the weighted Mark for each test and add them together 
		weight = float(test.weight)/100
		weightedMark = mark.weightedMark(weight)
		#make a copy of course so updateAverage() will not affect next loop
		copy = deepcopy(course)
		student.updateCourse(copy,weightedMark)
		id+=1

def main():
	# this list contain all the input file. 
	fileList=[f for f in sys.argv]
	testInfo = getTestInfo(fileList)
	courseInfo = getCourseInfo(fileList)
	markInfo = getMarkInfo(fileList)
	studentInfo = getStudentInfo(fileList)
	newStudent = updateStudent(markInfo,courseInfo,testInfo,studentInfo)
	
	# for student in studentInfo:
	# 	print (student.id)
	# for course in student.courses:
	# 	print(course)
	# print('testInfo-----------------------------------')
	# for e in testInfo:
	# 	print (e)
	# print('courseInfo-----------------------------------')
	# for e in courseInfo:
	# 	print (e)
	# print('markInfo-----------------------------------')
	# for e in markInfo:
	# 	print (e)
	# print('studentInfo-----------------------------------')
	# for e in studentInfo:
	# 	print (e)
	# print('-----------------------------------')
	# 
	# print('-----------------------------------')

	for student in studentInfo:
		student.updateTotal()
	output = open("test.json","w+")
	output.write(json.dumps(studentInfo, indent=4, cls=encoder))

main()