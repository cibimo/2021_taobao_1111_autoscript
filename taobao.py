import time
import uiautomator2 as u2
import logging

d = u2.connect()
# d = u2.connect_adb_wifi("192.168.31.215:38303")

hasTask = True

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def waitLoading(sec=2): #等待页面加载
    time.sleep(sec)

def closeFloatWindow(): #关闭悬浮窗口
    while d(text="关闭").exists:
        logging.info(f'正在关闭悬浮窗口')
        d(text="关闭").click()
        waitLoading()

def returnToTaskList(): #返回任务列表
    closeFloatWindow()
    logging.info(f'正在返回任务列表')
    d.press("back")
    waitLoading()

def getTaskList(): #获取任务列表
    taskButton = d.xpath('//android.widget.ListView/android.view.View').child("/android.widget.Button").all()
    taskTitle = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[1]").all()
    taskDetail = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[2]").child("/android.view.View[1]").all()
    taskReward = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[2]").child("/android.view.View[2]").all()

    taskList = []
    for i in range(len(d.xpath('//android.widget.ListView/android.view.View').all())):
        taskList.append({'taskButton':taskButton[i],'taskTitle':taskTitle[i],'taskDetail':taskDetail[i],'taskReward':taskReward[i]})

    return taskList

def waitDoingTask(timeout=60,timestep=5): #等待任务完成
    timetotal = 0
    while 1:
        time.sleep(timestep)
        timetotal += timestep
        if timetotal >= timeout:
            return
        if d(textContains='喵糖已发放').exists or d(descriptionContains='喵糖已发放').exists: #大多数情况
            return
        if d.xpath('//*[@resource-id="com.taobao.taobao:id/interactive_right_component_recycler"]/android.widget.FrameLayout[2]').exists: #直播
            if '喵糖已发放' in d.xpath('//*[@resource-id="com.taobao.taobao:id/interactive_right_component_recycler"]/android.widget.FrameLayout[2]').child("android.widget.TextView").text:
                return

def matchText(keywordList,targetList): #匹配关键字
    for m in targetList:
        for n in keywordList:
            if n in m:
                return True

def getMT(): #活动页面获取喵糖数量
    return int(d(textContains='22点清空').info['text'].split('，')[1])

if __name__ == '__main__':
    closeFloatWindow()

    # 检测是否位于活动页面
    print('正在进入淘宝活动页面（如需做支付宝任务请提前进入）')
    if not d(text="赚糖领红包").exists:
        d.open_url("taobao://pages.tmall.com/wow/z/hdwk/20211111/pk20211111")
        time.sleep(10)
        closeFloatWindow()

    # 打开任务列表
    d(text="赚糖领红包").click()
    waitLoading()

    #自动签到
    while d(text="完成签到").exists:
        logging.info(f'正在签到')
        d(text="完成签到").click()
        waitLoading()

    #自动做任务
    while hasTask:
        hasTask = False
        taskList = getTaskList()
        for task in taskList:
            buttonText = task['taskButton'].info['text']
            titleText = task['taskTitle'].info['text']
            detailText = task['taskDetail'].info['text']
            rewardText = task['taskReward'].info['text']

            if buttonText == '已完成':
                continue

            if matchText(['逛逛','浏览'],[buttonText]) or matchText(['逛逛','浏览','15秒'],[titleText,detailText]):
                hasTask = True
                logging.info(f'开始做 {titleText} (奖励: 喵糖{rewardText})')
                task['taskButton'].click()
                waitLoading()
                d.xpath('//*[@resource-id="module-container"]/android.view.View[1]/android.view.View[1]/android.view.View[1]').click_exists() #天天领现金
                # d(textMatches=".*((任务已完成)|(喵糖已发放)|(明天再来吧)).*").exists(timeout=60)
                waitDoingTask()
                returnToTaskList()

            if matchText(['互动'],[titleText,detailText]):
                hasTask = True
                logging.info(f'开始做 {titleText} (奖励: 喵糖{rewardText})')
                task['taskButton'].click()
                waitLoading(sec=5)
                h = 0.6
                while h <= 0.8: #进行一些点击，能完成一些互动
                    d.click(0.5, h)
                    h += 0.02
                    time.sleep(0.75)
                waitDoingTask()
                returnToTaskList()

    #自动领取红包
    while d(text="立即领取").exists:
        logging.info(f'领取红包')
        d(text="立即领取").click()
        waitLoading()
        d.xpath('//*[@text="恭喜获得"]/android.widget.Button[1]').click()
        waitLoading()

    closeFloatWindow()

    # 自动扔骰子
    num = getMT()
    while num > 0:
        logging.info('投掷骰子x1')
        d(textContains='22点清空').click()
        time.sleep(10)
        num = getMT()

    # 领取红包
    logging.warning('任务已完成，请记得手动领取红包')
    d.open_url("taobao://m.tb.cn/h.ffKfhIt")
