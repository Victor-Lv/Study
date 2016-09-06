##MapReduce小解析：##  
结合自己前几个月上过的数据挖掘课程（虽然学得很渣），根据回忆小谈当时课上老师讲的一个MapReduce小示例。  

MapReduce常用来解决大运算量+复杂运算量的问题（大数据）。  
**Map**：映射：将一个大的任务拆分成多个小任务一一映射到分布式计算区域（例如是多台机器）。然后这些分机各自执行自己的计算任务。  
**Reduce**：合并收缩。将所有分机各自计算好的结果合并得到初始的那个大任务的最终结果。  
举个例子，现在我们要交给服务器去帮我统计一篇很长很长的轮文中26个英文字母各自出现的频次，那我们可以这样做：  
1.	master机器（核心机器，主管分配）将这个大文件（大任务）拆分成6大块（可以是不均分的）；  
2.	然后把这6大块分别交给旗下的6个分机（master本算可以是台分机），任务的分配可以根据分机的处理能力来分配，比如分机A最强大，就把最大块的蛋糕分给它处理；  
3.	然后让这6个分机分别统计所属模块的26个字母出现次数，大家都得出了各自模块26个字母出现的频次。比如说大家都用哈希的方式存储计算结果的话，键为字母，值为一堆的1，每碰上一个对应的字母就添加一个1：    
A：1 1 1 1 1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A：1 1 1 1  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;……  
B：1 1 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;B：1 1  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;……  
C：1 1 1 1 1 1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C：1 1 1 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;……    
--分机A统计结果&nbsp;&nbsp;&nbsp;&nbsp;	--分机B统计结果  ……    
#### *以上就是Map操作*  
4.  然后master再将所有分机各自的计算结果收集起来,并进行归并，比如分机A和分机B归并结果为：  
A：1 1 1 1 1 1 1 1 1  
B：1 1 1 1 1  
C：1 1 1 1 1 1 1 1 1 1  
……  
5. 然后master再将每个字母后面跟了多少个1计算出来，比如上面A和B归并结果为：  
A：9  
B：5  
C：10  
……  

####*以上为Reduce操作*####

最后就得到了这个大任务的最终计算结果。
