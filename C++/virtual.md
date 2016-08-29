##C++虚函数与多态实例##
都说**virtual**关键字是用来实现多态和动态绑定，但是咋一听感觉挺抽象的，下面结合个实例来看看。
父类：  
    
	#include <iostream>
	using namespace std;
	
	class Dad
	{
	public:
		Dad(){}
		void sayName()
		{
			cout<<"I am Dad."<<endl;
		}
	};

子类：
  
    #include "Dad.cpp" 
  
	class Son :public Dad
	{
	public:
		Son(){}
		void sayName()
		{
			cout<<"I am Son"<<endl;
		}
	};
	
	void print(Dad *obj)
	{
		obj->sayName();
	}

	int main()
	{
		Dad *obj1 = new Son();
		obj1->sayName();
		Son *obj2 = new Son();
		cout<<"*******"<<endl;
		print(obj2);
		
		return 0;
	}

运行结果：

	I am Dad.
	*******
	I am Dad.

	--------------------------------
	Process exited after 0.05475 seconds with return value 0
	请按任意键继续. . .

会发现：我们本身new出来的是Son，但是因为在调用sayName方法前都对该new出来的对象进行了转型：从Son转型为Dad，经过了这样的转型之后，如果没有sayName不是虚函数的话，那么编译器只认识Dad类的sayName函数，Son的sayName函数不可见；这里是静态绑定（编译时绑定），编译器根据对象引用的类型（这里是Dad）将sayName的调用绑定到Dad的sayName函数。  
所以要是想再print函数中调用Son的sayName函数，要么重载（overload）print函数，添加

	void print(Son *obj){}
版本，那这里就有两个版本，是不是很麻烦。  
所以第二种方法就是使用虚函数（virtual）激活多态属性。如下，将Dad类的sayName函数声明为虚函数：  

	#include <iostream>
	using namespace std;
	
	class Dad
	{
	public:
		Dad(){}
		virtual void sayName()
		{
			cout<<"I am Dad."<<endl;
		}
	};

其他代码不用修改，再次运行工程，输出结果为：  
	
	I am Son
	*******
	I am Son
	
	--------------------------------
	Process exited after 0.05818 seconds with return value 0
	请按任意键继续. . .

可以发现，这里成功调用了Son的sayName函数。刚才说到，若不使用虚函数的话，编译器会在编译时就将函数调用和某个类的成员函数绑定，而它是根据对象的引用类型来确定如何绑定的。若使用虚函数，那么对于sayName这个函数的调用，编译器会跳过它的绑定，让程序运行时才去绑定函数调用的实际函数空间，这就是动态绑定（动态联编）或者说运行时绑定，编译时不会进行绑定，而当程序运行的时候，调用到sayName函数时，系统会根据实际的内存空间的类型（也就是说实际new出来的是哪个类）寻找函数所在的位置（这里找到的是Son的sayName版本），而不仅仅是对象引用的类型，因为对象引用的类型可以随便进行强制类型转换，但是new出来的空间却是代码写定了就唯一确定的。