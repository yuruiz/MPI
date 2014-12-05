import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

import mpi.MPI;

public class Main {

	private static final int SIZE_TAG = 3;
	private static final int DATA_TAG = 4;

	public static void main(String[] args) {
		MPI.Init(args);

		String fileName = args[3];
		String type = args[4];

		if (!type.equalsIgnoreCase("DNA") && !type.equalsIgnoreCase("POINT")) {
			printUsage();
			return;
		}

		int myRank = MPI.COMM_WORLD.Rank();
		int size = MPI.COMM_WORLD.Size();
		List<KData> dataList;

		if (myRank == 0) {
			dataList = new ArrayList<KData>();

			if (type.equalsIgnoreCase("Point")) {
				parsePoints(dataList, fileName);
			} else {
				parseDNA(dataList, fileName);
			}
			/*
			 * Read data into file, parse data into a list of points
			 */

			/*
			 * First of, tell slaves the size of data
			 */
			int[] length = new int[1];
			length[0] = dataList.size();
			for (int i = 1; i < size; i++) {
				MPI.COMM_WORLD.Send(length, 0, 1, MPI.INT, i, SIZE_TAG);
			}

			for (int i = 1; i < size; i++) {
				MPI.COMM_WORLD.Send(dataList.toArray(), 0, dataList.size(),
						MPI.OBJECT, i, DATA_TAG);
			}

		} else {

			/*
			 * Receive the length of the data
			 */
			int[] length = new int[1];
			MPI.COMM_WORLD.Recv(length, 0, 1, MPI.INT, 0, SIZE_TAG);

			/*
			 * Receive data
			 */
			KData[] data = new KData[length[0]];
			MPI.COMM_WORLD.Recv(data, 0, length[0], MPI.OBJECT, 0, DATA_TAG);

			dataList = Arrays.asList(data);

		}

		KMeans k = new KMeans(dataList, 3);
		k.cluster();

		MPI.Finalize();
	}

	private static void parsePoints(List<KData> points, String fileName) {

		try {
			Scanner s = new Scanner(new File(fileName));
			while (s.hasNextLine()) {
				String line = s.nextLine();
				String[] coordinate = line.split("[,]");
				double x = Double.parseDouble(coordinate[0]);
				double y = Double.parseDouble(coordinate[1]);
				Point p = new Point(x, y);
				points.add(p);
			}
			s.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	private static void parseDNA(List<KData> DNAs, String fileName) {
		try {
			Scanner s = new Scanner(new File(fileName));
			while (s.hasNextLine()) {
				String line = s.nextLine();
				for (int i = 0; i < line.length(); i++) {
					if(!Character.isAlphabetic(line.charAt(i))){
						throw new RuntimeException("fuck");
					}
				}
				DNAStrand dna = new DNAStrand(line);
				DNAs.add(dna);
			}
			s.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private static void printUsage() {
		System.out.println("Usage: java Main <DatFile> <Type>");
		System.out.println("Type should be either POINT or DNA");
	}
}
