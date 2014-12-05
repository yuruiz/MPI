/**
 * 
 * @author siyuwei
 *
 */
public class DNAStrand implements KData {

	private String DNA;
	private KData centroid;

	public DNAStrand(String DNA) {
		this.DNA = DNA;
	}

	public String getDNA() {
		return DNA;
	}

	@Override
	public double distance(Object toCompare) {
		DNAStrand s = (DNAStrand) toCompare;
		double dist = 0d;
		for (int i = 0; i < DNA.length(); i++) {
			if (DNA.charAt(i) != s.DNA.charAt(i)) {
				dist++;
			}
		}
		return dist;
	}

	@Override
	public KData getCentroid() {
		return centroid;
	}

	@Override
	public void setCentroid(KData d) {
		this.centroid = d;
	}

	@Override
	public boolean equals(Object o) {
		if (!(o instanceof DNAStrand)) {
			return false;
		}

		DNAStrand d = (DNAStrand) o;
		return d.DNA.equals(DNA);
	}

	@Override
	public int hashCode() {
		return DNA.hashCode();
	}

	@Override
	public String toString() {
		return "Strand: " + DNA;
	}
}
