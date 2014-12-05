/**
 * 
 * @author siyuwei
 *
 */
public class Point implements KData {
	private double x;
	private double y;
	private KData centroid;

	public Point(double x, double y) {
		this.x = x;
		this.y = y;
	}

	public double getX() {
		return x;
	}

	public double getY() {
		return y;
	}

	@Override
	public double distance(Object toCompare) {
		Point p = (Point) toCompare;
		return Math.sqrt(Math.pow(x - p.x, 2) + Math.pow(y - p.y, 2));
	}

	@Override
	public KData getCentroid() {
		return centroid;
	}

	@Override
	public void setCentroid(KData d) {
		centroid = d;
	}

	@Override
	public boolean equals(Object o) {
		if (!(o instanceof Point)) {
			return false;
		}
		Point p = (Point) o;
		return p.x == x && p.y == y;
	}

	@Override
	public int hashCode() {
		return new Double(x).hashCode() + new Double(y).hashCode();
	}

	@Override
	public String toString() {
		return "Point X: " + x + " Y:" + y;
	}
}
