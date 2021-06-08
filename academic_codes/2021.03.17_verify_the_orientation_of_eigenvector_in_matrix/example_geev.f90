program main 
    use lapack95
    implicit none
    integer i,j,info
    complex*16  A(3,3), eigenvalues(3), eigenvectors(3,3)

    A(1,1)=(3.d0, 0.d0)
    A(1,2)=(2.d0, 0.d0)
    A(1,3)=(-1.d0, 0.d0)
    A(2,1)=(-2.d0, 0.d0)
    A(2,2)=(-2.d0, 0.d0)
    A(2,3)=(2.d0, 0.d0)
    A(3,1)=(3.d0, 0.d0)
    A(3,2)=(6.d0, 0.d0)
    A(3,3)=(-1.d0, 0.d0)
    
    write(*,*) 'matrix:'
    do i=1,3
        do j=1,3
            write(*,"(f10.4, '+1i*',f7.4)",advance='no') A(i,j)  ! 内循环为列的指标
        enddo
        write(*,*) ''
    enddo
    
    call geev(A=A, W=eigenvalues, VR=eigenvectors, INFO=info)  
    
    write(*,*) 'eigenvectors:'
    do i=1,3
        do j=1,3
            write(*,"(f10.4, '+1i*',f7.4)",advance='no') eigenvectors(i,j)  ! 内循环为列的指标。输出结果列向量为特征向量。
        enddo
        write(*,*) ''
    enddo
    write(*,*) 'eigenvalues:'
    do i=1,3
        write(*,"(f10.4, '+1i*',f7.4)",advance='no') eigenvalues(i)  
    enddo
    write(*,*)  ''
    write(*,*)  ''
end program