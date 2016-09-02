##C++指针

### （1）野指针：
delete操作只是把内存释放以及把该指针与相应的内存（堆）空间解除绑定，但是该指针值未被清空删除，它会变成**野指针**。野指针在C++里面是一个略恐怖的东西。  
“造成野指针的原因：  
1、指针变量没有被初始化。任何指针变量刚被创建时不会自动成为NULL指针，它的默认值是随机的，它会乱指一气。  
2、指针p被free或者delete之后，没有置为NULL，让人误以为p是个合法的指针。  
3、指针操作超越了变量的作用范围。这种情况让人防不胜防。”  

下面这篇博客讲解**野指针**讲得挺好的：  
http://blog.chinaunix.net/uid-24227137-id-3270110.html  

### （2）指针复杂组合
摘自《让你不再害怕指针》：  
技巧是：从变量名处起，根据运算符优先级结合，一步一步分析。
结合例子认识下：  

![](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/pointer1.PNG)
![](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/pointer2.PNG)
![](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/pointer3.PNG)
![](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/pointer4.PNG)

在使用指针时，程序员心里必须非常清楚：我的指针究竟指向了哪里。

### （3）指针四大要素：
1. 指针的类型
2. 指针所指向的类型
3. 指针的值（指针所指向的内存区）--指针值为内存区首地址。在32位程序里，所有类型的指针的值都是一个32位整数，因为32位程序里内存地址全部是32位（4-bytes）长。所以sizeof(指针) 永远等于 4（bytes）
4. 指针本身所占据的内存区





