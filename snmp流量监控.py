from pysnmp.entity.rfc3413.oneliner import cmdgen

import matplotlib
import matplotlib.pyplot as plt

import paramiko
import time


def get_all_rate():
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sshClient.connect(hostname='127.0.0.1', port=22, username='admin', password='123456')
    channel = sshClient.get_transport().open_session()
    channel.get_pty()
    channel.invoke_shell()

    channel.send('en' + '\r\n')
    channel.send('show statistics interface' + '\r\n')
    time.sleep(1)
    channel.send('\r\n')
    channel.send('exit\r\n')
    time.sleep(1)
    output = channel.recv(102400)
    time.sleep(1)

    output = str(output).split('\\r\\n')[10:-5]
    all_rate = 0
    ports = ['ge15', 'ge17', 'ge19', 'ge21']
    data = []
    for i in output:
        rate = i[-9:]
        if i[-1] == "K":
            rate = float(rate.strip("K").strip()) / 1000
            rate = round(rate, 2)
            all_rate += rate
        elif i[-1] == "M":
            rate = float(rate.strip("M").strip())
            all_rate += rate
        else:
            continue

        port_name = i[0:4]
        if port_name == 'ge15' or port_name == 'ge17' or port_name == 'ge19' or port_name == 'ge21':
            print(i)
            port_rate = i[-9:]
            if i[-1] == "K":
                port_rate = float(port_rate.strip("K").strip()) / 1000
                port_rate = round(port_rate, 2)
                data.append(port_rate)
            elif i[-1] == "M":
                port_rate = float(port_rate.strip("M").strip())
                data.append(port_rate)
    all_rate = round(all_rate, 2)
    sshClient.close()
    return all_rate, data


def create_image(port):
    global rates
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure('test', figsize=(12, 10))

    # table_all = fig.add_subplot(8, 1, 1)
    # table_1 = fig.add_subplot(8, 1, 2)
    # table_3 = fig.add_subplot(8, 1, 3)
    # table_5 = fig.add_subplot(8, 1, 4)
    # table_7 = fig.add_subplot(8, 1, 5)
    table_9 = fig.add_subplot(8, 1, 5)

    # table_all.set_ylabel('All_Rate', rotation=0, fontsize=13, labelpad=20)
    # table_1.set_ylabel('binjiang', rotation=0, fontsize=13, labelpad=20)
    # table_3.set_ylabel('huanglong', rotation=0, fontsize=13, labelpad=20)
    # table_5.set_ylabel('anping', rotation=0, fontsize=13, labelpad=20)
    # table_7.set_ylabel('qingshan', rotation=0, fontsize=13, labelpad=20)
    table_9.set_ylabel('favor', rotation=0, fontsize=13, labelpad=20)

    plt.tight_layout()

    line1 = None
    line5 = None
    line9 = None
    line13 = None
    line17 = None
    line_all = None

    obsX = []
    table_1_in_Y = []
    table_3_in_Y = []
    table_5_in_Y = []
    table_7_in_Y = []
    table_9_in_Y = []
    table_all_in_Y = []

    i = 1
    while True:
        # all_rate, data = get_all_rate()
        rate = get_result("127.0.0.1", "admin", "ifInOctet")
        print(rate)
        for j in rate:
            if j[0] == port:
                rates = (float(j[1]) / 1024 / 1024)
                rates = round(rates, 2)
        obsX.append(i)

        # table_all_in_Y.append(int(all_rate))
        # table_1_in_Y.append(data[0])
        # table_3_in_Y.append(data[1])
        # table_5_in_Y.append(data[2])
        # table_7_in_Y.append(data[3])
        table_9_in_Y.append(float(rates))

        # if line_all is None:
        #     line_all = table_all.plot(obsX, table_all_in_Y, '-g', marker='.')[0]
        #
        # if line1 is None:
        #     line1 = table_1.plot(obsX, table_1_in_Y, '-g', marker='.')[0]
        #
        # if line5 is None:
        #     line5 = table_3.plot(obsX, table_3_in_Y, '-g', marker='.')[0]
        #
        # if line9 is None:
        #     line9 = table_5.plot(obsX, table_5_in_Y, '-g', marker='.')[0]
        #
        # if line13 is None:
        #     line13 = table_7.plot(obsX, table_7_in_Y, '-g', marker='.')[0]

        if line17 is None:
            line17 = table_9.plot(obsX, table_9_in_Y, '-g', marker='.')[0]

        # line_all.set_xdata(obsX)
        # line_all.set_ydata(table_all_in_Y)
        #
        # line1.set_xdata(obsX)
        # line1.set_ydata(table_1_in_Y)
        #
        # line5.set_xdata(obsX)
        # line5.set_ydata(table_3_in_Y)
        #
        # line9.set_xdata(obsX)
        # line9.set_ydata(table_5_in_Y)
        #
        # line13.set_xdata(obsX)
        # line13.set_ydata(table_7_in_Y)

        line17.set_xdata(obsX)
        line17.set_ydata(table_9_in_Y)

        if len(obsX) < 100:
            # table_all.set_xlim([min(obsX), max(obsX) + 30])
            # table_1.set_xlim([min(obsX), max(obsX) + 30])
            # table_3.set_xlim([min(obsX), max(obsX) + 30])
            # table_5.set_xlim([min(obsX), max(obsX) + 30])
            # table_7.set_xlim([min(obsX), max(obsX) + 30])
            table_9.set_xlim([min(obsX), max(obsX) + 30])
        else:
            # table_all.set_xlim([obsX[-80], max(obsX) * 1.2])
            # table_1.set_xlim([obsX[-80], max(obsX) * 1.2])
            # table_3.set_xlim([obsX[-80], max(obsX) * 1.2])
            # table_5.set_xlim([obsX[-80], max(obsX) * 1.2])
            # table_7.set_xlim([obsX[-80], max(obsX) * 1.2])
            table_9.set_xlim([obsX[-80], max(obsX) * 1.2])

        # 设置y轴最大最小值
        # table_all_ylim = table_all_in_Y
        # table_1_ylim = table_1_in_Y
        # table_3_ylim = table_3_in_Y
        # table_5_ylim = table_5_in_Y
        # table_7_ylim = table_7_in_Y
        table_9_ylim = table_9_in_Y

        # table_all.set_ylim([min(table_all_ylim), max(table_all_ylim) + 10])
        # table_1.set_ylim([min(table_1_ylim), max(table_1_ylim) + 10])
        # table_3.set_ylim([min(table_3_ylim), max(table_3_ylim) + 10])
        # table_5.set_ylim([min(table_5_ylim), max(table_5_ylim) + 10])
        # table_7.set_ylim([min(table_7_ylim), max(table_7_ylim) + 10])
        table_9.set_ylim([min(table_9_ylim), max(table_9_ylim) + 10])

        plt.pause(1)

        i += 1

        data = []
        time.sleep(1)


# def create_image2():
#     global rates
#     matplotlib.rcParams['axes.unicode_minus'] = False
#     fig = plt.figure('Favor', figsize=(12, 10))
#
#     table_all = fig.add_subplot(8, 1, 1)
#
#     table_all.set_ylabel('Favor_Rate', rotation=0, fontsize=13, labelpad=20)
#
#     plt.tight_layout()
#
#     line_all = None
#
#     obsX = []
#     table_all_in_Y = []
#
#     i = 1
#     # print(speed)
#
#     while True:
#         rate = get_result("127.0.0.1", "admin", "ifInOctet")
#         print(rate)
#         for j in rate:
#             if j[0] == "14":
#                 rates = (int(j[1]) / 1024 / 1024)
#         obsX.append(i)
#
#         table_all_in_Y.append(int(rates))
#
#         if line_all is None:
#             line_all = table_all.plot(obsX, table_all_in_Y, '-g', marker='.')[0]
#
#         line_all.set_xdata(obsX)
#         line_all.set_ydata(table_all_in_Y)
#
#         if len(obsX) < 100:
#             table_all.set_xlim([min(obsX), max(obsX) + 30])
#
#         else:
#             table_all.set_xlim([obsX[-80], max(obsX) * 1.2])
#
#         # 设置y轴最大最小值
#         table_all_ylim = table_all_in_Y
#
#         table_all.set_ylim([min(table_all_ylim), max(table_all_ylim) + 10])
#
#         plt.pause(1)
#
#         i += 1
#
#         data = []
#         time.sleep(0.5)
#

def walk(ip, community, oid: tuple):
    try:
        error_indication, error_status, error_index, generic = cmdgen.CommandGenerator().nextCmd(
            # 社区信息，my-agent ,self.strCommunity表示社区名团体字,1表示snmp v2c版本，0为v1版本
            cmdgen.CommunityData('my-agent', community, mpModel=1),
            # 这是传输的通道，传输到IP self.strSwitchIP, 端口 161上(snmp标准默认161 UDP端口)
            cmdgen.UdpTransportTarget((ip, 161)), oid)
        return generic
    except Exception as e:
        print("请求超时")
        return '0xAA'
    # if error_indication:
    #     print("请求超时！")
    #


def get_result(ip, community, oid):
    result.clear()
    ent_address = walk(ip, community, oTable[f'{oid}'])
    if ent_address == '0xAA':
        return False
    else:
        # 请求未超时
        for i in ent_address:
            temp = ''
            for j in i:
                temp += str(j)

            temp = temp.replace("SNMPv2-SMI::mib-2.2.2.1.", "")
            temp = temp[temp.find('.') + 1:]
            temp = temp.split(' = ')
            result.append(temp)

        return list(result)


if __name__ == '__main__':
    # create_image()
    result = []
    oTable = {
        "sysName": (1, 3, 6, 1, 2, 1, 1, 5),  # 系统名称
        "sysDescr": (1, 3, 6, 1, 2, 1, 1, 1),  # 系统描述，可以获取系统版本信息
        "ifNumber": (1, 3, 6, 1, 2, 1, 2, 1, 0),  # 网络接口的数目
        "ifIndex": (1, 3, 6, 1, 2, 1, 2, 2, 1, 1),  # 端口索引
        "ifDescr": (1, 3, 6, 1, 2, 1, 2, 2, 1, 2),  # 端口信息描述
        "ifType": (1, 3, 6, 1, 2, 1, 2, 2, 1, 3),  # 端口类型
        "ifSpeed": (1, 3, 6, 1, 2, 1, 2, 2, 1, 5),  # 接口当前带宽[bps]
        "ifInOctet": (1, 3, 6, 1, 2, 1, 2, 2, 1, 10),  # 接口收到的字节数
        "ifOutOctet": (1, 3, 6, 1, 2, 1, 2, 2, 1, 16),  # 接口发送的字节数
        "ifInUcastPkts": (1, 3, 6, 1, 2, 1, 2, 2, 1, 11),  # 接口收到的数据包个数
        "IfOutUcastPkts": (1, 3, 6, 1, 2, 1, 2, 2, 1, 17),  # 接口发出的数据包个数
        "ifPhysAddress": (1, 3, 6, 1, 2, 1, 2, 2, 1, 6),  # 端口物理地址
        "ifOperStatus": (1, 3, 6, 1, 2, 1, 2, 2, 1, 8),  # 端口的工作状态[up|down]
        "ifName": (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 1),  # 端口名称（节点值同节点ifDescr）
        "ipAdEntAddr": (1, 3, 6, 1, 2, 1, 4, 20, 1, 1),  # 接口IP地址
    }

    create_image("15")
