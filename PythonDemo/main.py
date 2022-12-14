import random
import sys

import requests
import time
import hashlib
import json
api_key = ''  # 这里需要替换你的APIKey
api_secret = ''  # 这里需要替换你的APISecret
from datetime import datetime

userName = 'tester'  # 你的姓名
botName = "小爱"  # AI姓名
userAge = 18
botAge = 18  # AI年龄
year = 2022
month = 12  # 月
day = 15  # 日
weekDay = "天"   # 星期几
season = "冬天"   # 季节
weather = "晴天"   # 天气
temperature = 15   # 温度
meaning_url = 'http://localhost:8000/semantic_score'  # 如部署远程服务器 对应修改请求URL
property_draw_url = 'http://localhost:8001/triplets'  # 如部署远程服务器 对应修改请求URL
robot_height = 160
robot_weight = 45
robot_chest = 50
robot_waistline = 10
robot_hipline = 10
robot_birth_month = 12
robot_birth_day = 26
location = "北京"
hairdo = "双马尾"
hair_color = "黑色"
robot_gender = "女"
userBirthYear = 1992
userBirthMonth = 5
userBirthDay = 25

url = 'https://openapi.singularity-ai.com/api/v2/generateByKey'
conversation = []
timestamp = str(int(time.time()))
prompt = '中国是一个伟大的国家'
model_version = 'benetnasch_common_gpt3'
useMeaning = True
use_property_draw = True


def help_info():
    help = """
usage : python {0}  
""".format(sys.argv[0])
    print(help)


def generate_sent_list():
    l = ['今天什么天气', '今天什么节日', '今天什么节气', '今天星期几', '今年什么年', '今年是哪一年', '你上的哪所大学', '你今年多大', '你会什么', '你体重是多少', '你叫什么名字',
         '你吃早饭了吗', '你在哪', '你在哪个城市生活', '你在干嘛', '你头发什么颜色', '你好', '你学的什么专业', '你是什么发型', '你是什么星座', '你是几月出生的', '你是哪一年出生的',
         '你是机器人吗', '你是男生还是女生', '你是谁', '你有什么爱好', '你有什么特长', '你有宠物吗', '你的工作是什么', '你的生日是什么时候', '你胸围是多少', '你腰围是多少',
         '你臀围是多少', '你自我介绍一下', '你身高是多少', '你骗人', '哈哈哈哈', '我不想上班', '我不漂亮', '我们在哪里', '我叫什么名字', '我喜欢你', '我困了', '我很开心',
         '我很无聊',
         '我很难过', '我肚子疼', '现在什么温度', '现在几点了', '现在是什么季节', '现在是几号', '现在是阴历几号', '给我讲个笑话']
    return l


def check_meaning(ask):
    input_sent = ask
    sent_list = generate_sent_list()
    resp = requests.post(meaning_url, data=json.dumps({'input_sent': input_sent, 'sent_list': sent_list, 'threshold': 0.8}),
                         headers={'content-type': "application/json"}, timeout=5)

    if resp.status_code == 200:
        resp_data = json.loads(resp.content)
        if resp_data['score'] >= 0.8:
            #print(resp_data)
            rst = resp_data['sent'][0]
            #print(rst)
            return lookup_data(rst)


def check_property_draw(conv):
    resp = requests.post(property_draw_url, data=json.dumps({'input': conv}),
                         headers={'content-type': "application/json"}, timeout=5)

    if resp.status_code == 200:
        a = json.loads(resp.content)
        try:
            rst = a['data'][0]
        except:
            return 'null'
        #print(resp.content)
        ret = rst["object"]+ ',' + rst['predicate'] + ',' + rst['subject']

    return ret

def lookup_data(rst):
    f = open("./huashu.csv", 'r', encoding='UTF-8')
    huashu_dic = {}
    count = 0
    for line in f:
        #print(line)
        strs = line.split(',')
        if count >= 1 and strs[7] == 'AI':
            huashu_dic[strs[8]] = strs[1]
        count = count + 1

    possible_answer = [k for k, v in huashu_dic.items() if v == rst]
    if len(possible_answer)<= 0:
        return 'Error: Check huashu doc'
    a = random.choice(possible_answer)
    return a


def fill_property(meaning_answer):
    if "[robot.name]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.name]", botName)
    if "[user.name]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[user.name]", userName)
    if "[robot.age]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.age]", str(botAge))
    if "[robot.weight]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.weight]", str(robot_weight))
    if "[robot.height]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.height]", str(robot_height))
    if "[robot.chest]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.chest]", str(robot_chest))
    if "[robot.hipline]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.hipline]", str(robot_hipline))
    if "[robot.gender_cn]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.gender_cn]", robot_gender)
    if "[location]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[location]", location)
    if "[time]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[time]", datetime.now().strftime("%H:%M:%S"))
    if "[time_interval]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[time_interval]", datetime.now().strftime("%H:%M:%S"))
    if "[year]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[year]", str(year))
    if "[month]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[month]", str(month))
    if "[day]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[day]", str(day))
    if "[week]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[week]", str(weekDay))
    if "[season]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[season]", season)
    if "[temperature]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[temperature]", str(temperature))
    if "[robot.place_origin]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.place_origin]", '北京')
    if "[robot.employed_by_company]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.employed_by_company]", '奇点')
    if "[robot.has_profession]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.has_profession]", '智能代表')
    if "[robot.has_ability]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.has_ability]", '跳舞')
    if "[robot.like_activity]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.like_activity]", '看剧')
    if "[robot.live_in_citystatecountry]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.live_in_citystatecountry]", '北京')
    if "[robot.major]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.major]", '土木')
    if "[robot.constellation]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.constellation]", '射手座')
    if "[robot.university]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.university]", '北京大学')
    if "[robot.have_pet]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.have_pet]", '猫')
    if "[robot.pet_name]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.pet_name]", '小黑')
    if "[robot.blood]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.blood]", 'B型')
    if "[robot.hairdo]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.hairdo]", hairdo)
    if "[robot.hair_color]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.hair_color]", hair_color)
    if "[robot.have_pet]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[robot.have_pet]", '猫')
    if "[user.age]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[user.age]", str(userAge))
    if "[user.birth_year]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[user.birth_year]", str(userBirthYear))
    if "[user.birth_month]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[user.birth_month]", str(userBirthMonth))
    if "[user.birth_day]" in meaning_answer:
        meaning_answer = meaning_answer.replace("[user.birth_day]", str(userBirthDay))
    return meaning_answer


def talk(ask):

    if useMeaning:
        meaning_answer = check_meaning(ask)
        if meaning_answer is not None:
            conversation.append(userName + ':' + ask)

            meaning_answer = fill_property(meaning_answer)
            print(meaning_answer)
            conversation.append(botName + ':' + meaning_answer)
            talk(input(f"{userName}: "))
            return

    if use_property_draw and len(conversation) >1:
        conv = [conversation[len(conversation)-1], ask]
        property = check_property_draw(conv)
        if property != 'null':
            print("**********提取到屬性可作為記憶使用 " + property)

    p = generate_prompt(ask)
    # print(p)
    sign_content = api_key + api_secret + model_version + p + timestamp
    sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()
    headers = {
        "App-Key": "Bearer " + api_key,
        "timestamp": timestamp,
        "sign": sign_result,
        "Content-Type": "application/json"
    }
    data = {
        "data": {
            "prompt": p,
            "model_version": model_version,
            "param": {
                "generate_length": 500,
                "top_p": 0.4,
                "top_k": 20,
                "repetition_penalty": 1.3,
                "length_penalty": 1.0,
                "min_len": 4,
                "bad_words": [],
                "end_words": ["[EOS]", "\n", "\t"],
                "temperature": 1.0
            }
        }
    }
    try:
        response = requests.post(url, json=data, headers=headers)

        # print(json.loads(response.text))
        reply = json.loads(response.text)['resp_data']['reply']
        answer = str(reply).split(' ')[0]

        print(botName + ': ' +answer)
        conversation.append(botName + ':' + answer)
        talk(input(f"{userName}: "))
    except Exception as e:
        print(e)


def generate_prompt(ask):
    conversation.append(userName + ':' + ask)
    while len(conversation) > 30:
        conversation.remove(0)
    conversation_str = ""
    count = 0
    for x in conversation:
        conversation_str += conversation[count] + '\n'
        count += 1

    pre_prompt = f"时间是{month}月的第{day}天，星期{weekDay}。{season}的一个{weather}, 外头大约{temperature}度。" \
                 f"{userName}是一个男孩子,{botName}是一个活泼的女孩子，{botName}是{userName}的朋友。{userName}现在在北京," \
                 f"{botName}现在在北京。这是一段{userName}和{botName}的对话" + '\n'
    return pre_prompt + conversation_str + botName + ":"


if __name__ == '__main__':
    args = help_info()
    print(f"开始和{botName}对话")
    talk(input(f"{userName}: "))
    #d = ['爱吃什么', '我爱吃牛肉']
    #check_property_draw(d)