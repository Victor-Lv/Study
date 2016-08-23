servlet菜鸟第一步（环境：eclipse + tomcat）
这篇我们来跑我们的第一个servlet程序。
首先，安装必备的环境：
1.安装jdk+环境变量配置
2.安装tomcat+环境变量配置
3.打开eclipse
4.Window->Preference->Server->Add 你刚才安装的Tomcat
5.New一个Dynamic Web Project:命令为Hello(因为我下面是按Hello工程名字来的)
6.New一个servlet：Hello.java

package com;

//导入必需的 java 库
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//扩展 HttpServlet 类
public class Hello extends HttpServlet {

private String message;

public void init() throws ServletException
{
   // 执行必需的初始化
   message = "Hello World";
}

public void doGet(HttpServletRequest request,
                 HttpServletResponse response)
         throws ServletException, IOException
{
   // 设置响应内容类型
   response.setContentType("text/html");

   // 实际的逻辑是在这里
   PrintWriter out = response.getWriter();
   out.println("<h1>" + message + "</h1>");
}

public void destroy()
{
   // 什么也不做
}
}


7：在工程Webcontent目录下的WEB-INF目录新建个web.xml文件:

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE web-app PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN" "http://java.sun.com/dtd/web-app_2_3.dtd">
<!-- 其实上面这两行不要一样可以正常运行-->

<web-app>
    <servlet>
        <servlet-name>Hello</servlet-name>    <!-- 名字随便,注意到时候浏览器打开这里是一个中间目录（url路径） -->
        <servlet-class>com.Hello</servlet-class>    <!-- servlet类名-->
    </servlet>

    <servlet-mapping>
        <servlet-name>Hello</servlet-name>
        <url-pattern>/Hello</url-pattern>    <!-- url访问虚拟路径，最后我们就是通过工程名/login进行访问的，像这样http://127.0.0.1:8000/LoginAction/login-->
    </servlet-mapping>

</web-app>

8.接下来就可以运行程序了，先选中Hello.java文件，然后Run on server，然后eclipse就会打开网页窗口就可以看到
网页显示一行：Hello World
如果选中的是工程文件再run的话，网页打开的只是到工程或servlet路径下(http://localhost:8080/Hello/)，
并没有打开到.java或者说.class。所以需要自行在网页窗口url后面添加/Hello(http://localhost:8080/Hello/Hello)

9.如果修改了.java文件，保存java文件时就会自动更新编译，我们只需要刷新下刚才那个网页窗口(可能刷新/编译得很慢，需要自己多摁几遍刷新键）就能看到修改后的效果。
例如把java文件里面的message字符串改为：
"Hello haha"
然后刷新下网页窗口，就能看到输出的是一行：Hello haha


