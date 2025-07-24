! 矩阵求逆子程序
subroutine inverse_matrix(A, Ainv)
    implicit none
    real(8), intent(in) :: A(:,:)       ! 输入矩阵
    real(8), intent(inout) :: Ainv(:,:)    ! 输出逆矩阵
    real(8), allocatable :: work(:)
    integer, allocatable :: ipiv(:)
    integer :: n, info

    n = size(A,1)
    allocate(ipiv(n), work(n))
    
    Ainv = A  ! 复制输入矩阵
    
    call dgetrf(n, n, Ainv, n, ipiv, info)  ! LU 分解
    call dgetri(n, Ainv, n, ipiv, work, n, info) ! 计算逆矩阵
        
    deallocate(ipiv, work)
end subroutine inverse_matrix