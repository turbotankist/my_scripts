from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import datetime, sys
import plotly
from plotly.graph_objs import Scatter, Layout

def Progress_bar(count, total, suffix=''):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * ( bar_len - filled_len )
	sys.stdout.write("[%s] %s%s ...%s\r" % ( bar, percents, '%', suffix[:50].rjust(50) ))
	sys.stdout.flush() 

c = CurrencyRates()
b = BtcConverter()

first_date = datetime.datetime(2017,5,1)
last_date  = datetime.datetime.now()
QUANT = (last_date - first_date) // datetime.timedelta(days=1)

dateline = [[first_date],[0],[0],[0]]
dif_date = (last_date - first_date)/QUANT


print(dif_date)
print(first_date)

for month in range(QUANT):
	item_date = first_date + month*dif_date
	dateline[0].append(item_date)
	dateline[1].append(dateline[1][-1])
	dateline[2].append(dateline[2][-1])
	dateline[3].append(dateline[3][-1])
	try:
		dateline[1][-1]=(b.get_previous_price('USD',item_date))
	except:
		print("cant get BTC value")
	try:
		dateline[2][-1]=(c.get_rates('USD',item_date)["RUB"])
	except:
		print("cant get RUB value")
	try:
		dateline[3][-1]=(c.get_rates('USD',item_date)["CNY"])
	except:
		print("cant get CNY value")
	Progress_bar(month,QUANT,str(item_date))


# print(c.get_rates('USD')["RUB"])
# print(b.get_latest_price('USD'))

# print(b.convert_to_btc(30000, 'RUB'))
# print(b.get_previous_price('USD',last_date))

trace_btc = Scatter(
	x=dateline[0],
	y=dateline[1],
	line = dict(color = '#17BECF'),
	opacity = 0.8 )

trace_usd = Scatter(
	x=dateline[0],
	y=dateline[2],
	line = dict(color = '#7F7F7F'),
	opacity = 0.8 )

trace_tng = Scatter(
	x=dateline[0],
	y=dateline[3],
	line = dict(color = '#3A7F7F'),
	opacity = 0.8 )

layout = dict(
    title='Time Series with Rangeslider',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
    )

plotly.offline.plot({
    "data": [trace_btc, trace_usd, trace_tng],
    "layout": layout
})

'file://plot-curren.html'