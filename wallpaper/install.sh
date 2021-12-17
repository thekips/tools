./wallpaper.py
(crontab -l; echo "0 0 */2 * * $(realpath ./wallpaper.py)") | crontab -
