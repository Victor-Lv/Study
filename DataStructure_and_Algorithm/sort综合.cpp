#include <iostream>
#include <cstdio>
using namespace std;

void swap(int *array, int left, int right)
{
	int temp = array[left];
	array[left] = array[right];
	array[right] = temp;
}

//buble sort
void buble_sort(int *array, int length)
{
	if(array == NULL)
		return;
	int i = 0, j = 0;
	for(j = 1; j < length - 1; j++)
	{
		for(i = 0; i < length - j; i++)
		{
			if(array[i+1] < array[i])
				swap(array,i,i+1);
		}
	}
}

void quick_sort(int *array, int left, int right)
{
	if(left >= right)
		return;
	int i = left, j = right;
	while(i < j)
	{
		while(array[j] > array[left] && i < j)
			j--;
		while(array[i] < array[left] && i < j)
			i++;
		swap(array, i ,j);
	}
	swap(array, left, i);
	quick_sort(array, left, i - 1);
	quick_sort(array, i+1, right);
	
}



int main()
{
	int array[6] = {3,2,6,1,7,9};
	cout<<"Unsorted array:"<<endl;
	for(int i = 0; i < 5;i++)
		cout<<array[i]<<" ";
	cout<<array[5]<<endl;
	//buble_sort(array,6);
	quick_sort(array,0,5);
	cout<<"Sorted array:"<<endl;
	for(int i = 0; i < 5;i++)
	cout<<array[i]<<" ";
	cout<<array[5]<<endl;
	
	return 0;
}
