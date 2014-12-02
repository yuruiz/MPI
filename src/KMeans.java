import java.util.ArrayList;
import java.util.List;

import mpi.*;

public class KMeans {

	private List<KData> data;
	private int k;
	private KData[] centroids;

	private static final int CENTROIDS_TAG = 0;

	public KMeans(List<KData> data, int k) {
		this.data = data;
		this.k = k;
		centroids = new KData[k];
	}

	public void cluster() {
		int myRank = MPI.COMM_WORLD.Rank();
		int size = MPI.COMM_WORLD.Size();

		// if master
		if (myRank == 0) {
			for (int i = 1; i < size; i++) {
				MPI.COMM_WORLD.Send(centroids, 0, k, MPI.OBJECT, i,
						CENTROIDS_TAG);
			}
		}
		// if slave
		else {
			MPI.COMM_WORLD.Recv(centroids, 0, k, MPI.OBJECT, 0, CENTROIDS_TAG);
			/*
			 * For each data, re-choose centroid
			 */
			double min = Double.MAX_VALUE;
			for (KData d : data) {
				
			}
		}
	}
}
