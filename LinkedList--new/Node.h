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
