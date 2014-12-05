import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

import mpi.*;

public class KMeans {

	private List<KData> data;
	private int k;
	private KData[] centroids;
	private Cluster[] clusters;
	private Map<KData, Cluster> map;

	// tag of sending centroids
	private static final int CENTROIDS_TAG = 0;
	// tag of sending data
	private static final int DATA_TAG = 1;
	// max iterations allowed
	private static final int MAX_ITERATION = 1000;

	/**
	 * A new k means instance takes a set of data and number of clusters
	 * expected to have
	 * 
	 * @param data
	 * @param k
	 */
	public KMeans(List<KData> data, int k) {
		this.data = data;
		this.k = k;
		centroids = new KData[k];
		clusters = new Cluster[k];
		map = new HashMap<KData, Cluster>();

	}

	public void cluster() {

		int myRank = MPI.COMM_WORLD.Rank();
		int size = MPI.COMM_WORLD.Size();

		// record the time of starting clustering
		long startTime = System.currentTimeMillis();

		// initialize several random centroids
		if (myRank == 0) {
			initialize();
		}

		/*
		 * Start iteration
		 */
		for (int j = 0; j < MAX_ITERATION; j++) {
			// if master
			if (myRank == 0) {

				List<KData> newData = new ArrayList<KData>(data.size());
				/*
				 * Master send the newly generated centroids to each slave
				 */
				for (int i = 1; i < size; i++) {
					MPI.COMM_WORLD.Send(centroids, 0, k, MPI.OBJECT, i,
							CENTROIDS_TAG);
				}

				/*
				 * Master receive the data from the slaves with the newly chosen
				 * centroid
				 */
				for (int i = 1; i < size; i++) {
					/*
					 * set up buffer
					 */
					KData[] temp = new KData[data.size() / size + 1];
					MPI.COMM_WORLD.Recv(temp, 0, temp.length, MPI.OBJECT, i,
							DATA_TAG);
					/*
					 * add data to the list
					 */
					for (KData d : temp) {
						if (d != null) {
							newData.add(d);
						}
					}
				}

				/*
				 * Update the clusters
				 */
				for (Cluster c : clusters) {
					c.setMember(new ArrayList<KData>());
				}

				/*
				 * Add the data to the cluster it belongs to
				 */
				for (KData d : newData) {
					Cluster c = map.get(d.getCentroid());
					c.getMember().add(d);
				}

				/*
				 * mapping from centroid to cluster
				 */
				map = new HashMap<KData, Cluster>();

				/*
				 * recalculate the centroid of clusters and update the centroids
				 * array
				 */
				int count = 0;
				for (Cluster c : clusters) {
					c.updateCentroid();
					map.put(c.getCentroid(), c);
					centroids[count] = c.getCentroid();
					count++;
				}

			}
			// if slave
			else {

				/*
				 * Get the centroids from master
				 */
				MPI.COMM_WORLD.Recv(centroids, 0, k, MPI.OBJECT, 0,
						CENTROIDS_TAG);
				/*
				 * For each data, re-choose centroid
				 */
				List<KData> newData = new ArrayList<KData>();
				int[] range = this.getRange(size, myRank);

				/*
				 * For each data, calculate which centroid is closes to them
				 */
				for (int i = range[0]; i < range[1] && i < data.size(); i++) {
					KData d = data.get(i);
					newData.add(d);
					double min = Double.MAX_VALUE;
					for (KData cen : centroids) {
						if (d.distance(cen) < min) {
							d.setCentroid(cen);
							min = d.distance(cen);
						}
					}
				}

				/*
				 * Send back the data with newly assigned centroid to master
				 */
				MPI.COMM_WORLD.Send(newData.toArray(), 0, newData.size(),
						MPI.OBJECT, 0, DATA_TAG);

			}
		}

		if (myRank == 0) {
			for (int i = 0; i < centroids.length; i++) {
				System.out.println(centroids[i]);
			}

		}

		long endTime = System.currentTimeMillis();
		System.out.println("Processor " + myRank + " Time taken: "
				+ (endTime - startTime));

	}

	private void initialize() {

		Set<Integer> set = new HashSet<Integer>();
		Random r = new Random();

		while (set.size() < k) {
			set.add(r.nextInt(data.size()));
		}

		Iterator<Integer> iterator = set.iterator();
		for (int i = 0; i < k; i++) {
			int temp = iterator.next();
			centroids[i] = data.get(temp);
			clusters[i] = new Cluster(centroids[i], new ArrayList<KData>());
			map.put(centroids[i], clusters[i]);

		}

	}

	private int[] getRange(int size, int rank) {
		int[] range = new int[2];
		int piece = (int) Math.ceil((double) data.size() / (double) size);
		range[0] = Math.min(data.size() - 1, (rank - 1) * piece);
		range[1] = Math.min(data.size() - 1, range[0] + piece - 1);

		return range;
	}

}
