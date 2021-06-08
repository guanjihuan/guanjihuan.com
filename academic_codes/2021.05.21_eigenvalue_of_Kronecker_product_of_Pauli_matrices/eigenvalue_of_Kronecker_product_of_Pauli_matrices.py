import numpy as np
import gjh

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
    a_00*gjh.sigma_00()+a_0x*gjh.sigma_0x()+a_0y*gjh.sigma_0y()+a_0z*gjh.sigma_0z()+ \
    a_x0*gjh.sigma_x0()+a_xx*gjh.sigma_xx()+a_xy*gjh.sigma_xy()+a_xz*gjh.sigma_xz()+ \
    a_y0*gjh.sigma_y0()+a_yx*gjh.sigma_yx()+a_yy*gjh.sigma_yy()+a_yz*gjh.sigma_yz()+ \
    a_z0*gjh.sigma_z0()+a_zx*gjh.sigma_zx()+a_zy*gjh.sigma_zy()+a_zz*gjh.sigma_zz()
eigenvalue_1 = gjh.calculate_eigenvalue(hamiltonian_1)

hamiltonian_2 = \
    a_00*gjh.sigma_00()+a_0x*gjh.sigma_x0()+a_0y*gjh.sigma_y0()+a_0z*gjh.sigma_z0()+ \
    a_x0*gjh.sigma_0x()+a_xx*gjh.sigma_xx()+a_xy*gjh.sigma_yx()+a_xz*gjh.sigma_zx()+ \
    a_y0*gjh.sigma_0y()+a_yx*gjh.sigma_xy()+a_yy*gjh.sigma_yy()+a_yz*gjh.sigma_zy()+ \
    a_z0*gjh.sigma_0z()+a_zx*gjh.sigma_xz()+a_zy*gjh.sigma_yz()+a_zz*gjh.sigma_zz()
eigenvalue_2 = gjh.calculate_eigenvalue(hamiltonian_2)


print()
print('Eigenvalue:')
print(eigenvalue_1)
print(eigenvalue_2)
print()
print('Difference of matrices:')
print(hamiltonian_1-hamiltonian_2)
print()
# print(hamiltonian_1)
# print(hamiltonian_2)