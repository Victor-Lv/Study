package com;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class HelloForm
 */
@WebServlet("/HelloForm")
public class HelloForm extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public HelloForm() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, 
			HttpServletResponse response) throws ServletException, IOException {
		request.setCharacterEncoding("UTF-8");
		
		//设置响应内容类型
		response.setHeader("Content-type", "text/html;charset=UTF-8");  
		//这句话的意思，是告诉servlet用UTF-8转码，而不是用默认的ISO8859  
		response.setCharacterEncoding("UTF-8");
		
		PrintWriter out = response.getWriter();
		String title = "使用GET方法读取表单数据";
		String docType = 
				"<!doctype html public \"-//w3c//dtd html 4.0 " +
						"transitional//en\">\n";
		out.println(docType + 
				 "<html>\n" +
				    "<head><title>" + title + "</title></head>\n" +
				    "<body bgcolor=\"#f0f0f0\">\n" +
				    "<h1 align=\"center\">" + title + "</h1>\n" +
				    "<ul>\n" +
				    "  <li><b>名字</b>："
				    + request.getParameter("first_name") + "\n" +
				    "  <li><b>姓氏</b>："
				    + request.getParameter("last_name") + "\n" +
				    "</ul>\n" +
				    "</body></html>");
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("text/html;charset=UTF-8");
		
		PrintWriter out = response.getWriter();
		String message = "Hello";
		out.println(message);
	}

}
