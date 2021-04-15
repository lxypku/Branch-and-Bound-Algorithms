'''
Author: Victor Li
Date  : 2021-04-14  
@@ Branch and Bound Algorithm for Job Assignment Problem.
@@ Branch and Bound is often used to solve difficult optimization problems when we can not
   find any efficient solutions using Divide-and-Conquer, Greedy or Dynamic Programming.
'''
from queue import PriorityQueue

inf = 1e9

def generate_an_empty_solution(n):
	return [-1 for i in range(n)]

def brute_force(cost_matrix):
	def dfs(n, i, current_solution, current_cost):
	# Use naive depth first search without pruning as brute force method.
		nonlocal ans, optimal_solution, cnt
		# nonlocal keyword in python3. 
		if i == n:
			cnt += 1
			if current_cost < ans:
				ans = current_cost
				optimal_solution = current_solution[:]
			return
		for j in range(n):
			if not j in current_solution:
				current_solution[i] = j
				current_cost += cost_matrix[i][j]
				dfs(n, i+1, current_solution, current_cost)
				# Backtracking.
				current_cost -= cost_matrix[i][j]
				current_solution[i] = -1
	n = len(cost_matrix)
	ans = inf
	optimal_solution = generate_an_empty_solution(n)
	cnt = 0 
	# Number of full solutions investigated.
	dfs(n, 0, generate_an_empty_solution(n), 0)
	return {'Minimal Total Cost':ans, 
	 		'Optimal Solution':optimal_solution, 
	 		'Number of Full Solutions Investigated':cnt}

def get_csf(cost_matrix, current_solution):
	# Get the current partial solution's Cost So Far.
	r = 0
	n = len(current_solution)
	for i in range(n):
		if current_solution[i] != -1:
			r += cost_matrix[i][current_solution[i]]
		else:
			break
	return r

def find_min_cost(cost_matrix, i, available_tasks):
	# Find the task from the available_tasks which can be assigned to person i with minimum cost.
	min_cost = inf
	for j in available_tasks:
		if cost_matrix[i][j] < min_cost:
			min_cost = cost_matrix[i][j]
			min_cost_idx = j
	return min_cost, min_cost_idx 
	# Return the minimum cost as well as the id of the minimum-cost task assigned to person i.

def get_gfc(cost_matrix, current_solution):
	# Get the current partial solution's Guaranteed Future Cost.
	# Lower bound = CSF + GFC
	r = 0
	n = len(current_solution)
	available_tasks = [i for i in range(n)]
	for i in range(n):
		if current_solution[i] != -1:
			available_tasks.remove(current_solution[i])
		else:
			min_cost, _ =  find_min_cost(cost_matrix, i, available_tasks)
			r += min_cost
	return r

def get_ffc(cost_matrix, current_solution):
	# Get the current partial solution's Feasible Future Cost.
	# Upper bound = CSF + FFC
	r = 0
	n = len(current_solution)
	available_tasks = [i for i in range(n)]
	for i in range(n):
		if current_solution[i] != -1:
			available_tasks.remove(current_solution[i])
		else:
			min_cost, min_cost_idx = find_min_cost(cost_matrix, i, available_tasks)
			r += min_cost
			available_tasks.remove(min_cost_idx)
			# Since the task min_cost_idx is assigned to person i, we remove it from available_tasks. 
	return r

def job_assignment(cost_matrix):
	n = len(cost_matrix)
	global_upper_bound = get_ffc(cost_matrix, generate_an_empty_solution(n))
	initial_lower_bound = get_gfc(cost_matrix, generate_an_empty_solution(n))
	Q = PriorityQueue()
	Q.put((initial_lower_bound, global_upper_bound, generate_an_empty_solution(n), 0))
	# A state contains the lower bound, the upper bound, the current partial solution and its length.
	cnt = 0 
	# Number of partial solutions evaluated.
	while not Q.empty():
		lower_bound, upper_bound, current_solution, l = Q.get()
		# Select the most promising state i.e. the one with minimum lower bound.
		if l == n:
			return {'Minimal Total Cost':lower_bound, 
	 				'Optimal Solution':current_solution, 
	 				'Number of Partial or Full Solutions Evaluated':cnt}
		for j in range(n):
			if not j in current_solution:
				# Go over all possible next decisions.
				new_solution = current_solution[:]
				new_solution[l] = j
				lower_bound_ =  get_csf(cost_matrix, new_solution) + get_gfc(cost_matrix, new_solution)
				upper_bound_ =  get_csf(cost_matrix, new_solution) + get_ffc(cost_matrix, new_solution)
				# Calculate lower_bound and upper_bound.
				cnt += 1
				if lower_bound_ > global_upper_bound:
					continue
				if upper_bound_ < global_upper_bound:
					global_upper_bound = upper_bound_ # Update global upper bound.
				Q.put((lower_bound_, upper_bound_, new_solution, l+1)) # Add new state to the priority queue.
	

def print_answer(d):
	for k, v in list(d.items()):
		print(k, ':', v)
	print()

if __name__ == "__main__":
	# cost_matrix[i][j] denotes the cost to assign task j to person i.
	# Sample 1
	cost_matrix = [[10,15,4,12,9],[7,18,3,10,16],[4,5,14,12,10],[17,2,18,6,21],[21,18,2,10,25]]
	print("==== For Test Case 1 ====")
	print("Brute Force Solution:")
	print_answer(brute_force(cost_matrix))
	print("Branch and Bound Solution:")
	print_answer(job_assignment(cost_matrix))
	# Sample 2
	cost_matrix = [[1,2,3],[4,6,8],[10,13,16]]
	print("==== For Test Case 2 ====")
	print("Brute Force Solution:")
	print_answer(brute_force(cost_matrix))
	print("Branch and Bound Solution:")
	print_answer(job_assignment(cost_matrix))

	