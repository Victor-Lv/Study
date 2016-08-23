package com;

//�������� java ��
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//��չ HttpServlet ��
public class Hello extends HttpServlet {

private String message;

public void init() throws ServletException
{
   // ִ�б���ĳ�ʼ��
   message = "Hello World";
}

public void doGet(HttpServletRequest request,
                 HttpServletResponse response)
         throws ServletException, IOException
{
   // ������Ӧ��������
   response.setContentType("text/html");

   // ʵ�ʵ��߼���������
   PrintWriter out = response.getWriter();
   out.println("<h1>" + message + "</h1>");
}

public void destroy()
{
   // ʲôҲ����
}
}