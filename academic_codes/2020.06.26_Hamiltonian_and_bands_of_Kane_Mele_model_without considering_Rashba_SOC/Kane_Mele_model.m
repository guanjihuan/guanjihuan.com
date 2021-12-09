% Purpose: Plot Kane-Mele's bands
% Date: Dec 07, 2021 @HNU
% Author: Ji-Huan Guan; 
% Modify by Zhong-Fu Li;
% More code can be found in https://www.guanjihuan.com/

close all
clc
clear all
tic;

k0 = linspace(0,2*pi,100);
for kk = 1:100
    k = k0(kk);
    H1 = HH(k);
    [VV,DD] = eig(H1);
    Ds(:,kk) = sort(diag(DD),'ascend'); % sort eigenvalue
end
plot(k0/2/pi,Ds,'k.');
ylim([-1 1])
set(gca,'xtick',[0:0.5:1])
set(gca,'XTickLabel',{'\bf 0','\bf \pi','\bf 2\pi'})
set(gcf,'color','w');
set(gca,'fontsize',16,'LineWidth',1.1);
ylabel('Energy(a.u.)','fontname','Arial');
toc

% define Hamiltonian
function H = HH(k)
N = 10;
M = 0;
t1 = 1;
t2 = 0.03;
phi = pi/2;
h00 = zeros(2 * 4 * N, 2 * 4 * N);
h01 = zeros(2 * 4 * N, 2 * 4 * N);
for spin = 1:2
    for ii = 0:N-1
        % nearest neighbor couplings
        h00(ii * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 1 * 2 + spin) = t1;
        h00(ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 0 * 2 + spin) = t1;
        
        h00(ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin) = t1;
        h00(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 1 * 2 + spin) = t1;
        
        h00(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t1;
        h00(ii * 4 * 2 + 3 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin) = t1;
        %next nearest neighbor couplings
        h00(ii * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin) = t2 * exp(-1j * phi) * sign_spin(spin);
        h00(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 0 * 2 + spin) = conj(h00(...
            ii * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin));
        h00(ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t2 * exp(-1j * phi) * sign_spin(spin);
        h00(ii * 4 * 2 + 3 * 2 + spin, ii * 4 * 2 + 1 * 2 + spin) = conj(h00(...
            ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin));
        %
    end
    for ii = 0:N-2
        % nearest neighbor couplings
        h00(ii * 4 * 2 + 3 * 2 + spin, (ii + 1) * 4 * 2 + 0 * 2 + spin) = t1;
        h00((ii + 1) * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t1;
        
        % next nearest neighbor couplings
        h00(ii * 4 * 2 + 2 * 2 + spin, (ii + 1) * 4 * 2 + 0 * 2 + spin) = t2 *exp(1j * phi) * sign_spin(spin);
        h00((ii + 1) * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin) = conj(h00(...
            ii * 4 * 2 + 2 * 2 + spin, (ii + 1) * 4 * 2 + 0 * 2 + spin));
        h00(ii * 4 * 2 + 3 * 2 + spin, (ii + 1) * 4 * 2 + 1 * 2 + spin) = t2 * exp(1j * phi) * sign_spin(spin);
        h00((ii + 1) * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = conj(h00(...
            ii * 4 * 2 + 3 * 2 + spin, (ii + 1) * 4 * 2 + 1 * 2 + spin) );
    end
    % hopping of intercell h01
    for ii = 0:N-1
        % nearest neighbor couplings
        h01(ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 0 * 2 + spin) = t1;
        h01(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t1;
        
        % next nearest neighbor couplings
        h01(ii * 4 * 2 + 0 * 2 + spin, ii * 4 * 2 + 0 * 2 + spin) = t2 * exp(1j * phi) * sign_spin(spin);
        h01(ii * 4 * 2 + 1 * 2 + spin, ii* 4 * 2 + 1 * 2 + spin) = t2 * exp(-1j * phi) * sign_spin(spin);
        h01(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 2 * 2 + spin) = t2 * exp(1j * phi) * sign_spin(spin);
        h01(ii * 4 * 2 + 3 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t2 * exp(-1j * phi) * sign_spin(spin);
        
        h01(ii * 4 * 2 + 1 * 2 + spin, ii * 4 * 2 + 3 * 2 + spin) = t2 * exp(1j * phi) * sign_spin(spin);
        h01(ii * 4 * 2 + 2 * 2 + spin, ii * 4 * 2 + 0 * 2 + spin) = t2 * exp(-1j * phi) * sign_spin(spin);
        if ii ~= 0
            h01(ii * 4 * 2 + 1 * 2 + spin, (ii - 1) * 4 * 2 + 3 * 2 + spin) = t2 * exp(1j * phi) * sign_spin(spin);
        end
    end
   for ii = 0:N-2
    h01(ii * 4 * 2 + 2 * 2 + spin, (ii + 1) * 4 * 2 + 0 * 2 + spin) = t2 *exp(-1j * phi) * sign_spin(spin);
   end
end
H = h00 + h01 * exp(1j * k) + h01' * exp(-1j * k);
end

function sign = sign_spin(spin)
if spin == 0
    sign = 1;
else
    sign = -1;
end
end