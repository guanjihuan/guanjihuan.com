% This code is supported by the website: https://www.guanjihuan.com
% The newest version of this code is on the web page: https://www.guanjihuan.com/archives/766


%在matlab里加上百分号“%”是注释。
%快捷键：选中按ctrl+R为注释，选中按ctrl+T为取消注释，
clc;  %clc有窗口清空的效果，一般都用上
clear all;  %clear all可以清空所有变量，一般都用上
clf;  %clf为清空输出的图片内容，在画图的时候最好添加上

aa=1   %没加分号“;”,默认打印输出
bb=2;  %加了分号“;”，即不打印输出
cc1=zeros(2,3)  %零矩阵用zeros()
cc2=eye(3,3)  %单位矩阵

%矩阵乘积
matrix1=[3,3;3,3]  %里面分号代表矩阵换一行。下标是从1开始记。
matrix2=[2,0;0,2]
matrix_product_1=matrix1*matrix2  % *是正常的矩阵乘积
matrix_product_2=matrix1.*matrix2  % .*是矩阵每个元素对应相乘

%循环
for i0=1:0.5:2  %循环内容为for到end。a:b:c代表最小为a，最大为c，步长为b
    for_result=i0+1i  %i在matlab中代表虚数，所以起变量名最好不要用i。要输出内容，后面不加分号即可
end

%判断
if aa~=1   %在matlab中，~=代表不等于，==代表等于
    dd=100
else
    dd=300
end

matrix=[2,3;5,7]
%求本征矢和本征值
[V,D]=eig(matrix)  %在matlab中，V的列向量是本征矢，注意是列。D的对角上是对应本征值。
%求逆
inv1=inv(matrix)  %求逆
inv2=matrix^-1    %求逆也可以这样写
%画图
plot([0:20],[10:-1:-10],'-o')  %更多画图技巧可参考官方文档或网上资料