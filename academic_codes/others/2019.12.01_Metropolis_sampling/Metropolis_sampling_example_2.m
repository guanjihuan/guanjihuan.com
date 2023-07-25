% This code is supported by the website: https://www.guanjihuan.com
% The newest version of this code is on the web page: https://www.guanjihuan.com/archives/1247

clc;clear all;clf;
s=100000;  % 取的样品数
f=[1,2,3,3,3,3,6,5,4,3,2,1];  % 期望得到样品的分布函数
d=zeros(1,s);  % 初始状态
x=1;
for i=1:s
     y=unidrnd(12);  % 1到12随机整数
     alpha=min(1,f(y)/f(x)); % 接收率
     u=rand;  
     if u<alpha   % 以alpha的概率接收转移
         x=y;
     end
     d(i)=x;
end
hist(d,1:1:12);