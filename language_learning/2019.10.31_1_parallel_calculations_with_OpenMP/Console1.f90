! This code is supported by the website: https://www.guanjihuan.com
! The newest version of this code is on the web page: https://www.guanjihuan.com/archives/764


program hello_open_mp
    use omp_lib   !这里也可以写成 include 'omp_lib.h' ，两者调用方式均可
    integer mcpu,tid,total,N,i,j,loop
    double precision starttime, endtime, time,result_0
    double precision, allocatable:: T(:)
    N=5   ! 用于do并行
    loop=1000000000  !如果要测试并行和串行运算时间，可以加大loop值
    allocate(T(N))
   
    
    !call OMP_SET_NUM_THREADS(2)  !人为设置线程个数，可以取消注释看效果
    total=OMP_GET_NUM_PROCS()  ! 获取计算机系统的处理器数量
    print '(a,i2)',  '计算机处理器数量：' , total    !也可以用write(*,'(a,i2)')来输出
    print '(a)', '-----在并行之前-----'
    tid=OMP_GET_THREAD_NUM()    !获取当前线程的线程号
    mcpu=OMP_GET_NUM_THREADS()  !获取总的线程数
    print '(a,i2,a,i2)', '当前线程号：',tid,'；总的线程数：', mcpu
    print *   !代表换行

    
    print'(a)','-----第一部分程序开始并行-----'
    !$OMP PARALLEL DEFAULT(PRIVATE)   ! 这里用的是DEFAULT(PRIVATE)
    tid=OMP_GET_THREAD_NUM()    !获取当前线程的线程号
    mcpu=OMP_GET_NUM_THREADS()  !获取总的线程数
    print '(a,i2,a,i2)', '当前线程号：',tid,'；总的线程数：', mcpu
    !$OMP END PARALLEL
    
    
    print *  !代表换行
    print'(a)','-----第二部分程序开始并行-----'
    starttime=OMP_GET_WTIME()   !获取开始时间
   !$OMP PARALLEL DO DEFAULT(PRIVATE) SHARED(T,N,loop)   ! 默认私有变量，把需要的参数以及各节点计算结果的存放器作为共享变量。
    do i=1,N     !这里放上do循环体。是多个样品。
        result_0=0
        tid=OMP_GET_THREAD_NUM()    !获取当前线程的线程号
        mcpu=OMP_GET_NUM_THREADS()  !获取总的线程数
        do j=1,loop                 !这代表我们要做的计算~
            result_0 = result_0+1   !这代表我们要做的计算~
        enddo                       !这代表我们要做的计算~
        T(i) = result_0-loop+i      !将各个线程的计算结果保存到公共变量中去。
        !这里i代表各个循环的参数，之后如果有需要可以根据参数再整理数据。
        print '(a,i2, a, f10.4,a,i2,a,i2 )', 'T(',i,')=', T(i) , '    来源于线程号',tid,'；总的线程数：', mcpu
    enddo
    !$OMP END PARALLEL DO   !并行结束
    endtime=OMP_GET_WTIME()  !获取结束时间
    time=endtime-starttime   !总运行时间
    print '(a, f13.5)' , '第二部分程序按并行计算所用的时间：', time
    
   
    print *  !代表换行
    print'(a)','-----第二部分程序按串行的计算-----'
    starttime=OMP_GET_WTIME()    !获取开始时间
    do i=1,N  
        result_0=0
        tid=OMP_GET_THREAD_NUM()    !获取当前线程的线程号
        mcpu=OMP_GET_NUM_THREADS()  !获取总的线程数
        do j=1,loop
            result_0 = result_0+1  
        enddo 
        T(i) = result_0-loop+i
        print '(a,i2, a, f10.4,a,i2,a,i2 )', 'T(' ,i,')=', T(i) , '    来源于线程号',tid,'；总的线程数：', mcpu
    enddo
    endtime=OMP_GET_WTIME()  !获取结束时间
    time=endtime-starttime   !总运行时间
    print '(a, f13.5)' , '第二部分程序按串行计算所用的时间：', time
    print *     !代表换行
    
    
    tid=OMP_GET_THREAD_NUM()   !获取当前线程的线程号
    mcpu=OMP_GET_NUM_THREADS() !获取总的线程数
    print '(a,i5,a,i5)', '当前线程号：',tid,'；总的线程数：', mcpu
    print *      !代表换行
end program hello_open_mp   ! 这里可以写成end, 也可以写成end program，都可以。
    