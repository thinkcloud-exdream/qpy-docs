
# 无线通信模块简介

QuecPython 是运行在无线通信模块上的开发框架。对于首次接触物联网开发的用户而言，无线通信模块可能是一个相对陌生的概念。本文主要针对模块的概念、特性和开发方式进行简要的介绍。

对于首次接触物联网开发的初学者，建议展开阅读下面关于无线通信和蜂窝网络的简介。

.. details:: 关于通信
    :open: false

    在 [前文](./iot-and-low-code.md) 中，我们介绍了物联网的四层结构。其中的网络层承担着设备接入和数据传输的重要功能。由于物联网设备数量较多，分布的空间范围极大，采用有线以太网方式接入网络显然无法满足需要。因此，大部分物联网设备都具备了无线通信的功能，即通过无线电波作为载体进行信号传输。当前，常用的物联网无线通信方式包括 Wi-Fi、蓝牙等十余种，不同方式的通信速率和通信距离存在显著差异。

    物联网无线通信的种类繁多，面向场景多样，因此在具体的功能结构和技术细节上存在较大的差异，但他们的基本流程和模式是类似的。为了便于理解，我们不妨使用人和人之间的通信进行类比。

    设想这样一个场景，在没有现代电子科技的情况下，位于两座相邻的山顶上的两人如何实现互相通信？

    <center>
        <img src="../media/background/wireless-modules/two-hills.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:30%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            两座孤单的山头
        </div>
    </center>

    显然，互相喊叫是最容易想到的答案。但当两人的距离远到一定程度时，靠声音传播信息显然已不太可行，通过视觉信号进行交流是更好的方式。因此，两人可以使用彩色旗帜或火把传递信息。不过，这一方法还有一个前提：双方都需要建立一种共识，了解并遵守不同的旗帜或者火光所代表的含义。这样，两人就可以在相距较远的山头实现低效但相对可靠的通信了。

    <center>
        <img src="../media/background/wireless-modules/help-signal-shown-flag.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:60%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            使用旗语传递求救信号
        </div>
    </center>

    与这个简陋的双人通信流程一样，现代通信同样包含类似的环节。有过使用电话线进行拨号上网经历的用户对于“猫”（Modem，调制解调器）应该不会感到陌生。电话线及电话网络是被设计成用于传输 300 Hz 到 3400 Hz 的模拟音频信号的，并不适合直接传输网络数据。要使得计算机之间可以通过电话线实现双向通信，需要满足两个基本条件：

    - 通过操作系统和网卡，实现用户原始数据与可在网络设备间互相传输和辨识的标准数据形式之间的相互转换。
    - 通过“猫”，实现数字信号与可通过电话线传输的模拟信号之间的相互转换。

    对于前者，这种通过规范化数据格式，使之符合某一标准或共识，从而提升信息传输效率和系统有效性的方法通常称为编码（Coding），在接收端则称为解码（Decoding）。对于后者，这种通过对原始信号进行各种转换，使之能借助不同的通信介质（或载体）进行传播的方法通常称为调制（Modulation），在接收端则称之为解调（Demodulation）。

    无线通信同样包含类似的环节。只不过与有线通信相比，其中的步骤更多、细节更为复杂。当然，作为用户和普通开发者，我们无需了解太多细节，各类无线终端设备和模块已经帮助我们处理好了一切。我们需要关注的，只是具体通信方式的选择和使用方法。

    <center>
        <img src="../media/background/wireless-modules/wireless-communication-route.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:50%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            无线通信系统简略框图
        </div>
    </center>

    > 需要注意的是，为降低入门难度，本节的讲解并不全面和严谨。对于无线通信原理以及各类物联网无线通信方式的具体内容，本文不做系统介绍。有兴趣的读者可以自行参考《通信原理》《无线通信原理与应用》《物联网》等教材进行自学。

.. details:: 关于蜂窝网络
    :open: false

    蜂窝网络（Cellular Network，又称移动网络 Mobile Network）是构成现代移动电话和个人通信系统的基础无线通信技术架构之一。蜂窝通信的概念在上世纪 70 年代由贝尔实验室提出，最初是为了移动语音电话业务开发的。它将移动电话的服务区域根据地形和无线接收特性分为一个个小区（Cell），在每个小区内设一套基站系统。在传统理论中，这些小区被设计为六边形、圆形或正方形，以六边形最为常见。小区之间彼此连接，实现区域的完整覆盖，形如蜂巢，这也是该项技术被译为蜂窝网络的原因。如今，在实际场景中，很多基站的覆盖区域已经不再是蜂窝形状，但这个称谓依旧流传了下来。

    <center>
        <img src="../media/background/wireless-modules/cellular-network-architecture.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:40%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            5G 毫米波蜂窝网络结构示意图
        </div>
    </center>

    如上图所示，与传统的通信方式相比，采用蜂窝通信方式的移动设备间不再通过无线信号直接相连，而是经由基站完成。这种方式在显著缩短通信距离和提升通信速率的同时，也减小了移动设备的体积和功耗。从诞生起，蜂窝网络和相关技术就一直在为无线通信注入革命性的推动和创新力量。

    <center>
        <img src="../media/background/wireless-modules/5g-evolution.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:35%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            从 1G 到 5G 的演进
        </div>
    </center>

    蜂窝移动通信技术发展到今天已经经历了五代，每一代都对应着不同的技术和标准，为用户提供了更高的数据传输速度，更好的语音通话质量，以及一系列新特性和新功能。从 1G 的模拟语音通信，到 5G 的全场景互联，蜂窝网络为已经成为现代社会运转的必不可少的信息基础设施之一。与其他无线通信方式相比，蜂窝通信依托电信运营商的已有网络，无需手动在应用现场进行网络部署，显著降低了联网的难度和工作量。在农业、环保、安防等物联网应用领域，蜂窝网络已成为首选的无线通信方式之一。

## 初识模块

无线通信模块，简称模块（Module，亦称模组或单元），是实现数据上云和远程通信的必不可少的组件，在各类物联网场景中已经得到了极为广泛的应用。从功能上看，它是在本地设备和网络之间构建连接的桥梁。像电脑插上 USB 网卡就可以开始上网一样，在嵌入式系统中加入了模块，系统就具有了连接无线网络的可能性。

<center>
    <img src="../media/background/wireless-modules/device-with-ec20.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:10%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        搭载移远 EC20 模块的某物联网产品主板
    </div>
</center>

很多初次接触模块的用户会对模块这样一个被金属壳笼罩着的奇怪器件感到陌生，它与传统的芯片和分立器件存在很大的不同。实际上，模块的本质就是一种小型的 PCBA（Printed Circuit Board Assembly，组装电路板）。当我们去掉模块表面的金属屏蔽罩，其内部依旧是熟悉（但更为密集）的 PCB 电路结构。

<center>
    <img src="../media/background/wireless-modules/ec20-naked-top.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:20%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        某 4G 模块的内部图像
    </div>
</center>

有过嵌入式系统开发经验的用户对于“核心板”或者 SoM（System on Module）应该不会陌生。模块同样可理解为一种将无线通信所需的各类器件集成在一起，用于完成本地电路与云端服务的通信功能的高密度、小体积、带屏蔽罩的“核心板”。在本文开头的关于通信的介绍中，我们讲到了编码 / 解码和调制 / 解调的概念。在无线通信，尤其是蜂窝通信中，这些步骤往往会演变和拓展得极为复杂。模块的作用即是帮助我们完成这些复杂的步骤，实现简单高效的通信。

模块的内部结构较为复杂。如下图所示，可以看到包含主芯片（高通 MDM9607）、存储器、电源管理芯片、功率放大器、射频前端等多种集成器件，以及大量密集分布的小尺寸封装的电阻、电容等元件。显然，模块的复杂度和精密度是远超传统电路板的。

<center>
    <img src="../media/background/wireless-modules/ec20-inner-components.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:20%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        EC20 Mini PCIe 模块的元件组成
    </div>
</center>

主芯片（Main Chip），部分厂家称之为基带（Baseband）芯片或调制解调器（Modem）芯片，是整个模块的核心。它的角色、功能和特性与手机中的 SoC（System on Chip，片上系统）十分相似。随着技术的发展和芯片制造工艺的提升，在现代模块中，主芯片通常已经集成了应用处理器（Application Processor，AP）、基带和射频的相关功能，运行着完备的操作系统（RTOS 或 Linux），对外提供包括 GPIO、USB 等在内的各种接口，并能够根据需求完成各类通信操作。从这个意义上看，模块既像一台没有屏幕和电池的手机，又像一种功能较为复杂的单片机。

<center>
    <img src="../media/background/wireless-modules/qcx216-diagram.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:40%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        高通最新的 QCX216 4G Modem 芯片功能框图
    </div>
</center>

## 模块的应用模式

对于同一台 Android 手机，不同人有不同的用法。一些用户会安分地使用出厂自带的系统和功能，另一些则热衷于解锁、刷机、root 等操作，更进一步地去开发和挖掘设备的潜力。和手机类似，模块也有这样的两类应用模式：标准模式和二次开发模式。

### 标准模式

和普通手机一样，模块在出厂时通常都会内置操作系统和应用程序。对于许多用户来说，直接使用模块出厂预置功能就可以满足大部分的网络通信需求。这种无需对模块进行开发和调整，直接作为成品功能单元进行使用的方式称为标准模式或传统模式，是当前应用最普遍的模块使用方式。

<center>
    <img src="../media/background/wireless-modules/standard-mode-module.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:100%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        标准模式示意图
    </div>
</center>

如上图所示，在标准模式中，模块与主控（MCU，如 STM32）之间通过 UART 或 USB 接口相连接，基于 AT 指令进行双向交互。不难看出，MCU 是整套系统的核心，通信模块是作为 MCU 的一个独立的功能外设的角色而存在的。系统的主要业务逻辑（用户应用，App）在 MCU 中运行，其他外设（图中的 External Devices）通过 UART、I2C 等接口与 MCU 相连，受 MCU 控制。

.. details:: 关于 AT 指令
    :open: false

    AT 指令是目前业界历史最悠久，使用领域最广泛的通讯指令集之一。它构建起了一套用户和模块间的完备的双向通信机制：用户（或 MCU）通过向模块发送 AT 指令，控制模块执行包括联网、通话、定位等在内的各类功能，模块则将执行结果和状态返回给用户。这种“一发一收”的机制和相对单一的处理方式非常适合在资源有限的嵌入式环境中使用。如今，市面上的绝大多数模块在出厂时都内置了 AT Server 程序，可以接收、解析和执行特定的 AT 指令。

    <center>
        <img src="../media/background/wireless-modules/at-command-architecture.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:50%;">
        <br>
        <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
            AT 指令的运行模式
        </div>
    </center>

对于开发者而言，在基于标准模式使用模块时，主要的开发工作量在于主控中运行的用户 App。其业务代码中需要包含较为复杂的 AT 指令发送和返回值解析功能，例如对 URC（Unsolicited Result Code，非请求结果码）的处理等，因而对于初学者难度较大。

除了 AT 指令功能，模块在标准模式下还可以作为无线网卡，为主控或其他上位机提供包括 PPP 拨号上网在内的一系列网络服务，此处不做赘述。

### 二次开发模式

在前文中我们曾提到，模块就像是功能较为复杂的单片机。事实上，模块所搭载的主芯片为了满足无线通信的需要，通常具有较高的性能和较多的资源，同时也配备了包括 GPIO、ADC、I2C 等在内的丰富的外设接口，只不过在标准模式下，这些资源对于用户通常不是直接可用的。如果能够“解锁”这一限制，模块的应用潜力将极大提升，这就需要对模块进行二次开发。

二次开发的本意是在软件本身提供的一些基本功能和接口的基础上，进行组合和扩展，开发出新的功能来满足用户的特殊需求。具体到模块开发上，二次开发模式允许开发者在底层操作系统的基础上调用 API 编写并运行自己的应用，充分调用模块的各种资源，实现更多的可能性。

<center>
    <img src="../media/background/wireless-modules/open-mode-module.png" style="border-radius: 0.3125em; box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08); zoom:100%;">
    <br>
    <div style="color: orange; border-bottom: 1px solid #d9d9d9; display: inline-block; color: #999; padding: 2px;">
        二次开发模式示意图
    </div>
</center>

二次开发最重要的意义在于使模块在一定程度上具备了取代标准模式中的主控的能力，因而这种模式又被称为 OpenCPU 或 OpenMCU（不同厂家可能有不同的专门称呼，如移远称之为 QuecOpen）。如上图所示，与标准模式相比，OpenCPU 模式由于将模块本身作为主控使用，用户应用（App）直接置于模块内部运行，外设（图中的 External Devices）与模块直接相连，整个系统中无需外部处理器（MCU）或只需简单的外部芯片（图中的 Simple Microchip），因而可以有效地达到精简硬件设计、降低器件成本、缩小产品尺寸的目的。在单片机价格居高不下的当下，OpenCPU 方案受到了众多公司的青睐。

但是，OpenCPU 方案也具有较为明显的局限性。由于这一模式通常需要用户直接在模块底层运行的操作系统的基础上进行开发，技术门槛较高，传统的、不具备系统级开发经验的单片机开发者很难适应。其次，由于 OpenCPU 技术支持难度大，模块厂家通常只向大客户提供相关的工具和资料，入门较为不便。最后，不同厂家、不同型号的模块，其 OpenCPU 开发环境和开发工具存在较大差别，用户编写的程序在不同模块间的移植存在一定的难度。

### 使用脚本语言开发模块

传统的 OpenCPU 开发通常使用 C 语言，因此也被称作 CSDK 开发。用户需要直接修改和控制底层的操作系统，具有较高的难度和一定的风险性。在 [前文](./iot-and-low-code.md) 中，我们介绍了低代码开发方式和它在物联网领域的应用。目前，已经有部分模块厂商通过在 CSDK 的基础上移植解释器 / 虚拟机的方式，使得用户可以使用 Lua、Python 等脚本语言对模块进行二次开发。

与 C 语言相比，脚本语言在语法和使用方式上普遍较为简单，开发者无需花费太多时间和精力即可掌握，并可相对轻松地实现业务逻辑，便于项目的快速开发和功能迭代。同时，对于低代码开发方式而言，开发者通常无需考虑内存回收、基础任务调度等底层细节，显著降低了模块二次开发的技术门槛。最后，对于不同型号的模块，只要它们运行的是同一种脚本语言解释器，用户编写的程序通常只需少量修改（甚至无需修改）即可完成移植。

如下的示例分别是在 EC100Y-CN 模块上使用 C 语言和 Python 语言实现 LED 闪灯的代码。可以看出，脚本语言更加简单直观，易于编写、便于理解。

.. tabset:: LED 闪灯代码

    ## 使用 QuecOpen（CSDK）
    
    ```c
    #include "ql_application.h"
    #include "ql_gpio.h"
    #include <stdio.h>

    static quec_gpio_cfg_t led_gpio_cfg[] = 
    {
        {GPIO_PIN_NO_75, PIN_DIRECTION_OUT, PIN_NO_EDGE, PIN_PULL_DISABLE, PIN_LEVEL_LOW}
    };

    static void led_test(void *argv)
    {
        ql_gpio_init(led_gpio_cfg[0].gpio_pin_num, led_gpio_cfg[0].pin_dir, led_gpio_cfg[0].pin_pull, led_gpio_cfg[0].pin_level);

        while (1)
        {
            ql_gpio_set_level(led_gpio_cfg[0].gpio_pin_num, PIN_LEVEL_LOW);
            ql_rtos_task_sleep_s(1);
            ql_gpio_set_level(led_gpio_cfg[0].gpio_pin_num, PIN_LEVEL_HIGH);
            ql_rtos_task_sleep_s(1);
        }
    }

    application_init(led_test, "led_test", 2, 2);
    ```
    
    ## 使用 QuecPython
    
    ```python
    from machine import Pin
    import utime as time

    led = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 0)

    def led_test():
        while 1:
            led.write(0)
            time.sleep(1)
            led.write(1)
            time.sleep(1)

    if __name__ == "__main__":
        led_test()
    ```

当然，由于使用脚本语言开发时屏蔽了很多底层细节，因而在灵活性和可控性上不如传统的 C 语言开发。此外，脚本语言与 C 语言相比，本身性能相对较差、执行速度较慢，因而在部分对于性能和实时性要求较高的场景下不适合使用。

## 选择合适的开发方式

下表比较了标准模式，CSDK 二次开发和脚本二次开发在多个维度的差异。用户可根据实际需求选择最适合自己的开发方式。

|   特性   | 标准模式 | 二次开发（CSDK） | 二次开发（脚本语言） | 备注                                                         |
| :------: | :------: | :--------------: | :------------------: | :----------------------------------------------------------- |
| 物料成本 |    ⭐⭐    |        ⭐         |          ⭐           | <ul><li>二次开发时，可将模块作为系统主控使用，节省单片机部分的成本。</li></ul> |
| 上手门槛 |    ⭐     |       ⭐⭐⭐        |          ⭐           | <ul><li>模块厂商通常只面向大客户提供 CSDK 开发技术支持和其他相关服务。</li></ul> |
| 开发难度 |    ⭐     |       ⭐⭐⭐        |          ⭐           | <ul><li>CSDK 开发需要开发者拥有 RTOS 或 Linux 开发经验，普通单片机开发者很难快速掌握。</li><li>标准模式仅需用户掌握单片机串口通信和字符串处理方法，无特殊要求。</li><li> 脚本语言开发方式仅需用户掌握基础语法，无特殊要求。</li></ul> |
| 开发周期 |    ⭐     |       ⭐⭐⭐        |          ⭐           | <ul><li>CSDK 开发的复杂度决定了其较长的开发周期和较高的开发成本。</li></ul> |
| 维护成本 |    ⭐⭐    |       ⭐⭐⭐        |          ⭐           | <ul><li>脚本语言的模块化开发的特性有助于保证其长期运行的稳定性，同时普遍内置了 OTA 功能，便于执行远程升级。</li></ul> |
|  灵活性  |    ⭐     |       ⭐⭐⭐        |          ⭐⭐          | <ul><li>标准模式下，开发者通常只能调用串口、ADC 等有限的功能。</li><li> 使用脚本语言开发时，开发者可以通过内置的功能库调用大部分的模块资源。</li><li> 使用 CSDK 开发时，开发者可以根据自身需求和想法直接控制所有可用资源。</li></ul> |
|   性能   |    -     |       ⭐⭐⭐        |          ⭐⭐          | <ul><li>脚本语言的性能远低于 C 语言，因此在对于运行速度、时间精度（时序）、资源数量等要求较高的少部分场合，不建议采用脚本语言开发。</li></ul> |
|   功耗   |    ⭐     |        ⭐⭐        |          ⭐⭐          | <ul><li>一般的 4G 模块在自主休眠时的功耗水平在 mA 级别。</li><li> 在标准模式下，可以通过使用系统主控切断模块供电的方式实现最大限度的省电，最低功耗可达前者的 1/10。</li></ul> |
| 生态系统 |   ⭐⭐⭐    |        ⭐         |         ⭐⭐⭐          | <ul><li>标准 AT 指令开发和脚本开发在网络上都具有较多的公开资料和教程。</li><li> CSDK 开发通常不具备开放生态。</li></ul> |
