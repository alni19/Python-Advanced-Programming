USE [Assignment9]
GO
/****** Object:  StoredProcedure [dbo].[GetSecurityMarkValDPnL]*****/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
Create PROCEDURE [dbo].[GetSecurityMarkValDPnL](@securityCode varchar(50),
									@startDate date, @endDate date)
AS
BEGIN

	Select SecurityCode, BusinessDate, SUM(pd.DayTotalPNL) DayTotalPNL, SUM(pd.BaseMarketValue) BaseMarketValue
    from PositionData pd
    Inner join Security s on pd.SecurityId = pd.SecurityId
    Where SecurityCode = @securityCode and BusinessDate >= @startDate and BusinessDate <= @endDate
    group by SecurityCode, BusinessDate
    Order by BusinessDate Asc

END

commit