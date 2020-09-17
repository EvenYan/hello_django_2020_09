# record_performance.py
#!/bin/sh

import os
import pymysql

# 创建数据库连接对象
db = pymysql.connect("192.168.0.9", "root", "root", "auto_ops")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def get_host_info():
    # DATE=$(date "+%Y-%m-%d %H:%M:%S")
    mem = os.popen('''
        IP=$(/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:")
        MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
        DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
        CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
        echo "$IP|$MEMORY|$DISK|$CPU"
        ''')
    result = mem.read().strip()
    return result.split("|")


def main():
    
    ret = get_host_info()
    print(ret)
    if len(ret) != 4:
        print("未获取到主机的运行状态！")
        return
    IP = ret[0]
    MEMORY = float(ret[1][:-1])
    DISK = float(ret[2][:-1])
    CPU = float(ret[3][:-1])
    try:
        if MEMORY > 20 or DISK > 80 or CPU > 90:
            sql = "insert into host(ip, mem, disk, cpu, status) values('%s', '%s', '%s', '%s', '%s');" % (IP, MEMORY, DISK, CPU, "warning")
            cursor.execute(sql)
        else:
            sql = "insert into host(ip, mem, disk, cpu, status) values('%s', '%s', '%s', '%s', '%s');" % (IP, MEMORY, DISK, CPU, "normal")
            cursor.execute(sql)
        print(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.close()


if __name__ == "__main__":
    main()