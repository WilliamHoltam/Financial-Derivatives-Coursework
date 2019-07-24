program FD
    implicit none

!   Sun 15 Apr 2018 12:44:36
!
!   Compile with: "gfortran FD.f95 -o FD"
!   Run with: "./FD"
    
    integer, dimension(:),allocatable :: a_seed
    integer :: i_seed
    integer, dimension(1:8) :: dt_seed

    real :: pi, x1, x2, z1, z2, ds, s, dw, t
    integer, parameter :: num_trading_days = 250, s_0 = 100
    real, parameter :: drift = 0.16, r = 0.04, k = 0.2!, volatility = 0.2
!   Change volatility from 0.2 to 0.6 for section 2 (g)
    real, parameter :: dt = 1.0/float(num_trading_days)
    real, dimension(:,:), allocatable :: portfolio_value
    integer, dimension(4) :: indx = [1, 2, 5, 20]
    real, dimension(2) :: volatility_array = [0.2, 0.6]
    real, dimension(:), allocatable :: prob_loss
    integer :: num_years, itter_per_simulation, i, j, h, l, m, f, q
    real :: mean, variance, volatility

    pi = acos(-1.0)

!   Question 2. (b)
    call random_seed(size=i_seed)
    allocate(a_seed(1:i_seed))
    call random_seed(get=a_seed)
    call date_and_time(values=dt_seed)
    a_seed(i_seed)=dt_seed(8); a_seed(1)=dt_seed(8)*dt_seed(7)*dt_seed(6)
    call random_seed(put=a_seed)
    deallocate(a_seed)

!   Question 2. (c)
    s = float(s_0)
    t = 0.0
    open(10 , file = "s_price_1yr.dat")
        do i = 1, num_trading_days
            call random_number(x1)
            call random_number(x2)
!           write(6,*) "The random number x1 is: ", x1
!           write(6,*) "The random number x2 is: ", x2
            z1 = sqrt(-2.0*log(x1))*cos(2.0*pi*x2)
            z2 = sqrt(-2.0*log(x2))*sin(2.0*pi*x2)
!           write(6,*) "The value of z1 is: ", z1
!           write(6,*) "The value of z2 is: ", z2

!           Question 2. (c)
            dw = sqrt(dt)*z1
            ds = s*(drift*dt + volatility_array(1)*dw )
            s = s + ds
            write(10,*) s , t
            t = t+dt
        end do
    close(10)


!   Question 2. (d)

    open(11, file = "portfolio_value_1yr.dat")
    open(12, file = "portfolio_value_2yr.dat")
    open(13, file = "portfolio_value_5yr.dat")
    open(14, file = "portfolio_value_20yr.dat")
        do q=1,size(volatility_array)
            volatility = volatility_array(q)
            do i=1,size(indx)
                num_years = indx(i)
                itter_per_simulation = num_trading_days*num_years
!                write(6,*) itter_per_simulation
                allocate(portfolio_value(itter_per_simulation,1000))
                m = 0
                portfolio_value(:,:) = 0.0
                allocate(prob_loss(itter_per_simulation))
                prob_loss = 0
                do j = 1, 1000
                    s = float(s_0)
                    t = 0.0
                    do h = 1, itter_per_simulation

                        call random_number(x1)
                        call random_number(x2)

                        z1 = sqrt(-2.0*log(x1))*cos(2.0*pi*x2)
                        z2 = sqrt(-2.0*log(x2))*sin(2.0*pi*x2)

                        dw = sqrt(dt)*z1
                        ds = s*(drift*dt + volatility*dw )
                        s = s + ds
                        t = t+dt

                        portfolio_value(h,j) = s*exp(-r*t)-s_0

                        if (s .ge. (s_0*(1.0+k)*exp(r*t))) then
                            portfolio_value(h,j) = s_0*k
                            exit
                        end if

                        if (volatility .eq. 0.2) then
                            if (num_years .eq. 1) then
                                write(11,*) portfolio_value(h,j), t
                            else if (num_years .eq. 2) then
                                write(12,*) portfolio_value(h,j), t
                            else if (num_years .eq. 5) then
                                write(13,*) portfolio_value(h,j), t
                            else if (num_years .eq. 20) then
                                write(14,*) portfolio_value(h,j), t
                            end if
                        end if

                        if (portfolio_value(h,j) .le. 0) then
                            prob_loss(h) = (prob_loss(h) + 1)
                        end if
                    end do

                    do l = 1 , int(itter_per_simulation-h)
                        t = t+dt
                        f = h + l
                        portfolio_value(f,j) = s_0*k
                        if (volatility .eq. 0.2) then
                            if (num_years .eq. 1) then
                                write(11,*) portfolio_value(f,j), t
                            else if (num_years .eq. 2) then
                                write(12,*) portfolio_value(f,j), t
                            else if (num_years .eq. 5) then
                                write(13,*) portfolio_value(f,j), t
                            else if (num_years .eq. 20) then
                                write(14,*) portfolio_value(f,j), t
                            end if
                        end if
!                       p = p + 1
                    end do

                end do

!            prob_loss = prob_loss(h)/1000

                if (indx(i) .eq. 20) then
                    t = 0.0
                    open(15, file = "statistics.dat")
                    open(16, file = "prob_loss.dat")
                    open(17, file = "prob_loss_06.dat")
                    open(18, file = "statistics_06.dat")
                        do h = 1, itter_per_simulation
                            t = t+dt
                            if (volatility .eq. 0.2) then
                                write(16,*) prob_loss(h)/1000, t
                            else if (volatility .eq. 0.6) then
                                write(17,*) prob_loss(h)/1000, t
                            end if
                            mean = sum(portfolio_value(h,:))/1000
                            !WORK OUT HOW VARIANCE CHANGES OVER PORTFOLIO TIMEFRAME
                            variance = 0.0
                            do j = 1, 1000
                                variance=variance+(portfolio_value(h,j)-mean)**2.0
                            end do
                            variance = variance/real(j-1)
                            if (volatility .eq. 0.2) then
                                write(15,*) mean, variance, t
                            else if (volatility .eq. 0.6) then
                                write(18,*) mean, variance, t
                            end if
                        end do
                    close(15)
                    close(16)
                    close(17)
                    close(18)
                end if
!               write(6,*) "m_count", m
                deallocate (portfolio_value)
                deallocate(prob_loss)
            end do
        end do
    close(11)
    close(12)
    close(13)
    close(14)
end program FD
