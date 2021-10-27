import time
import uiautomator2 as u2

d = u2.connect()

# d = u2.connect_adb_wifi("192.168.31.215:38303")
hasTask = True

def waitLoading(sec=2):
    # print(f'等待 {sec}s')
    time.sleep(sec)

def closeFloatWindow():
    while d(text="关闭").exists:
        print(f'正在关闭悬浮窗口',end='')
        d(text="关闭").click()
        print(f' 任务完成')
        waitLoading()

def returnToTaskList():
    closeFloatWindow()
    print(f'返回任务列表')
    d.press("back")
    waitLoading()

def getTaskList():
    taskButton = d.xpath('//android.widget.ListView/android.view.View').child("/android.widget.Button").all()
    taskTitle = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[1]").all()
    taskDetail = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[2]").child("/android.view.View[1]").all()
    taskReward = d.xpath('//android.widget.ListView/android.view.View').child("/android.view.View").child("/android.view.View[2]").child("/android.view.View[2]").all()

    taskList = []
    for i in range(len(d.xpath('//android.widget.ListView/android.view.View').all())):
        taskList.append({'taskButton':taskButton[i],'taskTitle':taskTitle[i],'taskDetail':taskDetail[i],'taskReward':taskReward[i]})

    return taskList

def waitDoingTask(timeout=60,timestep=5):
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

def matchText(keywordList,targetList):
    for m in targetList:
        for n in keywordList:
            if n in m:
                return True

if __name__ == '__main__':
    closeFloatWindow()

    d(text="赚糖领红包").click()
    waitLoading()

    #自动签到
    while d(text="完成签到").exists:
        print(f'开始签到',end='')
        d(text="完成签到").click()
        waitLoading()
        print(f' 任务完成')

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
                print(f'开始做 {titleText} (奖励: 喵糖{rewardText})',end='')
                task['taskButton'].click()
                waitLoading()
                d.xpath('//*[@resource-id="module-container"]/android.view.View[1]/android.view.View[1]/android.view.View[1]').click_exists() #天天领现金
                # d(textMatches=".*((任务已完成)|(喵糖已发放)|(明天再来吧)).*").exists(timeout=60)
                waitDoingTask()
                print(' 任务完成')
                returnToTaskList()
            if matchText(['互动'],[titleText,detailText]):
                hasTask = True
                print(f'开始做 {titleText} (奖励: 喵糖{rewardText})',end='')
                task['taskButton'].click()
                waitLoading(sec=5)
                h = 0.6
                while h <= 0.8:
                    d.click(0.5, h)
                    h += 0.02
                    time.sleep(0.75)

                waitDoingTask()
                print(' 任务完成')
                returnToTaskList()

    #自动领取红包
    while d(text="立即领取").exists:
        print(f'领取红包',end='')
        d(text="立即领取").click()
        waitLoading()
        d.xpath('//*[@text="恭喜获得"]/android.widget.Button[1]').click()
        print(f' 任务完成')
        waitLoading()

    closeFloatWindow()

    # 自动扔骰子
    num = int(d(textContains='22点清空').info['text'].split('，')[1])
    while num > 0:
        print('投掷骰子x1')
        d(textContains='22点清空').click()
        time.sleep(10)
        num = int(d(textContains='22点清空').info['text'].split('，')[1])
