ticketChecker

on remote host:
/home/ubuntu/logrotate.conf
/var/log/scripts/ticketChecker/*.log {
        daily
        missingok
        rotate 24
        compress
        maxage 1
}

in crontab:
2 * * * * /home/ubuntu/scripts/ticketChecker/scraping_final.py
5 * * * * /usr/bin/logrotate /home/ubuntu/logrotate.conf --state /home/ubuntu/logrotate-state