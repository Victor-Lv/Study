[toc]

# 《HTTP权威指南》学习笔记之URI和URL
*本文作者为吕浪（Victor Lv）,原出处为[Victor Lv's blog](http://langlv.me)([www.langlv.me](http://langlv.me))，转载请保留此句。*
### URI和URL：
> URI：统一资源标识符Uniform Resource Identifier
> URL：统一资源定位符Uniform / Universal Resource Locator   

URL是URI的一个子集,URI表示资源在因特网上的位置，而如何表示这个位置，可以有多种方法，URL就是其中一种，另一种主要的方法是URN，URN直接通过资源的key来确定资源的位置（例如：`urn:ietf:rfc:2141`）,URN技术尚未成熟和普及，所以目前我们看到的URI都是URL的天下。而URL确定位置的方法如下：  
典型的URL如下：  
```url
http://207.200.83.29:80/index.html
http://www.google.com:80/index.html
http://www.google.com/index.html
```
HTTP发送报文之前，需要与HTTP服务器建立起下层的**TCP连接**，这就类似于给公司办公室某个人打电话，首先，要拨打公司的电话号码，这样才能进去正确的机构，其次，拨打联系人的**分机号**。在TCP中，IP地址就是公司号码，端口号就是联系人分机号，端口号往往跟操作系统上运行的特定软件相关。  

在上面的第一个url例子中，最前面的http是**方案scheme**，表明使用http协议，其他scheme有诸如ftp等。后面的207.200.83.29就是**IP地址**，80是**端口**，IP地址加端口就能让你联系上你需要联系的那个人，然后/index.html这些在ip地址后面的都是**资源的相对位置**，告诉联系人你把你这边放在index.html的资源给我，在web开发中，这些相对位置通常指的是文件夹结构，比如`/home/user/index.html`。    

然后第二个url例子则换了种方式，通过域名这样更符合用户体验的来代替IP地址，实际上也是先通过DNS域名服务器先把**域名转换成IP地址**再向服务器发送http请求的。  

然后第三个例子省略了端口号，HTTP的URL中没有指定端口号时，会给出默认的**端口号假设**，比如假设默认是是80。  



