! This code is supported by the website: https://www.guanjihuan.com
! The newest version of this code is on the web page: https://www.guanjihuan.com/archives/762


module global ! module是用来封装程序模块的，把相关功能的变量和函数封装在一起。一般来说，可以不设置全局变量，把这些变量写在module里，在需要用的地方用use调用即可。
    implicit none
    double precision sqrt3,Pi 
    parameter(sqrt3=1.7320508075688773d0,Pi=3.14159265358979324d0)  ! parameter代表不能改的常数
   end module global 
      
    
program main  !主函数用program开始,用end program结束。在Fortran里不区分大小写。用感叹号!来做注释
use global
use f95_precision  !这个还不知道什么时候用上，这里注释掉也可正常运行。
use blas95  ! 里面包含了矩阵相乘的gemm()等
use lapack95 !里面包括了矩阵求逆的GETRF,GETRI和求本征矢和本征矢的GEEV等
implicit none  ! implicit是用来设置默认类型，即根据变量名称的第一个字母来决定变量的类型。implicit none是关闭默认类型功能，所有变量要先声明


integer i,j,info,index1(2) ! 定义整型
double precision a(2,2),b(2,2),c(2,2),&  ! 比较长的语句可以用&换行。在续行的开始位置可加&号，也可不加。
    x1, x2, result_1, result_2, fun1   !定义双精度浮点数
complex*16  dd(2,2), eigenvalues(2)  !定义复数
complex*16, allocatable::  eigenvectors(:,:)  ! 定义动态分配的变量  ! 这里的两个冒号::是必须要的。其他的可加可不加。
character(len=15) hello, number  ! 定义字符串,len是规定长度，如果不写，只会给一个字符的空间
allocate(eigenvectors(2,2))  ! 分配空间


write(*,*) '----输出----'
hello='hello world'
write(*,*) hello  ! 第一个代表输出的设备，*代表屏幕。第二个是输出的格式，*代表默认。
write(number,'(f7.3)') pi  ! 用write可以把数字类型转成字符类型。'(f7.3)'是输出浮点数的格式，如果用*来代替，字符串的长度需要够长才行。整型格式用类似'(i3)'这样
write(*,*) '数字转成字符串后再输出:', number
write(*,"(a,18x)",advance="no") hello   ! advance='no'代表不换行，在有advance的时候，必须格式化输出，否则报错。'(a)'按照字符型变量的实际长度读取，这里也可以写a15或者其他。'(10x)'代表空格
write(*,*) number,'这是不换行输出测试'
write(*,"('一些固定文字也可以写在这里面', a, a,//)")  hello, number  !字符串也可以直接写在"()"里面。里面有引号，外面要用上双引号才行，不然会报错。
!'(a)'按照字符型变量的实际长度读取，也可以写a15或者其他。这里'(/)'代表再换一次行。一个斜杠换一个。


write(*,*) '----写入文件----'
open(unit=10,file='learn-fortran-test.txt')   ! 打开文件用open
write(10,*) hello, number
close(10)  ! 关闭文件用close
write(*,*) ''

write(*,*) '----矩阵乘积----'
a(1,1)=2;a(1,2)=5;a(2,1)=3;a(2,2)=2  ! 两个语句写在同一行是可以的，要用分号隔开
b(1,1)=3;b(2,2)=3
write(*,*) '矩阵直接默认输出，是按列的顺序一个个输出'
write(*,*) 'a='
write(*,*) a
write(*,*) '矩阵格式化输出'
write(*,*) 'a='
do i=1,2
    do j=1,2
        write(*,'(f10.4)',advance='no') a(i,j)  !内循环为列的指标
    enddo
    write(*,*) ''
enddo
write(*,*) 'b='
do i=1,2
    do j=1,2
        write(*,'(f10.4)',advance='no') b(i,j)  !内循环为列的指标
    enddo
    write(*,*) ''
enddo
call gemm(a,b,c)  ! 矩阵乘积用call gemm()
write(*,*) '矩阵乘积：c=a*b='
do i=1,2
    do j=1,2
        write(*,'(f10.4)',advance='no') c(i,j)  !内循环为列的指标
    enddo
    write(*,*) ''
enddo
write(*,*)  ''


write(*,*) '----矩阵求逆----'
call getrf(a,index1,info);  call getri(a,index1,info)  !getrf和getri要配合起来使用求逆。
! info是需定义为整型。If info = 0, the execution is successful.
! 上面index1是在getrf产生，在getri里输入。index1也是需要定义为整型，而且是一维数组，数组长度一般为矩阵的维度。
! 这时候a不再是原来的矩阵了，而是求逆后的矩阵。
do i=1,2
    do j=1,2
        write(*,'(f10.4)',advance='no') a(i,j)  !内循环为列的指标
    enddo
    write(*,*) ''
enddo


write(*,*) '----复数矩阵----'
dd(1,1)=(1.d0, 0.d0)
dd(1,2)=(7.d0, 0.d0)
dd(2,1)=(3.d0, 0.d0)
dd(2,2)=(2.d0, 0.d0)
do i=1,2
    do j=1,2
        write(*,"(f10.4, '+1i*',f7.4)",advance='no') dd(i,j)  !内循环为列的指标
    enddo
    write(*,*) ''
enddo
write(*,*)  ''


write(*,*) '----矩阵本征矢和本征值----'
call geev(A=dd, W=eigenvalues, VR=eigenvectors, INFO=info)  
! 这里A矩阵最好用上复数，W是本征值一维数组，VR是本征矢二维数组，都是复数。INFO是整数。
! 注意求完本征值后，dd的值会发生改变，不再是原来的了!
write(*,*) 'eigenvectors:'
do i=1,2
    do j=1,2
        write(*,"(f10.4, '+1i*',f7.4)",advance='no') eigenvectors(i,j)  !内循环为列的指标。输出结果列向量为特征向量。
    enddo
    write(*,*) ''
enddo
write(*,*) 'eigenvalues:'
do i=1,2
    write(*,"(f10.4, '+1i*',f7.4)",advance='no') eigenvalues(i)  
enddo
write(*,*)  ''
deallocate(eigenvectors)  ! 释放动态变量的空间


write(*,*) ''  ! 输出空一行
write(*,*) '----循环加判断----'
do i=1,5  ! 循环用do到enddo
    if (mod(i,2)==0) then  ! 判断用if()then 
        write(*,*) '我是偶数', i   
    else if (i==3) then
        write(*,*) '我是第3个数字，也是奇数'
    else
        write(*,*) '我是奇数', i
    endif
enddo
write(*,*) ''


call sub1(2.d0, 3.d0, result_1, result_2)   ! 这里要写成2.d0或者2.0d0表示双精度，因为子程序规定该参数为双精度。写成2或者2.0都会报错。
write(*,*) '调用子程序，求和：',result_1
write(*,*) '调用子程序，乘积：',result_2
write(*,*) '使用函数，返回减法结果：', fun1(2.d0, 3.d0)
write(*,*) ''


end program


    
subroutine sub1(x1,x2,y1,y2)  !子程序。输入输出都在括号里面，用call调用。
double precision,intent(in):: x1, x2   ! 这里的两个冒号::是必须要的。
double precision,intent(out):: y1, y2
! intent(in) 表示这个参数是输入的；intent(out) 表示参数是输出的；intent(inout)表示这个参数同时用于两个方向的数据传递；
! intent()不是必须的，但最好加上，因为可读性比较强，知道哪些是输入，哪些是输出。而且intent(in)是不能赋值更改的，会提示错误，这样可以防止一些错误。
y1=x1+x2
y2=x1*x2
end subroutine


    
function fun1(x1,x2) ! 函数。函数只能返回一个数值，不能多个。而子程序可以返回多个，所以一般用子程序subroutine
double precision x1,x2,fun1  ! 要对函数名(或返回变量）定义
fun1=x1-x2    ! 返回变量要和函数名一样
return        ! 这里的return也可以不写。写的作用是直接返回值，而不运行后面的代码。一般会跟if配合用。
end function  ! 也可以直接写end，不会报错。但最好把后面的也带上，看起来比较清晰点。