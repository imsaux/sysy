# -*- coding:utf-8 -*-

class sy_date():
    @staticmethod
    def datetime_format(date=None, mode=1):
        """
        获取特定格式的日期时间字符串
        """
        import datetime
        if date is None:
            date = datetime.datetime.now()
        if mode == 1:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日'
        elif mode == 2:
            return date.strftime('%Y%m%d%H%M%S')
        elif mode == 3:
            return date.strftime('%m/%d/%Y')
        elif mode == 4:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日 ' + str(date.hour).zfill(
                2) + ':' + str(date.minute).zfill(2) + ':' + str(date.second).zfill(2)
        elif mode == 5:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return date

