# from models import Site, Bot
# from api import engine

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import select

# import requests
# import re

# from enum import Enum

# class SiteState(Enum):
#     LIVE=1
#     DIE=0


# Session = sessionmaker(bind=engine)

# BOT_SEND_MESSAGE_URL = r'https://api.telegram.org/bot{token}/sendMessage'


# def get_sites():
#     with Session() as session:
#         sites = session.query(Site).where(checking_active=True).all()
#         return sites

# def get_bot(id) -> Bot:
#     with Session() as session:
#         q = select(Bot).where(Bot.id==id)
#         bot = session.execute(q).scalar()
#         return bot

# def make_report_text(message_pattern,site):
#     return message_pattern.format(
#         label=site.label,
#         url=site.url,
#         description=site.description,
#     )
    

# def report(site):
#     try:
#         bot = get_bot(site.bot_id)
#         text = make_report_text(bot.message_pattern,site)
#         data = { 
#             'chat_id' : bot.chat_id,
#             'text' : text
#         }
#         response = requests.post(BOT_SEND_MESSAGE_URL.format(token=bot.token), data=data)
#     except:
#         pass

# def test(site: Site):
#     try:
#         response = requests.get(site.url)
#         if site.expected_response_body_pattern == '' or site.expected_response_body_pattern is None:
#             return SiteState.LIVE if str(response.status_code) in site.expected_response_code else SiteState.DIE
#         pattern = re.compile(site.expected_response_body_pattern, re.MULTILINE)
#         return SiteState.LIVE if (str(response.status_code) in site.expected_response_code and \
#             pattern.search(response.content.decode('utf-8'))) \
#             else SiteState.DIE
#     except:
#         return SiteState.DIE

# def check_sites():
#     with Session() as session:
#         q = select(Site).where(Site.checking_active==True)
#         sites = session.execute(q).scalars().all()
#         for site in sites:
#             if test(site) == SiteState.DIE:
#                 report(site)

# def main():
#     check_sites()

# if __name__ == '__main__':
#     main()


from models import Site, Bot
from api import engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

import requests
import re

from enum import Enum

import threading

from croniter import croniter
from datetime import datetime

class SiteState(Enum):
    LIVE=1
    DIE=0


Session = sessionmaker(bind=engine)

BOT_SEND_MESSAGE_URL = r'https://api.telegram.org/bot{token}/sendMessage'


def get_sites():
    with Session() as session:
        sites = session.query(Site).where(checking_active=True).all()
        return sites

def get_bot(id) -> Bot:
    with Session() as session:
        q = select(Bot).where(Bot.id==id)
        bot = session.execute(q).scalar()
        return bot

def make_report_text(message_pattern,site):
    return message_pattern.format(
        label=site.label,
        url=site.url,
        description=site.description,
    )
    

def report(site: Site):
    for bot in site.bots:
        text = make_report_text(bot.message_pattern,site)
        for contact in filter(lambda x:x.is_active, bot.contacts):
            data = { 
                'chat_id' : contact.contact_string,
                'text' : text
            }
            try:
                response = requests.post(BOT_SEND_MESSAGE_URL.format(token=bot.token), data=data)
            except Exception as e :
                print(e)

def test_body(site: Site, body: str):
    if site.expected_response_body_pattern == '' or site.expected_response_body_pattern is None:
        return SiteState.LIVE
    pattern = re.compile(site.expected_response_body_pattern, re.MULTILINE)
    return SiteState.LIVE if (str(body) in site.expected_response_code and \
        pattern.search(body)) \
        else SiteState.DIE

def test_status_code(site: Site, response_code: str):
    if site.expected_response_code == '' or site.expected_response_code is None:
        return SiteState.LIVE
    return SiteState.LIVE if (str(response_code) in site.expected_response_code) \
        else SiteState.DIE

def test(site: Site):
    try:
        response = requests.get(site.url)
        code_test = test_status_code(site, str(response.status_code))
        body_test = test_body(site, response.content.decode('utf-8'))
        if site.inverse_conditions:
            return SiteState.LIVE if code_test == SiteState.DIE and body_test == SiteState.DIE else SiteState.DIE
        else:
            return SiteState.LIVE if code_test == SiteState.LIVE and body_test == SiteState.LIVE else SiteState.DIE
    except Exception as e:
        return SiteState.DIE

    
def test_and_report_at_schedule(site: Site):
    time = datetime.now().replace(second=0, microsecond=0)
    cron = croniter(site.cron_schedule, time)
    if cron.get_current(datetime) == time:
        if test(site) == SiteState.DIE:
            report(site)

def check_sites():
    with Session() as session:
        q = select(Site).where(Site.checking_active==True)
        sites = session.execute(q).scalars().unique().all()
        for site in sites:
            th = threading.Thread(target=test_and_report_at_schedule, args=(site,))
            th.start()

def main():
    check_sites()

if __name__ == '__main__':
    main()