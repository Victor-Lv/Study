import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
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
	public static void main(String[] args) throws IOException {
		InputStream in = new FileInputStream(
			"C:/Users/lv.lang/Desktop/Study/Readme.md");
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
		catch(FileNotFoundException e){
			System.out.println("File not found");
		}
		catch(UnknownHostException e){}
		catch(IOException e){}
		finally
		/**
		 * finally里面的代码必定会被执行,常用于执行空间释放
		 * 例如出现异常则断开数据库连接,或者像本例的关闭文件
		 */
		{
			in.close();
		}
	}
}
/**
 * eclipse快捷键汇总：
 * http://blog.csdn.net/wconvey/article/details/41743365
 *
 * ctrl+shift+o:自动import全部需要的包 
 */