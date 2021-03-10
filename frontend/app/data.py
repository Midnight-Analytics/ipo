import FinancialModelingPrep



session = FinancialModelingPrep.Calendars()
data = session.ipo_calendar('2021-03-10', '2021-03-30')

#print(list(data[0].keys()))
#print(data)


session2 = FinancialModelingPrep.StockMarket()

that = session2.most_gainer_stock()
print(that)