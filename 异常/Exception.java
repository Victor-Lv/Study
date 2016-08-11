import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.UnknownHostException;

/**
 * @author lv.lang
 *
 */
public class Exception {
	public static void print(String s) 
			throws FileNotFoundException,
				   UnknownHostException,
				   IOException
	{}
	public static void main(String[] args) {
		try
		{
			//code that might throw exceptions
			print("Hello");
			/**
			如果没有调用print()或者print后面没跟有相应的异常类型,
			程序会报错：Unreachable catch block for 
			FileNotFoundException. 
			This exception is never thrown from
			the try statement body。
			*/
		}
		catch(FileNotFoundException e){}
		catch(UnknownHostException e){}
		catch(IOException e){}
	}
}
/**
 * eclipse快捷键汇总：
 * http://blog.csdn.net/wconvey/article/details/41743365
 *
 * ctrl+shift+o:自动import全部需要的包 
 */