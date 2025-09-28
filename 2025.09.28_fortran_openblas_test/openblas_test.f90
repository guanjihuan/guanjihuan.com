program invert_simple
    implicit none
    integer, parameter :: n = 2
    double precision :: a(n,n)
    integer :: ipiv(n)
    double precision :: work(n)  ! 最小工作空间（LWORK = N）
    integer :: info

    ! 初始化一个简单的可逆矩阵: [[2, 1], [1, 2]]
    a(1,1) = 2.0d0; a(1,2) = 1.0d0
    a(2,1) = 1.0d0; a(2,2) = 2.0d0

    ! LU 分解
    call DGETRF(n, n, a, n, ipiv, info)
    if (info /= 0) stop 'DGETRF failed'

    ! 求逆（使用最小工作空间 LWORK = N）
    call DGETRI(n, a, n, ipiv, work, n, info)
    if (info /= 0) stop 'DGETRI failed'

    ! 输出结果（应为 [[0.6667, -0.3333], [-0.3333, 0.6667]]）
    print *, 'Inverse:'
    print *, a(1,1), a(1,2)
    print *, a(2,1), a(2,2)
end program