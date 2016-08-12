import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

/**
 * HelloWorld.java
 * @author ����
 * 2016��8��12��
 */


public class HelloWorld extends HttpServlet{
	private String message;
	
	public void init() throws  ServletException
	{
		message = "Hello World!";
	}
	
	public void doGet(HttpServletRequest request,
					  HttpServletResponse response)
				throws ServletException, IOException
	{
		response.setContentType("tesxt/html");
		PrintWriter out = response.getWriter();
		out.println("<h1>" + message + "</h1>");
	}
	
	public void destroy()
	{
		//do nothing
	}
}
