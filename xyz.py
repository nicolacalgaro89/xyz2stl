import numpy as np


class XYZ:
    def __init__(self):
        self.points = []
        self.allx = []
        self.ally = []
        self.allz = []
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.max_z = 0
        self.min_z = 0

    def add_point(self, x, y, z):
        self.points.append((x, y, z))

    def remove_point(self, x, y, z):
        if (x, y, z) in self.points:
            self.points.remove((x, y, z))

    def get_points(self):
        return self.points

    def clear_points(self):
        self.points = []

    # metod to get point by x and y
    def get_point(self, x, y):
        if x in self.allx and y in self.ally:
            x_idx = self.allx.index(x)
            y_idx = self.ally.index(y)
            return (x,y,float(self.allz[x_idx,y_idx]))
        return None
    
    # method to import points from xyx file

    def import_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y, z = line.split()
                self.add_point(float(x), float(y), float(z))
        self.build()

    # method to shift all points by a vector
    def shift(self, vector):
        for i in range(len(self.points)):
            self.points[i] = tuple(map(sum, zip(self.points[i], vector)))
        #empty allx and ally vectors
        self.build()

    # method to import points froma a dataframe with columns X, Y, Z
    def import_from_dataframe(self, df):
        for index, row in df.iterrows():
            self.add_point(row['X'], row['Y'], row['Z'])
        self.build()


    def build(self):
        self.allx = []
        self.allx = sorted(set(x for x, y, z in self.points))

        self.ally = []
        self.ally = sorted(set(y for x, y, z in self.points))
        # Create a 2D grid to hold Z values
        self.allz = []
        self.allz = np.full((len(self.allx), len(self.ally)), 0.0)  # Initialize with 0

        # Map the Z values to their respective X and Y indices
        for x, y, z in self.points:
            x_idx = self.allx.index(x)
            y_idx = self.ally.index(y)
            self.allz[x_idx, y_idx] = float(z)
        print('XYZ model built')
        self.max_x = max(self.allx)
        self.min_x = min(self.allx)
        self.max_y = max(self.ally)
        self.min_y = min(self.ally)
        self.max_z = np.max(self.allz)
        self.min_z = np.min(self.allz)
        #print minimum and maximum values of self.allx, self.ally and self.allz
        print('min_x:', self.min_x)
        print('max_x:', self.max_x)
        print('min_y:', self.min_y)
        print('max_y:', self.max_y)
        print('min_z:', self.min_z)
        print('max_z:', self.max_z)

    
    # method to get the point with the nearest following x
    def get_next_point_x(self, point):
        (x,y,z) = point
        x_idx = self.allx.index(x)
        y_idx = self.ally.index(y)
        if x_idx < len(self.allx) - 1:
            return (self.allx[x_idx + 1],self.ally[y_idx],float(self.allz[x_idx + 1, y_idx]))
        return None
    
     # method to get the point with the nearest previous x
    def get_previous_point_x(self, point):
        (x,y,z) = point
        x_idx = self.allx.index(x)
        y_idx = self.ally.index(y)
        if x_idx > 0:
            return (self.allx[x_idx - 1],self.ally[y_idx],float(self.allz[x_idx - 1, y_idx]))
        return None
    
    # method to get the point with the nearest following y
    def get_next_point_y(self,point):
        (x,y,z) = point
        x_idx = self.allx.index(x)
        y_idx = self.ally.index(y)
        if y_idx < len(self.ally) - 1:
            return (self.allx[x_idx],self.ally[y_idx+1],float(self.allz[x_idx, y_idx + 1]))
        return None  

    # method to get the point with the nearest previous y
    def get_next_point_y(self,point):
        (x,y,z) = point
        x_idx = self.allx.index(x)
        y_idx = self.ally.index(y)
        if y_idx > 0:
            return (self.allx[x_idx],self.ally[y_idx-1],float(self.allz[x_idx, y_idx - 1]))
        return None        

    def get_origin(self):
        return self.get_point(self.allx[0], self.ally[0])

    def __str__(self):
        return '\n'.join(f'{x} {y} {z}' for x, y, z in self.points)