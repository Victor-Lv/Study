##《Java Network Programming》摘录：##

###一个HTTP-GET报文头部header示例：###
**我：client客户端**

	GET /index.html HTTP/1.0  
	Accept: text/html, text/plain, image/gif, image/jpeg  
	User-Agent: Lynx/2.4 libwww/2.1.4  
	Host: www.cafeaulait.org

- 第一句表示我要GET 这个位置上的资源，以及我使用的协议为HTPP/1.0
- 第二句表示我能接受html、plain、gif、jpeg四种资源并正确解析
> "which tells the server what kinds of data the client can handle (though servers often ignore this)"

- 第三句告诉服务器说我现在使用的浏览器类型  
> "User-Agent is another common keyword that lets the server know what browser is being used, allowing the server to send files optimized for the particular browser type. The line below says that the request comes from Version 2.4 of theLynx browser:"

- 第四句说明我请求的服务器的域名[因为同个IP下可有多个host域名--一台服务器挂载多个网站]

> " ……include a Host field specifying the server’s name, which allows web servers to distinguish between different named hosts served from the same IP address. "


### 一个http响应示例： ###
**我：server服务器**

	HTTP/1.1 200 OK
	Date: Mon, 15 Sep 2003 21:06:50 GMT
	Server: Apache/2.0.40 (Red Hat Linux)
	Last-Modified: Tue, 15 Apr 2003 17:28:57 GMT
	Connection: close
	Content-Type: text/html; charset=ISO-8859-1
	Content-length: 107
	
	<html>
	<head>
	<title>
	A Sample HTML file
	</title>
	</head>
	<body>
	The rest of the document goes here
	</body>
	</html>





1. 第一句表示我使用的协议为HTTP/1.1，以及响应状态码为200 OK,状态码是啥？上网的时候看到过网页返回个404吧,404[请求的资源未找到]也就是一种状态码。


> "The first line indicates the protocol the server is using ( HTTP/1.1 ), followed by a response code. 200 OK is the most common response code, indicating that the request was successful."


2. 第二句表示时间

3. 第三句表示服务器使用的软件类型

4. 第四句表示该资源最后被修改的时间

5. 第五句表示我在发完响应报文之后会关闭我们之间的连接

6. 第六句表示MIME文件类型,这里表示正文使用的是text/html格式(前一个单词表示父类型[text、media]，后一个单词表示子类型[html、gif]），字符编码为ISO-8859-1（常见的UTF-8就是一种字符编码类型）

7. 最后一句表示正文总长度[单位为字节]，不包括报文头部的长度。


> "The other header lines identify the date the request was made in the server’s time frame, the server software(Apache 2.0.40), the date this document was last modified, a promise that the server will close the connection when it’s finished sending, the MIME content type, and the length of the document delivered (not counting this header) — in this case, 107 bytes."



###连接的状态性：###
 

> "If the client reconnects, the server retains no memory of the previous connection or its results. A protocol that retains no memory of past requests is called stateless; in contrast, a stateful protocol such as FTP can process many requests before the connection is closed. The lack of state is both a strength and a weakness of HTTP."

 **解析：**如果客户端和服务器断开连接后，服务器会清除所有跟先前连接相关的资源(包括内存、上下文信息等等)，那么这种情况叫"无状态"，反之，"有状态"的就是类似FTP协议,某一次断开连接之后仍会保留跟先前连接相关的资源，然后下一次恢复连接的时候，一方面能用到旧的资源，更快捷响应，另一方面因为保留了前面连接时的历史记录，这个的好处我估计：断点续传就是这个意思。HTTP协议的无连接性，一方面是它的优势所在，另一方面也是它的劣势所在，孰优孰劣看实际应用场景。

####返回的状态码列表如下（摘自《Java Network Programming》：####
![](https://github.com/Victor-Lv/Study/blob/master/java%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B/%E7%8A%B6%E6%80%81%E7%A0%811.PNG)
![](https://github.com/Victor-Lv/Study/blob/master/java%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B/%E7%8A%B6%E6%80%81%E7%A0%812.PNG)

####状态码各区间数值的意义：####
- 200~299：成功
- 300~399:重定向
- 400~499:来自客户端的错误
- 500~599:来自服务器端的错误

> HTTP 1.1 more than doubles the number of responses. However, a response code from 200 to 299 always indicates success, a response code from 300 to 399 always indicates redirection, one from 400 to 499 always indicates a client error, and one from 500 to 599 indicates a server error.



> **MIME：**"Web servers use MIME to identify the kind of data they’re sending. Web clients use MIME to identify the kind of data they’re willing to accept. "

部分MIME列表（摘自《Java Network Programming》：


查询字符串（分GET和POST两种方法，GET方法把查询字符串直接附在URL上，POST方法把查询字符串放在输出流中）：
	"username=Elliotte+Harold&email=elharo%40macfaq.com"
This is called the query string.
There are two methods by which the query string can be sent to the server: GET and
POST . If the form specifies the GET method, the browser attaches the query string to
the URL it sends to the server. Forms that specify POST send the query string on an
output stream. The form in Example 3-1 uses GET to communicate with the server, so
it connects to the server and sends the following command:
一个完整的HTTP-url（路径元素决定了该请求交由服务器端的哪个程序来处理，然后会把查询字符串传递给该程序来处理以及由它来返回响应给客户端）：
	"GET /cgi/reg.pl?username=Elliotte+Harold&email=elharo%40macfaq.com HTTP/1.0"
The server uses the path component of the URL to determine which program should
handle this request. It passes the query string’s set of name-value pairs to that program, which normally takes responsibility for replying to the client.


 