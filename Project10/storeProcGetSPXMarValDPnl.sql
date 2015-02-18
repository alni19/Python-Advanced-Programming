USE [Assignment9]
GO
/****** Object:  StoredProcedure [dbo].[GetSecurityMarkValDPnL]    Script Date: 2014-12-06 11:08:00 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
Create Proc [dbo].[GetSPXMarkValDPnL](@startDate date, @endDate date)
AS
BEGIN

	Select SecurityCode, BusinessDate, SUM(md.PriceChangePct1D) DayTotalPNL
    from MarketData md
    Inner join Security s on s.SecurityId = md.SecurityId
    Where SecurityCode = 'SPX' and BusinessDate >= @startDate and BusinessDate <= @endDate
    group by SecurityCode, BusinessDate
    Order by BusinessDate Asc

END

