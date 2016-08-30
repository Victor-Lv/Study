##C++的虚析构函数：###

> 用C++开发的时候，用来做基类的类的析构函数一般都是虚函数。  
这样做是为了当用一个基类的指针删除一个派生类的对象时，派生类的析构函数会被调用，如果析构函数不是虚拟的，则将只调用对应于指针类型的析构函数。当然，并不是要把所有类的析构函数都写成虚函数。因为当类里面有虚函数的时候，编译器会给类添加一个虚函数表，里面来存放虚函数指针，这样就会增加类的存储空间。所以，只有当一个类被用来作为基类的时候，才把析构函数写成虚函数。

下面来看一个实例：

父类Dad.cpp：

	#include <iostream>
	using namespace std;

	class Dad
	{
	public:
		Dad(){}
		~Dad(){
			cout<<"Dad's destructor"<<endl;
		}
		virtual void sayName()
		{
			cout<<"I am Dad."<<endl;
		}
	};
	  
子类Son.cpp：

	#include "Dad.cpp"

	class Son :public Dad
	{
	public:
		Son(){}
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
		Dad *obj1 = new Son();
		delete obj1;
		
		return 0;
	}

运行结果：

    Dad's destructor

	--------------------------------
	Process exited after 0.009591 seconds with return value 0
	请按任意键继续. . .

可以发现如果不用虚析构函数时，用父类指针进行delete时，子类的析构函数并不会被执行，但这里实际new的是子类对象，所以就会造成了内存泄露的隐患。  
当然如果对象指针和new出来的空间都是同个类对象的：  

	Son *obj1 = new Son();

则子类和父类的析构函数都会调用，运行结果为：

	Son's destructor
	Dad's destructor
	
	--------------------------------
	Process exited after 0.009003 seconds with return value 0
	请按任意键继续. . .

&nbsp;&nbsp;&nbsp;&nbsp;所以，C++编程中，如果写的某个类是作为基类存在的话，应将其析构函数定义成virtual的。