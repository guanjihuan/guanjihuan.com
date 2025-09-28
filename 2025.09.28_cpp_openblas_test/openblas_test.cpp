#include <iostream>
#include <vector>
#include <cmath>

extern "C" {
    void dgetrf_(int* m, int* n, double* a, int* lda, int* ipiv, int* info);
    void dgetri_(int* n, double* a, int* lda, int* ipiv, double* work, int* lwork, int* info);
}

int main() {
    const int N = 3;
    
    double A_data[] = {
        1, 0, 5,   // 第1列
        2, 1, 6,   // 第2列
        3, 4, 0    // 第3列
    };
    std::vector<double> A(A_data, A_data + 9);

    std::cout << "Original matrix (column-major):\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            std::cout << A[j*N + i] << " ";
        }
        std::cout << "\n";
    }

    // LU 分解
    std::vector<int> ipiv(N);
    int info;
    int n = N;
    int lda = N;
    
    dgetrf_(&n, &n, &A[0], &lda, &ipiv[0], &info);
    if (info != 0) {
        std::cerr << "LU decomposition failed! (info=" << info << ")\n";
        return 1;
    }

    // 计算逆矩阵
    std::vector<double> work(N);
    int lwork = N; // 关键：必须是可变变量
    dgetri_(&n, &A[0], &lda, &ipiv[0], &work[0], &lwork, &info);
    if (info != 0) {
        std::cerr << "Matrix inversion failed! (info=" << info << ")\n";
        return 1;
    }

    std::cout << "\nInverse matrix:\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            std::cout << A[j*N + i] << " ";
        }
        std::cout << "\n";
    }

    return 0;
}