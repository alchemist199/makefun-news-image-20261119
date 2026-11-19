# The World, 19 November 2026

A broadsheet front page summing up the world's news of Thursday, 19 November 2026 in one image, built for the make.fun bounty "Sum up 19 November's world news in one image".

Bounty: https://make.fun/bounty/news-image-20261119

Referral code: epg3svvz

## How it works

`build_frontpage.py` draws `entry.png` (1024x1024) deterministically with Pillow: masthead and date, the lead story (Trump, Xi and Putin's first three-way summit in Shenzhen), eight more stories in a grid, and a strip of shorter items. `main.py` (stdlib only) verifies the PNG and copies it to `/output/entry.png`.
