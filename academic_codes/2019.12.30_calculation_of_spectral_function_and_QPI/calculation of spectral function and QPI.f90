! This code is supported by the website: https://www.guanjihuan.com
! The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3785

module global
  implicit none
  double precision sqrt3,Pi
  parameter(sqrt3=1.7320508075688773d0,Pi=3.14159265358979324d0)
end module global 



program QPI  !QPI主程序
    use blas95
    use lapack95,only:GETRF,GETRI
    use global
    implicit none
    integer i,j,info,index_0(4)
    double precision omega,kx,ky,Eigenvalues(4),eta,V0,kx1,kx2,ky1,ky2,qx,qy,time_begin,time_end
    parameter(eta=0.005)
    complex*16 H0(4,4),green_0(4,4),green_1(4,4),green_0_k1(4,4),green_0_k2(4,4),A_spectral,V(4,4),gamma_0(4,4),Temp_0(4,4),T(4,4),g_1,rho_1
    character(len=*):: Flname
    parameter(Flname='')  !可以写上输出文件路径，也可以不写，输出存在当前文件的路径

    omega=0.070d0
    open(unit=10,file=Flname//'Spectral function_w=0.07.txt')
    open(unit=20,file=Flname//'QPI_intra_nonmag_w=0.07.txt')
    call CPU_TIME(time_begin)
     
    !计算谱函数A(kx,ky)
    write(10,"(f20.10,x)",advance='no') 0
    do ky=-Pi,Pi,0.01d0     !谱函数图案的精度
        write(10,"(f20.10,x)",advance='no') ky
    enddo
    write(10,"(a)",advance='yes') ' '
    do kx=-Pi,Pi,0.01d0      !谱函数图案的精度
        write(10,"(f20.10,x)",advance='no') kx
        do ky=-Pi,Pi,0.01d0         !谱函数图案的精度
            call Greenfunction_clean(kx,ky,eta,omega,green_0)
            A_spectral=-(green_0(1,1)+green_0(3,3))/Pi
            write(10,"(f20.10)",advance='no') imag(A_spectral)
        enddo
        write(10,"(a)",advance='yes') ' '
    enddo     

    !计算QPI(qx,qy)
    V0=0.4d0
    V=0.d0
    V(1,1)=V0
    V(2,2)=-V0
    V(3,3)=V0
    V(4,4)=-V0
    gamma_0=0.d0
    do kx=-Pi,Pi,0.01
        do ky=-Pi,Pi,0.01
            call Greenfunction_clean(kx,ky,eta,omega,green_0)
            do i=1,4
                do j=1,4
                    gamma_0(i,j)=gamma_0(i,j)+green_0(i,j)*0.01*0.01
                enddo
            enddo
        enddo
    enddo
    gamma_0=gamma_0/(2*Pi)/(2*Pi)
    call gemm(V,gamma_0,Temp_0)
    do i=1,4
        Temp_0(i,i)=1-Temp_0(i,i)
    enddo
    call GETRF( Temp_0,index_0,info ); call GETRI( Temp_0,index_0,info) !求逆
    call gemm(Temp_0,V,T)  !矩阵乘积
    write(20,"(f20.10,x)",advance='no') 0
    do qy=-Pi,Pi,0.01     !QPI图案的精度
        write(20,"(f20.10,x)",advance='no') qy
    enddo
    write(20,"(a)",advance='yes') ' '
    do qx=-Pi,Pi,0.01     !QPI图案的精度
        write(*,"(a)",advance='no')  'qx='  
        write(*,*) qx    !屏幕输出可以实时查看计算进度
        write(20,"(f20.10)",advance='no') qx
        do qy=-Pi,Pi,0.01     !QPI图案的精度
            rho_1=0.d0
            do kx1=-Pi,Pi,0.06   !积分的精度
                kx2=kx1+qx
                do ky1=-Pi,Pi,0.06  !积分的精度
                    ky2=ky1+qy
                    call Greenfunction_clean(kx1,ky1,eta,omega,green_0_k1)
                    call Greenfunction_clean(kx2,ky2,eta,omega,green_0_k2)
                    call gemm(green_0_k1,T,Temp_0)
                    call gemm(Temp_0, green_0_k2, green_1)
                    g_1=green_1(1,1)-dconjg(green_1(1,1))+green_1(3,3)-dconjg(green_1(3,3))
                    rho_1=rho_1+g_1*0.06*0.06
                enddo
            enddo
            rho_1=rho_1/(2*Pi)/(2*Pi)/(2*Pi)*(0.d0,1.d0)
            write(20,"(f20.10,x,f20.10)",advance='no') real(rho_1)
        enddo
        write(20,"(a)",advance='yes') ' '
    enddo

    call CPU_TIME(time_end)
    write(*,"(a)",advance='no') 'The running time of this task='
    write (*,*) time_end-time_begin   !屏幕输出总的计算时间，单位为秒（按照当前步长的精度，在个人计算机上运算大概需要4个小时）
end program

    

subroutine Greenfunction_clean(kx,ky,eta,omega,green_0)  !干净体系的格林函数
use blas95
use lapack95,only:GETRF,GETRI
use global
integer info,index_0(4)
double precision, intent(in):: kx,ky,eta,omega
complex*16 H0(4,4)
complex*16,intent(out):: green_0(4,4)
call Hamiltonian(kx,ky,H0)
green_0=H0
do i=1,4
    green_0(i,i)=omega+(0.d0,1.d0)*eta-green_0(i,i)
enddo
call GETRF( green_0,index_0,info ); call GETRI( green_0,index_0,info );
end subroutine Greenfunction_clean
    


subroutine Hamiltonian(kx,ky,Matrix)  !哈密顿量
use global
implicit none
integer i,j
double precision t1,t2,t3,t4,mu,epsilon_x,epsilon_y,epsilon_xy,delta_1,delta_2,delta_0
double precision, intent(in):: kx,ky
complex*16,intent(out):: Matrix(4,4)

t1=-1;t2=1.3;t3=-0.85;t4=-0.85;delta_0=0.1;mu=1.54
Matrix=(0.d0,0.d0)

epsilon_x=-2*t1*dcos(kx)-2*t2*dcos(ky)-4*t3*dcos(kx)*dcos(ky)
epsilon_y=-2*t1*dcos(ky)-2*t2*dcos(kx)-4*t3*dcos(kx)*dcos(ky)
epsilon_xy=-4*t4*dsin(kx)*dsin(ky)
delta_1=delta_0*dcos(kx)*dcos(ky)
delta_2=delta_1

Matrix(1,1)=epsilon_x-mu
Matrix(2,2)=-epsilon_x+mu
Matrix(3,3)=epsilon_y-mu
Matrix(4,4)=-epsilon_y+mu

Matrix(1,2)=delta_1
Matrix(2,1)=delta_1
Matrix(1,3)=epsilon_xy
Matrix(3,1)=epsilon_xy
Matrix(1,4)=0.d0
Matrix(4,1)=0.d0

Matrix(2,3)=0.d0
Matrix(3,2)=0.d0
Matrix(2,4)=-epsilon_xy
Matrix(4,2)=-epsilon_xy

Matrix(3,4)=delta_2
Matrix(4,3)=delta_2
end subroutine Hamiltonian