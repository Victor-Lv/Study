![矩阵数组的两种顺序表达：行优先和列优先](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/rectangular_table.PNG)
###Indexing Rectangular Tables:矩阵表   
i: 0~m  
j: 0~n  
(1) index function： Entry (i,j) in arectangular tablegoes toposition ni + j in asequential array.  
元素(i,j)所在位置为ni + j  
(2) access array: find the position for (i,j) by taking the entry in position i of the auxiliary table, adding j ,and going to the resulting position.  先根据 ni找到辅助表（数组）的位置，再加上j找到最终的位置。如图：  
![索引数组](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/access_array.PNG)  

###哈希表实现（冲突避免）之拉链法：  
![拉链法](https://github.com/Victor-Lv/Study/blob/master/CPlusPlus/image/chained_hash_table.PNG)  

**表table**：可以看成就是一串数组，value就是数组里面存的值，key通过某种计算后得到数组相应的下表，从而得到取得value  

**哈希表**：键key——>通过哈希函数(如取余)根据key计算出索引->再根据索引找到相应的值。  

**冲突避免之拉链法**：使用数组作为前索引（存储后面跟的链表的首地址），后面跟一个链表存该前索引引出的所有key。同时链表每个元素可以存的是key-value组合元素。也可以只存放key，再拿这个key去另一个数组中寻找value。  

