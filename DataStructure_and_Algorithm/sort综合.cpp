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
/**
* 冒泡排序的代码还可以优化一下：
* 当序列本来就是有序的时候，复杂度降为O(n)而不是依然去做两轮循环，
* 只需要在内层循环中添加一个标识位，当发现第一次遍历的时候并没有发生任何交换
* 则直接完成排序，从而达到最好情况下O(n)的复杂度
*/
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

void merge(int *array,const int left,const int right)
{
	int mid = (left + right) / 2;
	int *temp= new int[right - left + 1]; //新开个暂存数组存储有序序列 
	int i = left, j = mid + 1, k = 0;
	while(i <= mid && j <= right)
	{
		if(array[i] <= array[j])
			temp[k++] = array[i++];
		else
			temp[k++] = array[j++];
	}
	while(i <= mid) //左半边仍未完全抽取 
		temp[k++] = array[i++];
	while(j <= right) //右半边仍未完全抽取 
		temp[k++] = array[j++];
	//将temp映射回array
	int length = right - left + 1;
	for(k = 0, i = left; i <= right;) 
		array[i++] = temp[k++];
	delete temp;
	temp = NULL; //拒绝野指针
	/**
	* delete操作只是回收了temp原来指向的那部分空间，但是对于temp这个指针变量，
	* 在其离开作用域之前仍然是可用的，只是它究竟指向哪部分区域，这个依系统而定，
	* 这时它就变成了所谓的"野指针",有时候它是危险的因为可能指向一片不该指向的内存，
	* 所以良好的代码习惯是delete与赋NULL同时存在，使该指针指向无效的NULL。 
	*/ 
}
	
/**归并排序： 
 * 两大关键步骤 ：
 * 1. 切分 -->  将序列不断对半切分，直至每组为单个元素 -->递归放网 
 * 2. 归并 -->  将每组归并成有序的大组，往上逐渐归并   -->递归收网 
 */
void merge_sort(int *array, int left, int right)
{
	if(left >= right)
		return;
	int mid = (left + right) / 2;
	//1:切分 
	merge_sort(array, left, mid);
	merge_sort(array, mid+1, right);
	//2:归并 
	merge(array, left, right);
}

//堆排序
void heap_sort()

int main()
{
	int array[6] = {3,2,6,1,7,9};
	cout<<"Unsorted array:"<<endl;
	for(int i = 0; i < 5;i++)
		cout<<array[i]<<" ";
	cout<<array[5]<<endl;
	//buble_sort(array,6);
	//quick_sort(array,0,5);
	merge_sort(array, 0, 5);
	cout<<"Sorted array:"<<endl;
	for(int i = 0; i < 5;i++)
	cout<<array[i]<<" ";
	cout<<array[5]<<endl;
	
	return 0;
}
