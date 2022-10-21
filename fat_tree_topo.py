from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.util import dumpNodeConnections
from mininet.link import Link, Intf, TCLink
import sys
from time import sleep

PORT = 4


class FatTreeTypo(Topo):

    def __init__(self, port=4):
        # 2 stage fat tree with N ports

        Topo.__init__(self)
        self.buildTree(port)

    def buildTree(self, K):
        core_num = K // 2
        core_sw = [None] * core_num
        aggr_num = K
        aggr_sw = [None] * aggr_num
        hosts = [None] * (K ** 2 // 2)

        port = int(port)

        if (port % 2 != 0):
            raise Exception('Port number should be an even number')

        output_num = port // 2

        # create first stage
        for i in range(0, core_num):
            sw = self.addSwitch("s1-%s" % i)
            core_sw[i] = sw

        cnt = 0
        # create second stage
        for i in range(0, aggr_num):
            sw = self.addSwitch("s2-%s" % i)
            aggr_sw[i] = sw
            # add host
            for i in range(0, K//2):
                host = self.addHost("h%s" % i)
                self.addLink(sw, host)
                hosts[cnt] = host
                cnt += 1

        # link first stage switches to second stage switches
        for sw1 in core_sw:
            for sw2 in aggr_sw:
                # sw1 connect to every sw2
                self.addLink(sw1, sw2)


topos = {'mytopo': (lambda: FatTreeTypo())}


def main():
    fat_tree_typo = FatTreeTypo(PORT)
    net = Mininet(topo=fat_tree_typo, link=TCLink)

    # start net
    net.start()
    # Wait for links setup (sometimes, it takes some time to setup, so wait for a while before mininet starts)
    print("\nWaiting for links to setup . . . ."),
    sys.stdout.flush()
    for time_idx in range(3):
        print("."),
        sys.stdout.flush()
        sleep(1)

    # 2. Start the CLI commands
    info('\n*** Running CLI\n')
    CLI(net)

    # 3. Stop mininet properly
    net.stop()


main()
