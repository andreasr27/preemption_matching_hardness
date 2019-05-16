# Python program to find 
# maximal Bipartite matching. 
import numpy as np



def list_to_adj_matrix(list_of_edges, num_vtxs):
#''' this is a function that takes as input a list of edges,
#    and the number of vertexes in each side of the graph
#    and outputs the adjajency matrix of this graph
#    Note: THE GRAPH IS ASSUME TO BE BIPARTITE
#    that means that an edge [2,3] in the list of edges denotes
#    an edge between L(2) and R(3) (where L and R denote the left
#    and right part of the bipartite graph respectively'''
	A = np.zeros((2*num_vtxs, 2*num_vtxs))
	for e in list_of_edges:
		vL = e[0]
		vR = e[1]
		A[vL, num_vtxs + vR] = 1
	return A



class GFG: 
	def __init__(self,graph): 
		
		# residual graph 
		self.graph = graph 
		self.ppl = len(graph) 
		self.jobs = len(graph[0]) 

	# A DFS based recursive function 
	# that returns true if a matching 
	# for vertex u is possible 
	def bpm(self, u, matchR, seen): 

		# Try every job one by one 
		for v in range(self.jobs): 

			# If applicant u is interested 
			# in job v and v is not seen 
			if self.graph[u][v] and seen[v] == False: 
				
				# Mark v as visited 
				seen[v] = True

				'''If job 'v' is not assigned to 
				an applicant OR previously assigned 
				applicant for job v (which is matchR[v]) 
				has an alternate job available. 
				Since v is marked as visited in the 
				above line, matchR[v] in the following 
				recursive call will not get job 'v' again'''
				if matchR[v] == -1 or self.bpm(matchR[v], 
											matchR, seen): 
					matchR[v] = u 
					return True
		return False

	# Returns maximum number of matching 
	def maxBPM(self): 
		'''An array to keep track of the 
		applicants assigned to jobs. 
		The value of matchR[i] is the 
		applicant number assigned to job i, 
		the value -1 indicates nobody is assigned.'''
		matchR = [-1] * self.jobs 
		
		# Count of jobs assigned to applicants 
		result = 0
		for i in range(self.ppl): 
			
			# Mark all jobs as not seen for next applicant. 
			seen = [False] * self.jobs 
			
			# Find if the applicant 'u' can get a job 
			if self.bpm(i, matchR, seen): 
				result += 1
		return result 



#edge_lst = [[0, 0],
#	   [0, 1],
#           [1, 0],
#           [1, 2],
#           [2, 1]]
#num_vtxs = 3
#for i in range(0,len(edge_lst)):
#	bpGraph  = list_to_adj_matrix(edge_lst[:i+1], num_vtxs)
#	g = GFG(bpGraph) 
#	print ("Maximum number of applicants that can get job is %d " % g.maxBPM()) 
#bpGraph =[[0, 1, 1, 0, 0, 0], 
#		[1, 0, 0, 1, 0, 0], 
#		[0, 0, 1, 0, 0, 0], 
#		[0, 0, 1, 1, 0, 0], 
#		[0, 0, 0, 0, 0, 0], 
#		[0, 0, 0, 0, 0, 1]] 



# This code is contributed by Neelam Yadav 

