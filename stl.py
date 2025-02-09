import numpy as np
from xyz import XYZ


class STL:
    def __init__(self):
        self.triangles = []

    def add_triangle(self, v1, v2, v3, orientation):
        n = self.compute_normal_vector(v1, v2, v3, orientation)
        triangle = {'v1': v1, 'v2': v2, 'v3': v3, 'n': n}
        # calculate the normal vector

        self.triangles.append(triangle)

    def compute_normal_vector(self,v1, v2, v3, orientation):
        """
        Computes the normal vector of a plane defined by three points in 3D space and an orientation like 
        "x>0" or "y>0" or "z>0".
        
        Parameters:
        v1, v2, v3: Tuples or lists representing the coordinates of the three vertex (x, y, z).
        
        Returns:
        A numpy array representing the normal vector of the plane.
        """
        # Convert points to numpy arrays
        A = np.array(v1)
        B = np.array(v2)
        C = np.array(v3)
        
        # Compute vectors AB and AC
        AB = B - A
        AC = C - A
        
        # Compute the cross product of AB and AC
        normal_vector_1 = np.cross(AB, AC)
        normal_vector_2 = np.cross(AC, AB)
        if orientation == "x>0":
            #verify if x component of the normal vector is positive
            if normal_vector_1[0] >= 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2 
        if orientation == "x<0":
            #verify if x component of the normal vector is positive
            if normal_vector_1[0] < 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2 
        if orientation == "y>0":
            #verify if y component of the normal vector is positive
            if normal_vector_1[1] >= 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2
        if orientation == "y<0":
            #verify if y component of the normal vector is positive
            if normal_vector_1[1] < 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2
        if orientation == "z>0":
            #verify if z component of the normal vector is positive
            if normal_vector_1[2] >= 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2
        if orientation == "z<0":
            #verify if z component of the normal vector is positive
            if normal_vector_1[2] < 0 : 
                normal_vector = normal_vector_1 
            else:
                normal_vector = normal_vector_2
        #normalize the normal vector
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        return normal_vector
    

    def get_triangles(self):
        return self.triangles
    
    def import_xyz_model(self, xyz, x_len, y_len):
        #add triangles for base
        v1 = (xyz.allx[0], xyz.ally[0], 0)
        v2 = (xyz.allx[x_len - 1], xyz.ally[0], 0)
        v3 = (xyz.allx[x_len - 1], xyz.ally[y_len - 1], 0)
        self.add_triangle(v1, v2, v3, "z>0")
        v1 = (xyz.allx[0], xyz.ally[0], 0)
        v2 = (xyz.allx[x_len - 1], xyz.ally[y_len - 1], 0)
        v3 = (xyz.allx[0], xyz.ally[y_len - 1], 0)
        self.add_triangle(v1, v2, v3, "z>0")        
        # Add tringles for x border
        for i in range(x_len - 1):
            v1 = (xyz.allx[i], 0, 0)
            v2 = xyz.get_point(xyz.allx[i], 0)
            v3 = (xyz.allx[i+1], 0 ,0)
            self.add_triangle(v1, v2, v3, "y<0")
            v1 = xyz.get_point(xyz.allx[i], 0)
            v2 = xyz.get_point(xyz.allx[i+1], 0)
            v3 = (xyz.allx[i+1], 0 ,0)
            self.add_triangle(v1, v2, v3, "y<0")    

            v1 = (xyz.allx[i], xyz.ally[y_len - 1], 0)
            v2 = xyz.get_point(xyz.allx[i], xyz.ally[y_len - 1])
            v3 = (xyz.allx[i+1], xyz.ally[y_len - 1] ,0)
            self.add_triangle(v1, v2, v3, "y>0")
            v1 = xyz.get_point(xyz.allx[i], xyz.ally[y_len - 1])
            v2 = xyz.get_point(xyz.allx[i+1], xyz.ally[y_len - 1])
            v3 = (xyz.allx[i+1], xyz.ally[y_len - 1] ,0)
            self.add_triangle(v1, v2, v3, "y>0")  

        # Add tringles for y border
        for i in range(y_len - 1):
            v1 = (0, xyz.ally[i], 0)
            v2 = xyz.get_point(0, xyz.ally[i])
            v3 = (0, xyz.ally[i+1] ,0)
            self.add_triangle(v1, v2, v3, "x<0")
            v1 = xyz.get_point(0, xyz.ally[i])
            v2 = xyz.get_point(0, xyz.ally[i+1])
            v3 = (0, xyz.ally[i+1], 0)
            self.add_triangle(v1, v2, v3, "x<0")   

            v1 = (xyz.allx[x_len - 1], xyz.ally[i], 0)
            v2 = xyz.get_point(xyz.allx[x_len - 1], xyz.ally[i])
            v3 = (xyz.allx[x_len - 1], xyz.ally[i+1] ,0)
            self.add_triangle(v1, v2, v3, "x>0")
            v1 = xyz.get_point(xyz.allx[x_len - 1], xyz.ally[i])
            v2 = xyz.get_point(xyz.allx[x_len - 1], xyz.ally[i+1])
            v3 = (xyz.allx[x_len - 1], xyz.ally[i+1], 0)
            self.add_triangle(v1, v2, v3, "x>0")    

        for i in range(x_len - 1):
            print(f"Processing row {i} of {x_len - 1}")
            for j in range(y_len - 1):
                v1 = xyz.get_point(xyz.allx[i], xyz.ally[j])
                v2 = xyz.get_point(xyz.allx[i+1], xyz.ally[j])
                v3 = xyz.get_point(xyz.allx[i], xyz.ally[j+1])
                self.add_triangle(v1, v2, v3, "z>0")
                v1 = xyz.get_point(xyz.allx[i+1], xyz.ally[j])
                v2 = xyz.get_point(xyz.allx[i+1], xyz.ally[j+1])
                v3 = xyz.get_point(xyz.allx[i], xyz.ally[j+1])
                self.add_triangle(v1, v2, v3, "z>0")

    def import_complete_xyz_model(self, xyz):
        self.import_xyz_model(xyz, len(xyz.allx), len(xyz.ally))

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write('solid STLModel\n')
            for triangle in self.triangles:
                file.write(f'  facet normal {" ".join(map(str, triangle["n"]))}\n')
                file.write('    outer loop\n')
                file.write(f'      vertex {" ".join(map(str, triangle["v1"]))}\n')
                file.write(f'      vertex {" ".join(map(str, triangle["v2"]))}\n')
                file.write(f'      vertex {" ".join(map(str, triangle["v3"]))}\n')
                file.write('    endloop\n')
                file.write('  endfacet\n')
            file.write('endsolid STLModel\n')   

    # save to binary file
    def save_to_binary_file(self, file_path):
        with open(file_path, 'wb') as file:
            file.write(b'\0' * 80)
            file.write(int(len(self.triangles)).to_bytes(4, 'little'))
            for triangle in self.triangles:
                file.write(triangle['n'].astype('float32').tobytes())
                for v in [triangle['v1'], triangle['v2'], triangle['v3']]:
                    file.write(np.array(v).astype('float32').tobytes())
                file.write(b'\0' * 2)
        