#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 File Name: db_utils.py
 Author: longhui
 Created Time: 2018-03-22 20:30:55
 Descriptions: This file is used to update information to databse, don't care about which table
'''

from lib.Log.log import log
from lib.Db.db_factory import DbFactory
from lib.Val.virt_factory import VirtFactory


def create_vm_base_info(inst_name, **kwargs):
    """

    :param inst_name: VM name
    :param kwargs: host, user, passwd dict
    :return:
    """
    log.info("Start to update [%s] information to databse.", inst_name)

    host_name = kwargs['host']
    user = kwargs['user'] if kwargs['user'] else "root"
    passwd = str(kwargs['passwd']).replace('\\', '') if kwargs['passwd'] else ""

    vnet_driver = VirtFactory.get_vnet_driver(host_name, user, passwd)
    virt_driver = VirtFactory.get_virt_driver(host_name, user, passwd)
    db_driver = DbFactory.get_db_driver("VirtHost")

    vm_record = virt_driver.get_vm_record(inst_name=inst_name)
    hostname = inst_name
    sn = vm_record['uuid']
    cpu_cores = vm_record['VCPUs_max']
    memory_size = vm_record['memory_target']

    disk_info = virt_driver.get_all_disk(inst_name=inst_name)
    disk_num = len(disk_info)
    disk_size = virt_driver.get_disk_size(inst_name, 0) #only write the system disk size when create
    # for disk in disk_info:
    #     disk_size += virt_driver.get_disk_size(inst_name, disk)

    ret = db_driver.create(hostname, sn, cpu_cores, memory_size, disk_size, disk_num)
    if ret:
        log.info("Create record to database successfully.")
    else:
        log.error("Create record to database failed.")

    return ret


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--host", dest="host", help="IP for host server")
    parser.add_option("-u", "--user", dest="user", help="User name for host server")
    parser.add_option("-p", "--pwd", dest="passwd", help="Passward for host server")

    (options, args) = parser.parse_args()
    log.debug("options:%s, args:%s", str(options), str(args))
    print  create_vm_base_info(inst_name="test2", host=options.host, user=options.user, passwd=options.passwd)

