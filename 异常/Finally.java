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
			���û�е���print()����print����û������Ӧ���쳣����,
			����ᱨ��Unreachable catch block for 
			FileNotFoundException. 
			This exception is never thrown from
			the try statement body��
			*/
		}
		catch(FileNotFoundException e){
			System.out.println("File not found");
		}
		catch(UnknownHostException e){}
		catch(IOException e){}
		finally
		/**
		 * finally����Ĵ���ض��ᱻִ��,������ִ�пռ��ͷ�
		 * ��������쳣��Ͽ����ݿ�����,���������Ĺر��ļ�
		 */
		{
			in.close();
		}
	}
}
/**
 * eclipse��ݼ����ܣ�
 * http://blog.csdn.net/wconvey/article/details/41743365
 *
 * ctrl+shift+o:�Զ�importȫ����Ҫ�İ� 
 */