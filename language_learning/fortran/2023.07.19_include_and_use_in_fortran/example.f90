! This code is supported by the website: https://www.guanjihuan.com
! The newest version of this code is on the web page: https://www.guanjihuan.com/archives/34966


module module_1  ! 第一个模块

  implicit none
  contains  ! 模块中包含以下子程序和函数

  subroutine subroutine_1()  ! 模块中的子程序
    write(*,*) 'test_1'
  end subroutine subroutine_1

  function function_1(x) result(y) ! 模块中的函数
  double precision x, y
    y = 2.d0*x
  end function function_1
  
end module module_1


include 'example_include_1.f90'  ! include文件中包含第二个模块


program main

use module_1
use module_2

implicit none
double precision x, function_3, function_4
x = 1.d0

call subroutine_1()
write(*,*) function_1(x)

call subroutine_2()
write(*,*) function_2(x)

call subroutine_3()
write(*,*) function_3(x)

call subroutine_4()
write(*,*) function_4(x)

end program main


subroutine subroutine_3()
write(*,*) 'test_3'
end subroutine subroutine_3


function function_3(x) result(y)
double precision x, y
y = 8.d0*x
end function function_3

include 'example_include_2.f90'  ! include文件中包含第四个子程序和第四个函数