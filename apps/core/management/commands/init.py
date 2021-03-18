from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime
from apps.core.models import BaseUser
from apps.ctf.models import (
    StandardChallenge,
    DynamicChallenge,
    Challenge,
    Flag,
)
from apps.competition.models import (
    Competition,
)
from apps.ctf.consts import *
from apps.competition.consts import *


class Command(BaseCommand):
    help = 'Initialize default values'

    def handle(self, *args, **kwargs):
        self.create_admin()
        self.create_competitions()
        self.create_challenges()
        self.create_flags()

    def create_admin(self):
        BaseUser.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='tmppass123'
        )
        self.stdout.write("[+] Created admin")

    def create_competitions(self):

        Competition.objects.create(
            name='OyuSec CTF #5',
            description="""For the first time, Taif University organizes an online cybersecurity Capture The Flag (CTF) competition. This competition is a side-event to the 4th National Conference for Computing Colleges (4th NCCC 2021), which is organized by the College of Computers and Information Technology at Taif University from March 27th to March 28th, 2021. The CTF hacking competition starts on the first day of the conference from 03:00 PM to 11:00 PM. \nThe competition will be a Jeopardy Style CTF where every team will have a list of challenges in different categories like Reverse Engineering, Web Security, Digital Forensics, Network Security and others. For every challenge solved, the team will get a certain amount of points depending on the difficulty of the challenge. The team who will get the highest score at the end of the day will be the winning team.""",
            rule="""- Sharing the flags between different teams is prohibited.\n- Brute Force attacks on the challenges submission portal or challenges links are not allowed.\n- Any attack against the site or the hosted servers will be observed and the player will be banned from participating in the CTF immediately.\n- Organizers have the permission to disqualify teams for any unethical behavior or any trials to interrupt the CTF.""",
            prize="""- $XXX\n- $YYY\n- $ZZZ""",
            start_date=make_aware(datetime(2021, 3, 27, 18, 0)),
            end_date=make_aware(datetime(2021, 3, 28, 18, 0)),
            photo="https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Sudan+National+CTF+Thumbnail.jpg"
        )
        Competition.objects.create(
            name='OyuSec CTF #2',
            description="""For the first time, Taif University organizes an online cybersecurity Capture The Flag (CTF) competition. This competition is a side-event to the 4th National Conference for Computing Colleges (4th NCCC 2021), which is organized by the College of Computers and Information Technology at Taif University from March 27th to March 28th, 2021. The CTF hacking competition starts on the first day of the conference from 03:00 PM to 11:00 PM. \nThe competition will be a Jeopardy Style CTF where every team will have a list of challenges in different categories like Reverse Engineering, Web Security, Digital Forensics, Network Security and others. For every challenge solved, the team will get a certain amount of points depending on the difficulty of the challenge. The team who will get the highest score at the end of the day will be the winning team.""",
            rule="""- Sharing the flags between different teams is prohibited.\n- Brute Force attacks on the challenges submission portal or challenges links are not allowed.\n- Any attack against the site or the hosted servers will be observed and the player will be banned from participating in the CTF immediately.\n- Organizers have the permission to disqualify teams for any unethical behavior or any trials to interrupt the CTF.""",
            prize="""- $XXX\n- $YYY\n- $ZZZ""",
            status=COMPETITION_LIVE,
            start_date=make_aware(datetime(2021, 3, 15, 18, 0)),
            end_date=make_aware(datetime(2021, 3, 16, 18, 0)),
            photo="https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Kenya+National+CTF+Thumbnail.jpg",
        )

        Competition.objects.create(
            name='OyuSec CTF #1',
            description="""For the first time, Taif University organizes an online cybersecurity Capture The Flag (CTF) competition. This competition is a side-event to the 4th National Conference for Computing Colleges (4th NCCC 2021), which is organized by the College of Computers and Information Technology at Taif University from March 27th to March 28th, 2021. The CTF hacking competition starts on the first day of the conference from 03:00 PM to 11:00 PM. \nThe competition will be a Jeopardy Style CTF where every team will have a list of challenges in different categories like Reverse Engineering, Web Security, Digital Forensics, Network Security and others. For every challenge solved, the team will get a certain amount of points depending on the difficulty of the challenge. The team who will get the highest score at the end of the day will be the winning team.""",
            rule="""- Sharing the flags between different teams is prohibited.\n- Brute Force attacks on the challenges submission portal or challenges links are not allowed.\n- Any attack against the site or the hosted servers will be observed and the player will be banned from participating in the CTF immediately.\n- Organizers have the permission to disqualify teams for any unethical behavior or any trials to interrupt the CTF.""",
            prize="""- $XXX\n- $YYY\n- $ZZZ""",
            status=COMPETITION_ARCHIVE,
            start_date=make_aware(datetime(2021, 3, 10, 18, 0)),
            end_date=make_aware(datetime(2021, 3, 11, 18, 0)),
            photo="https://website-cybertalents.s3-us-west-2.amazonaws.com/Competitions/Saudi+Arabia+National+CTF+Thumbnail.jpg"
        )

    def create_challenges(self):
        compettion1 = Competition.objects.all()[0]
        compettion2 = Competition.objects.all()[1]
        compettion3 = Competition.objects.all()[2]

        StandardChallenge.objects.create(
            name='Cypher Anxiety',
            category='Forensics',
            description='An image was leaked from a babies store. the manager is so annoyed because he needs to identify the image to fire charges against the responsible employee. the key is the md5 of the image',
            competition=compettion1,
        )

        StandardChallenge.objects.create(
            name='Hidden Message',
            category='Forensics',
            description='A cyber Criminal is hiding information in the below file . capture the flag ? submit Flag in MD5 Format [Link](https://s3-eu-west-1.amazonaws.com/talentchallenges/Forensics/hidden_message.jpg)',
            competition=compettion2,
        )

        DynamicChallenge.objects.create(
            name='Crack the Hash',
            category='Cryptography',
            description='A hacker leaked the below hash online.Can you crack it to know the password of the CEO? > 1ab566b9fa5c0297295743e7c2a6ec27',
            competition=compettion3,
        )
        DynamicChallenge.objects.create(
            name='Postbase',
            category='Cryptography',
            description="We got this letters and numbers and don't understand them. Can you? > R[corrupted]BR3tCNDUzXzYxWDdZXzRSfQ==",
        )
        DynamicChallenge.objects.create(
            name='Postbase 2',
            category='Cryptography',
            description="We got this letters and numbers and don't understand them. Can you? > R[corrupted]BR3tCNDUzXzYxWDdZXzRSfQ==",
        )
        DynamicChallenge.objects.create(
            name='Postbase 3',
            category='Cryptography',
            description="We got this letters and numbers and don't understand them. Can you? > R[corrupted]BR3tCNDUzXzYxWDdZXzRSfQ==",
        )

        self.stdout.write("[+] Created challenges")

    def create_flags(self):
        for _ in Challenge.objects.all():
            Flag.objects.create(content='flag{a}', challenge=_)

        self.stdout.write('[+] Created flags')