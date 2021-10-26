# 2021_taobao_1111_autoscript
2021淘宝双11 自动获取猫糖

使用adb与uiautomator2实现，须连接电脑使用，虽然使用方法不是非常优雅，但理论上淘宝难以检测

根据uiautomator2文档中quick start安装后，打开活动页面，运行此脚本即可

脚本中默认通过有线的方式连接手机，如果有需要可以参照uiautomator2文档，修改代码使用WiFi连接

当然如果不担心被淘宝检测，本人推荐使用 https://github.com/MonsterNone/tmall-miao
此方法基于无障碍服务，无需电脑连接，但据说淘宝会扫描开启的无障碍服务的包名，可能被检测到
