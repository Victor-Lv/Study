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
* ð������Ĵ��뻹�����Ż�һ�£�
* �����б������������ʱ�򣬸��ӶȽ�ΪO(n)��������Ȼȥ������ѭ����
* ֻ��Ҫ���ڲ�ѭ�������һ����ʶλ�������ֵ�һ�α�����ʱ��û�з����κν���
* ��ֱ��������򣬴Ӷ��ﵽ��������O(n)�ĸ��Ӷ�
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
	int *temp= new int[right - left + 1]; //�¿����ݴ�����洢�������� 
	int i = left, j = mid + 1, k = 0;
	while(i <= mid && j <= right)
	{
		if(array[i] <= array[j])
			temp[k++] = array[i++];
		else
			temp[k++] = array[j++];
	}
	while(i <= mid) //������δ��ȫ��ȡ 
		temp[k++] = array[i++];
	while(j <= right) //�Ұ����δ��ȫ��ȡ 
		temp[k++] = array[j++];
	//��tempӳ���array
	int length = right - left + 1;
	for(k = 0, i = left; i <= right;) 
		array[i++] = temp[k++];
	delete temp;
	temp = NULL; //�ܾ�Ұָ��
	/**
	* delete����ֻ�ǻ�����tempԭ��ָ����ǲ��ֿռ䣬���Ƕ���temp���ָ�������
	* �����뿪������֮ǰ��Ȼ�ǿ��õģ�ֻ��������ָ���Ĳ������������ϵͳ������
	* ��ʱ���ͱ������ν��"Ұָ��",��ʱ������Σ�յ���Ϊ����ָ��һƬ����ָ����ڴ棬
	* �������õĴ���ϰ����delete�븳NULLͬʱ���ڣ�ʹ��ָ��ָ����Ч��NULL�� 
	*/ 
}
	
/**�鲢���� 
 * ����ؼ����� ��
 * 1. �з� -->  �����в��϶԰��з֣�ֱ��ÿ��Ϊ����Ԫ�� -->�ݹ���� 
 * 2. �鲢 -->  ��ÿ��鲢������Ĵ��飬�����𽥹鲢   -->�ݹ����� 
 */
void merge_sort(int *array, int left, int right)
{
	if(left >= right)
		return;
	int mid = (left + right) / 2;
	//1:�з� 
	merge_sort(array, left, mid);
	merge_sort(array, mid+1, right);
	//2:�鲢 
	merge(array, left, right);
}

//������
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
