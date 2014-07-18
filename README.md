150-days-of-trolling
====================

[150 Days of Giving](http://www.150daysofgiving.com/) fail.

Disclaimer
==========

This project merely *demonstrates* the weaknesses of the 150 Days of Giving website by showing how it is possible to obtain an insane number of votes very quickly, due a combination of no rate limiting, stupidly simple captchas, no enforced login, cookie-only authentication, general sloppiness, and more.

Usage
=====

```
$ python troll.py group_id [-t times]
```

Just call `troll.py` with the group id you'd like to vote for as the first positional parameter. You can obtain the group id by inspecting the vote button for that particular nonprofit &ndash; very helpfully (and quite non-best practice-y, but I'm not complaining), they've included it in the HTML in the onclick handler (`captchaAlert(GROUP_ID)`) directly on the 150 Days of Giving homepage.

By default, `troll.py` will vote for that nonprofit exactly once. To vote more than once, use the `-t` argument.

```
# Vote for group_id 500 times
$ python troll.py group_id -t 500
```

Dependencies
============

- Tesseract OCR ([link](https://code.google.com/p/tesseract-ocr/))
- `pytesser` ([link](https://code.google.com/p/pytesser/))
- `PIL` ([link](http://www.pythonware.com/products/pil/))
- `requests` ([link](http://docs.python-requests.org/en/latest/))

License
=======

Copyright (C) 2014 Theopolisme <theopolismewiki@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


