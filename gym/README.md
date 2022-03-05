# GYM-SYSU

## Badminton

### 1. Installation

- Install `tesseract-v5.0.0.exe`, and you may need to add it to env path by yourself.

- Add `chromedriver.exe` to env path or put it in this folder.

- install python library as follow instruction.

```bash
pip install -r requirement.txt
```

### 2. Usage

Please input information in config.json first, and then you can run this script to reserve badminton field.

`NetID` is known by youself.

`Password` is known by youself.

`book_date` is the date when you want play.

`book_time` is the time table when you want play.

```python
# config.json book_time explain as follows.
book_time = {
    9: "09:00-10:00",
    10: "10:01-11:00",
    11: "11:01-12:00",
    14: "14:00-15:00",
    15: "15:01-16:00",
    16: "16:01-17:00",
    17: "17:01-18:00",
    18: "18:00-19:00",
    19: "19:01-20:00",
    20: "20:01-21:00",
    21: "21:01-22:00",
}
```

`switch_time` can adjust the interval time between switching tabs.

`max_tab` set the up limit of max tabs we can open.

`hide_chrome` use 1 to hide chrome and 0 to display chrome.
