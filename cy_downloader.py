import requests
import re
from getpass import getpass

def login(user,password):
	login_data = {"log":user ,"pwd": password}
	a = s.post("https://www.cybrary.it/wp-login.php",login_data)

def course_menu():
	a = s.get("https://www.cybrary.it/")
	pattern = re.compile('\<a href\=\"(.+?course\/.+?)\"\>\<div class\=\"hp\_coursecard\"\>')
	courses = pattern.findall(a.content)
	return courses
	
def course_links(module_link):
	a = s.get(module_link)
	pattern = re.compile(r'\<a href\=\"(.*?)\" class\=\"title\".+?\>(.+?)\<\/a\>')
	modules = pattern.findall(a.content)
	return modules	

def download_file(filename,url):
	print "Writting to..." + filename
	a = requests.get(url)
	with open(filename,"wb") as f:
		for chunk in a.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
	print "done!"

def get_module(module_link):
	a = s.get(module_link)
	pattern = re.compile('\<iframe src\=\"(.+?)\"')
	link = pattern.findall(a.content)[0]
	a = requests.get(link,headers={'Host': 'player.vimeo.com', 'Referer': 'https://www.cybrary.it'})
	pattern = re.compile('progressive\"\:(.+?\])')
	videos = pattern.findall(a.content)[0]
	info_videos = eval(videos)
	for index,video in enumerate(info_videos):
		print (index,video['quality'])
	option = raw_input("Option: ")
	url = info_videos[int(option)]['url']
	download_file(module_link.split("/")[-2] + ".mp4",url)

s = requests.Session()
user = getpass("User: ")
password = getpass("Password: ")
login(user,password)
courses = course_menu()

for index,course in enumerate(courses):
	print str(index) + ". " + course.replace("_"," ")

option = raw_input("Option: ")
modules = course_links(courses[int(option)])

for index, module in enumerate(modules):
	print(index,module[1])

option = raw_input("Option: ")
get_module(modules[int(option)][0])
