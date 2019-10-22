#########备份基本配置###########
# 本地要进行备份的目录(每个路径前利用r将路径转义，避免/n，/t等特殊用法)
# 备份目录为列表格式，可设置多个本地备份路径
# 每一个目录的配置为字典类型{"localpath":本地路径,"remotepath":远程路径}
"""
示例
BACKUPDIR = [
    {"localpath": r"D:\Youdao", "remotepath": "Youdao"},
    {"localpath": r"D:\softbak\kwifi", "remotepath": "kwifi"},
]
"""
BACKUPDIR = [
    {"localpath": r"D:\Youdao", "remotepath": ""},
    {"localpath": r"", "remotepath": ""},
]

# 排除的目录或者文件(每个路径前利用r将路径转义，避免/n，/t等特殊用法)
EXCLUDE = [r'D:\test\qqq', r'D:\test\test.txt']
# 设置全备日期（周）
"""
0: '星期一',
1: '星期二',
2: '星期三',
3: '星期四',
4: '星期五',
5: '星期六',
6: '星期日',
"""
FULLWEEKDAY = [6, 2]
# ftp_theadpool线程池数量
FtpTheadpoolNum = 10

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
HOSTIP = ''
# FTP用户名
USERNAME = ''
# FTP密码
PASSWORD = ''
# 端口号
PORT = 21

###########邮箱服务器############
# 设置服务器所需信息
"""是否开启邮箱配置"""
EMAIL = 0
# 163邮箱服务器地址
mail_host = "smtp.163.com"
# 163用户名
mail_user = ""
# 密码(部分邮箱为授权码)
mail_pass = ''
# 邮件发送方邮箱地址
sender = ''
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['']

##########企业微信配置#############
WECHAT = False
corpid = ''
corpsecret = ''
touser = []
agentid = ''

###########钉钉机器人配置##########
DINGTALK = False
webhook = ''
