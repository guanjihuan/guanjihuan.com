from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "guan_cpp.guan_cpp_module",             # 包名.模块名
        ["src/cpp/main.cpp"],                   # C++ 源文件列表
        include_dirs=[pybind11.get_include()],  # pybind11头文件
        language="c++",                         # 指定语言为 C++
        extra_link_args=["-static-libstdc++"],  # 可选静态链接
    ),
]

setup(
    name="guan_cpp",                        # 项目的名称（用于 pip install）
    version="0.0.1",                        # 版本号
    package_dir={"": "src"},                # ​​指定 Python 包的根目录​​
    packages=["guan_cpp"],                  # 包的名称（用于 import）
    ext_modules=ext_modules,                # 指定 C++ 扩展模块
)