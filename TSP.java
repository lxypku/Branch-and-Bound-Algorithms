/*
Author: Victor Li
Date  : 2021-04-15
@@ Branch and Bound Algorithm for Traveling Salesman Problem.
*/
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Collections;

public class TSP{
	public static int n;
	public static int[][] adj;
	public static ArrayList<Integer> edge_l = new ArrayList<Integer>(); // Edge lengths.
	public static int[] sum; // Prefix sum of the sorted edge lengths.
	public static int inf = Integer.MAX_VALUE;
	public static int ans = inf;
	public static ArrayList<Integer> solution;
	public static int cnt = 0; // Recording the number of the parital solutions evaluated.
	public static class Path{
		int length, current_cost, lower_bound, last;
		ArrayList<Integer> path;
		boolean[] in_path;
		public Path(){
			this.length = 0;
			this.current_cost = 0;
			this.lower_bound = sum[n];
			this.path = new ArrayList<Integer>();
			this.path.add(0);
			this.last = 0;
			this.in_path = new boolean[n];
			this.in_path[0] = true;
			for (int i = 1; i < n; i++)
				this.in_path[i] = false;
		}
		public Path(Path that){
			this.length = that.length;
			this.current_cost = that.current_cost;
			this.lower_bound = that.lower_bound;
			this.path = new ArrayList<Integer>();
			for (int i = 0; i < that.path.size(); i++)
				this.path.add(that.path.get(i));
			this.last = that.last;
			this.in_path = new boolean[n];
			for (int i = 0; i < n; i++)
				this.in_path[i] = that.in_path[i];
		}
	}
	public static Comparator<Path> path_cmp = new Comparator<Path>(){
		@Override
		public int compare(Path p1, Path p2){
			return p2.lower_bound - p1.lower_bound;
		}
	};
	public static int lower_bound(Path p){
		return sum[n - p.length];
	}
	public static void main(String[] args) throws Exception{
		String input_file = "TSP_Input.csv";
		BufferedReader br = new BufferedReader(new FileReader(input_file));
		String line = br.readLine();
		n = Integer.parseInt(line);
		adj = new int[n][n];
		for (int i = 0; i < n; i++)
			for (int j = 0; j < n; j++)
				adj[i][j] = -1;
		while ((line=br.readLine())!=null){
			String s[] = line.split(",");
			int u = Integer.parseInt(s[0]);
			int v = Integer.parseInt(s[1]);
			int d = Integer.parseInt(s[2]);
			adj[u][v] = d;
			edge_l.add(d);
		}
		Collections.sort(edge_l);
		sum = new int[n+1];
		sum[0] = 0;
		for (int i = 1; i <= n; i++)
			sum[i] += edge_l.get(i-1);
		
		PriorityQueue<Path> q = new PriorityQueue<Path>(100, path_cmp);
		q.add(new Path());
		while (!q.isEmpty()){
			Path p = q.poll();
			if (p.length == n-1){
				if (adj[p.last][0] != -1)
					if (p.current_cost + adj[p.last][0] < ans){
						ans = p.current_cost + adj[p.last][0];
						solution = (ArrayList<Integer>)p.path.clone();
					}
				continue;
			}	
			if (p.lower_bound >= ans) continue;
			for (int u = 1; u < n; u++)
				if (!p.in_path[u] && adj[p.last][u] != -1){
					Path r = new Path(p);
					r.length++;
					r.current_cost += adj[p.last][u];
					r.lower_bound = lower_bound(r);
					r.path.add(u);
					r.last = u;
					r.in_path[u] = true;
					cnt++;
					if (r.lower_bound >= ans) continue;
					q.add(r);
				}
		}
		System.out.println("The length of the shortest route for the traveling salesman: "+Integer.toString(ans));
		System.out.println("The shortest route: ");
		for (int i = 0; i < n; i++)
			System.out.print(Integer.toString(solution.get(i))+" --> ");
		System.out.println(0);
		System.out.println("The number of the parital solutions evaluated: "+Integer.toString(cnt));
	}
}