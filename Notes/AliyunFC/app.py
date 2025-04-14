import calendar
from flask import Flask, request
from tabulate import tabulate
import logging
import json

logger = logging.getLogger()
app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_month_calendar():
    # 获取请求ID并打印日志
    requestId = request.headers.get('x-fc-request-id', '')
    logger.info("FC Invoke Start RequestId: " + requestId)
    # 获取请求内容并检查请求格式
    data = json.loads(request.stream.read().decode('utf-8'))
    if not ('year' in data and 'month' in data):
        message = "Request must be in format like {'year': '1999', 'month': '12'}"
        return message

    # 获取日历表格
    result = print_calendar(year=int(data['year']), month=int(data['month']))
    # 返回前打印函数执行完成的日志
    logger.info("FC Invoke End RequestId: " + requestId)
    return result


def print_calendar(year, month):
    # 获取指定年份和月份的日历矩阵
    cal = calendar.monthcalendar(year, month)
    # 将不属于该月的日期从0转为空字符
    cal = list(map(lambda sublist: list(map(lambda x: '' if x == 0 else x, sublist)), cal))
    # 创建表头
    headers = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    # 使用tabulate打印日历表格
    return tabulate(cal, headers=headers, tablefmt="grid", stralign='center', numalign='center')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
