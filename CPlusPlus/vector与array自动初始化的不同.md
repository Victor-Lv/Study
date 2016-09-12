vector容器定义时如果程序中没有显式初始化，则容器会自动对所有元素进行初始化，例如vector<int>数组所有元素会被自动初始化为0.然而如果是用传统的方法定义数组：int array[size],若程序员不显式初始化则数组的初值会是奇怪的值。示例代码如下：

	#include <iostream>
	#include <vector>
	using namespace std;
	
	int main()
	{
		//vector<int> *myVector = new vector<int>(5);//new方法,注意需要用指针来接收new的返回值 
		vector<int> myVector(5);//方法2:对象的普通定义--变量法 
		
		//使用迭代器来访问vector 
		vector<int>::iterator iter;
		
		int myArray[5];
		
		for(iter = myVector.begin(); iter != myVector.end(); iter++)
			cout<<*iter<<endl;
		for(int i = 0; i < 5; i++)
			cout<<myArray[i]<<endl;
		
		return 0;
	}
	
	/**
	程序运行输出： 
	0
	0
	0
	0
	0
	4236816
	0
	36
	0
	5435648
	*/

在我的Dev-C++ && gcc环境下，int array[]方式定义数组，编译器会给“被夹着”的数组元素（如上面的array[1]、array[3])初始化为0，其他位置貌似会变化。