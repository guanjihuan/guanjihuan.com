% This code is supported by the website: https://www.guanjihuan.com
% The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5778

clear;clc;
delta=0.1;
Z2=0; 
for kx=-pi:0.1:0
    for ky=-pi:0.1:pi
        [V1,V2]=get_vector(Hamiltonian(kx,ky));
        [Vkx1,Vkx2]=get_vector(Hamiltonian(kx+delta,ky)); % 略偏离kx的波函数
        [Vky1,Vky2]=get_vector(Hamiltonian(kx,ky+delta)); % 略偏离ky的波函数
        [Vkxky1,Vkxky2]=get_vector(Hamiltonian(kx+delta,ky+delta)); % 略偏离kx，ky的波函数
        
        Ux = dot_and_det(V1, Vkx1, V2, Vkx2);
        Uy = dot_and_det(V1, Vky1, V2, Vky2);
        Ux_y = dot_and_det(Vky1, Vkxky1, Vky2, Vkxky2);
        Uy_x = dot_and_det(Vkx1, Vkxky1, Vkx2, Vkxky2);
        
        F=imag(log(Ux*Uy_x*(conj(Ux_y))*(conj(Uy))));
        A=imag(log(Ux))+imag(log(Uy_x))+imag(log(conj(Ux_y)))+imag(log(conj(Uy)));
        
        Z2 = Z2+(A-F)/(2*pi);
    end
end
Z2= mod(Z2, 2)


function dd = dot_and_det(a1,b1,a2,b2)   % 内积组成的矩阵对应的行列式
x1=a1'*b1;
x2=a2'*b2;
x3=a1'*b2;
x4=a2'*b1;
dd =x1*x2-x3*x4;
end


function [vector_new_1, vector_new_2] = get_vector(H)
[vector,eigenvalue] = eig(H);
[eigenvalue, index]=sort(diag(eigenvalue), 'ascend');
vector_new_2 = vector(:, index(2));
vector_new_1 = vector(:, index(1));
end


function H=Hamiltonian(kx,ky)  % BHZ模型
A=0.3645/5;
B=-0.686/25;  
C=0;
D=-0.512/25;
M=-0.01;

H=zeros(4,4);
varepsilon = C-2*D*(2-cos(kx)-cos(ky));
d3 = -2*B*(2-(M/2/B)-cos(kx)-cos(ky));
d1_d2 = A*(sin(kx)+1j*sin(ky));
H(1, 1) = varepsilon+d3;
H(2, 2) = varepsilon-d3;
H(1, 2) = conj(d1_d2);
H(2, 1) = d1_d2 ;

varepsilon = C-2*D*(2-cos(-kx)-cos(-ky));
d3 = -2*B*(2-(M/2/B)-cos(-kx)-cos(-ky));
d1_d2 = A*(sin(-kx)+1j*sin(-ky));
H(3, 3) = varepsilon+d3;
H(4, 4) = varepsilon-d3;
H(3, 4) = d1_d2 ;
H(4, 3) = conj(d1_d2);
end