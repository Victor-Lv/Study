#include "Dad.cpp"

class Son :public Dad
{
public:
	Son(){}
	void sayName()
	{
		cout<<"I am Son"<<endl;
	}
};

void print(Dad *obj)
{
	obj->sayName();
}

int main()
{
	Dad *obj1 = new Son();
	obj1->sayName();
	Son *obj2 = new Son();
	cout<<"*******"<<endl;
	print(obj2);
	
	return 0;
}
