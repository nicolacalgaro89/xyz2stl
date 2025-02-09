import sys
from stl import STL
from xyz import XYZ

#read model name from parameter -m
model_name = sys.argv[2]

xyz = XYZ()
xyz.import_from_file('input/' + model_name + '.xyz')
z_shift = -round(xyz.min_z-0.05*(xyz.max_z-xyz.min_z),-1)
print('z_shift:',z_shift)
xyz.shift((-xyz.get_origin()[0],-xyz.get_origin()[1],z_shift))

stl = STL()
#stl.import_xyz_model(xyz,10,10)
stl.import_complete_xyz_model(xyz)
#stl.save_to_file('output.stl')
stl.save_to_binary_file('output/' + model_name + '.stl')