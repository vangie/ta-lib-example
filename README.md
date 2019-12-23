# 移植 Python 量化交易 TA-Lib 库到函数计算

[TA-Lib](https://github.com/mrjbq7/ta-lib)，全称“Technical Analysis Library”, 即技术分析库，是 Python 金融量化的高级库，涵盖了150 多种股票、期货交易软件中常用的技术分析指标，如 MACD、RSI、KDJ、动量指标、布林带等等。

TA-Lib 可分为 10 个子板块：

- Overlap Studies(重叠指标)
- Momentum Indicators(动量指标)
- Volume Indicators(交易量指标)
- Cycle Indicators(周期指标)
- Price Transform(价格变换)
- Volatility Indicators(波动率指标)
- Pattern Recognition(模式识别)
- Statistic Functions(统计函数)
- Math Transform(数学变换)
- Math Operators(数学运算)

![](https://img.alicdn.com/tfs/TB1pFE6rAL0gK0jSZFAXXcA9pXa-553-183.png)
![](https://data-analysis.cn-shanghai.log.aliyuncs.com/logstores/article-logs/track_ua.gif?APIVersion=0.6.0&title=%E7%A7%BB%E6%A4%8D%20Python%20%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93%20TA-Lib%20%E5%BA%93%E5%88%B0%E5%87%BD%E6%95%B0%E8%AE%A1%E7%AE%97&author=%E5%80%9A%E8%B4%A4&src=article)

本文介绍通过 Funcraft 的模板将 Python 量化交易库 TA-lib 移植到[函数计算](https://statistics.functioncompute.com/?title=%E7%A7%BB%E6%A4%8D%20Python%20%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93%20TA-Lib%20%E5%BA%93%E5%88%B0%E5%87%BD%E6%95%B0%E8%AE%A1%E7%AE%97&author=%E5%80%9A%E8%B4%A4&url=http%3A%2F%2Ffc.console.aliyun.com%2F%3Ffctraceid%3DYXV0aG9yJTNEJUU1JTgwJTlBJUU4JUI0JUE0JTI2dGl0bGUlM0QlRTclQTclQkIlRTYlQTQlOEQlMjBQeXRob24lMjAlRTklODclOEYlRTUlOEMlOTYlRTQlQkElQTQlRTYlOTglOTMlMjBUQS1MaWIlMjAlRTUlQkElOTMlRTUlODglQjAlRTUlODclQkQlRTYlOTUlQjAlRTglQUUlQTElRTclQUUlOTc%3D)。

## 依赖工具

本项目是在 MacOS 下开发的，涉及到的工具是平台无关的，对于 Linux 和 Windows 桌面系统应该也同样适用。在开始本例之前请确保如下工具已经正确的安装，更新到最新版本，并进行正确的配置。

* [Docker](https://www.docker.com/)
* [Funcraft](https://github.com/alibaba/funcraft)

对于 MacOS 用户可以使用 [homebrew](https://brew.sh/) 进行安装：

```bash
brew cask install docker
brew tap vangie/formula
brew install fun
```

Windows 和 Linux 用户安装请参考：

<https://github.com/aliyun/fun/blob/master/docs/usage/installation.md>

安装好后，记得先执行 `fun config` 初始化一下配置。

## 初始化

使用 fun init 命令可以快捷地将本模板项目初始化到本地。

```bash
fun init vangie/ta-lib-example
```

## 安装依赖

```bash
$ fun install
using template: template.yml
start installing function dependencies without docker

building ta-lib-example/ta-lib-example
Funfile exist, Fun will use container to build forcely
Step 1/5 : FROM registry.cn-beijing.aliyuncs.com/aliyunfc/runtime-python3.6:build-1.7.7
 ---> 373f5819463b
Step 2/5 : COPY ta-lib-0.4.0-src.tar.gz /tmp
 ---> Using cache
 ---> 64f9f85112b4
Step 3/5 : RUN cd /tmp; tar -xzf ta-lib-0.4.0-src.tar.gz
 ---> Using cache
 ---> 9f2d3f836de9
Step 4/5 : RUN cd /tmp/ta-lib/ ;     ./configure --prefix=/code/.fun/root/usr ;     make ; make install
 ---> Using cache
 ---> 7725836973d4
Step 5/5 : RUN TA_LIBRARY_PATH=/code/.fun/root/usr/lib     TA_INCLUDE_PATH=/code/.fun/root/usr/include     fun-install pip install TA-Lib
 ---> Using cache
 ---> a338e71895b7
sha256:a338e71895b74a0be98278f35da38c48545f04a54e19ec9e689bab976265350b
Successfully built a338e71895b7
Successfully tagged fun-cache-d4ac1d89-5b75-4429-933a-2260e2f7fbec:latest
copying function artifact to /Users/vangie/Workspace/ta-lib-example/{{ projectName }}

Install Success


Tips for next step
======================
* Invoke Event Function: fun local invoke
* Invoke Http Function: fun local start
* Build Http Function: fun build
* Deploy Resources: fun deploy
```

## 本地调用

```bash
$ fun local invoke
using template: template.yml

Missing invokeName argument, Fun will use the first function ta-lib-example/ta-lib-example as invokeName

skip pulling image aliyunfc/runtime-python3.6:1.7.7...
FunctionCompute python3 runtime inited.
FC Invoke Start RequestId: dc1495b2-13ec-4ecf-a2dc-a0026d82651a
FC Invoke End RequestId: dc1495b2-13ec-4ecf-a2dc-a0026d82651a
[
    "HT_DCPERIOD",
    "HT_DCPHASE",
    "HT_PHASOR",
    "HT_SINE",
    "HT_TRENDMODE"
]

RequestId: dc1495b2-13ec-4ecf-a2dc-a0026d82651a          Billed Duration: 350 ms         Memory Size: 1998 MB    Max Memory Used: 34 MB
```

## 部署

```bash
$ fun deploy
using template: template.yml
using region: cn-shanghai
using accountId: ***********4733
using accessKeyId: ***********EUz3
using timeout: 600

Waiting for service ta-lib-example to be deployed...
        Waiting for function ta-lib-example to be deployed...
                Waiting for packaging function ta-lib-example code...
                The function ta-lib-example has been packaged. A total of 39 files files were compressed and the final size was 3.23 MB
        function ta-lib-example deploy success
service ta-lib-example deploy success
```

## 执行

```bash
$ fun invoke
using template: template.yml

Missing invokeName argument, Fun will use the first function ta-lib-example/ta-lib-example as invokeName

========= FC invoke Logs begin =========
FC Invoke Start RequestId: 83e23eba-02b4-4380-bbca-daec6856bf4a
FC Invoke End RequestId: 83e23eba-02b4-4380-bbca-daec6856bf4a

Duration: 213.86 ms, Billed Duration: 300 ms, Memory Size: 128 MB, Max Memory Used: 43.50 MB
========= FC invoke Logs end =========

FC Invoke Result:
[
    "HT_DCPERIOD",
    "HT_DCPHASE",
    "HT_PHASOR",
    "HT_SINE",
    "HT_TRENDMODE"
]
```

## 参考阅读

1. [函数计算](https://statistics.functioncompute.com/?title=%E7%A7%BB%E6%A4%8D%20Python%20%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93%20TA-Lib%20%E5%BA%93%E5%88%B0%E5%87%BD%E6%95%B0%E8%AE%A1%E7%AE%97&author=%E5%80%9A%E8%B4%A4&src=article&url=https%3A%2F%2Fwww.aliyun.com%2Fproduct%2Ffc)
2. [【手把手教你】股市技术分析利器之TA-Lib（一）](https://zhuanlan.zhihu.com/p/57389880)