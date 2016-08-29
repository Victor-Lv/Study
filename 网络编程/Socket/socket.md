##《Java Network Programming》学习笔记之Socket篇：  ##
####Socket概念：####

>Sockets shield the programmer from low-level details of the network, such as error detection, packet sizes, packet retransmission, network addresses, and more.
  
Socket的一个重大作用是它帮我们屏蔽（搞定）了下层诸如错误检测，包的长度，包的重传，网络地址，**（三次/四次）握手**等诸多细节。

----------

> A socket is a connection between two hosts. It can perform seven basic operations:  
• Connect to a remote machine  
• Send data  
• Receive data  
• Close a connection  
• Bind to a port  
• Listen for incoming data  
• Accept connections from remote machines on the bound port    

####Socket的几大操作： #### 
1. 与远程机器建立连接  
2. 发送数据  
3. 接收数据  
4. 关闭连接  
5. 绑定端口号  
6. 监听数据管道  
7. 从绑定的端口号获悉及允许来自远程机器的连接请求  

其中前四个为客户端socket和服务器端socket共有的，后三个为服务器端socket专有。

----------
####Java程序中的socket：####

> Java programs normally use client sockets in the following fashion:  
1. The program creates a new socket with a constructor.  
2. The socket attempts to connect to the remote host.  
3. Once the connection is established, the local and remote hosts get input and output streams from the socket and use those streams to send data to each other.This connection is full-duplex; both hosts can send and receive data simultaneously. What the data means depends on the protocol; different commands are sent to an FTP server than to an HTTP server. There will normally be some
agreed-upon hand-shaking followed by the transmission of data from one to the other.  
4. When the transmission of data is complete, one or both sides close the connection. Some protocols, such as HTTP 1.0, require the connection to be closed after each request is serviced. Others, such as FTP, allow multiple requests to be processed in a single connection.  

1. 通过构造函数创建新的socket
2. socket应该去连接远程主机
3. 一旦连接被建立，本地和远程主机通过输入输出流进行数据的发送和接收。并且这个连接时全双工的--任意一方都可以同时进行发送和接收
4. 数据传输完成后，某一方或者双方关闭该socket连接  

![](https://github.com/Victor-Lv/Network_Programming/blob/master/image/socket_communication_root.PNG)

另外：附几个讲解Socket的博客链接：  
http://www.cnblogs.com/dolphinX/p/3460545.html  
http://goodcandle.cnblogs.com/archive/2005/12/10/294652.aspx  
http://www.cnblogs.com/skynet/archive/2010/12/12/1903949.html