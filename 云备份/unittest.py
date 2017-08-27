#!/usr/bin/python
# -*- coding: UTF-8 -*- 
'''
Unittest for lib dependency checker.
@author: victor.lyu@asml.com
'''
import lib_dependency_check

def get_module_name_test():
    try:
        assert "luatools" in LEVEL
        assert "canvas" in LEVEL
        assert "CommonService" in LEVEL
        assert "qtdebugger_luadebugger" in LEVEL
        assert "qtinfra_commongui" in LEVEL
        assert "pnp_externaltool" in LEVEL
        assert "qtgui_api" in LEVEL
    except:
        print "get_module_name_test fail"
    else:
        print "get_module_name_test success"

def cut_string_test():
    type1 = "target_link_libraries"
    file1 = os.path.join(ROOT,'lib','fem','result','CMakeLists.txt')
    f1 = open(file1, "r")
    list1 = ['femjob', 'mod', 'infra']
    try:
        text1 = f1.read()
        try:
            result1 = clip(text1,type1)
            assert result1 == list1
        except:
            print "cut_string_test fail(1)"
            print result1
            return
    finally:
        f1.close()
        
    type2 = "add_shared_wrapper_lib"
    file2 = os.path.join(ROOT,'qtgui','infra','CMakeLists.txt')
    f2 = open(file2, "r")
    list2 = ['infra', 'mod', 'util', 'qtgui_api']
    try:
        text2 = f2.read()
        try:
            result2 = clip(text2,type2)
            assert result2 == list2
        except:
            print "cut_string_test fail(2)"
            print result2
            return
    finally:
        f2.close()

    type3 = "add_whole_archive_lib"
    file3 = os.path.join(ROOT,'lib','fem','femjob','CMakeLists.txt')
    f3 = open(file3, "r")
    list3 = ['mask', 'mod', 'infra', 'util']
    try:
        text3 = f3.read()
        try:
            result3 = clip(text3,type3)
            assert result3 == list3
        except:
            print "cut_string_test fail(3)"
            print result3
            return
        else:
            print "cut_string_test success"
    finally:
        f3.close()
    
def level_test():
    try:
        assert LEVEL["smo"] == LEVEL_OF_SO
        assert LEVEL["qtdebugger"] == LEVEL_OF_SO
        assert LEVEL["pnp_lmcplusdebugger"] == LEVEL_OF_SO
        assert LEVEL["qtinfra_commongui"] == LEVEL_OF_A
        assert LEVEL["qttools_spy"] == LEVEL_OF_A
        assert LEVEL["infracomm"] == LEVEL_OF_A
    except:
        print "level_test fail"
    else:
        print "level_test success"
    
def path_test():
    global TEST
    TEST = True
    try:
        assert PATH_OF_LAST_LEVEL["exposure"] == os.path.join(ROOT,'lib','mask')
        assert PATH_OF_LAST_LEVEL["smo"] == os.path.join(ROOT,'lib')
        assert PATH_OF_LAST_LEVEL["qtdebugger_debugviewer"] == os.path.join(ROOT,'qtgui','debugger')
        assert PATH_OF_LAST_LEVEL["pnp_pyterminal"] == os.path.join(ROOT,'qtgui','plugin')
        assert PATH_OF_LAST_LEVEL["qtsmo"] == os.path.join(ROOT,'qtgui')
        assert PATH_OF_LAST_LEVEL["qttools_recorder"] == os.path.join(ROOT,'qtgui','tools')
    except:
        print "path_test fail"
    else:
        print "path_test success"
    
def dependence_test():
    try:
        lib_a1 = "infracomm"
        lib_a11 = "infra_process"
        lib_a2 = "exposure"
        qtgui_a1 = "qtlmc_conditionsetup"
        qtgui_a11 = "qtlmc_lmcreview"
        qtgui_a2 = "qtdebugger_luadebugger"
        lib_so = "infra"
        qtgui_so = "qtsmo"
        plugin_so = "pnp_femreview"
        unittest = "qtmask_layerwidget"
        whether_is_unittest = False
        assert check_dependence(lib_a1,lib_a11,whether_is_unittest) #lib .a -> lib .a(brother) : T
        assert check_dependence(qtgui_a1,qtgui_a11,whether_is_unittest) #qtgui .a -> qtgui .a(brother) : T
        assert check_dependence(qtgui_so,lib_so,whether_is_unittest) #qtgui .so -> lib .so : T
        assert check_dependence(qtgui_a2,lib_so,whether_is_unittest) #qtgui .a -> lib .so : T
        assert check_dependence(lib_a1,lib_so,whether_is_unittest) #lib .a -> lib .so : T
        assert check_dependence(plugin_so,qtgui_so,whether_is_unittest) #/qtgui/plugin .so -> qtgui .so : T
        assert check_dependence(plugin_so,lib_so,whether_is_unittest) #/qtgui/plugin .so -> lib .so : T
        whether_is_unittest = True
        assert check_dependence(unittest, qtgui_so,whether_is_unittest) #unittest -> .so T
        whether_is_unittest = False
        
        assert not check_dependence(plugin_so,lib_a1,whether_is_unittest) #/qtgui/plugin .so -> lib .a : F
        assert not check_dependence(plugin_so,qtgui_a1,whether_is_unittest) #/qtgui/plugin .so -> qtgui .a : F
        assert not check_dependence(lib_a1,lib_a2,whether_is_unittest) #lib .a -> lib .a(not brother) : F
        assert not check_dependence(qtgui_a11,qtgui_a2,whether_is_unittest) #qtgui .a -> qtgui .a(not brother) : F
        assert not check_dependence(lib_so,lib_a1,whether_is_unittest) #lib .so -> lib .a : F
        assert not check_dependence(lib_so,qtgui_so,whether_is_unittest) #lib .so -> qtgui .so : F
        assert not check_dependence(lib_a1,qtgui_so,whether_is_unittest) #lib .a -> qtgui .so : F
        assert not check_dependence(qtgui_a1,lib_a1,whether_is_unittest) #qtgui .a -> lib .a  : F
        whether_is_unittest = True
        assert not check_dependence(unittest, lib_a1,whether_is_unittest) #unittest -> .a F
        assert not check_dependence('pnp_imageprofile','qtinfra_imageprofile',False)
        assert not check_dependence('qtlmc_lmcreport','lmcjob',False)
    except:
        print "dependence_test fail"
    else:
        print "dependence_test success"
        


get_module_name_test()
level_test()
cut_string_test()
path_test()
dependence_test()
        
