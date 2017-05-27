[toc]

# python notes of lib dependency checker
*本文作者为吕浪（Victor Lv）,原出处为[Victor Lv's blog](http://langlv.me)([www.langlv.me](http://langlv.me))，转载请保留此句。*
##0.程序全文(based on python2.7)

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*- 
'''
Lib dependency check of lib and qtgui.
@author: Victor Lv
'''

import os
import sys
import getopt

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT = ""
LEVEL = {} #an dictionary which express the LEVEL(.so:1, .a:2) of dir
PATH_OF_LAST_LEVEL = {}
LEVEL_OF_SO = 1
LEVEL_OF_A = 2
CURRENT_LEVEL = LEVEL_OF_SO #1 means .so LEVEL, 2 means .a LEVEL
ERROR_COUNT = 0 #count the error of lib dependency

############## 1: construct level tree	##############
def cut_string(fileText, index1, index2):
	str = fileText[index1+1:index2] 
	list1 = str.split(" ")
	list2 = map(lambda s: s.strip(), list1) #remove \n in list
	list3 = filter(None, list2) #remove empty item in list
	return list3
 
def divide_and_cut_string(fileText,stringType):
	index1 = fileText.index(stringType)
	index2 = fileText.index('(', index1)
	index3 = fileText.index(')', index2)
	#cut out the string between '()')
	return cut_string(fileText, index2, index3)
 
def get_new_name(fileText,stringType):
	newName = divide_and_cut_string(fileText,stringType)[0]
	return newName
 
def find_and_get_name(fileText):
	newName = ""
	if fileText.find("target_link_libraries") != -1:
		newName = get_new_name(fileText,"target_link_libraries")
	elif fileText.find("TARGET_LINK_LIBRARIES") != -1:
		newName = get_new_name(fileText,"TARGET_LINK_LIBRARIES")
	elif fileText.find("add_shared_wrapper_lib") != -1:
		newName = get_new_name(fileText,"add_shared_wrapper_lib")
	elif fileText.find("add_whole_archive_lib") != -1:
		newName = get_new_name(fileText,"add_whole_archive_lib")
	else:
		return None
	return newName
 
def tag_and_rename(dirName):
	global LEVEL
	path_of_cmake_file = os.path.join(os.getcwd(),dirName,"CMakeLists.txt")
	if os.path.exists(path_of_cmake_file):
		f = open(path_of_cmake_file, "r")
		try:
			fileText = f.read()
			name = find_and_get_name(fileText)
		finally:
			f.close()
		if name == None or name == "" or name == " ":
			name = dirName
		if name not in LEVEL:
			LEVEL[name] = CURRENT_LEVEL
			PATH_OF_LAST_LEVEL[name] = os.getcwd()
		elif LEVEL[name] > CURRENT_LEVEL: #when name conflicts, save the higher LEVEL(.so) name
			LEVEL[name] = CURRENT_LEVEL
			PATH_OF_LAST_LEVEL[name] = os.getcwd()
	else:
		if dirName not in LEVEL and dirName not in PATH_OF_LAST_LEVEL:
			LEVEL[dirName] = CURRENT_LEVEL
			PATH_OF_LAST_LEVEL[dirName] = os.getcwd()

#attach label for all dirs in path
def tag():
	for name in os.listdir("./"):
		if os.path.isdir(os.path.join("./", name)):
			tag_and_rename(name)
	
def attach_level(dirName):
	global CURRENT_LEVEL
	os.chdir(os.path.join(ROOT,dirName)) #chdir ./lib ./qtgui
	tag()#.so LEVEL
	CURRENT_LEVEL = LEVEL_OF_A
	for name in os.listdir("./"):
		if os.path.isdir(os.path.join("./", name)):
			os.chdir(os.path.join("./", name))
			tag() #.a LEVEL
			os.chdir("./..")
	os.chdir(ROOT)

###############   2: check dependence	###################
def toDir_is_so_level(toDir):
	if LEVEL[toDir] == LEVEL_OF_SO:
		return True
	else:
		return False

def is_lib_link_to_qtgui(fromDir, toDir):
	qtgui_start = os.path.join(ROOT,'qtgui')
	lib_start = os.path.join(ROOT,'lib')
	if lib_start in PATH_OF_LAST_LEVEL[fromDir] and qtgui_start in PATH_OF_LAST_LEVEL[toDir]:
		return True
	return False
	
def is_brother(fromDir, toDir):
	if fromDir in PATH_OF_LAST_LEVEL and toDir in PATH_OF_LAST_LEVEL:
		if PATH_OF_LAST_LEVEL[fromDir] == PATH_OF_LAST_LEVEL[toDir]:
			return True
		else:
			return False
	else:
		return True

#check the dependence of dir1 -> dir2
def dependence_is_true(fromDir, toDir, fromDir_is_unittest):
	if fromDir_is_unittest:
		if toDir_is_so_level(toDir):
			return True
		else:
			return False
	#Dirs in lib cannot link to dirs in qtgui"
	elif is_lib_link_to_qtgui(fromDir, toDir):
		return False
	elif toDir_is_so_level(toDir):
		return True
	#check whether the two nodes are brother-german
	elif is_brother(fromDir, toDir):
		return True
	else:
		return False

def check_dependence(fromDir, toDir, fromDir_is_unittest):
	if toDir != "util": #ignore util
		if dependence_is_true(fromDir, toDir, fromDir_is_unittest):
			return True
		else:
			return False
		
########### 	extract out the dependence	##########
def is_key(name):
	if name in LEVEL:
		return True
	else:
		return False

#remove libs that aren't keys of LEVEL dictionary
def clip_out_key_libs(list):
	libList = []
	for lib in list:
		if is_key(lib):
			libList.append(lib)
	if libList: #not empty
			return libList
	else:
		return None

def clip(fileText,stringType):
	LEN_OF_LIB_DEPENDS = 11
	if stringType == "target_link_libraries" or stringType == "TARGET_LINK_LIBRARIES":
		list = divide_and_cut_string(fileText,stringType)
		list.pop(0) #remove the first name
		return clip_out_key_libs(list)
				
	elif stringType == "add_shared_wrapper_lib":
		if fileText.find("LIB_DEPENDS") != -1:
			index1 = fileText.index(stringType)
			#cut out the string between 'LIB_DEPENDS' and 'WHOLE_ARCHIVE_LIBS'
			index2 = fileText.index('LIB_DEPENDS', index1)
			index3 = fileText.index('WHOLE_ARCHIVE_LIBS', index2)
			list = cut_string(fileText, index2+LEN_OF_LIB_DEPENDS, index3)
			result = clip_out_key_libs(list)
			return result
		
	elif stringType == "add_whole_archive_lib":
		if fileText.find("LIB_DEPENDS") != -1:
			index1 = fileText.index(stringType)
			#cut out the string between 'LIB_DEPENDS' and ')'
			index2 = fileText.index('LIB_DEPENDS', index1)
			index3 = fileText.index(')', index2)
			list = cut_string(fileText, index2+LEN_OF_LIB_DEPENDS, index3)
			result = clip_out_key_libs(list)
			return result
	else:
		return None
		
def find_and_clip(fileText): #return a list []
	if fileText.find("target_link_libraries") != -1:
		return clip(fileText,"target_link_libraries")
	elif fileText.find("TARGET_LINK_LIBRARIES") != -1:
		return clip(fileText,"TARGET_LINK_LIBRARIES")
	elif fileText.find("add_shared_wrapper_lib") != -1:
		return clip(fileText,"add_shared_wrapper_lib")
	elif fileText.find("add_whole_archive_lib") != -1:
		return clip(fileText,"add_whole_archive_lib")
	else:
		return None

#throw error if there's STATIC in add_library()
def check_static(fileText,dirName):
	if fileText.find("add_library") != -1:
		index1 = fileText.index("add_library")
		index2 = fileText.index(")",index1)
		if fileText[index1:index2].find("STATIC") != -1:
			print "Keyword STATIC cannot exist in add_library()."
			print "Path is " + os.path.join(os.getcwd(),dirName)
			print

def is_in_whitelist(fromName, toName):
	whitelist_path = os.path.join(SCRIPT_PATH,'whitelist_of_lib_dependency_check.txt')
	if os.path.exists(whitelist_path):
		try:
			f = open(whitelist_path,'r')
			for l in f.readlines():
				if not l.startswith('#'):
					list = filter(None, map(lambda s: s.strip(), l.split(" ")))
					if cmp(list, [fromName, toName]) == 0:
						return True
						break
			return False
		finally:
			f.close()
'''
def add_whitelist(fromName, toName):
	whitelist_path = os.path.join(ROOT,'BCTools','LibDependencyChecker','whitelist_of_lib_dependency_check.txt')
	if os.path.exists(whitelist_path):
		try:
			f = open(whitelist_path,'a')
			f.write(fromName + " " +  toName + '\n')
		except:
			print "Cannot open the whitelist_of_lib_dependency_check.txt in write mode. Please check the authority of file."
		finally:
			f.close()
'''
def find_and_check_dependence(dirName):
	path_of_cmake_file = os.path.join(os.getcwd(),dirName,"CMakeLists.txt")
	f = open(path_of_cmake_file, "r")
	try:
		fileText = f.read()
		name = find_and_get_name(fileText)
	finally:
		f.close()
	check_static(fileText, dirName) #throw error if there's STATIC in add_library()
	if name == None or name == "" or name == " ":
		name = dirName
	if dirName == "unittest":
		fromDir_is_unittest = True
	else:
		fromDir_is_unittest = False
	clipResult = find_and_clip(fileText)
	if clipResult != None:
		for lib in clipResult:
			if not is_in_whitelist(name,lib):
				if check_dependence(name, lib, fromDir_is_unittest) == False:
					global ERROR_COUNT
					ERROR_COUNT += 1
					print "Lib dependency of: " + name + " -> " + lib + " is false."
					print "Path is " + os.path.join(os.getcwd(),dirName)
					print
		
def dependence_checker(dirName):
	os.chdir(os.path.join(ROOT,dirName))
	for name1 in os.listdir("./"):
		if os.path.isdir(os.path.join(os.getcwd(), name1)):
			if os.path.exists(os.path.join(os.getcwd(),name1,"CMakeLists.txt")):
				find_and_check_dependence(name1)
			os.chdir(os.path.join(os.getcwd(),name1))
			for name2 in os.listdir("./"):
				if os.path.isdir(os.path.join(os.getcwd(), name2)):
					if os.path.exists(os.path.join(os.getcwd(),name2,"CMakeLists.txt")):
						find_and_check_dependence(name2)
					os.chdir(os.path.join(os.getcwd(),name2))
					#check unittest dir
					if os.path.exists(os.path.join(os.getcwd(),'unittest','CMakeLists.txt')):
						find_and_check_dependence("unittest")
					os.chdir("./..")
			os.chdir("./..")

def init_contruct():
	global CURRENT_LEVEL
	os.chdir(ROOT)
	#construct the level tree
	attach_level("lib")	
	CURRENT_LEVEL = LEVEL_OF_SO #reset current level
	attach_level("qtgui")

	#especially /qtgui/plugin is an unreal .so level whose subdirs are .so level
	CURRENT_LEVEL = LEVEL_OF_SO
	os.chdir(os.path.join(ROOT,'qtgui','plugin'))
	tag()

def check_dependence_error():
	os.chdir(ROOT)
	dependence_checker("lib")
	dependence_checker("qtgui")
	
def usage():
	print """
Usage: python lib_dependency_check.py [-r] [-c] [-h]
where:
-r/--root ROOT_PATH: 
	Provide the parent path where lib and qtgui dirs locate in(absolutely path needed).
	The script will search the root automatically if root path wasn't provided.
-c/--changelist changelist_id:
	Provide the changlist id to check whether the pending files are in lib/qtgui.
	If yes, triggers the lib dependency check.
-h/--help: 
	Prints this message and exits.
"""

def error_throw(error_message):
	print error_message
	usage()
	sys.exit(1)

def root_has_lib_and_qtgui_dirs(ROOT):
	if os.path.exists(os.path.join(ROOT,'lib')) and os.path.exists(os.path.join(ROOT,'qtgui')):
		return True
	else:
		return False

def changelist_affects_lib_dependency(depotFiles):
	import re
	
	affect_position = 0
	for line in depotFiles:
		if re.search(r'//depot/tachyon/tachyon-RDI-10/(lib|qtgui)/.*CMakeLists.txt', line):
			return affect_position
		
		affect_position += 1
	#connot match r"//depot/tachyon/tachyon-RDI-10/(lib|qtgui)/"
	return None

def find_lib_and_qtgui_from_dir(dirpath):
	dir_list = os.listdir(dirpath)
	if 'qtgui' in dir_list and 'lib' in dir_list:
		return True
	else:
		return False

def convert_local_path_into_root(local_path_of_file):
	path = os.path.dirname(os.path.realpath(local_path_of_file))
	count = 0
	while not find_lib_and_qtgui_from_dir(path):
		path = os.path.dirname(path)
		if count >= 4:
			print "Cannot found lib&qtgui root."
			return None
		count += 1
	return path

def find_the_root(path):
	comm = 'p4 where ' + path
	try:
		output = os.popen(comm) # run the command to get absolutely local path
		ret = output.read()
	except:
		print "Cannot get the local path"
		return None
	finally:
		output.close()
	
	local_path_of_file = ret.split(" ")[2]
	return convert_local_path_into_root(local_path_of_file)

def check_changelist(changelist_id):
	try:
		comm = 'p4 -ztag opened -c ' + changelist_id
		
		import platform
		
		linux_comm = comm + ' | grep depotFile'
		mswindows_comm = comm + ' | findstr depotFile'
		comm_get_depot_path = ''
		if platform.system() == 'Windows':
			comm_get_depot_path = mswindows_comm
		else:
			comm_get_depot_path = linux_comm
		
		output = os.popen(comm_get_depot_path) # run the command to get depotFile path
		lines = output.readlines()
	except:
		print "\nException: Cannot get the clienFile according to the changelist.\n"
		return None
	finally:
		output.close()
	
	paths = []
	for line in lines:
		paths.append(line.split(' ')[-1])  #get the depotFile path
	
	paths = map(lambda s: s.strip(), paths) #remove \n in list
	
	ret = changelist_affects_lib_dependency(paths)
	if ret == None:
		#print "Do not affect lib dependency, checker will not be triggerred."
		return None
	print "\nThe file change triggers lib dependency checker.\n"
	return find_the_root(paths[ret])
	
def main():
	print "\n===> lib dependency checking ...\n"
	global ROOT
	if not sys.argv == None:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'hc:r:', ['help','changelist=','root='])
		except getopt.GetoptError:
			error_throw("Error: invalid parameters")
			
		flag_of_root = False
		
		for opt, arg in opts:
			if opt in ['-h', '--help']:
				usage()
				sys.exit(0)
				
			elif opt in ['-c', '--changelist']:
				changelist_id = arg
				ret = check_changelist(changelist_id)
				if ret == None: 
					#print "\nCannot find the root path for lib dependency checker.\n"
					print "\n===> lib dependency done\n"
					return 0
				else:
					ROOT = ret
					flag_of_root = True
					
			elif opt in ['-r', '--root']:
				path = arg
				flag_of_root = True
				ROOT = path
				if not root_has_lib_and_qtgui_dirs(ROOT):
					error_throw("Error: this path doesn't contain lib and qtgui dirs, please check your input.")
				if not os.path.isabs(ROOT):
					error_throw("Error: please input the absolute path.")
					
			else:
				error_throw("Error: invalid parameters.")
				
	if not flag_of_root: #search the root automatically if root path wasn't provided
		ROOT = os.path.join(SCRIPT_PATH,'../../..','depot/tachyon/tachyon-RDI-10')
		if not root_has_lib_and_qtgui_dirs(ROOT):
			#print "\nCannot search the real root automatically.\n"
			print "\n===> lib dependency check done\n"
			return 0 #do not throw error
	
	print "Root path to check is: " + ROOT + "\n"
						
	init_contruct()
	check_dependence_error()
	print "Total lib_dependency error found: ",ERROR_COUNT
	print "\n===> lib dependency done\n"
	return ERROR_COUNT

if __name__ == '__main__':
	sys.exit(main())
```

##1.程序入口
阅读程序和程序的执行一样，先从main函数读起，如果程序没声明main函数入口，那么程序会从上往下执行，如果定义了main函数入口，会从main函数进去，`if __name__ == '__main__':`这句话就声明了程序的入口，一般写成：  
```python
if __name__ == '__main__':
	main()
```
这样子即可。  

##2.在哪使用sys.exit()
但是在本次项目开发中，涉及到一些异常情况需要sys.exit退出系统，而我在main函数里面又不直接使用sys.exit，而是使用return返回函数，所以在这里的声明使用`sys.exit(main())`，实际上效果和在main函数里面使用sys.exit直接退出是一样的。  

##3.sys.exit()用途
`sys.exit(number)`表示退出当前python程序的执行，注意是当前程序，因为经常看到系统不止运行一个程序，通常在一个程序（不管是python还是shell）还会继续开一个子线程去执行另一个程序，这里`sys.exit(num)`退出的只是当前执行的这个程序（线程），并不会终止整个父线程程序的执行，只是结束了该子程序执行之后返回了，而*num*值就是返回值，通过这个返回值我们可以判断sys.exit是正常执行完然后退出，还是遭遇异常中断退出。大多数语言（python、shell、C/C++）里面都是使用*0*来表示正常退出，而非0的返回值表示异常退出，但这只是人为的规定，习惯而已。`sys.exit(0)`和return 0的区别顾名思义了，`return 0`仅仅是函数返回，也就是函数不再往下执行剩余代码直接return，而`sys.exit(0)`则相对暴力，直接是不再执行该程序的所有剩余代码，直接退出程序。如果在程序的某个函数里你对于异常的处理是直接退出程序，那么用`sys.exit()`就好，但是如果你想把这个异常的处理交给上游函数来处理，那么`return num`回去，*强力甩锅*，哈哈，这也是一种风格，因为有时候去查找程序是否在某个地方使用`sys.exit()`退出挺麻烦的，如果你到处都用了这个方法，有时不知道程序在哪退出的还得去翻代码中的`sys.exit()`，所以就形成了一种风格是，我只在main函数里面`sys.exit()`，而其他子函数即便遇到异常，也是通过return不同的值来告诉父函数去让它来处理异常，比如`return 0/1/2...`或者`return "hello"/None`，对，就是这个`return None`，挺方便的，不管返回的是string还是int，我返回一个空`None`都可以，父函数就可以根据这个返回值来发现子函数执行出现了异常。  

##4.global修改全局变量
python和shell里面都有全局变量和局部变量的区分，shell对于全局变量的修改是和C/C++一样直接改就行了的，但python特殊，如果你在某个函数（也就是非全局的作用域）里面想要修改全局变量的值，必须先这样声明`global var`，其中var是你之前声明的全局变量。没有这句话还想修改全局变量会报错。当然，如果你只是想read only全局变量，那么就不需要这句话。

##5.if/elif/else
```python
if condition1:
	do something
elif condition2:
	do something
else:
	pass
```
没啥好说的，需要注意都需要在最后面加上冒号`:`即可，不要会报错。 
##6.try/except/finally
`try`里面的语句就是*尝试去做*，`except`表示处理try里面抛出来的异常，可以直接`except:`处理所有异常，也可以只处理单个异常`except ValueError:`或多个异常`except (RuntimeError, TypeError, NameError)`,至于在列表里的异常？who care.我不管了，也就是不会进去except直接去执行finally语句去了。  
在开发中，关于try/except/finally发现过一个奇葩的报错：
> finally:
>           ^
> SyntaxError: invalid syntax

明明缩进和语法都没有错误，在本地run也通过，却在别的地方运行时给我来这么一壶，而且对于`SyntaxError: invalid syntax`这样的报错真是一脸瞢币啊，相比python还是喜欢其他语言有更具体的报错信息给出。还好，有强大的*google*和*stackoverflow*，一查问答，发现是因为python版本的问题，python2.5或以上版本才支持try-except-finally直接写在一块，而python2.4或更低的版本只能单独使用try-except或try-finally。
> try except finally was only added in 2.5 and before you had to wrap try except in a try finally. 

```python
#/usr/bin/python2.6

try:
    print 'try'
except:
    print 'except'
finally:
    print 'finally'



#/usr/bin/python2.4

try:
    try:
        print 'try'
    except:
        print 'except'
finally:
    print 'finally'
```
看来python版本变化这一老大难问题不仅在于python2和python3之间，但就python2.4和python2.5也有地方不兼容，不过这也不怪语言设计者，毕竟他们只是想把语言设计得更好。应该怪python编译版本，在Linux服务器你给我整个python2.4来运行我基于python2.7写的程序？够我吃一壶的，而且服务器这东西不是自己的电脑，我看不顺眼就可以直接升了python2.7就完事了。你必须去修改你的代码去兼容python2.4，而不是让它来兼容你的代码。  
不过好在最后我也不需要去逐一改代码，那得多大工作量啊，当时想到要全部改掉程序里的try-except-finally我差点崩溃，还好我机智，想到能不能翻一翻看服务器里面有没有更高版本的python。因为我不能直接登录到服务器去跑终端脚本，只能通过在python脚本里面嵌入这样的一句去print出pathon版本：  
```python
Python 2.4-:

python -c 'import sys; print(sys.version)'

Python 2.5+:

python --version / python -V
```
不对，这只是我拿来查看print python版本的，实际上我是手动测试各种python版本，也就是这样`python2.7 -V`，这样`python3 -V`，这样`python2.5 -V`，逐个试试，如果没有报错，那个版本就是有的，最后被我发现服务器里面有python2.7版本的，所以搞定，只需要在执行python脚本时，使用`python2.7 file.py`指定用python2.7而不是默认的`python`运行程序即可。





















