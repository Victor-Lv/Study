#include "LinkedList.h"
#include "stdio.h"

int main()
{
	/**
	ע��C++��������java��ͬ��C++������Ҫ�� * :
	LinkedList<myInt> *myList��
	����ᱨ���´��� 
	conversion from 'LinkedList<myInt>*' to non-scalar type 'LinkedList<myInt>' requested
	*/
	LinkedList<int> mylist;
	int a = 2;
	Error_code r = mylist.insert(0,a);
	printf("%s", r);
	
	return 0;
}
