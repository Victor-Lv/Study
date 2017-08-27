#!/usr/bin/python
# -*- coding: UTF-8 -*- 
'''
Lib dependency check of lib and qtgui.
@author: victor.lyu@asml.com
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

