#include "LinkedList.h"
#include "stdio.h"

int main()
{
	/**
	注意C++定义对象和java不同，C++里面需要有 * :
	LinkedList<myInt> *myList…
	否则会报如下错误： 
	conversion from 'LinkedList<myInt>*' to non-scalar type 'LinkedList<myInt>' requested
	*/
	LinkedList<int> mylist;
	int a = 2;
	Error_code r = mylist.insert(0,a);
	printf("%s", r);
	
	return 0;
}
