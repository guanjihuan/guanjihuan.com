"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7516
"""

def find_vector_with_the_same_gauge(vector_1, vector_0):
    # 寻找近似的同一的规范
    phase_1_pre = 0
    phase_2_pre = pi
    n_test = 10001
    for i0 in range(n_test):
        test_1 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_1_pre) - vector_0))
        test_2 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_2_pre) - vector_0))
        if test_1 < 1e-6:
            phase = phase_1_pre
            # print('Done with i0=', i0)
            break
        if i0 == n_test-1:
            phase = phase_1_pre
            print('Gauge Not Found with i0=', i0)
        if test_1 < test_2:
            if i0 == 0:
                phase_1 = phase_1_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_1_pre
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
        else:
            if i0 == 0:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre 
        phase_1_pre = phase_1
        phase_2_pre = phase_2
    vector_1 = vector_1*cmath.exp(1j*phase)
    # print('二分查找找到的规范=', phase)   
    return vector_1