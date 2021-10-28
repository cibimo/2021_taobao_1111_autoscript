import time
import uiautomator2 as u2
import logging

d = u2.connect()
# d = u2.connect_adb_wifi("192.168.31.215:38303")

hasTask = True

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def waitLoading(sec=4): #等待页面加载
    time.sleep(sec)

def returnToTaskList(back=True): #返回任务列表
    logging.info(f'正在返回任务列表')
    if back:
        d.press("back")
        waitLoading(2)
    d.click(0.5, 0.98)
    waitLoading(2)

def isTaskFinish():
    if d(textContains='任务已完成').exists or d(descriptionContains='任务已完成').exists: #大多数情况
        return True

def waitDoingTask(timeout=60,timestep=5): #等待任务完成
    timetotal = 0
    while 1:
        time.sleep(timestep)
        timetotal += timestep
        if timetotal >= timeout:
            return
        if isTaskFinish():
            return

def viewItem(x,y,sec=5):
    logging.info(f'正在浏览物品 ({x}, {y})')
    d.click(x,y)
    time.sleep(sec)
    d.press("back")
    waitLoading(1)



if __name__ == '__main__':
    if not d(text="主会场").exists:
        logging.info('正在进入活动页面')
        d.open_url("taobao://m.tb.cn/h.ffKfhIt")
        waitLoading(10)

    if not d(text="去浏览").exists:
        returnToTaskList(False)

    # 打开任务列表
    while d(text="去浏览").exists:
        logging.info('开始进行浏览')
        d(text="去浏览").click()
        waitLoading(5)

        if d(textContains='浏览商品').exists:
            for y in [0.3, 0.6, 0.9]:
                for x in [0.25, 0.75]:
                    viewItem(x, y)
                    if isTaskFinish():
                        break
                else:
                    continue
                break

            returnToTaskList(True)

        elif d(textContains='浏览店铺').exists:
            for y in [0.4, 0.6, 0.8]:
                for x in [0.2, 0.5, 0.8]:
                    viewItem(x, y)
                    if isTaskFinish():
                        break
                else:
                    continue
                break

            returnToTaskList(True)

        else: # d(textContains='下滑浏览').exists: #有时无法识别出“下滑”
            d.swipe_ext(u2.Direction.FORWARD)
            waitDoingTask()
            returnToTaskList(False)
