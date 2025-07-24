subroutine sum_matrix(matrix, total)
    implicit none
    ! 输入参数
    real, intent(in)  :: matrix(:,:)  ! 假定形状数组
    real, intent(out) :: total  ! 输出总和
    
    ! 局部变量
    integer :: i, j
    
    ! 双重循环计算总和
    total = 0.0
    do j = 1, size(matrix, 2)  ! 获取列数
        do i = 1, size(matrix, 1)  ! 获取行数
            total = total + matrix(i, j)
        end do
    end do
end subroutine sum_matrix