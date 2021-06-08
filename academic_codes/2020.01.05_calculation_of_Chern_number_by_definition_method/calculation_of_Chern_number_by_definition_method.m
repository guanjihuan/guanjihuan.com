% This code is supported by the website: https://www.guanjihuan.com
% The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3932

% 陈数定义法
clear;clc;
n=100; % 积分密度
delta=1e-9; % 求导的偏离量
C=0; 
for kx=-pi:(1/n):pi
    for ky=-pi:(1/n):pi
        VV=get_vector(HH(kx,ky));
        Vkx=get_vector(HH(kx+delta,ky)); % 略偏离kx的波函数
        Vky=get_vector(HH(kx,ky+delta)); % 略偏离ky的波函数
        Vkxky=get_vector(HH(kx+delta,ky+delta)); % 略偏离kx，ky的波函数
        if  sum((abs(Vkx-VV)))>0.01    % 为了波函数的连续性（这里的不连续只遇到符号问题，所以可以直接这么处理）
            Vkx=-Vkx;
        end
        
        if  sum((abs(Vky-VV)))>0.01
            Vky=-Vky;
        end
        
        if  sum(abs(Vkxky-VV))>0.01
            Vkxky=-Vkxky;
        end
        % 价带的波函数的berry connection，求导后内积
        Ax=VV'*(Vkx-VV)/delta; % Berry connection Ax
        Ay=VV'*(Vky-VV)/delta; % Berry connection Ay
        Ax_delta_ky=Vky'*(Vkxky-Vky)/delta; % 略偏离ky的berry connection Ax
        Ay_delta_kx=Vkx'*(Vkxky-Vkx)/delta; % 略偏离kx的berry connection Ay
        % berry curvature
        F=((Ay_delta_kx-Ay)-(Ax_delta_ky-Ax))/delta;
        % chern number
        C=C+F*(1/n)^2;  
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