# 中山大学教务系统自动化脚本

因为实在看不惯教务系统的迟迟不升级，都2017年了还只能使用IE进行访问。因此，便有了做这么一个小项目的念头。目前完成了基本的登陆和评教功能，以后有时间将会不定期更新其他功能。

个人水平有限，希望能有大神加入指出我还做得不足的地方，并完善我们的脚本 :)

第三方库：requests, lxml, demjson

## 各模块功能

### base

提供一个 session ，并提供 login 方法调用，建议每个子功能类都继承 base 类进行操作。

### ping-jiao

实现评教功能，代码来源于大神 @linjinjin123(https://github.com/linjinjin123) 的一个一键评教脚本，但是因为现在已经不能用了，所以个人作了一些微小的改动。

> usage: python ping-jiao.py

### 其他

正在开发中.... 希望能有小伙伴可以帮忙一起完成其他新的功能 (体育选课、查询课表、四六级等等) ^-^

