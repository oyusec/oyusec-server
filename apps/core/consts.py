from apps.competition.consts import *

AUTHENTICATION_REQUIRED = "Authentication required"
ACCESS_DENIED = "You dont have access to this resource"

SUCCESS_UPDATED = "Амжилттай шинэчлэлээ"
SUCCESS_ADD = "Амжилттай нэмэгдлээ"
SUCCESS_DELETED = "Амжилттай хасагдлаа"

USER_TYPE_NORMAL = "normal"
USER_TYPE_ADMIN = "admin"

USER_TYPE_CHOICES = (
    (USER_TYPE_NORMAL, "normal"),
    (USER_TYPE_ADMIN, "admin"),
)


# Fake data

# Mostly user related
FAKE_ADMIN = 'admin'
FAKE_ADMIN_EMAIL = 'admin@zxc.zxc'
FAKE_USER_USERNAME = 'fake'
FAKE_GUEST_USERNAME = 'guest'
FAKE_GUEST_EMAIL = 'guest@zxc.zxc'
FAKE_PASSWORD = 'tmppass123'

# Mostly competition related
FAKE_COMPETITION_NAME = 'OyuSec'
FAKE_COMPETITION_DESCRIPTION = """For the first time, Taif University organizes an online cybersecurity Capture The Flag (CTF) competition. This competition is a side-event to the 4th National Conference for Computing Colleges (4th NCCC 2021), which is organized by the College of Computers and Information Technology at Taif University from March 27th to March 28th, 2021. The CTF hacking competition starts on the first day of the conference from 03:00 PM to 11:00 PM. \n\nThe competition will be a Jeopardy Style CTF where every team will have a list of challenges in different categories like Reverse Engineering, Web Security, Digital Forensics, Network Security and others. For every challenge solved, the team will get a certain amount of points depending on the difficulty of the challenge. The team who will get the highest score at the end of the day will be the winning team."""
FAKE_COMPETITION_RULE = """- Sharing the flags between different teams is prohibited.\n- Brute Force attacks on the challenges submission portal or challenges links are not allowed.\n- Any attack against the site or the hosted servers will be observed and the player will be banned from participating in the CTF immediately.\n- Organizers have the permission to disqualify teams for any unethical behavior or any trials to interrupt the CTF."""
FAKE_COMPETITION_PRIZE = """- $XXX\n- $YYY\n- $ZZZ"""
FAKE_COMPETITION_CHALLENGE_NAME = 'Hidden Message'
FAKE_IMAGES = ["https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Sudan+National+CTF+Thumbnail.jpg",
               "https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Kenya+National+CTF+Thumbnail.jpg", "https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Saudi+Arabia+National+CTF+Thumbnail.jpg"]
FAKE_STATUS = [COMPETITION_LIVE, COMPETITION_ARCHIVE, COMPETITION_COMING]
FAKE_COMPETITION_LOCATIONS = ['онлайн', 'дэлхийд', 'монголд', 'хөдөө']

# Mostly related challenges
FAKE_CHALLENGE_NAME = 'Cyber Anxiety'
FAKE_CHALLENGE_CATEGORIES = ['reverse engineering', 'misc',
                             'forensics', 'cryptography', 'binary exploitation', 'web']
FAKE_CHALLENGE_DESCRIPTION = """RSA encryption is modular exponentiation of a message with an exponent `e` and a modulus `N` which is normally a product of two primes: `N = p * q`.

Together the exponent and modulus form an RSA "public key" `(N, e)`. The most common value for e is `0x10001` or `65537`.

> This is fake data, flag{thisisdemo}

[download](https://google.com)
"""

FAKE_FLAG = 'flag{thisisdemo}'
