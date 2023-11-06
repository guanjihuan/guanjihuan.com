% This code is supported by the website: https://www.guanjihuan.com
% The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4179

% 陈数高效法
clear;clc;
n=1000 % 积分密度
delta=2*pi/n;
C=0; 
for kx=-pi:(2*pi/n):pi
    for ky=-pi:(2*pi/n):pi
        VV=get_vector(HH(kx,ky));
        Vkx=get_vector(HH(kx+delta,ky)); % 略偏离kx的波函数
        Vky=get_vector(HH(kx,ky+delta)); % 略偏离ky的波函数
        Vkxky=get_vector(HH(kx+delta,ky+delta)); % 略偏离kx，ky的波函数
        
        Ux = VV'*Vkx/abs(VV'*Vkx);
        Uy = VV'*Vky/abs(VV'*Vky);
        Ux_y = Vky'*Vkxky/abs(Vky'*Vkxky);
        Uy_x = Vkx'*Vkxky/abs(Vkx'*Vkxky);
        
        % berry curvature
        F=log(Ux*Uy_x*(1/Ux_y)*(1/Uy));
        % chern number
        C=C+F;  
    end
end
C=C/(2*pi*1i)

function vector_new = get_vector(H)
[vector,eigenvalue] = eig(H);
[eigenvalue, index]=sort(diag(eigenvalue), 'descend');
vector_new = vector(:, index(2));
end

function H=HH(kx,ky)
H(1,2)=2*cos(kx)-1i*2*cos(ky);
H(2,1)=2*cos(kx)+1i*2*cos(ky);
H(1,1)=-1+2*0.5*sin(kx)+2*0.5*sin(ky)+2*cos(kx+ky);
H(2,2)=-(-1+2*0.5*sin(kx)+2*0.5*sin(ky)+2*cos(kx+ky));
end