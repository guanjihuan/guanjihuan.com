#include <pybind11/pybind11.h>

int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(guan_cpp_module, m) {
    m.doc() = "My C++ extension for Python";
    m.def("add", &add, "A function that adds two numbers");
}
