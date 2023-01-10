# this script must run MON_FRI at 00:00:00
# cronjob 0 0 * * 1-5 /path/to/cron.py

from main import set_data_in_file

set_data_in_file('executed_today.txt', '0')
