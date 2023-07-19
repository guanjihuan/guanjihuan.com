subroutine subroutine_4()
    write(*,*) 'test_4'
end subroutine subroutine_4


function function_4(x) result(y)
    double precision x, y
    y = 16.d0*x
end function function_4