# -*- coding: utf-8 -*-

"""
troll.py
========

Automated voting on http://www.150daysofgiving.com/
usage: troll.py [-h] [-t TIMES] group_id

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
"""

import sys
import argparse
from cStringIO import StringIO
import requests
from PIL import Image
from pytesser import image_to_string

CAPTCHA_ENDPOINT = 'http://www.150daysofgiving.com/simpleCaptcha/captcha'
VOTE_ENDPOINT = 'http://www.150daysofgiving.com/npo/captchaVote'

def solve_captcha(captcha):
    """Returns a string solution to a PIL.Image of a captcha."""
    # Make all non-black pixels white
    pixeldata = captcha.load()
    for y in xrange(captcha.size[1]):
        for x in xrange(captcha.size[0]):
            if pixeldata[x, y] != (0, 0, 0):
                pixeldata[x, y] = (255, 255, 255)

    # OCR this sucker
    result = str(image_to_string(captcha)).split('\n')[0]

    # A few tweaks to improve success rate based on knowns about simpleCaptcha
    result = result.replace('|', 'I') # The I's look suspiciously pipe-like
    result = result.replace( ' ', '' ) # There aren't ever any spaces
    result = result.upper() # All captchas are uppercased

    return result

def vote(group_id):
    """Votes for a specific group_id once."""
    response = requests.get(CAPTCHA_ENDPOINT)
    captcha = Image.open(StringIO(response.content))
    solution = solve_captcha(captcha)

    # Now submit the solution, making sure we copy the cookies
    # from the first request to the next one
    resp_json = requests.post(VOTE_ENDPOINT, {
        'name': solution,
        'npoid': group_id
    }, cookies=response.cookies).json()

    # Successful
    if resp_json['status'] == 'OK':
        print resp_json['results']
        return True

    # OCR fail
    elif resp_json['results'] == 'You entered wrong captcha text':
        print 'captcha failed! we guessed: ' + solution
        return False

    # Something weird, let's stop... maybe they've started rate-limiting us?
    else:
        print 'unknown error occured; stopping to investigate.'
        print resp_json
        sys.exit(1)

def vote_for(group_id, number_of_times):
    """Votes for a specific group on the website a specific number of times."""
    success = 0

    print 'Now voting...\n------'

    for _ in range(number_of_times):
        if vote(group_id):
            success += 1

    print '------\nRun completed - {} / {} successful ({:.2%})'.format(
        success, number_of_times, float(success) / number_of_times)

def main():
    parser = argparse.ArgumentParser(description='Automated voting on 150 Days of Giving.')
    parser.add_argument('group_id', type=int,
                       help='group id to vote for')
    parser.add_argument('-t', '--times', type=int, default=1,
                       help='number of times to vote for the group')

    args = parser.parse_args()

    vote_for(args.group_id, args.times)

if __name__ == '__main__':
    main()
