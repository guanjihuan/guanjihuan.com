#include <iostream>
#include <chrono>

int main() {
    double x = 0.0; 
    auto start = std::chrono::high_resolution_clock::now();  // 记录开始时间
    for (long long i = 0; i < 1e10; ++i) {
        x += 1e-10;   // 模拟一些计算
    }
    auto end = std::chrono::high_resolution_clock::now(); // 记录结束时间
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start); // 计算时间差
    std::cout << "Running time: " << duration.count() << " s" << std::endl;
    std::cout << "Result x = " << x << std::endl;
    return 0;
}