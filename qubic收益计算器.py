version = "v2.4.2"
import os
import json
import requests

print('项目地址：https://github.com/EdmundFu-233/Qubic_revenue_calculator')
print('如果你是花钱购买的本程序，那么你被骗了，请申请退款。')
print('已知问题：打开2FA的账户无法登入，请使用离线模式')
print('版本号： ',version)
print('---------------------------------------------------------------------')

offline_mode = input("是否进入离线模式？（无需输入账号密码）\n输入[Y]es或[N]o回车确认: ")
if offline_mode == "Y" or offline_mode == "y":
    offline_mode = True
else:
    offline_mode = False

def get_name_passwd():
    file_name = "calculator_temp"
    if os.path.isfile(file_name):
        use_saved_pass = input("已发现之前使用的用户密码，是否使用？\n输入[Y]es或[N]o回车确认: ")
        if use_saved_pass == "Y" or use_saved_pass == "y":
            with open(file_name, "r") as json_file:
                user_pswd_data = json.load(json_file)
            return user_pswd_data
        else:
            os.remove(file_name)
            user_name = input("请输入你的qubic.li用户名： ")
            user_passwd = input("请输入你的qubic.li密码： ")
            user_pswd_data = {"user_name": user_name,
                            "user_passwd":user_passwd }
            with open(file_name, "w") as json_file:
                json.dump(user_pswd_data, json_file)
            return user_pswd_data
    else:
        user_name = input("请输入你的qubic.li用户名： ")
        user_passwd = input("请输入你的qubic.li密码： ")
        user_pswd_data = {"user_name": user_name,
                          "user_passwd":user_passwd }
        with open(file_name, "w") as json_file:
            json.dump(user_pswd_data, json_file)
        return user_pswd_data
    
def miner_info(user_name,user_password):
    url = "https://api.qubic.li/Auth/Login"
    request_payload = {
    "userName": user_name,
    "password": user_password
    }
    request_header = {
    "Content-Type": "application/json",
    "Origin": "https://app.qubic.li",
    "Referer": "https://app.qubic.li/"
    }
    miner_data = requests.post(url, json=request_payload, headers=request_header)
    token = miner_data.json().get("token")
    headers = {
    'Accept': 'application/json',
    "Authorization": f"Bearer {token}"
    }  
    miner_performance_url = "https://api.qubic.li/My/Pool/f4535705-eeac-4c4f-9ddc-4c3a91b40b13/Performance"
    miner_performance_json=requests.get(miner_performance_url,headers=headers)
    miner_performance=miner_performance_json.json()
    return miner_performance

def miner_hashrate(miners_info):
    miners = miners_info["miners"]
    hashrate = 0
    for miner in miners:
        hashrate += int(miner["currentIts"])
    return hashrate

if offline_mode == False:
    name_passwd = get_name_passwd()
    miner_info_temp = miner_info(name_passwd["user_name"],name_passwd["user_passwd"])
    myHashrate = miner_hashrate(miner_info_temp)
    print("正在获取信息，请稍等")
else:
    myHashrate = int(input("请输入算力: "))
    print("正在获取信息，请稍等")

import datetime
import locale
from datetime import datetime, timedelta
import pytz
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter
from rich.console import Console
from rich.table import Table
locale.setlocale(locale.LC_ALL, '')

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

def past_score_info(data,table_name):
    for entry in data["scoreStatistics"]:
        date = entry["daydate"]
        date = date.replace(" AM","").replace(" PM","")
        date = datetime.strptime(date, "%m/%d/%Y %I:%M:%S")
        date = date.strftime("%m月%d日")
        max_score = entry["maxScore"]
        min_score = entry["minScore"]
        avg_score = entry["avgScore"]
        table_name.add_row(date,str(max_score),str(min_score),str(avg_score))

def latest_avg_score(data):
    latest_entry = max(data["scoreStatistics"], key=lambda x: x['daydate'])
    latest_avg_score = latest_entry['avgScore']
    return latest_avg_score

def sol_convert_qus(curSolPrice):
    qus_quantity = curSolPrice / qubicPrice
    return int(qus_quantity)

def day_per_sol_warning(table_name):
    if 24 * myHashrate * netSolsPerHour / netHashrate < 1:
        table_name.add_row('预测获取sol的周期', str(round(1 / (24 * myHashrate * netSolsPerHour / netHashrate),2)) + " 天")
        if 7 < 1 / (24 * myHashrate * netSolsPerHour / netHashrate):
            table_name.add_row("⚠  获得 sol 周期超过 1 纪元，请注意风险⚠","⚠  获得 sol 周期超过 1 纪元，请注意风险⚠")

def miner_luckiness(network_its,Its,solutionsFound,latest_avg_score):       ##存在算法层面的疑惑，如果您有更好的解决方法，请提交issue
    if solutionsFound == 0:
        return "N/A"
    else:
        luckyness = (Its / solutionsFound) / (network_its / (latest_avg_score * 676))
        return luckyness

def miner_detail(miner_info,table_name):
    miner_info = miner_info["miners"]
    for miner in miner_info:
        if miner_luckiness(netHashrate,miner['currentIts'],miner['solutionsFound'],latest_avg_score(networkStat)) == "N/A":
            table_name.add_row(miner['alias'],str(miner['currentIts']) + " it/s",str(miner['solutionsFound']),"N/A")
        else:
            table_name.add_row(miner['alias'],str(miner['currentIts']) + " it/s"
                               ,str(miner['solutionsFound'])
                               ,"{:.1%}".format(miner_luckiness(netHashrate,miner['currentIts'],miner['solutionsFound'],latest_avg_score(networkStat))))


table_epoch_info = Table(title="⌛ 目前纪元信息⌛")
table_epoch_info.add_column('信息类型', style="cyan")
table_epoch_info.add_column('数值', justify="right", style="green")
table_epoch_info.add_row('目前纪元',str(epochNumber))
table_epoch_info.add_row('目前纪元开始的中国时间',convert_utc_to_china(str(curEpochBegin)))
table_epoch_info.add_row('目前纪元结束的中国时间',convert_utc_to_china(str(curEpochEnd)))
table_epoch_info.add_row('纪元进度','{:.1f}%'.format(100 * curEpochProgress))
Console().print(table_epoch_info)

table_network_info = Table(title="🌐 网络信息🌐")
table_network_info.add_column('信息类型', style="cyan")
table_network_info.add_column('数值', justify="right", style="green")
table_network_info.add_row('估测的网络算力', '{0:,} it/s'.format(netHashrate).replace(',', ' '))
table_network_info.add_row('平均分',  '{:.1f}'.format(netAvgScores))
table_network_info.add_row('sol/每小时',  '{:.1f}'.format(netSolsPerHour))
Console().print(table_network_info)

table_past_score_info = Table(title="📆 往期分数📆")
table_past_score_info.add_column('日期', style="cyan")
table_past_score_info.add_column('最高分', style="green")
table_past_score_info.add_column('最低分', style="green")
table_past_score_info.add_column('平均分', style="green")
past_score_info(networkStat,table_past_score_info)
Console().print(table_past_score_info)

table_revenue_estimate = Table(title="💰 收益预计💰 (85%收益池)")
table_revenue_estimate.add_column('信息类型', style="cyan")
table_revenue_estimate.add_column('数值', justify="right", style="green")
table_revenue_estimate.add_row('Qubic 价格', '{:.8f}$'.format((qubicPrice)))
table_revenue_estimate.add_row('预测的每 1 it/s 每日的收入', '{:.2f}￥'.format(currency_convert_cny(incomerPerOneITS)))
table_revenue_estimate.add_row('预测的每日收入', '{:.2f}￥'.format(currency_convert_cny((myHashrate * incomerPerOneITS))))
table_revenue_estimate.add_row('预测的每 sol 的收入', '{:.2f}￥'.format(currency_convert_cny(curSolPrice)))
table_revenue_estimate.add_row('预测的每日 sol 数量', '{:.3f}'.format(24 * myHashrate * netSolsPerHour / netHashrate))
table_revenue_estimate.add_row('预测的每 sol 的币量', '{0:,}'.format(sol_convert_qus(curSolPrice)))
day_per_sol_warning(table_revenue_estimate)
Console().print(table_revenue_estimate)

if offline_mode == False:
    table_miner_detail = Table(title="🖥️ 矿机信息🖥️")
    table_miner_detail.add_column('名称', style="cyan")
    table_miner_detail.add_column('目前算力', justify="right", style="green")
    table_miner_detail.add_column('sol 数量', justify="right", style="red")
    table_miner_detail.add_column('幸运值', justify="right", style="green")
    miner_detail(miner_info(name_passwd["user_name"],name_passwd["user_passwd"]),table_miner_detail)
    Console().print(table_miner_detail)

    table_miner_summary = Table(title="🖥️ 矿机总结🖥️")
    table_miner_summary.add_column('总算力', style="cyan")
    table_miner_summary.add_column('总 Sol ', justify="right", style="green")
    table_miner_summary.add_column('总幸运值', justify="right", style="green")
    table_miner_summary.add_row(str(myHashrate) + " it/s",str(miner_info_temp["foundSolutions"])
                            ,"{:.1%}".format(miner_luckiness(netHashrate,myHashrate,miner_info_temp["foundSolutions"],latest_avg_score(networkStat))))
    Console().print(table_miner_summary)

print('↑上方可能有信息被遮盖住，请注意窗口大小↑')
print('项目地址：https://github.com/EdmundFu-233/Qubic_revenue_calculator')
print('如果你是花钱购买的本程序，那么你被骗了，请申请退款。')
input("\n按回车退出")