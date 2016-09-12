###C++里的抽象类和纯虚函数
在C++中，含有至少一个纯虚函数的类是抽象类，但是注意**在C++中没有abstract这个关键字**（Java和C#里面有），所以C++里面的抽象类无需添加abstract这个单词。抽象类不可以直接实例化，也就是不能直接用抽象类来定义对象，只有实现了父类所有纯虚方法并且不包含纯虚函数的子类才能实例化。  

来看一个示例：  

	#include <iostream>  
  
	using namespace std;  
	  
	class Base  
	{  
	public:  
	    virtual void fun() = 0;
	};  
	  
	class Derived:public Base 
	{  
	public:  
	  void fun(){};
	};  
	  
	int main()  
	{  
	    Base b1;//编译不通过，抽象类不可实例化 
	    Derived d1;//编译通过 
	    return 0;  
	}  

1. 这里Base基类是含有一个纯虚函数的抽象类，所以main函数里直接对它进行实例化会编译不过；但是Derived子类实现了父类fun这个纯虚函数（只需要把virtual关键字抹掉，即便实现里面一句代码都没有，一样算是“实现”了这个函数），所以子类不再是抽象类，它可以进行实例化。

2. 如果把Derived的fun()实现删去呢？当然Derived自然也变成一个抽象类了，因为它继承了基类的纯虚函数，如果它不去实现它的话，那这个子类依然是一个抽象类，无法进行实例化。

3. 此外，针对“纯虚函数是否可以具有实现”这个问题，我在我“IDE:DevC++ & GCC编译器”环境下是编译不通过的：  
		
		#include <iostream>  
		  
		using namespace std;  
		  
		class Base  
		{  
		public:  
		    virtual void fun() = 0
			{
			cout<<"Hello";
			}
		};  
		  
		class Derived:public Base 
		{  
		public:  
		  void fun(){};
		};  
		  
		int main()  
		{  
		    //Base b1;//编译不通过，抽象类不可实例化 
		    Derived d1;//编译通过 
		    return 0;  
		}  

	这里的代码试图给在定义纯虚函数的时候就给出实现，编译会报错，报错信息为：

		[Error] pure-specifier on function-definition（指向virtual void fun() = 0那行报错）
	这个问题网上有不少人说纯虚函数是可以在定义时即被实现的，在上面的环境下编译不通过，这里不争执孰是孰非，因为本身而言，C++提供纯虚函数就是为了声明一个抽象的方法（我只提供“接口”，不亲自实现，实现由衍生类来完成），既然是“接口”，那在定义时就实现它根本无实际用处，也不科学，所以争执孰是孰非无现实应用价值。


