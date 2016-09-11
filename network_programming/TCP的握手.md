###TCP的握手主要有两个：建立连接时的三次握手、释放连接时的四次握手  
首先理解下TCP协议中用到的几个关键字：  

![](https://github.com/Victor-Lv/Study/blob/master/network_programming/image/tcp_keyword.png)  

最常用的是SYN（发起连接时的同步序列号）、ACK（确认包的接收）、FIN（结束连接）、RST（重置连接、通知双方马上关闭连接）  
###一、建立TCP连接的三次握手：  
示意图：  

![](https://github.com/Victor-Lv/Study/blob/master/network_programming/image/tcp_connetct.png)  

1. 首先由某一方主机主动发起连接（C/S架构中通常时Client发起），发送SYN命令同时附带值为x的序列号；  
2. 另一端收到这个连接请求之后，会回复一个SYN命令同时附带值为x+1的ACK（表明x+1之前不包括x+1的所有值都收到了，下一次再发应从x+1开始发），同时附带自己的一个值为y的序列号；  
3. 然后这边再收到之后，回复一个ACK=y+1的表明收到了对方的SEQ=y，同时附到自己的序列号SEQ=x+1。当这个包发出去之后，**其会同步开启本方的连接**  
4. 另一端收到这个包之后，不再回复确认包，**直接开启本方的连接**，由此，双方都各自开启了连接，一个TCP连接由此形成。下面就可以**全双工**地发数据了。  

###二、释放TCP连接的四次握手：  
示意图：  

![](https://github.com/Victor-Lv/Study/blob/master/network_programming/image/tcp_release.png)  

1. 首先，由host1主动发起结束连接的请求，发送FIN包以及SEQ=x的序列号，注意，这之后host1不会再发送data，单仍会接收data    
2. host2接收到来自host1的请求之后，回复一个ACK包，但并不会发送SEQ，要等到下一次发包，这是因为host2本机可能仍有数据没发完给host1，所以需要一些时间来进行这些殿后的处理    
3. host2把殿后的工作处理完了，发送一个FIN包附带SEQ=y，告诉host1我已经准备好了可以释放连接了，这之后host2页不再发送数据   
4. host1接收到来自host2的FIN包之后，回复一个Ack=y+1的ACK包，然后再等待一个timeout wait时间之后才正式关闭连接（这个timeout是用来防止来自host2的包在网络中延迟稍晚才来到）  
5. host2接收到这个ACK包之后也正式关闭TCP连接，至此，TCP连接完全关闭（释放）  