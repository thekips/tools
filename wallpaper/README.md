### Description

`bing.py`: 必应每日壁纸

`pixiv.py`: P站热门壁纸

### Dependency

- python

- `pixivpy`库

  ```
  pip install pixivpy
  ```

### Usage

- ##### Linux

```bash
(crontab -l; echo "0 0 */2 * * python $(realpath ./wallpaper.py)") | crontab -
```

- ##### Windows

​	需要使用任务计划程序，定时启动`*.py`