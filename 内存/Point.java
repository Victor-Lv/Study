/**
 * Point.java
 * @author ÂÀÀË
 * 2016Äê8ÔÂ12ÈÕ
 */

public class Point{
	private int px;
	private int py;
	Point(){
		this.px = 0;
		this.py = 0;
	}
	Point(int x, int y){
		this.px = x;
		this.py = y;
	}
	public void move(int x,int y){
		this.px += x;
		this.py += y;
	}
	
	public static void main(String[] args){
		Point p1 = new Point(2,3);
		Point p2 = new Point(4,5);
		p1.move(1, 1);
	}
}
