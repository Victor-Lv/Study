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
			���û�е���print()����print����û������Ӧ���쳣����,
			����ᱨ��Unreachable catch block for 
			FileNotFoundException. 
			This exception is never thrown from
			the try statement body��
			*/
		}
		catch(FileNotFoundException e){}
		catch(UnknownHostException e){}
		catch(IOException e){}
	}
}
/**
 * eclipse��ݼ����ܣ�
 * http://blog.csdn.net/wconvey/article/details/41743365
 *
 * ctrl+shift+o:�Զ�importȫ����Ҫ�İ� 
 */