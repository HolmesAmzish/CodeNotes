import datetime

def solve():
    """解决问题。"""
    t = int(input())
    for _ in range(t):
        date_str, time_str, x = input().split()
        x = int(x)

        # 将时间字符串转换为 datetime 对象
        time_obj = datetime.datetime.strptime(f'{date_str} {time_str}', "%Y-%m-%d %H:%M:%S")

        # 计算从纪元时间到给定时间的分钟数
        epoch_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
        total_minutes = int((time_obj - epoch_time).total_seconds() / 60)

        # 计算最近一次闹铃时间的分钟数
        nearest_alarm_minutes = (total_minutes // x) * x

        # 将分钟数转换为 datetime 对象
        nearest_alarm_time = epoch_time + datetime.timedelta(minutes=nearest_alarm_minutes)

        # 将 datetime 对象转换为时间字符串
        nearest_alarm_time_str = nearest_alarm_time.strftime("%Y-%m-%d %H:%M:%S")
        print(nearest_alarm_time_str)

solve()