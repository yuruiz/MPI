import java.util.ArrayList;
import java.util.List;

public class Util {

	public static KData getCentroid(List<KData> samples) {

		double xSum = 0d;
		double ySum = 0d;

		if (samples.get(0) instanceof Point) {
			for (KData d : samples) {
				Point p = (Point) d;
				xSum += p.getX();
				ySum += p.getY();
			}

			return new Point(xSum / samples.size(), ySum / samples.size());
		}

		if (samples.get(0) instanceof DNAStrand) {
			DNAStrand dna = (DNAStrand) samples.get(0);
			int length = dna.getDNA().length();

			Count A = new Count('A', length);
			Count G = new Count('C', length);
			Count C = new Count('C', length);
			Count T = new Count('T', length);

			for (KData d : samples) {
				DNAStrand s = (DNAStrand) d;
				String strand = s.getDNA();
				for (int i = 0; i < strand.length(); i++) {
					switch (strand.charAt(i)) {
					case 'A':
						A.count[i]++;
					case 'G':
						G.count[i]++;
					case 'C':
						C.count[i]++;
					case 'T':
						T.count[i]++;
					default:
						break;
					}
				}
			}

			List<Count> list = new ArrayList<Count>();
			StringBuilder b = new StringBuilder();
			for (int i = 0; i < length; i++) {
				int max = 0;
				char base = ' ';
				for (int j = 0; j < list.size(); j++) {
					if (list.get(j).count[i] > max) {
						max = list.get(j).count[i];
						base = list.get(i).base;
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

	private static class Count {
		private char base;
		private int[] count;

		public Count(char base, int size) {
			this.base = base;
			count = new int[size];
		}

	}
}
