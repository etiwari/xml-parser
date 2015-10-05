#!/usr/bin/env python
import sys
import optparse
import re

parser = optparse.OptionParser()
parser.add_option('-r', '--read', action="store_true" , dest="read", default=False, help="reads the file with read logs")
parser.add_option('-e', '--eventsearch', dest="eventsearch", help="performs search based on Windows Event ID")
parser.add_option('-w', '--write', action="store_true" , dest="write", default=False, help="writes all the data sequencially")
parser.add_option('-u', '--usearch', dest="usearch", help="performs search based on Username")
parser.add_option('-l', '--lsearch', action="store_true", dest="lsearch", default=False, help="Lists all distinct Event IDs")

(options, args) = parser.parse_args()
FilePath = None
if len(sys.argv) == 2:
	FilePath = sys.argv[1]
elif len(sys.argv) == 1:
	FilePath = raw_input('Enter XML log File Path: ')
else:
	print "Invalid Syntax"
	sys.exit(0)	
f = open(FilePath,'r')
list = []
#readlog=False
class Event:
	def __init__(self):
		self.execution = self.Execution()
		#self.eventdata = self.EventData()
		self.EventID = ""
		self.Version = ""
		self.Level = ""
		self.Task = ""
		self.Opcode = ""
		self.Keywords = ""
		self.TimeCreated = ""
		self.SecurityUserID = ""
		self.EventRecordID = ""
		self.Channel = ""
		self.Computer = ""
		self.eventdatalist = []
	def writeEvent(self):
		print "Event ID: " + self.EventID
		print "Version: " + self.Version
		print "Level: " + self.Level
		print "Task: " + self.Task
		print "Opcode: " + self.Opcode
		print "Keywords: " + self.Keywords
		print "Time Stamp: " + self.TimeCreated
		print "Event Record ID: " + self.EventRecordID
		print "Channel: " + self.Channel
		print "Computer: " + self.Computer
		print "User ID (Security): " + self.SecurityUserID
		self.execution.writeExecution()
		print "\n-------------Data-----------------"
		for data in self.eventdatalist:
			data.writeEventData()
	class Execution:
		def __init__(self):
			self.ProcessID = ""
			self.ThreadID = ""
		def writeExecution(self):
			print "ProcessID: " + self.ProcessID + "\tThreadID: " + self.ThreadID
class EventData:
	def __init__(self):
		self.Name = ""
		self.Content = ""
	def writeEventData(self):
		print "\nData Name: " + self.Name
		print "Data: \t" + self.Content
def readfile():
	eventdataBool = False
	#DataBool = False
	EventCount = 0
	ifcheck = 0
	line = f.readline()
	while "</Events>" not in line:
		line = f.readline()
		line = line.strip('\t\n')
		if line.startswith("<Event xmlns="):			
			temp = Event()
			#temp.writeEvent()
			if readlog:
				EventCount+=1
				print "NEW Event " + str(EventCount) + "\t lines: " + str(ifcheck)
				ifcheck = 0
		if ("</Event>" not in line) & (line != "\n"):
			ifcheck+=1
			if line.startswith("<EventID>"):
				line = re.sub('<EventID>','',line)
				line = re.sub('</EventID>','',line)
				temp.EventID = line
			elif line.startswith("<Version>"):
				line = re.sub('<Version>','',line)
				line = re.sub('</Version>','',line)
				temp.Version = line
			elif line.startswith("<Level>"):
				line = re.sub('<Level>','',line)
				line = re.sub('</Level>','',line)
				temp.Level = line
			elif line.startswith("<Task>"):
				line = re.sub('<Task>','',line)
				line = re.sub('</Task>','',line)
				temp.Task = line
			elif line.startswith("<Opcode>"):
				line = re.sub('<Opcode>','',line)
				line = re.sub('</Opcode>','',line)
				temp.Opcode = line
			elif line.startswith("<Keywords>"):
				line = re.sub('<Keywords>','',line)
				line = re.sub('</Keywords>','',line)
				temp.Keywords = line
			elif line.startswith("<TimeCreated"):
				line = re.sub('<TimeCreated SystemTime="','',line)
				line = re.sub('" />','',line)
				temp.TimeCreated = line
			elif line.startswith("<Security"):
				line = re.sub('<Security UserID="','',line)
				line = re.sub('" /></System>','',line)
				temp.SecurityUserID = line
			elif line.startswith("<EventRecordID>"):
				line = re.sub('<EventRecordID>','',line)
				line = re.sub('<EventRecordID>','',line)
				temp.EventRecordID = line
				#temp.writeEvent()
			elif line.startswith("<Execution"):
				line = re.sub('<Execution>','',line)
				line = re.sub('</Execution>','',line)
				arr = line.split(' ')
				for attribute in arr:
					if attribute.startswith("ProcessID="):
						attribute = re.sub('ProcessID="','',attribute)
						temp.execution.ProcessID = attribute.rstrip('"')
					elif attribute.startswith("ThreadID="):
						attribute = re.sub('ThreadID="','',attribute)
						temp.execution.ThreadID = attribute.rstrip('"')
			elif line.startswith("<Channel>"):
				line = re.sub('<Channel>','',line)
				line = re.sub('</Channel>','',line)
				temp.Channel = line
			elif line.startswith("<Computer>"):
				line = re.sub('<Computer>','',line)
				line = re.sub('</Computer>','',line)
				temp.Computer = line
				#temp.writeEvent()
			elif "<EventData>" in  line:
				eventdataBool = True
			elif eventdataBool == True:
				#This is creating a new data element each line read. We dont need that
				DataElement = EventData()
				if ("<Data" in line) & ("</Data>" in line) & ("</EventData>" in line):
					eventdataBool = False
					#DataBool = False
					line = re.sub('<Data ','',line)
					line = re.sub('</Data>','',line)
					line = re.sub('</EventData>','',line)
					arr = line.split('>')
					for attribute in arr:
						if attribute.startswith("Name="):
							attribute = re.sub('Name=','',attribute)
							DataElement.Name = attribute.rstrip('"')
						else:
							attribute = attribute.rstrip('"')
							DataElement.Content = attribute
					#temp.writeEvent()					
					list.append(temp)
				elif ("<Data" in line) & ("</Data>" in line):
					line = re.sub('<Data ','',line)
					line = re.sub('</Data>','',line)
					arr = line.split('>')
					for attribute in arr:
						if attribute.startswith("Name="):
							attribute = re.sub('Name="','',attribute)
							DataElement.Name = attribute.rstrip('"')
						else:
							attribute = attribute.rstrip('"')
							DataElement.Content = attribute
					#DataBool = False
				elif "<Data" in line:
					#DataBool = True
					line = re.sub('<Data Name="','',line)
					DataElement.Name = line.rstrip('">')
					line = f.readline()
					while ("</Data>" not in line):
						line = line.strip('\t\n')
						DataElement.Content += (line + "\n\t")
						line = f.readline()
				temp.eventdatalist.append(DataElement)
def writefile():
	i=1
	choice = 'y'
	for obj in list:
		print "---------------------Event " + str(i) + "-----------------------"
		obj.writeEvent()
		choice = raw_input('Do you wish to continue?(y/n)')
		i+=1
		if choice == 'n':
			break
def EventIDSearch(EventID):
	i=1
	choice = 'y'
	for obj in list:
		if obj.EventID == EventID:
			print "---------------------Event " + str(i) + "-----------------------"
			obj.writeEvent()			
			#print "Time Stamp: " + obj.TimeCreated
			#for DataElement in obj.eventdatalist:
			#	if DataElement.Name == "SubjectUserName":
			#		DataElement.writeEventData()
			choice = raw_input('Do you wish to continue?(y/n)')
			if choice == 'n':
				break
			i+=1
	print "-------------------------\nMatches viewed: " + str(i)
def UserSearch(Username):
	i=1
	for obj in list:
		for DataElement in obj.eventdatalist:
			if DataElement.Name == "SubjectUserName":
				if DataElement.Content == Username:
					print "---------------------Event " + str(i) + "-----------------------"
					obj.writeEvent()
					i+=1
	print "-------------------------\nMatches found: " + str(i)
def ListEvent():
	i=0
	EventIDList = []
	#EventIDList.append("5447")
	#print EventIDList
	for obj in list:
		if obj.EventID != "5447" and obj.EventID not in EventIDList:
			EventIDList.append(obj.EventID)
			i+=1
			#print "object: " + str(i)
	EventIDList.sort()
	#print EventIDList
	ff = open('./WEID.txt','r')
	for line in ff:
		arr = line.split(',')
		if arr[0] in EventIDList:
			print arr[0] + "\t" + arr[1].rstrip('\n')
	print "Security.xml also includes Event ID: 5447, A Windows Filtering Platform filter has been changed"
readlog=True
readfile()
readlog=False
if options.read:
	readlog=True
	readfile()
if options.eventsearch != None:
	readfile()
	EventIDSearch(options.eventsearch)
if options.write:
	readfile()
	writefile()
if options.usearch != None:
	readfile()
	UserSearch(options.usearch)
if options.lsearch:	
	readfile()
	print "------------------------------------------------------------------\n" 
	print "These are the following Event types present in the Security logs:\n"
	ListEvent()
	eventsearch2 = raw_input('Enter Event ID: ')
	EventIDSearch(eventsearch2)
