import java.io.Serializable;

public interface KData extends Serializable {

	/**
	 * 
	 * @param d
	 * @return the distance of data
	 */
	public double distance(Object toCompare);

	/**
	 * 
	 * @return
	 */
	public KData getCentroid();

	/**
	 * 
	 */
	public void setCentroid(KData d);
}
