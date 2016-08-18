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
