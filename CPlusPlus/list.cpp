/*
	Author: Victor LV
	Date: 2016-9-1 11:20
	Description: C++ list merge(sort)
*/

/**
* C++:�������������е�����ϲ���һ���������е����� 
* ����:����list��ͷָ��
* ����:�µ�listͷָ�� 
*/ 

ListNode* find(ListNode *head1, ListNode *head2)
{
	if(head1 == NULL || head2 == NULL)
		return NULL;
	ListNode *p1 = head1;
	ListNode *p2 = head2;
	ListNode *newHead = NULL;//�������ͷ��� 
	ListNode *p3 = newHead;
	while(p1 != NULL || p2 != NULL)
	{
		if(p1 == NULL && p2 != NULL)
		{
			ListNode *temp = new ListNode(p2->value,NULL);
			p3->next = temp;
			p2 = p2->next;
		}
		if(p1 != NULL && p2 == NULL)
		{
			ListNode *temp = new ListNode(p1->value,NULL);
			p3->next = temp;
			p1 = p1->next;
		}
		else
		{
			if(p1->value < p2->value)
				ListNode *temp = new ListNode(p1->value,NULL);
			else
				ListNode *temp = new ListNode(p1->value,NULL);	
			if(newHead == NULL)//��δ�е�һ���ڵ�
			{
				newHead = temp;
				p3 = temp;
			}
			else
			{
				
			}
		}
	}
	
	
}
