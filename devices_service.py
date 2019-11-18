import subprocess
import time
from db_access import WorkshopDb

debug = False


def ping(ip_base, static_start, dynamic_start, groups_number):
    """Calls 'pinger.exe' in order to try and keep arp table updated"""
    static_ip_start = ip_base + str(static_start)
    static_ip_end = ip_base + str(int(static_start) + int(groups_number))
    subprocess.call("pinger.exe " + static_ip_start + " " + static_ip_end)
    dynamic_ip_start = ip_base + str(dynamic_start)
    dynamic_ip_end = ip_base + str(int(dynamic_start) + 50)
    subprocess.call("pinger.exe " + dynamic_ip_start + " " + dynamic_ip_end)


def get_device_ip(mac):
    """try to find an IP that matches the mac address in arp table"""
    output = subprocess.check_output(("arp", "-a"))
    lines = output.decode("ascii").split('\r\n')
    for line in lines:
        if line.find('dynamic') != -1 or line.find('static') != -1:
            device_line = line.split()
            if device_line[1] == mac:
                return device_line[0]
    return ''


def update_known_devices(db):
    groups_number = db.get_config_item('groups_number')
    ping(db.get_config_item('subnet_ip'), db.get_config_item('base_ip'),
         db.get_config_item('dynamic_ip'), groups_number)
    for group in range(1,groups_number+1):
        mac = db.get_group_mac(group)
        ip = get_device_ip(mac)
        if ip != '':
            if debug:
                print(f'updating {mac} - {ip} (Group {group})')
            db.update_mac_ip(mac, ip)


def run():
    db = WorkshopDb()
    while True:
        update_known_devices(db)
        time.sleep(10)


if __name__ == '__main__':
    debug = True
    run()
