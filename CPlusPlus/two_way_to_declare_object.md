##C++定义类和对象的两种方式--对比Java##

搞了一段时间java再回来搞C++，在有些地方会偶尔不太适应，例如，这里要说的对象的声明，Java和C++就有很大的不同。  
比如说这里有一个类：  

    //C++方式定义一个class
	class Son :public Dad 
	{
	private:
		const int count;
	public:
	    Son()
		{
			cout<<"Son's constructor"<<endl;
		}
	    void sayName()
	    {
	        cout<<"I am Son"<<endl;
	    }
	    ~Son()
	    {
	        cout<<"Son's destructor"<<endl;
	    }
	};

	//java方式定义一个class
	class Son extends Dad
	{
		private final int count;
		
		public Son(){}
		public void sayName(){}
	}

可以发现，在对class的定义上，C++和Java就有很多差别。这里举例几个：  

1. class声明最后，C++需要在大括号后面添加分号";"，而java不用  

2. 继承的表达，C++使用&nbsp;冒号+继承方式&nbsp;“:public”，Java使用“extends”  

3. 方法和属性的访问控制关键字，C++是一次性使用，比如上面使用"public:"然后在后面跟所有声明为public的方法或属性；而Java则需要在每一个方法或属性前面都添加访问控制关键字  

4. 构造函数C++和Java都可以有，但是只有C++可以创建析构函数，Java有垃圾回收机制，所以并不需要析构函数，这是Java对C++的改进之一  

5. Java使用final代替了C++里面的const，当然static（静态）的用法还是大家一致的  

应该还有别的差别，这里暂时就列这么几点了。

然后再来看对象的声明方式上，C++和Java的差别。
我们首先先来看C++的，对象的声明有两种方式：  

    1. Son obj; //变量式声明  
    
    2. Son *obj; //指针式声明
    
结合实例代码来看这两种声明方式会带来什么差异：  

	#include <iostream>
	using namespace std;
	
	class Son
	{
	public:
	    Son()
		{
			cout<<"Son's constructor"<<endl;
		}
	    void sayName()
	    {
	        cout<<"I am Son"<<endl;
	    }
	    ~Son()
	    {
	        cout<<"Son's destructor"<<endl;
	    }
	};
	int main()
	{
		cout<<"Way 1--Son obj1:"<<endl;
	    Son obj1;
		obj1.sayName();
	
	    return 0;
	}

输出结果：  
    
	Way 1--Son obj1:
	Son's constructor
	I am Son
	Son's destructor
	
	--------------------------------
	Process exited after 0.02231 seconds with return value 0
	请按任意键继续. . .

&nbsp; &nbsp; &nbsp; &nbsp; 这是C++的声明对象的方式，如果是习惯了很久的Java而把C++忘得差不多了的话，看到这里的输出会觉得略惊诧。  
&nbsp; &nbsp; &nbsp; &nbsp; 没错！在Java中"Son obj1;"这样的对象声明方式并不会给对象分配空间，仅仅是声明了一个对象的引用，分配的空间只是这个引用的空间，实际的类对象的空间并没有被创建（初始化）。  
&nbsp; &nbsp; &nbsp; &nbsp; 然而在C++中，会发现这里该种创建对象的方式一样会调用构造函数和析构函数！也就是说，C++是支持这种方式声明对象并为其分配空间的。  
&nbsp; &nbsp; &nbsp; &nbsp; 所以在对象这块，我感觉Java对于空间分配相比C++更加严格，并且我们知道在java中如果你并没有给对象分配空间（例如只是上面这样声明了一个对象:"Son Obj;"但并没有使用new等方式分配内存），那么你想直接去调该对象的成员方法，是会发现编译直接就报错，或者即便编译通过了(例如Java智能卡applet平台的编程编译器就没提示错误)，然而运行的时候会发现奇怪的运行结果，然后debug的时候艰难地发现对该对象成员方法的调用根本就跳不进去！因为前面没有用new等方法给对象分配内存空间，没有分配内存，何谈函数调用？  

	//Java创建未初始化的对象
	public class Son {

	public Son(){}
	
	public void sayName()
	{
		System.out.println("I am Son");
	}
	
	public static void main(String[] args) {
		Son obj;
		obj.sayName();
	}
	}
编译器会直接提示如下错误（对象/变量未初始化就调用其成员方法报错）：  

	The local variable obj may not have been initialized


&nbsp; &nbsp; &nbsp; &nbsp; 所以说我觉得Java对内存空间管理比C++严格。程序分配内存Java就有严格的管理，例如要求你要用new关键字，然后内存的回收Java的垃圾回收机制它又帮你做了，所以在java里面在内存管理这块就没C++那么费心也没那么容易出错，因为它从语言的设计上就对程序员屏蔽了容易出错或者说容易导致不规范编程的那几块东西。而在C++，你需要考虑和惦记着的东西就多了很多，一旦编程不慎，就容易导致错误。  
&nbsp; &nbsp; &nbsp; &nbsp; 上面是C++的第一种创建对象的方式，下面介绍第二种也就是使用指针的方式。当然Java里面已经对程序员屏蔽了指针，所以不存在指针方式创建对象。  
	
	cout<<"Way 2--Son *obj2:"<<endl;
	Son *obj2 = new Son();
    obj2->sayName();
	delete obj2;

程序输出结果：  

	Way 2--Son *obj2:
	Son's constructor
	I am Son
	Son's destructor

	--------------------------------
	Process exited after 0.01643 seconds with return value 0
	请按任意键继续. . .


特别注意，这种用new的方式创建对象时，需要用指针来接收new的返回值，而不能是：  

	Son obj2 = new Son(); 
	//编译器会报错说[Error] conversion from 'Son*' to non-scalar type 'Son' requested

另外一个需要特别注意的是，这种创建对象的方式之后，对成员方法的调用只能使用箭头：obj->sayName();而不能是obj.sayName();否则编译报错提示叫你替换成&nbsp; ->&nbsp; 。而上面第一种创建对象的方法后面则只能用obj.sayName();调用方法，用箭头则会报错。  

&nbsp; &nbsp; &nbsp; &nbsp; 接下来，就着这第二种创建对象的方式，我们对代码做一些调整，看看效果如何：  

	cout<<"Way 2--Son *obj2:"<<endl;
	Son *obj2;
    obj2->sayName();
	delete obj2;
你猜这样的程序效果会怎样？
答案是编译通过并且运行正常，输出结果为：  

	Way 2--Son *obj2:
	I am Son
	Son's destructor
	
	--------------------------------
	Process exited after 0.01833 seconds with return value 0
	请按任意键继续. . .
这里虽然没有使用new关键字，但是程序依然可以调用对象的成员方法，同时也可以用delete调用析构函数。然而构造函数并没有被调用到。来看个更明显的例子：  

	#include <iostream>
	using namespace std;
	
	class Son
	{
	private:
		int i; 
	public:
	    Son()
		{
			i = 6;
			cout<<"Son's constructor "<<i<<endl;
		}
	    void sayName()
	    {
	        cout<<"I am Son"<<endl;
	    }
	    ~Son()
	    {
	        cout<<"Son's destructor"<<endl;
	    }
	    void setI(int a) 
		{
			i = a;
		}
		int getI()
		{
			return i;
		}
	};
	int main()
	{
	//	cout<<"Way 1--Son obj1:"<<endl;
	//    Son obj1;
	//    obj1.sayName();
		cout<<"Way 2--Son *obj2:"<<endl;
		Son *obj2;
		int r = obj2->getI();
		cout<<r<<endl;
		
		obj2->setI(3);
		r = obj2->getI();
		cout<<r<<endl;
	
	    return 0;
	}

程序在gcc下编译通过，运行输出为：  

	Way 2--Son *obj2:
	1528349827
	3
	
	--------------------------------
	Process exited after 0.01925 seconds with return value 0
	请按任意键继续. . .
这证明程序确实没有调用到Son的构造函数（第一遍cout输出的i的初值为一个奇葩的数，并且每次运行都是固定的这个数），但是Son *obj;这般定义的对象一样可以直接调用其成员方法。并且运行结果最后并没有自动调用析构函数（没有析构函数的输出）。可见该对象的作用域不仅限于main函数，证明它是在堆空间存储。如果运用上面说的java中对象分配空间的严格要求，这里就会显得很奇怪了，程序并没有使用new关键字，而是直接声明一个Son类型的指针，然而它却可以操作成员属性、调用成员方法。问了公司一个编程方面挺有经验的一个前辈，也说不应该编译通过，应该是堆栈溢出，因为并没有给该对象分配空间就去操作它的方法了。但是在Dev-gcc的编译环境下却可以正常地编译通过并正常运行，所以这就很难解释了，究竟是编译器的问题，还是其实C++是支持这种声明和使用方式的，有待自己后面发掘答案。 
 
-----  分割线 &nbsp; &nbsp; 第二天更新上述问题解释  -----  
今天就着昨天的问题请教了下网上的前辈，知道了Son *obj2;这样定义的是一个野指针（关于野指针后面会另开一篇文章），前辈说一般说来编译运行的时候会报错：字段错误。然而这里在我自己的机器上（Dev + g++）跑野指针，是完全可行，自己写了个循环建立超多个野指针一样没问题，可以修改类成员属性。前辈说可能是因为我的编译环境的问题，会给野指针分配安全的内存区域，并不会导致野指针指向非法的内存区域而导致出现字段错误。  

------     分割线    ------


&nbsp; &nbsp; &nbsp; &nbsp; 总结下本篇讲的两种C++定义对象的两种方式：  
1.

	Son obj;
	obj.method();
2.

	Son *obj = new Son();
	obj->method();

&nbsp; &nbsp; &nbsp; &nbsp; 

&nbsp; &nbsp; &nbsp; &nbsp; 

&nbsp; &nbsp; &nbsp; &nbsp; 

&nbsp; &nbsp; &nbsp; &nbsp; 