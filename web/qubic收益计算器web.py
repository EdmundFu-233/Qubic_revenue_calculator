from pywebio.input import *
from pywebio.session import *
import pywebio
import requests
import datetime
import json
from datetime import datetime, timedelta
import pytz
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter
def main():
    try:
        pywebio.config(title="Qubic收益计算器")
        pywebio.session.run_js("$('head link[rel=icon]').attr('href', image_url)", image_url="https://framerusercontent.com/images/Hz7gOuXD46YyfCTTafJLOvWNi0.png")
        offline_options = [["是",True,True],["否",False]]
        def begging():
            pywebio.output.put_info("免费项目，如果您愿意，请赞助此项目的维护，谢谢\nQubic地址：\nTGVFDIRGWBGOUCVRYQSUVPXFVDWBMDRRTIXHSBYGVEFRRQWDJDLAXNYCZPDB\nXMR地址：\n43ic8XkEXRxEFUaCh52NfB4bG7wA8LCjm5Yrmpizx8zUDQHf8zjyyNAKcbseYzyw3ZLGicQvPeJw2g8LRCNWHSgwTRxRCDc")
        begging()
        pywebio.output.put_markdown("<font size=10> <center>Qubic 收益计算器</center> </font>")
        pywebio.output.put_markdown("<font size=10> A open-source project By EdmundFu </font>")
        is_offline_mode = pywebio.input.select(label="是否进入离线模式（不查看矿机信息）",options=offline_options)
        if is_offline_mode == False:
            user_info = input_group('请输入Qubic-li池账户密码',[input("用户名",type=TEXT, name='username',hxt='例如邮箱', required=True),
                                    input("密码", name='password',type=PASSWORD, required=True)])
            user_name = user_info['username']
            user_password = user_info['password']
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
            miner_info_temp = miner_info(user_name,user_password)
            myHashrate = miner_hashrate(miner_info_temp)

        else:
            myHashrate = pywebio.input.input(label="请输入算力",type=TEXT,required=True)

        myHashrate = int(myHashrate)

        pywebio.output.put_loading(shape='border')
        
        rBody = {'userName': 'guest@qubic.li', 'password': 'guest13@Qubic.li', 'twoFactorCode': ''}
        rHeaders = {'Accept': 'application/json', 'Content-Type': 'application/json-patch+json'}
        r = requests.post('https://api.qubic.li/Auth/Login', data=json.dumps(rBody), headers=rHeaders)
        token = r.json()['token']
        rHeaders = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
        r = requests.get('https://api.qubic.li/Score/Get', headers=rHeaders)
        networkStat = r.json()

        epochNumber = networkStat['scoreStatistics'][0]['epoch']
        epoch97Begin = datetime.strptime('2024-02-21 12:00:00', '%Y-%m-%d %H:%M:%S')
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

        def past_score_info(data):
            score_info = [['日期','最高分','最低分','平均分']]
            for entry in data["scoreStatistics"]:
                date = entry["daydate"]
                date = date.replace(" AM","").replace(" PM","")
                date = datetime.strptime(date, "%m/%d/%Y %I:%M:%S")
                date = date.strftime("%m月%d日")
                max_score = entry["maxScore"]
                min_score = entry["minScore"]
                avg_score = entry["avgScore"]
                score_info.append([date,str(max_score),str(min_score),str(avg_score)])
            return score_info

        def latest_avg_score(data):
            latest_entry = max(data["scoreStatistics"], key=lambda x: x['daydate'])
            latest_avg_score = latest_entry['avgScore']
            return latest_avg_score

        def sol_convert_qus(curSolPrice):
            qus_quantity = curSolPrice / qubicPrice
            return int(qus_quantity)

        def day_per_sol_period():
            if 24 * myHashrate * netSolsPerHour / netHashrate < 1:
                pywebio.output.put_warning('预测获取sol的周期为 ' + str(round(1 / (24 * myHashrate * netSolsPerHour / netHashrate),2)) + " 天")
            
        def day_per_sol_warning():
            if 7 < 1 / (24 * myHashrate * netSolsPerHour / netHashrate):
                pywebio.output.put_warning("⚠获得 sol 周期超过 1 纪元，请注意风险⚠")

        def miner_luckiness(network_its,Its,solutionsFound,latest_avg_score):       ##存在算法层面的疑惑，如果您有更好的解决方法，请提交issue
            if solutionsFound == 0:
                return "N/A"
            else:
                luckyness = (Its / solutionsFound) / (network_its / (latest_avg_score * 676))
                return luckyness

        def miner_last_active(utc_datetime):
            utc_datetime = utc_datetime.replace('T',' ')
            try:
                utc_datetime = datetime.strptime(utc_datetime, '%Y-%m-%d %H:%M:%S.%f')
            except:
                utc_datetime = datetime.strptime(utc_datetime, '%Y-%m-%d %H:%M:%S')
            utc_timezone = pytz.timezone('UTC')
            china_timezone = pytz.timezone('Asia/Shanghai')
            utc_datetime = utc_timezone.localize(utc_datetime)
            china_datetime = utc_datetime.astimezone(china_timezone)
            return china_datetime.strftime('%m月%d日 %H:%M:%S')
        
        def miner_detail(miner_info):
            miner_info = miner_info["miners"]
            miner_detail_temp = [['名称','目前算力','sol 数量','幸运值','最后一次心跳']]
            for miner in miner_info:
                if miner_luckiness(netHashrate,miner['currentIts'],miner['solutionsFound'],latest_avg_score(networkStat)) == "N/A":
                    miner_detail_temp.append([miner['alias'],str(miner['currentIts']) + " it/s",str(miner['solutionsFound']),"N/A",str(miner_last_active(miner['lastActive']))])
                else:
                    miner_detail_temp.append([miner['alias'],str(miner['currentIts']) + " it/s"
                                    ,str(miner['solutionsFound'])
                                    ,"{:.1%}".format(miner_luckiness(netHashrate,miner['currentIts'],miner['solutionsFound'],latest_avg_score(networkStat))),str(miner_last_active(miner['lastActive']))])
            return miner_detail_temp
        
        def summary_luckiness():
            luckiness = miner_luckiness(netHashrate,myHashrate,miner_info_temp["foundSolutions"],latest_avg_score(networkStat))
            if luckiness != "N/A":
                return "{:.1%}".format(miner_luckiness(netHashrate,myHashrate,miner_info_temp["foundSolutions"],latest_avg_score(networkStat)))
            else:
                return "N/A"
            
        pywebio.output.clear()

        begging()
        try:
            day_per_sol_period()
            day_per_sol_warning()
            pywebio.output.put_text("⌛ 目前纪元信息⌛")
            pywebio.output.put_table([['信息类型','数值'],
                                    ['目前纪元',str(epochNumber)],
                                    ['目前纪元开始的中国时间',convert_utc_to_china(str(curEpochBegin))],
                                    ['目前纪元结束的中国时间',convert_utc_to_china(str(curEpochEnd))],
                                    ['纪元进度','{:.1f}%'.format(100 * curEpochProgress)]])
            
            pywebio.output.put_text("🌐 网络信息🌐")
            pywebio.output.put_table([['信息类型','数值'],
                                    ['估测的网络算力', '{0:,} it/s'.format(netHashrate).replace(',', ' ')],
                                    ['平均分',  '{:.1f}'.format(netAvgScores)],
                                    ['sol/每小时',  '{:.1f}'.format(netSolsPerHour)]])
            
            pywebio.output.put_text("📆 往期分数📆")
            pywebio.output.put_table(past_score_info(networkStat))

            pywebio.output.put_text("💰 收益预计💰 (85%收益池)")
            pywebio.output.put_table([['信息类型','数值'],
                                    ['Qubic 价格', '{:.8f}$'.format((qubicPrice))],
                                    ['预测的每 1 it/s 每日的收入', '{:.2f}￥'.format(currency_convert_cny(incomerPerOneITS))],
                                    ['预测的每日收入', '{:.2f}￥'.format(currency_convert_cny((myHashrate * incomerPerOneITS)))],
                                    ['预测的每 sol 的收入', '{:.2f}￥'.format(currency_convert_cny(curSolPrice))],
                                    ['预测的每日 sol 数量', '{:.3f}'.format(24 * myHashrate * netSolsPerHour / netHashrate)],
                                    ['预测的每 sol 的币量', '{0:,}'.format(sol_convert_qus(curSolPrice))]])
            
            if is_offline_mode == False:
                pywebio.output.put_text("🖥️ 矿机信息🖥️")
                pywebio.output.put_table(miner_detail(miner_info(user_name,user_password)))

                pywebio.output.put_text("🖥️ 矿机总结🖥️")
                pywebio.output.put_table([['总算力','总 Sol ','总幸运值','截至目前收益'],
                                        [str(myHashrate) + " it/s",str(miner_info_temp["foundSolutions"])
                                        ,summary_luckiness()
                                        ,'{:.2f}￥'.format(currency_convert_cny(curSolPrice) * miner_info_temp["foundSolutions"])]])
            pywebio.output.put_text("                       ")
        except ZeroDivisionError:
            pywebio.output.put_error("获取信息中遇到错误，请检查您的账号密码输入是否正确。")
    except:
        pywebio.output.put_error("处理过程中遇到致命错误，请联系作者。")

pywebio.platform.aiohttp.start_server(main,port=80,cdn=True)