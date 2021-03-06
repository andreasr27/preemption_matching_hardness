import numpy as np
import matplotlib.pyplot as plt
import maximum_matching as mm
from scipy.optimize import linprog



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
		#Initialization of object vectors
		if first_line == 0:
			num_edges , num_vtxs = map(int, line.split())
			T = num_edges
			left_seen  = np.zeros(num_vtxs)
			right_seen = np.zeros(num_vtxs)
			left_vertexes_list =  [Vertex(i, 0, []) for i in range(num_vtxs)]
			right_vertexes_list = [Vertex(i, 1, []) for i  in range(num_vtxs)]
			first_line =1
		else:
		#here I create the vertexes that I have not already see, and I upgrade the list of edges adjacent to this vertex 
		# (each edge is stored as (a,b, t) where t denote the arrival time of this edge )
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
				left_seen[vL] = 1
			else:
				left_vertexes_list[vL].add_edge(e)
			#########################################
			if right_seen[vR] == 0:
				right_vertexes_list[vR].add_edge(e)
				right_seen[vR] = 1
			else:
				right_vertexes_list[vR].add_edge(e)








#here I am constructing a mask
Mask_matrix = []
mask = np.zeros(T*T)
for t in range(0,T):
	for i in range(0,T):
		mask[i*T + t] = 1
	Mask_matrix.append(mask.copy())
Mask_matrix = np.array(Mask_matrix)










##################   DEGREE CONSTRAINTS ######################
#here I will construct the degree constraint of each vertex
#each vertex has T degree constraints, one whenever a new edge arrives.  (---> in order to have an easier impleme)

A_degree_constraints = np.zeros((1, T*T))
for V in left_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	row_to_add = np.zeros(T*T)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	Matrix_to_add = Mask_matrix * row_to_add
	A_degree_constraints = np.vstack((A_degree_constraints,Matrix_to_add))

A_degree_constraints = np.delete(A_degree_constraints, (0), axis=0)



#degree constraints for right vertexes
for V in right_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	#print(adjacent_edges_arrivals)
	row_to_add = np.zeros(T*T)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	Matrix_to_add = Mask_matrix * row_to_add
	A_degree_constraints = np.vstack((A_degree_constraints,Matrix_to_add))


#turn list of lists that represent the degree constarints into a numpy matrix

A_degree_constraints = np.array(A_degree_constraints)
#print( A_degree_constraints)
#exit()


# we want an additional coloumn of zeros in order that represent the terms that are multiplied to the competitiveness ratio
c1 = np.zeros((A_degree_constraints.shape[0], 1))
#this final submatrix which represent the degree constraints of the vertexes has the correct sign
A_degree_constraints = np.hstack((A_degree_constraints, c1))






##################   NONNEGATIVITY EDGE  CONSTRAINTS ######################
# let e \in T and t(e) be the arrival time of the edge e, then the nonnegativity constraint of each edge can be formulated as:
#								z_e_t(e) - z_e_(t(e)+1) - z_e_(t(e)+2)-...- z_e_T >=0 \forall e \in E
A_nonneg_edge_constraint = [] 
for t in range(0,T):
	A_nonneg_edge_constraint.append(edge_vectors_lst[t])
A_nonneg_edge_constraint = np.array(A_nonneg_edge_constraint)
#this final submatrix which represent the nonnegativity of the edge weight  constraints has  incorrect sign
A_nonneg_edge_constraint = - A_nonneg_edge_constraint
# we want an additional coloumn of zeros in order that represent the terms that are multiplied to the competitiveness ratio
c2 = np.zeros((A_nonneg_edge_constraint.shape[0], 1))
A_nonneg_edge_constraint = np.hstack((A_nonneg_edge_constraint, c2))




##################   COMPETITIVENESS CONSTRAINTS ######################
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


#this final submatrix which represent a part of the competitiveness constraints (it does not have the last coloumn which is competitiveness ration coloumn) has the wrong sign 
A_comp_constraints = - np.array(A_comp_constraints)

#now I have to calculate the size of the matching in after each edge addition

matchings_size = np.zeros((len(edges_lst), 1))
for i in range(0,len(edges_lst)):
	bpGraph  = mm.list_to_adj_matrix(edges_lst[:i+1], num_vtxs)
	g = mm.GFG(bpGraph) 
	matchings_size[i] = g.maxBPM()


A_comp_constraints = np.hstack((A_comp_constraints, matchings_size))



A = np.vstack(( A_degree_constraints , A_nonneg_edge_constraint, A_comp_constraints))


c = np.zeros(T*T+1)
c[-1] = -1


b = np.zeros(2*num_vtxs*num_edges + num_edges + num_edges)
for i in range(0, 2*num_vtxs*num_edges):
	b[i] = 1
#print(b)
#print(c)
#print(" b shape is ", b.shape)
#print(" c shape is ", c.shape)
res = linprog(c, A_ub=A, b_ub=b,  options={"disp": True})
print(res)














