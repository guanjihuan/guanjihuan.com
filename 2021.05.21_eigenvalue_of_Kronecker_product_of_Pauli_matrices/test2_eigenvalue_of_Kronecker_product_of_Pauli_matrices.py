"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/12731
"""

import numpy as np
import guan

a_00 = np.random.uniform(-1, 1)
a_0x = np.random.uniform(-1, 1)
a_0y = np.random.uniform(-1, 1)
a_0z = np.random.uniform(-1, 1)

a_x0 = np.random.uniform(-1, 1)
a_xx = np.random.uniform(-1, 1)
a_xy = np.random.uniform(-1, 1)
a_xz = np.random.uniform(-1, 1)

a_y0 = np.random.uniform(-1, 1)
a_yx = np.random.uniform(-1, 1)
a_yy = np.random.uniform(-1, 1)
a_yz = np.random.uniform(-1, 1)

a_z0 = np.random.uniform(-1, 1)
a_zx = np.random.uniform(-1, 1)
a_zy = np.random.uniform(-1, 1)
a_zz = np.random.uniform(-1, 1)

hamiltonian_1 = \
    a_00*guan.sigma_00()+a_0x*guan.sigma_0x()+a_0y*guan.sigma_0y()+a_0z*guan.sigma_0z()+ \
    a_x0*guan.sigma_x0()+a_xx*guan.sigma_xx()+a_xy*guan.sigma_xy()+a_xz*guan.sigma_xz()+ \
    a_y0*guan.sigma_y0()+a_yx*guan.sigma_yx()+a_yy*guan.sigma_yy()+a_yz*guan.sigma_yz()+ \
    a_z0*guan.sigma_z0()+a_zx*guan.sigma_zx()+a_zy*guan.sigma_zy()+a_zz*guan.sigma_zz()
eigenvalue_1 = guan.calculate_eigenvalue(hamiltonian_1)


# only guan.sigma_0x() is changed to guan.sigma_x0()
hamiltonian_3 = \
    a_00*guan.sigma_00()+a_0x*guan.sigma_x0()+a_0y*guan.sigma_0y()+a_0z*guan.sigma_0z()+ \
    a_x0*guan.sigma_x0()+a_xx*guan.sigma_xx()+a_xy*guan.sigma_xy()+a_xz*guan.sigma_xz()+ \
    a_y0*guan.sigma_y0()+a_yx*guan.sigma_yx()+a_yy*guan.sigma_yy()+a_yz*guan.sigma_yz()+ \
    a_z0*guan.sigma_z0()+a_zx*guan.sigma_zx()+a_zy*guan.sigma_zy()+a_zz*guan.sigma_zz()
eigenvalue_3 = guan.calculate_eigenvalue(hamiltonian_3)

print()
print('Eigenvalue:')
print(eigenvalue_1)
print(eigenvalue_3)
print()