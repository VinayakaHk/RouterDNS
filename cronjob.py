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

# Define the new cron job line
cron_command = f"/home/vinayakahk/Projects/DnsRouter/venv/bin/python /home/vinayakahk/Projects/DnsRouter/router_reboot.py"
cron_command2 = f"/home/vinayakahk/Projects/DnsRouter/venv/bin/python /home/vinayakahk/Projects/DnsRouter/router_dns.py"
cron_timing = f"00 {new_hour} * * * {cron_command}"
cron_timing2 = f"05 {new_hour} * * *  {cron_command2}"

# Update crontab
cron = CronTab(user=True)
cron.remove_all(command=cron_command)
cron.remove_all(command=cron_command2)
job = cron.new(command=cron_command)
job = cron.new(command=cron_command2)
job.setall(cron_timing)
job.setall(cron_timing2)
cron.write()

print(f"Updated crontab to: {cron_timing} and {cron_timing2}")
