/*
	Author: Victor LV
	Date: 2016-9-1 11:20
	Description: C++ list merge(sort)
*/

/**
* C++:将两个升序排列的链表合并成一个升序排列的链表 
* 输入:两个list的头指针
* 返回:新的list头指针 
*/ 

ListNode* find(ListNode *head1, ListNode *head2)
{
	if(head1 == NULL || head2 == NULL)
		return NULL;
	ListNode *p1 = head1;
	ListNode *p2 = head2;
	ListNode *newHead = NULL;//新链表的头结点 
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
			if(newHead == NULL)//尚未有第一个节点
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
