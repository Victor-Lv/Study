#include <iostream>
using namespace std;

class Dad
{
public:
	Dad(){}
	~Dad(){
		cout<<"Dad destructor"<<endl;
	}
	virtual void sayName()
	{
		cout<<"I am Dad."<<endl;
	}
};

