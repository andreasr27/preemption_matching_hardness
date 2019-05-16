import numpy as np
import matplotlib.pyplot as plt
import maximum_matching as mm



class Vertex:
#	ID -> identifier of the vertex
#	if Right = 1 then the vertex belongs to the right side of the bipartite graph, otherwise on the left'''
	def __init__(self, ID, Right, first_edge):
		self.ID = ID
		self.Right  = Right
		if first_edge == []:
			self.edges = []
		else:
			self.edges.append(first_edge)

	def add_edge(self, e):
		self.edges.append(e)

	def print(self):
		if self.Right == 1:
			loc = "right"
		else:
			loc = "left"
		print("I am the vertex ", self.ID, "  I am in the ", loc, " side of the bp graph")
		print("the edges adjacent to me are :")
		self.print_edge_list()
		

	def print_edge_list(self):
		res = ""
		for edge in self.edges:
			vL = edge[0]
			vR = edge[1]
			t  = edge[2]
			res = res + "-(" + str(vL) + "," + str(vR) + ")-"
		print(res)

	def get_adjacent_edges(self):
		ts = []
		for edge in self.edges:
			t  = edge[2]
			ts.append(t)
		return ts


# we have three types of constraints:
#  1) degree constraints
#  2) nonnegativity constraints
#  3) competitiveness constraints




with open("preemption_input.txt", 'r') as f:
	first_line = 0
	t = -2
	edges_lst = []
	edge_vectors_lst = []
	for line in f.readlines():
	#t will denote the arrival itme
		t+=1
		if first_line == 0:
			num_edges , num_vtxs = map(int, line.split())
			T = num_edges
			left_seen  = np.zeros(num_vtxs)
			right_seen = np.zeros(num_vtxs)
			left_vertexes_list =  [Vertex(i, 0, []) for i in range(num_vtxs)]
			right_vertexes_list = [Vertex(i, 1, []) for i  in range(num_vtxs)]
			first_line =1
		else:
		#here I create the vertexes
			vL, vR = map(int, line.split())
			e = [vL, vR, t]
			edges_lst.append(e)
			edge_vector = np.zeros(T*T)
			edge_vector[t*T+t] = 1
			for t_prime in range(t*T+t+1, (t+1)*T):
				edge_vector[t_prime] = -1
			edge_vectors_lst.append(edge_vector)
			#create or update (depending if the vertex already appeared) his object and update the list
			if left_seen[vL] == 0:
				left_vertexes_list[vL].add_edge(e)
				left_seen[vR] = 1
			else:
				left_vertexes_list[vL].add_edge(e)
			#########################################
			if right_seen[vR] == 0:
				right_vertexes_list[vL].add_edge(e)
				right_seen[vR] = 1
			else:
				right_vertexes_list[vL].add_edge(e)
















#here I will construct the degree constraint of each vertex

A_degree_constraints = []
#degree constraints for left vertexes
for V in left_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	row_to_add = np.zeros(T*T)
#	print(adjacent_edges_arrivals)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	A_degree_constraints.append(row_to_add)

#degree constraints for right vertexes
for V in right_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	row_to_add = np.zeros(T*T)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	A_degree_constraints.append(row_to_add)
#turn list of lists that represent the degree constarints into a numpy matrix
A_degree_constraints = np.array(A_degree_constraints)






# let e \in T and t(e) be the arrival time of the edge e, then the nonnegativity constraint of each edge can be formulated as:
#								z_e_t(e) - z_e_(t(e)+1) - z_e_(t(e)+2)-...- z_e_T >=0 \forall e \in E
A_nonneg_edge_constraint = [] 
for t in range(0,T):
	A_nonneg_edge_constraint.append(-edge_vectors_lst[t])
A_nonneg_edge_constraint = np.array(A_nonneg_edge_constraint)





#here I will construct the competitiveness constraints
A_comp_constraints = []
accum_lst = [0]*(T*T)

for t in range(0,len(edge_vectors_lst)):
	accum_lst += edge_vectors_lst[t]



for t in range(0,T):
	#t denote the particular arrival time of an edge
	v = accum_lst.copy()
	for i in range(0,T):
		# we will handle the variables of each edge separately
		# the variables of edge that arrived at time i are between the positions
		# i*T --> i*T + (T-1)
		
		# here I will make the modification of the edges
		for j in range(i*T + (t+1) , i*T + T):
			v[j] = 0
	
	A_comp_constraints.append(v)


A_comp_constraints = np.array(A_comp_constraints)
print(A_comp_constraints)
exit()















#for t in range(0,T):
#	#t denote the particular arrival time of an edge
#	print("-"*10)
#	v = accum_lst.copy()
#	print("I am at time ", t)
#	print("and my initial vector is ")
#	print(v)
#	print(accum_lst)
#	#print(v)
#	for i in range(0,T):
#		# we will handle the variables of each edge separately
#		# the variables of edge that arrived at time i are between the positions
#		# i*T --> i*T + (T-1)
#		my_str = ""
#		for j in range(i*T , i*T + T):
#			my_str += " "+str(v[j])
#		#	print("I will set zero the ", j, "th coordinate ")
#		print("variables of edge ", i, "at time ", t,"  ",  my_str)
#		
#		
#		# here I will make the modification of the edges
#		for j in range(i*T + (t+1) , i*T + T):
#			v[j] = 0
#
#
#
#		my_str = ""
#		for j in range(i*T , i*T + T):
#			my_str += " "+str(v[j])
#		#	print("I will set zero the ", j, "th coordinate ")
#
#		print("variables of edge ", i, "at time ", t,"  ",  my_str)
#
#
#	print("I finished time ", t)
#	print("-"*10)
#








for i in range(0,len(edges_lst)):
	bpGraph  = mm.list_to_adj_matrix(edges_lst[:i+1], num_vtxs)
	g = mm.GFG(bpGraph) 
	g.maxBPM()










exit()

for t in range(0,T):
	print("-"*10)
	print(t)
	print(edge_vectors_lst[t])
	print("-"*10)

exit()

for V in left_vertexes_list:
	print("-"*10)
	V.print()
	print("-"*10)
