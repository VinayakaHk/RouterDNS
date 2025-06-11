import os
from crontab import CronTab

def adjust_time(time: int) -> int:
    """
    Adjusts the time by subtracting 2 hours.
    If the result goes below 0, it wraps around using modulo 24.
    """
    new_time = (time - 2) % 24
    return new_time

# Define the original hour in crontab
original_hour = 14
new_hour = adjust_time(original_hour)

# Define the new cron job commands
cron_command = "/home/vinayakahk/Projects/DnsRouter/venv/bin/python /home/vinayakahk/Projects/DnsRouter/router_reboot.py"
cron_command2 = "/home/vinayakahk/Projects/DnsRouter/venv/bin/python /home/vinayakahk/Projects/DnsRouter/router_dns.py"

# Update crontab
cron = CronTab(user=True)
cron.remove_all(command=cron_command)
cron.remove_all(command=cron_command2)

# Create first job
job = cron.new(command=cron_command)
job.minute.on(0)
job.hour.on(new_hour)

# Create second job
job2 = cron.new(command=cron_command2)
job2.minute.on(5)
job2.hour.on(new_hour)

# Write changes to crontab
cron.write()

print(f"Updated crontab to: '00 {new_hour} * * * {cron_command}' and '05 {new_hour} * * * {cron_command2}'")
