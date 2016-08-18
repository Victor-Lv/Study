/*
 * LinkedList.h
 *
 *  Created on: 2016Äê8ÔÂ18ÈÕ
 *      Author: lv.lang
 */

#ifndef LINKEDLIST_H_
#define LINKEDLIST_H_

#include "Node.h"

enum Error_code {success, underflow, overflow, notFound};
const int maxSize = 100;

template <typename List_entry>
class LinkedList
{
protected:
	int count;
	Node<List_entry> *head;
	//find the current pointer accoding to position
	Node<List_entry> *find_position(int position)const;
public:
	LinkedList();
	~LinkedList();
	bool empty()const;
	bool full()const;
	int size()const;
	void clear();
	Error_code insert(int position, const List_entry &x);
	Error_code replace(int position, const List_entry &x);
	Error_code retrieve(int position, List_entry &x)const;
	Error_code remove(int position, List_entry &x);
	void traverse(void(*visit)(List_entry &x))const;
};

#endif /* LINKEDLIST_H_ */
