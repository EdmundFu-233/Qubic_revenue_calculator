#enter you total hashrate of your rigs here (in it/s)
myHashrate = float(input("请输入您的算力："))

#doing the math
import requests
import json
from datetime import datetime, timedelta
import pytz
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter

rBody = {'userName': 'guest@qubic.li', 'password': 'guest13@Qubic.li', 'twoFactorCode': ''}
rHeaders = {'Accept': 'application/json', 'Content-Type': 'application/json-patch+json'}
r = requests.post('https://api.qubic.li/Auth/Login', data=json.dumps(rBody), headers=rHeaders)
token = r.json()['token']
rHeaders = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
r = requests.get('https://api.qubic.li/Score/Get', headers=rHeaders)
networkStat = r.json()

epochNumber = networkStat['scoreStatistics'][0]['epoch']
epoch97Begin = date_time_obj = datetime.strptime('2024-02-21 12:00:00', '%Y-%m-%d %H:%M:%S')
curEpochBegin = epoch97Begin + timedelta(days=7 * (epochNumber - 97))
curEpochEnd = curEpochBegin + timedelta(days=7) - timedelta(seconds=1)
curEpochProgress = (datetime.utcnow() - curEpochBegin) / timedelta(days=7)

netHashrate = networkStat['estimatedIts']
netAvgScores = networkStat['averageScore']
netSolsPerHour = networkStat['solutionsPerHour']

crypto_currency = 'qubic-network'
destination_currency = 'usd'
cg_client = CoinGeckoAPI()
prices = cg_client.get_price(ids=crypto_currency, vs_currencies=destination_currency)
qubicPrice = prices[crypto_currency][destination_currency]
poolReward = 0.85
incomerPerOneITS = poolReward * qubicPrice * 1000000000000 / netHashrate / 7 / 1.06
curSolPrice = 1479289940 * poolReward * curEpochProgress * qubicPrice / (netAvgScores * 1.06)

def convert_utc_to_china(utc_time):
    utc_datetime = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
    utc_timezone = pytz.timezone('UTC')
    china_timezone = pytz.timezone('Asia/Shanghai')
    utc_datetime = utc_timezone.localize(utc_datetime)
    china_datetime = utc_datetime.astimezone(china_timezone)
    return china_datetime.strftime('%Y-%m-%d %H:%M:%S')

def currency_convert_cny(amount_usd):
    convert_rate = CurrencyConverter().convert(1,'USD','CNY')
    cny = amount_usd * convert_rate
    return round(cny,2)


print('有些奸商拿开源的玩意来卖钱，你要是只挂个赞赏都没那么恶心')
print('-----------------------------------------------------------')
print('\n\n目前纪元信息:')
print('目前纪元:',  epochNumber)
print('目前纪元开始的中国时间:',  convert_utc_to_china(str(curEpochBegin)))
print('目前纪元结束的中国时间:',  convert_utc_to_china(str(curEpochEnd)))
print('纪元进度:',  '{:.1f}%'.format(100 * curEpochProgress))
print('-----------------------------------------------------------')
print('网络信息:')
print('网络算力:', '{0:,}'.format(netHashrate).replace(',', ' '), 'it/s')
print('平均分:',  '{:.1f}'.format(netAvgScores))
print('sol/每小时:',  '{:.1f}'.format(netSolsPerHour))
print('-----------------------------------------------------------')
print('收益预计:')
print('使用固定85%收益池预测\n')
print('Qubic 价格: {:.8f}$'.format((qubicPrice)))
print('预测的每 1 it/s 每日的收入:', '{:.4f}￥'.format(incomerPerOneITS))
print('预测的每日收入:', '{:.2f}￥'.format(currency_convert_cny((myHashrate * incomerPerOneITS))))
print('预测的每 sol 的收入:', '{:.2f}￥'.format(currency_convert_cny(curSolPrice)))
print('预测的每日 sol 数量:', '{:.5f}\n\n'.format(24 * myHashrate * netSolsPerHour / netHashrate))
input("\n\n按回车退出")