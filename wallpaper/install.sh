pip install pixivpy
python ./wallpaper.py
(crontab -l; echo "0 0 */2 * * python $(realpath ./wallpaper.py)") | crontab -
