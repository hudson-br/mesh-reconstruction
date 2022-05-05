import numpy as np
import copy
import os

class MyMesh:
    def __init__(self,mesh_text):
        # self.mymesh = open(filename,'r')
        self.mesh_text = mesh_text
        # Need to initialise these lists so that np.vstack works properly
        self.list_of_vertices = np.empty(shape = [0,4])
        self.list_of_triangles = np.empty(shape = [0,4])
        self.get_number_of_triangles()
        self.get_number_of_vertices()
        self.get_list_of_vertices()
        self.get_list_of_triangles()
        
    def get_number_of_vertices(self):
        string_to_match = 'Vertices'
        for index, line in enumerate(self.mesh_text):
            line = line.rstrip()  # Need to remove the \n at the end of the line
            if line == string_to_match:
                # print("Number of vertices: ", self.mesh_text[index+1])
                break
        self.index_vertices = index
        self.number_of_vertices = int(self.mesh_text[index+1])
        # return [index,int(mesh[index+1])]

    def get_number_of_triangles(self):
        string_to_match = 'Triangles'
        for index, line in enumerate(self.mesh_text):
            line = line.rstrip() 
            if line == string_to_match:
                # print("Number of triangles: ", self.mesh_text[index+1])
                break
        self.index_triangles = index
        self.number_of_triangles = int(self.mesh_text[index+1])
    def get_list_of_vertices(self):
        for i in range(self.number_of_vertices):
            x = np.array(self.mesh_text[self.index_vertices+i+2].rstrip().split())
            y = x.astype(float)
            self.list_of_vertices = np.vstack((self.list_of_vertices, y)) 
    def get_list_of_triangles(self):
        for i in range(self.number_of_triangles):
            x_t = np.array(self.mesh_text[self.index_triangles+i+2].rstrip().split())
            y_t = x_t.astype(int)
            self.list_of_triangles = np.vstack((self.list_of_triangles, y_t))
    
    def symmetry_xy_plane(self):
        new_vertices = copy.deepcopy(self.list_of_vertices)
        new_vertices[:,2]*=-1
        self.list_of_vertices = np.vstack((self.list_of_vertices,new_vertices))
        self.number_of_vertices*=2
    
    def symmetry_xz_plane(self):
        new_vertices = copy.deepcopy(self.list_of_vertices)
        new_vertices[:,1]*=-1
        self.list_of_vertices = np.vstack((self.list_of_vertices,new_vertices))
        self.number_of_vertices*=2
    
    def symmetry_yz_plane(self):
        new_vertices = copy.deepcopy(self.list_of_vertices)
        new_vertices[:,0]*=-1
        self.list_of_vertices = np.vstack((self.list_of_vertices,new_vertices))
        self.number_of_vertices*=2

    def symmetric_triangles(self):
        new_triangles = copy.deepcopy(self.list_of_triangles)
        new_triangles[:,0]+=self.number_of_vertices
        new_triangles[:,1]+=self.number_of_vertices
        new_triangles[:,2]+=self.number_of_vertices
        self.list_of_triangles = np.vstack((self.list_of_triangles, new_triangles))
        self.number_of_triangles*=2
    def symmetrise_the_hell_out_of_the_mesh(self):
        self.symmetric_triangles()
        self.symmetry_xy_plane()
        self.symmetric_triangles()
        self.symmetry_yz_plane()
        self.symmetric_triangles()
        self.symmetry_xz_plane()
        
    def write_mesh(self, filename): 
        
        f = open(filename, 'w')
        f.write(self.mesh_text[0])
        f.write(self.mesh_text[1])
        f.write(self.mesh_text[2])
        f.write('Vertices\n')
        f.write(str(self.number_of_vertices)+'\n')
        for line in self.list_of_vertices:
            y=line.astype(str)
            f.write(y[0]+ ' '+ y[1] + ' ' + y[2]+ ' ' + y[3]+ '\n')
        
        f.write('\n')
        f.write('Triangles'+ '\n')
        f.write(str(self.number_of_triangles)+ '\n')

        for line in self.list_of_triangles:
            y = [int(i) for i in line]
            f.write(str(y[0])+ ' '+ str(y[1]) + ' ' + str(y[2])+ ' ' + str(y[3])+ '\n')

        f.write("End"+'\n')
        f.close()         


def read_text(file):
    with open(file,'r') as f:
        for line in f:
            print(line)




path_input = '/Users/morpho/TURLIERLAB Dropbox/Hudson Rocha/Postdoc/mesh-reconstruction/mesh_cytokinesis/'
os.chdir(path_input)
cwd = os.getcwd()

for elem in os.listdir(cwd):
    if elem.endswith('.mesh'):
        print(elem)
        mymesh = open(elem,'r')
        mesh_text = mymesh.readlines()
        mesh = MyMesh(mesh_text)
        mesh.symmetrise_the_hell_out_of_the_mesh()
        out_file = '../mesh_cytokinesis_symmetrised/'+elem
        mesh.write_mesh(filename = out_file)




# cwd = os.getcwd()
# print(cwd)
# # Open mesh to "symmetrize"
# mymesh = open('mesh.mesh','r')
# mesh_text = mymesh.readlines()

# mesh = MyMesh(mesh_text)
# mesh.symmetrise_the_hell_out_of_the_mesh()
# out_file = 'output/out_.mesh'
# mesh.write_mesh(filename = out_file)
