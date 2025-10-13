#define EIGEN_USE_BLAS  // 注释或取消注释来测试 
// #define EIGEN_USE_MKL_ALL  // 如果使用 MKL，优先用 EIGEN_USE_MKL_ALL
#include <iostream>
#include <chrono>
#include <vector>
#include <iomanip> 
#include <Eigen/Dense>

int main() {
    std::vector<int> sizes = {100, 200, 300, 500, 1000, 2000, 3000, 5000};  // 要测试的不同矩阵大小 
    const int trials = 3;  // 每个尺寸的测试次数

    for (int size : sizes) {
        std::cout << "Testing size: " << size << "x" << size << std::endl;
        
        Eigen::MatrixXd A = Eigen::MatrixXd::Random(size, size);
        A = A.transpose() * A + Eigen::MatrixXd::Identity(size, size);  // 确保矩阵可逆

        auto start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < trials; ++i) {
            Eigen::MatrixXd A_inv = A.inverse();
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Average time per inversion: " 
                  << std::fixed << std::setprecision(3) 
                  << (static_cast<double>(duration.count()) / 1000 / trials) 
                  << " s" << std::endl;
        std::cout << "----------------------------------" << std::endl;
    }

    return 0;
}