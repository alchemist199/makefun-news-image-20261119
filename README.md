# makefun-news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/alchemist199/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/alchemist199/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A broadsheet front page summing up the world's news of Thursday, 19 November 2026 in one image, built for the make.fun bounty "Sum up 19 November's world news in one image". Lead story: Trump, Xi and Putin's first three-way summit in Shenzhen. `build_frontpage.py` draws `entry.png` (1024x1024) deterministically with Pillow: masthead and date, the lead story, eight more stories in a grid, and a strip of shorter items. `main.py` (stdlib only) verifies the PNG and copies it to `/output/entry.png`.

## Run it

```sh
python3 build_frontpage.py && python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=epg3svvz&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
