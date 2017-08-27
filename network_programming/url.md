---
title: testPage
date: 2017-05-27 22:29:11
tags: http

---


[toc]

# 《HTTP权威指南》学习笔记之URI和URL
*本文作者为吕浪（Victor Lv）,原出处为[Victor Lv's blog](http://langlv.me)([www.langlv.me](http://langlv.me))，转载请保留此句。*
### URI和URL：
> URI：统一资源标识符Uniform Resource Identifier
> URL：统一资源定位符Uniform / Universal Resource Locator   

URL是URI的一个子集,URI表示资源在因特网上的位置，而如何表示这个位置，可以有多种方法，URL就是其中一种，另一种主要的方法是URN，URN直接通过资源的key来确定资源的位置（例如：`urn:ietf:rfc:2141`）,URN技术尚未成熟和普及，所以目前我们看到的URI都是URL的天下。   

URL语法由9部分通用格式组成：  
```url
<scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<frag>
```
一般url不会同时出现所有这些组件，URL最重要的是方案scheme、主机host和路径path。  

> 方案：指定使用协议，无默认值  
> 
> 用户：访问资源时需要的用户名，默认值为匿名  
> 
> 密码：用户名后面的密码，默认值为<E-mail地址>  
> 
> 主机：资源宿主服务器的主机名或者IP地址，无默认值  
> 
> 端口：资源宿主服务器正在监听的端口号，很多scheme都有默认的端口号（HTTP默认80端口），默认值是每个scheme特有  
> 
> 路径：服务器上资源的本地名，无默认值  
> 
> 参数：某些方案会用这个组件来指定输入参数，无默认值  
> 
> 查询：某些方案会用这个组件传递参数以激活应用程序（比如数据库、公告板、搜索引擎以及其他因特网网关）。查询组件的内容没有通用格式。无默认值  
> 
> 片段：一小片或一部分资源的名字，frag字段不会传送给服务器，而是在客户端内部使用，无默认值  




典型的三种URL如下：  
```url
http://207.200.83.29:80/index.html
http://www.google.com:80/index.html
http://www.google.com/index.html
```
HTTP发送报文之前，需要与HTTP服务器建立起下层的**TCP连接**，这就类似于给公司办公室某个人打电话，首先，要拨打公司的电话号码，这样才能进去正确的机构，其次，拨打联系人的**分机号**。在TCP中，IP地址就是公司号码，端口号就是联系人分机号，端口号往往跟操作系统上运行的特定软件相关。  

在上面的第一个url例子中，最前面的http是**方案scheme**，表明使用http协议，其他scheme有诸如ftp等。后面的207.200.83.29就是**IP地址**，80是**端口**，IP地址加端口就能让你联系上你需要联系的那个人，然后/index.html这些在ip地址后面的都是**资源的相对位置**，告诉联系人你把你这边放在index.html的资源给我，在web开发中，这些相对位置通常指的是文件夹结构，比如`/home/user/index.html`。  

然后第二个url例子则换了种方式，通过域名这样更符合用户体验的来代替IP地址，实际上也是先通过DNS域名服务器先把**域名转换成IP地址**再向服务器发送http请求的。  

然后第三个例子省略了端口号，HTTP的URL中没有指定端口号时，会给出默认的**端口号假设**，比如假设默认是是80。  



