ticketChecker

ellenőrzi, hogy a jegyárusító oldal elérhető jegyeket listázó része változik-e (a minden elfogyott állapotról), ha igen, akkor küld egy email, hogy van jegy (debug miatt a kérdéses részt is kiküldi a mailben)

vm-en futtava óránként

on remote host:
```sh
/home/ubuntu/logrotate.conf
/var/log/scripts/ticketChecker/*.log {
        daily
        missingok
        rotate 24
        compress
        maxage 1
}
```

in crontab:
```sh
2 * * * * /home/ubuntu/scripts/ticketChecker/scraping_final.py
5 * * * * /usr/bin/logrotate /home/ubuntu/logrotate.conf --state /home/ubuntu/logrotate-state
```