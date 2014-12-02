public class Point implements KData {
	private double x;
	private double y;

	@Override
	public double distance(Object toCompare) {
		Point p = (Point) toCompare;
		return Math.sqrt(Math.pow(x - p.x, 2) + Math.pow(y - p.y, 2));
	}
}
