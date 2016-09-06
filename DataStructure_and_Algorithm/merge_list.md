	/*
		Author: Victor LV
		Date: 2016-9-1 11:20
		Description: C++ list merge(sort)
	*/
	
	/**
	* C++:将两个升序排列的链表合并成一个升序排列的链表(不开辟新的链表,直接将原链表重新组合) 
	* 输入:两个list的头指针
	* 返回:新的list头指针 
	*/ 
	
	ListNode* find(ListNode *head1, ListNode *head2)
	{
		if(head1 == NULL || head2 == NULL)
			return NULL;
		ListNode *newHead = NULL;
		ListNode *p1 = head1;
		ListNode *p2 = head2;
		if(head1->value <= head2->value)
		{
			newHead = head1;
			p1 = p1->next;
		}	
		else
		{
			newHead = head2;
			p2 = p2->next;
		}
		ListNode *ptemp = newHead;
		while(p1 != NULL && p2 != NULL)
		{
			if(p1->value <= p2->value)
			{
				ptemp->next = p1;
				p1 = p1->next;
			}	
			else
			{
				ptemp->next = head2;
				p2 = p2->next;
			}
		}
		while(p1 != NULL)
		{
			ptemp->next = p1;
			p1 = p1->next;
		}
		while(p2 != NULL)
		{
			ptemp->next = p2;
			p2 = p2->next;
		}
		return newHead;
	}
