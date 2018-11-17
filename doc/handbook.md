# CCAT Handbook


## Binance API Rate Limit
At the current time Binance rate limits are:
- 1200 requests per minute
- 10 orders per second
- 100,000 orders per 24hrs

# Exception Tables
# exceptions, code, message, detail
# okexException, code=-1001, message = exceptions throwed related to okex exchange
# binanceException, code=-1002, message = exceptions throwed related to binance exchange
# huobiException, code=-1003, message = exceptions throwed related to huobi exchange
# gateException, code=-1004, message = exceptions throwed related to gate exchange


#测试
if __name__ == '__main__':
    import time
    EVENT_ARTICAL = "Event_Artical"

    # 事件源 公众号
    class PublicAccounts:
        def __init__(self, eventManager):
            self.__eventManager = eventManager

        def writeNewArtical(self):
            # 事件对象，写了新文章
            event = Event(EVENT_ARTICAL)
            event.dict["artical"] = u'如何写出更优雅的代码\n'
            # 发送事件
            self.__eventManager.sendEvent(event)
            print(u'公众号发送新文章\n')


    # 监听器 订阅者
    class ListenerTypeOne:
        def __init__(self, username):
            self.__username = username

        # 监听器的处理函数 读文章
        def ReadArtical(self, event):
            print(u'%s 收到新文章' % self.__username)
            print(u'%s 正在阅读新文章内容：%s' % (self.__username, event.dict["artical"]))


    class ListenerTypeTwo:
        def __init__(self, username):
            self.__username = username

        # 监听器的处理函数 读文章
        def ReadArtical(self, event):
            print(u'%s 收到新文章 睡3秒再看' % self.__username)
            time.sleep(3)
            print(u'%s 正在阅读新文章内容：%s' % (self.__username, event.dict["artical"]))


    def test():
        listner1 = ListenerTypeOne("thinkroom")  # 订阅者1
        listner2 = ListenerTypeTwo("steve")  # 订阅者2

        ee = EventEngine()

        # 绑定事件和监听器响应函数(新文章)
        ee.register(EVENT_ARTICAL, listner1.ReadArtical)
        ee.register(EVENT_ARTICAL, listner2.ReadArtical)
        for i in range(0, 20):
            listner3 = ListenerTypeOne("Jimmy")  # 订阅者X
            ee.register(EVENT_ARTICAL, listner3.ReadArtical)

        ee.start()

        #发送事件
        publicAcc = PublicAccounts(ee)
        publicAcc.writeNewArtical()

    test()
