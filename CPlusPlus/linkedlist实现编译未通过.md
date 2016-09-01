##linkedList-C++实现--编译未通过--待完善

Node.h

	#include "stdlib.h" //support "NULL"

	#ifndef NODE_H
	#define NODE_H
	
	template <typename Node_entry>
	struct Node
	{
		Node_entry value;
		Node<Node_entry> *next;
		Node();
		Node(Node_entry value, Node<Node_entry> *next = NULL);
	};
	
	#endif

Node.cpp

	#include "Node.h"

	template <typename Node_entry>
	Node<Node_entry>::Node()
	{
		this->value = 0;
		this->next = NULL;
	}
	
	template <typename Node_entry>
	Node<Node_entry>::Node(Node_entry value, Node<Node_entry> *next)
	{
		this->value = value;
		this->next = next;
	}

LinkedList.h

	/*
	 * LinkedList.h
	 *
	 *  Created on: 2016年8月18日
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

LinkedList.cpp

	#include "LinkedList.h"

	template <typename List_entry>
	Node<List_entry>* LinkedList<List_entry>::find_position(int position)const
	{
		if(position < 0 || position > count)	
			return NULL;
		int counter = 0;
		Node<List_entry> *temp = head;
		while(temp != NULL)
		{
			if(counter == position)
				return temp;
			counter++;
			temp = temp->next;
		}
		return NULL;
	}
	
	template <typename List_entry>
	LinkedList<List_entry>::LinkedList()
	{
		count = 0;
		head = NULL;
	}
	
	template <typename List_entry>
	LinkedList<List_entry>::~LinkedList()
	{
		clear();
	}
	
	template <typename List_entry>
	bool LinkedList<List_entry>::empty()const
	{
		return count==0;
	}
	
	template <typename List_entry>
	bool LinkedList<List_entry>::full()const
	{
		return count >= maxSize;
	}
	
	template <typename List_entry>
	int LinkedList<List_entry>::size()const
	{
		return count;
	}
	
	template <typename List_entry>
	void LinkedList<List_entry>::clear()
	{
		List_entry temp;
		for(int i = 0; i < count; i++)
			remove(i,temp);
	}
	
	template <typename List_entry>
	Error_code LinkedList<List_entry>::insert(int position, const List_entry &x)
	{
		if(position < 0)
			return underflow;
		if(position > count || full())
			return overflow;
		if(position == 0 || empty())
		{
			head = new Node<List_entry>(x,head);
			count++;
			return success;
		}
		Node<List_entry> *current = find_position(position);
		if(current == NULL)
			return notFound;
		Node<List_entry> *newNode = new Node<List_entry>(x,current->next);
		if(newNode == NULL)//heap storage overflow
			return overflow; 
		current->next = newNode;
		count++; //don't forget this
		return success;
	}
	
	template <typename List_entry>
	Error_code LinkedList<List_entry>::retrieve(int position, List_entry &x)const
	{
		if(empty())
			return underflow;
		if(position < 0)
			return underflow;
		if(position > count)
			return overflow;
		Node<List_entry> *current = find_position(position);
		if(current == NULL)
			return notFound;
		x = current->value;
		return success;
	}
	
	template <typename List_entry>
	Error_code LinkedList<List_entry>::replace(int position, const List_entry &x)
	{
		return success;
	}
	
	template <typename List_entry>
	Error_code LinkedList<List_entry>::remove(int position, List_entry &x)
	{
		if(empty())
			return underflow;
		if(position < 0)
			return underflow;
		if(position > count)
			return overflow;
		Node<List_entry> *pre_node = find_position(position - 1);
		if(pre_node == NULL)
			return notFound;
		if(pre_node->next == NULL)
			return overflow;
		Node<List_entry> *delete_node = pre_node->next;
		Node<List_entry> *next_node = pre_node->next->next;
		pre_node->next = next_node;
		x = delete_node->value;
		delete delete_node;
		return success;
	}
	
	template <typename List_entry>
	void LinkedList<List_entry>::traverse(void(*visit)(List_entry &x))const
	{
		return success;
	}


main.cpp

	#include "LinkedList.h"
	#include "stdio.h"
	
	int main()
	{
		/**
		注意C++定义对象和java不同，C++里面需要有 * :
		LinkedList<myInt> *myList…
		否则会报如下错误： 
		conversion from 'LinkedList<myInt>*' to non-scalar type 'LinkedList<myInt>' requested
		*/
		LinkedList<int> mylist;
		int a = 2;
		Error_code r = mylist.insert(0,a);
		printf("%s", r);
		
		return 0;
	}