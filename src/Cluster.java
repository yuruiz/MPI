import java.util.List;

public class Cluster {
	private KData centroid;
	private List<KData> member;

	public Cluster(KData centroid, List<KData> member) {
		this.centroid = centroid;
		this.member = member;
	}

	public List<KData> getMember() {
		return member;
	}

	public void setMember(List<KData> memeber) {
		this.member = memeber;
	}

	public KData getCentroid() {
		return centroid;
	}

	public void setCentroid(KData centroid) {
		this.centroid = centroid;
	}

	public void updateCentroid() {
		KData d = Util.getCentroid(member);
		if (d != null) {
			centroid = d;
		}
	}

}
