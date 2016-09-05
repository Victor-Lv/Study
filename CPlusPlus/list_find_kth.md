###输入一个链表，输出该链表的倒数第k个节点
主要思路就是使用两个指针，先让前面的指针走到正向第k个结点，这样前后两个指针的距离差是k-1，之后前后两个指针一起向前走，前面的指针走到最后一个结点时，后面指针所指结点就是倒数第k个结点。

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