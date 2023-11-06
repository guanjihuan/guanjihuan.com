module module_2

      implicit none
      contains  ! 模块中包含以下子程序和函数
    
      subroutine subroutine_2()  ! 模块中的子程序
         write(*,*) 'test_2'
      end subroutine subroutine_2

      function function_2(x) result(y) ! 模块中的函数
          double precision x, y
            y = 4.d0*x
      end function function_2
      
end module module_2