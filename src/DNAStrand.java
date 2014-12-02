/**
 * 
 * @author siyuwei
 *
 */
public class DNAStrand implements KData {

	private String DNA;

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
}
