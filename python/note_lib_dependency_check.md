[toc]

# python notes of lib dependency checker
*本文作者为吕浪（Victor Lv）,原出处为[Victor Lv's blog](http://langlv.me)([www.langlv.me](http://langlv.me))，转载请保留此句。*  

## 0.程序全文(based on python2.7 no python3)

```python

```

## 1.程序入口
阅读程序和程序的执行一样，先从main函数读起，如果程序没声明main函数入口，那么程序会从上往下执行，如果定义了main函数入口，会从main函数进去，`if __name__ == '__main__':`这句话就声明了程序的入口，一般写成：  
```python
if __name__ == '__main__':
	main()
```
这样子即可。  

## 2.在哪使用sys.exit()
但是在本次项目开发中，涉及到一些异常情况需要sys.exit退出系统，而我在main函数里面又不直接使用sys.exit，而是使用return返回函数，所以在这里的声明使用`sys.exit(main())`，实际上效果和在main函数里面使用sys.exit直接退出是一样的。  

## 3.sys.exit()用途
`sys.exit(number)`表示退出当前python程序的执行，注意是当前程序，因为经常看到系统不止运行一个程序，通常在一个程序（不管是python还是shell）还会继续开一个子线程去执行另一个程序，这里`sys.exit(num)`退出的只是当前执行的这个程序（线程），并不会终止整个父线程程序的执行，只是结束了该子程序执行之后返回了，而*num*值就是返回值，通过这个返回值我们可以判断sys.exit是正常执行完然后退出，还是遭遇异常中断退出。大多数语言（python、shell、C/C++）里面都是使用*0*来表示正常退出，而非0的返回值表示异常退出，但这只是人为的规定，习惯而已。`sys.exit(0)`和return 0的区别顾名思义了，`return 0`仅仅是函数返回，也就是函数不再往下执行剩余代码直接return，而`sys.exit(0)`则相对暴力，直接是不再执行该程序的所有剩余代码，直接退出程序。如果在程序的某个函数里你对于异常的处理是直接退出程序，那么用`sys.exit()`就好，但是如果你想把这个异常的处理交给上游函数来处理，那么`return num`回去，*强力甩锅*，哈哈，这也是一种风格，因为有时候去查找程序是否在某个地方使用`sys.exit()`退出挺麻烦的，如果你到处都用了这个方法，有时不知道程序在哪退出的还得去翻代码中的`sys.exit()`，所以就形成了一种风格是，我只在main函数里面`sys.exit()`，而其他子函数即便遇到异常，也是通过return不同的值来告诉父函数去让它来处理异常，比如`return 0/1/2...`或者`return "hello"/None`，对，就是这个`return None`，挺方便的，不管返回的是string还是int，我返回一个空`None`都可以，父函数就可以根据这个返回值来发现子函数执行出现了异常。  

## 4.global修改全局变量
python和shell里面都有全局变量和局部变量的区分，shell对于全局变量的修改是和C/C++一样直接改就行了的，但python特殊，如果你在某个函数（也就是非全局的作用域）里面想要修改全局变量的值，必须先这样声明`global var`，其中var是你之前声明的全局变量。没有这句话还想修改全局变量会报错。当然，如果你只是想read only全局变量，那么就不需要这句话。

## 5.if/elif/else
```python
if condition1:
	do something
elif condition2:
	do something
else:
	pass
```
没啥好说的，需要注意都需要在最后面加上冒号`:`即可，不要会报错。 
## 6.try/except/finally
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

## 7. list, tuple, dict, set
关于list,dict,set的选择问题，引用stackoverflow里面的一个回答：
> Do you just need an ordered sequence of items? Go for a list.
Do you just need to know whether or not you've already got a particular value, but without ordering (and you don't need to store duplicates)? Use a set.
Do you need to associate values with keys, so you can look them up efficiently (by key) later on? Use a dictionary.  

- - -

> list:链表,有序的项目, 通过索引进行查找,使用方括号”[]”;
tuple:元组,元组将多样的对象集合到一起,不能修改,通过索引进行查找, 使用括号”()”;
dict:字典,字典是一组键(key)和值(value)的组合,通过键(key)进行查找,没有顺序, 使用大括号”{}”;
set:集合,无序,元素只出现一次, 自动去重,使用”set([])”

list链表是顺序存储的，查找需要给出索引，可以动态修改（增加、删除）。  
tuple元组相当于“固定不变”的list。  
set集合是无序的元素集合，注意是value集合并不是key-value的形式，一般只用来存储并判断元素是否存在的。  
dict字典是key-value的形式，通过key来寻找value。

用法可参考：[Python中list,tuple,dict,set的区别和用法](http://www.cnblogs.com/soaringEveryday/p/5044007.html)

## 8. 使用函数减少重复性代码
例如常见的程序输入参数检查，在这里我用了一个error_throw()函数提示输入参数错误并终止程序。errot_throw()函数和usage()函数可以合并为usage()函数

## 9. 关于在何处import
对于经常用到例如在多个函数里面都会用到的模块，如os,sys等，在程序开头imort进来，对于特定的模块或者说仅在一处地方使用到的模块，应在使用到时才import进来，这样一来，当程序没执行到此处就退出时，并不会import模块进来增加代码量或者导致可能的import异常（特别是import网络上的模块）。

## 10. subprocess子进程模块	
如果在python程序中希望执行cmd命令，需要用subprocess模块，除了subprocess模块，其他的诸如
```python
os.system
os.spawn*
os.popen*
popen2.*
commands.*
```
模块已经不被推荐使用了（虽然上面的程序我还是用了os.popen()）。
subprocess使用方法：参见[subprocess — Subprocess management](https://docs.python.org/2/library/subprocess.html)或者[How to use subprocess popen Python?--stackoverflow](https://stackoverflow.com/questions/12605498/how-to-use-subprocess-popen-python)
(1)subprocess.call() / subprocess.check_output():
```python
#不需要读取stdout
subprocess.call(["ls", "-l"]) #逐一输入合并成list,自动添加空格
subprocess.call("ls -l") #把整条命令读入不需要[]

#如果需要读取子进程的stdout(标准输出)用check_output()
import subprocess

out = subprocess.check_output(['ls','-l'])
print out
```
(2)subprocess.Popen():
```python
from subprocess import Popen, PIPE

process = Popen(['swfdump', '/tmp/filename.swf', '-d'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
```




