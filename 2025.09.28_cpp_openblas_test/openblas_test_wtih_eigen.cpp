#define EIGEN_USE_BLAS
#include <iostream>
#include <Eigen/Dense>

int main() {
    Eigen::MatrixXd A(4, 4);
    A << 2, 1, 1, 0,
         1, 3, 1, 1,
         1, 1, 4, 1,
         0, 1, 1, 5;

    Eigen::MatrixXd A_inv = A.inverse();

    std::cout << "A:\n" << A << std::endl;
    std::cout << "\nA_inv:\n" << A_inv << std::endl;
    std::cout << "\nA*A_inv:\n" << A * A_inv << std::endl;

    return 0;
}