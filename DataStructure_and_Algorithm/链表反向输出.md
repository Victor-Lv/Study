##C++ list反向输出/反转实例##
&nbsp;&nbsp;&nbsp;&nbsp;给定一个单向链表，从尾到头输出其每个值。  
代码：  

	#include <iostream>
	#include "stdio.h"
	#include <list>
	#include <stack>
	using namespace std;

	//从尾到头输出list--1.递归方法 
	void list_reverse1(list<int> &mylist, list<int>::iterator &it)//传递引用比传值副本更高效 
	{
		if(mylist.empty()) //判断list是否为空,如果没有判断即便链表为空后面仍会执行一遍cout 
			return;
		it++;
		if(it != mylist.end())
		{
			list_reverse1(mylist, it);	
		}
		cout<<*(--it)<<endl; 
		/**
	 	*这里要注意一点是it是对象的引用或者理解为对象指针,
	 	*所以对它的值得修改(it++) 会影响递归的其他轮回。
	 	*所以最后输出时要进行--it
		*/ 
	}

		/**
	    *递归有个通病,就是当递归次数过长,比如这里的链表过长时,可能会导致函数调用栈溢出.
    	*可以用下面循环的方式实现避免这个问题. 
    	*/ 

	//从尾到头输出list--2.栈+循环方法
	    /**
    	* list是从头到尾循迹的,要将其从尾到头输出, 会想到stack栈结构,
    	*所以可以先把list一一取出放到stack暂存.然后后面只需要迭代输出stack即可.
    	*这个思想同样可以用于list的反转 
    	*/
	void list_reverse2(list<int> &mylist)
	{
		stack<int> mystack;
		if(mylist.empty()) //判断list是否为空,如果没有判断即便链表为空后面仍会执行一遍cout 
			return;
		list<int>::iterator it = mylist.begin();
		while(it != mylist.end())
		{
			mystack.push(*it);
			it++;
		}
		while(!mystack.empty())
		{
			cout<<mystack.top()<<endl;
			mystack.pop();	
		}
	}

	int main()
	{
		list<int> mylist;
		for(int i=0; i < 5; i++)
			mylist.push_back(i);
		list<int>::iterator it = mylist.begin();
	
	    //逆序输出 
    	cout<<"逆序输出" <<endl;
    	//list_reverse1(mylist, it);
    	list_reverse2(mylist);
    	
    	//顺序输出 
    	cout<<"顺序输出" <<endl;
    	for(it = mylist.begin(); it != mylist.end(); it++)
    		cout<<*it<<endl;
    	
    	
    	return 0;
    }

运行输出：

    逆序输出
    4
    3
    2
    1
    0
    顺序输出
    0
    1
    2
    3
    4
    
    --------------------------------
    Process exited after 0.01161 seconds with return value 0
    请按任意键继续. . .

###markdown插入整段代码时发现只有第一行被当做是代码怎么破：  
####选定其他的代码，继续摁一下ctrl+k插入代码键就ok了。