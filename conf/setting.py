#########备份目录配置###########
# 本地要进行备份的目录
BACKUPDIR = r'D:\python\脚本\test'
# 远程备份目录
REMOTEPATH = 'testbak'

##########日志文件配置###########
"""
当LOGFILE设置为1或者True是，必须配置LOGFILEPATH
"""
# 是否开启自定义日志文件
LOGFILE = 0
# 自定义日志文件路径
LOGFILEPATH = ''

##########FTP配置###############
# 主机ip
HOSTIP = '192.168.8.142'
# FTP用户名
USERNAME = 'administrator'
# FTP密码
PASSWORD = 'Wandu2017'
# 端口号
PORT = 21

###########邮箱服务器############
# 设置服务器所需信息
"""是否开启邮箱配置"""
EMAIL = True
# 163邮箱服务器地址
mail_host = "smtp.163.com"
# 163用户名
mail_user = "yunweijsf"
# 密码(部分邮箱为授权码)
mail_pass = 'jsf0408'
# 邮件发送方邮箱地址
sender = 'yunweijsf@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['jsf0408it@163.com']

##########企业微信配置#############
WECHAT = False
corpid = ''
corpsecret = ''
touser = []
agentid = ''


###########钉钉机器人配置##########
DINGTALK = False
