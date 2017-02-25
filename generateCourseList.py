import requests
from bs4 import BeautifulSoup

url_roll_list = 'http://10.1.1.150/iitris/modules/academics/courses/course_roll_list'
url_authenticate = 'http://10.1.1.150/iitris/modules/user/user_authenticate.php'
url = "http://10.1.1.150/iitris/modules/academics/courses/course_roll_list"

s = requests.Session()

# authenticate
p = {'entry_post' : ''}
r = s.post(url_authenticate, data = p)

# get the list of courses
r = s.get(url)
soup = BeautifulSoup(r.text,'html.parser')

course_list = []
courses = soup.find_all('option')
for course in courses:
	course = course.get_text()
	course_list.append(course.split(' ')[1])

numCourses = len(course_list)
print('Number of Courses are: ',numCourses)
count = 0
printString = ''
student_db = {};
for course in course_list:
	# now load the course
	count = count + 1
	printString = 'Processing... ' + ' (' + str(count) + '/' + str(numCourses) +') ' + course
	print(printString,end='\r')
	p = {'course' : course}
	r = s.post(url, data = p)
	# print (r.text)

	# get your required data

	soup = BeautifulSoup(r.text,'html.parser')
	tr = soup.find_all('tr')
	titleFlag = False;
	for row in tr:
		td = row.find_all('td')

		if len(td) == 0:
			continue;
		elif not titleFlag:
			titleFlag = True;
			continue;

		entryNum = td[1].get_text()
		name = td[2].get_text()
		
		hasCourse = True;
		if td[4].get_text() == 'DROP':
			hasCourse == False;

		student_db.setdefault(entryNum,[])
		student = student_db.get(entryNum)
		if hasCourse:
			student.append(course);	

		# for col in td:
		# 	print(col.get_text())
	printString = 'Processed.... ' + ' (' + str(count) + '/' + str(numCourses) +') ' + course
	print(printString ,end='\r')

	# print(student_db)
nullString = ''
for i in range(len(printString)):
	nullString += ' '

print (nullString,end='\r')
print ('Completed ;)')

fo = open('details.txt','w')

keys = sorted(student_db.keys())
for key in keys:
	value = student_db.get(key)
	writeString = key +" "+ str(value).replace("[","]").replace("]","").replace("\'","")+"\n";
	fo.write(writeString)

fo.close()
#display student result
print(student_db)
