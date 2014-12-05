import java.util.ArrayList;
import java.util.List;

public class Util {

	/**
	 * Get the centroid of a list of data
	 * 
	 * @param samples
	 * @return
	 */
	public static KData getCentroid(List<KData> samples) {

		double xSum = 0d;
		double ySum = 0d;

		if (samples.size() == 0) {
			return null;
		}

		/*
		 * If the data is a list of 2d points, simply calculate the mean
		 */
		if (samples.get(0) instanceof Point) {
			for (KData d : samples) {
				Point p = (Point) d;
				xSum += p.getX();
				ySum += p.getY();
			}

			return new Point(xSum / samples.size(), ySum / samples.size());
		}

		/*
		 * If data is a list of DNA strands, count the number of appearances of
		 * each kind of base at each position, assign the base as the one
		 * appears the most
		 */
		if (samples.get(0) instanceof DNAStrand) {
			DNAStrand dna = (DNAStrand) samples.get(0);
			int length = dna.getDNA().length();

			/*
			 * Four count array for four kinds of base
			 */
			Count A = new Count('A', length);
			Count G = new Count('G', length);
			Count C = new Count('C', length);
			Count T = new Count('T', length);

			/*
			 * Count the appearance of bases
			 */
			for (KData d : samples) {
				DNAStrand s = (DNAStrand) d;
				String strand = s.getDNA();
				for (int i = 0; i < strand.length(); i++) {
					switch (strand.charAt(i)) {
					case 'A':
						A.count[i]++;
						break;
					case 'G':
						G.count[i]++;
						break;
					case 'C':
						C.count[i]++;
						break;
					case 'T':
						T.count[i]++;
						break;
					default:
						break;
					}
				}
			}

			/*
			 * Assign the base that appears most frequent to a position
			 */
			List<Count> list = new ArrayList<Count>();
			list.add(A);
			list.add(G);
			list.add(C);
			list.add(T);
			
			
			StringBuilder b = new StringBuilder();
			for (int i = 0; i < length; i++) {
				int max = 0;
				char base = ' ';
				for (int j = 0; j < list.size(); j++) {
					//System.out.println(list.get(j).base + " " + list.get(j).count[i]);
					if (list.get(j).count[i] > max) {
						max = list.get(j).count[i];
						base = list.get(j).base;
					}
				}
				if (base == ' ') {
					throw new RuntimeException("wrong dna base");
				}
				b.append(base);
			}

			return new DNAStrand(b.toString());

		}

		throw new RuntimeException("wrong type");

	}

	/**
	 * Private helper class of encapsulating base and its count
	 * 
	 * @author siyuwei
	 *
	 */
	private static class Count {
		private char base;
		private int[] count;

		public Count(char base, int size) {
			this.base = base;
			count = new int[size];
		}

	}
}
