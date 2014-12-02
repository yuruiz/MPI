import mpi.*;

public class Test {
	public static void main(String[] args) {
		MPI.Init(args);

		int myRank = MPI.COMM_WORLD.Rank();
		if (myRank == 0) {
			char[] message = "Hello, World".toCharArray();
			MPI.COMM_WORLD.Send(message, 0, message.length, MPI.CHAR, 0, 99);
		} else {
			char[] message = new char[20];
			MPI.COMM_WORLD.Recv(message, 0, 20, MPI.CHAR, 0, 99);
			System.out.println(new String(message));
		}

		MPI.Finalize();

	}
}
