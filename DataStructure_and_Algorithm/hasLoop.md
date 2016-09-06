	/*
		Author: Victor LV
		Date: 2016-9-6 10:14
		Description: 判断单链表是否有回环C++ 
	*/
	
	/**
	* C++:判断单链表是否存在回环 
	* 输入:list的头指针
	* 返回:bool:true表示有回环,false表示无 
	*/ 
	
	/**解题思想： 
	*这里也是用到两个指针。如果一个链表中有环，
	*也就是说用一个指针去遍历，是永远走不到头的。
	*因此，我们可以用两个指针去遍历，
	*一个指针一次走两步，一个指针一次走一步，
	*如果有环，两个指针肯定会在环中相遇。
	*时间复杂度为O（n）。
	*/ 
	
	bool hasLoop(ListNode *pHead)
	{
		if(pHead == NULL || phead->next == NULL)
			return false;
		ListNode *pFast = pHead; //快指针每次前进两步 
		ListNode *pSlow = pHead; //快指针每次前进一步 
		while(pFast != NULL && pSlow !== NULL)
		{
			pFast = pFast->next;
			pSlow = pSlow->next;
			if(pFast->next != NULL)
				pFast = pFast->next;
			if(pFast == pSlow)
				return true;
		}
		return false;
	}