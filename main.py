import messagebird
import os
import configparser
import pandas as pd
import logging
import time

# 配置文件
config_file = 'config.ini' 
# 日志文件
log_file = 'sms_' + time.strftime("%Y%m%d", time.localtime()) + '.log'

# 发送短信
def send_sms(item):
    # 这里要转字符串, 否则文本为数字会报错, 空值会返回nan也要处理
    phone   = '' if pd.isnull(item['phone']) else str(item['phone']) # 联系人手机号, 不加+也能收到, 格式 85586207239
    name    = '' if pd.isnull(item['name']) else str(item['name'])   # 联系人姓名
    content = '' if pd.isnull(item['content']) else str(item['content']) # 短信内容
    
    try:
        conf = configparser.ConfigParser()
        conf.read(config_file, encoding='utf-8') # 这里要加utf-8, 否则会报错, 默认gbk
        config_section  = 'sms_config'
        app_key         = conf.get(config_section, 'messagebird_app_key')
        origin          = conf.get(config_section, 'messagebird_origin')
        
        client = messagebird.Client(app_key)
        if phone != '':
            client.message_create(originator=origin, recipients=phone, body=content) # 发送短信
            msg = '%s %s %s 发送成功' % (name, phone, content)
        else:
            msg = '%s %s %s 发送失败' % (name, phone, content)
        logger(msg) # 写入日志
        print(msg)
    except messagebird.client.ErrorException as e:
        msg = '%s 发送失败' % e
        logger(msg) # 写入日志
        print(msg)

# 写入日志
def logger(data):
    logging.basicConfig(filename = log_file, encoding = 'utf-8', level = logging.DEBUG, 
        format = '[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(data) # 根据日期生成日志

def main():
    if not os.path.exists(os.path.join(os.getcwd(), config_file)): # 检测配置文件是否存在
        print('%s 配置文件不存在' % config_file)
    else:
        df = pd.read_csv('list.csv', encoding='utf-8')
        df.apply(send_sms, axis=1) # apply添加send_sms函数, 且数据逐行加入

if __name__ == '__main__': # 主入口
    main()