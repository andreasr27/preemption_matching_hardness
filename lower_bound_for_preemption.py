import numpy as np
import matplotlib.pyplot as plt




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
			edge_vector[t*T] = 1
			for t_prime in range(t*T+1, (t+1)*T):
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
#constraints for left vertexes
for V in left_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	row_to_add = np.zeros(T*T)
	print(adjacent_edges_arrivals)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	A_degree_constraints.append(row_to_add)

#constraints for right vertexes
for V in right_vertexes_list:
	adjacent_edges_arrivals = V.get_adjacent_edges()
	row_to_add = np.zeros(T*T)
	for t in adjacent_edges_arrivals:
		row_to_add = row_to_add + edge_vectors_lst[t]
	A_degree_constraints.append(row_to_add)





A_degree_constraints = np.array(A_degree_constraints)
print(A_degree_constraints)






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
