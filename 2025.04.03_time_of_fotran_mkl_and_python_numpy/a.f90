! This code is supported by the website: https://www.guanjihuan.com
! The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45966

module random_matrix_mod
    implicit none
    contains
        subroutine generate_random_matrix(n, A)
            integer, intent(in) :: n
            double precision, allocatable, intent(out) :: A(:,:)
            integer :: ierr
            
            allocate(A(n, n), stat=ierr)
            if (ierr /= 0) stop "内存分配失败"
            
            call init_random_seed()
            call random_number(A)
        end subroutine

        subroutine init_random_seed()
            integer :: i, n, clock, ierr
            integer, allocatable :: seed(:)
            
            call random_seed(size = n)
            allocate(seed(n), stat=ierr)
            if (ierr /= 0) stop "种子分配失败"
            
            call system_clock(count=clock)
            seed = clock + 37 * [(i - 1, i = 1, n)]
            call random_seed(put=seed)
            
            deallocate(seed)
        end subroutine
end module

program main
    use random_matrix_mod
    use f95_precision
    use blas95
    use lapack95
    implicit none

    integer, allocatable :: index1(:)
    integer n, i, j, info, ierr, stage, start, end_val, step, count_start, count_end, count_rate
    double precision, allocatable :: A(:,:)
    double precision time_used

    ! 定义不同阶段的参数
    do stage = 1, 3
        select case(stage)
        case(1)  ! 第一阶段：100-1000，步长100
            start = 100
            end_val = 1000
            step = 100
        case(2)  ! 第二阶段：2000-10000，步长1000
            start = 2000
            end_val = 10000
            step = 1000
        case(3)  ! 第三阶段：20000-50000，步长10000
            start = 20000
            end_val = 50000
            step = 10000
        end select

        n = start
        do while (n <= end_val)

            allocate(index1(n), stat=ierr)
            call generate_random_matrix(n, A)

            call system_clock(count_start, count_rate)
            call getrf(A, index1, info);  call getri(A, index1, info)  ! 使用 getrf 和 getri 对矩阵求逆。这时候 A 不再是原来的矩阵了，而是求逆后的矩阵。
            call system_clock(count_end)

            ! 打印计算时间
            if (count_rate > 0) then
                time_used = real(count_end - count_start) / real(count_rate)
                write(*, '(a, I6, a, f12.6, a)') 'n = ', n, ' 的计算时间: ', time_used, ' 秒'
            else
                write(*,*) "无法获取计算时间"
            endif

            deallocate(A, stat=ierr)
            deallocate(index1, stat=ierr)

            n = n + step
        end do
    end do

end program