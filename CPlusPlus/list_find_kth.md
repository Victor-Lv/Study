###输入一个链表，输出该链表的倒数第k个节点

![](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/list_find_kth.PNG)

    /**
    * C++:寻找链表的倒数第k个元节点
    * 输入:list头指针, k
    * 返回:list倒数第k个节点 
    */ 
    
    ListNode* find(ListNode *pListHead, int k)
    {
    	if(pListHead == NULL || k <= 0)
    		return NULL;
    	ListNode *p1 = pListHead;
    	ListNode *p2 = pListHead;
    	for(int i=0; i < k-1; i++)
    	{
    		if(p2->next != NULL)
    			p2 = p2->next;
    		else
    			return NULL;
    	}
    	while(p2->next != NULL)
    	{
    		p1 = p1->next;
    		p2 = p2->next;
    	}
    	return p1;
    }

注意对于空指针和越界等情况的判断处理。