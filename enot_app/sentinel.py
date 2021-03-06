from datetime import datetime
from enot_app.toolbox import now_in_moscow
from enot_app.models import Status, Bid, Trip
import logging
from django.core.mail import send_mail
from enot.settings import ADMINS, DEFAULT_FROM_EMAIL
from enot_app.planner import make_TP_plan

logger = logging.getLogger('elog')


def inform_admin(msg, subj=''):
    if subj != '':
        subj = ': '+subj
    send_mail(
        'Sentitnel report'+subj,
        msg,
        DEFAULT_FROM_EMAIL,
        [a[1] for a in ADMINS],
        fail_silently=False,
    )

def report(msg, **kwargs):
    src=''
    if 'src' in kwargs:
        src = kwargs['src'].split('.')[-1].upper()+": "
    if 'mail' in kwargs and kwargs['mail'] is True:
        if 'subj' in kwargs:
            subj = kwargs['subj']
        else:
            subj = ''
        inform_admin(msg, src+subj)
    smsg = src+msg
    #print(smsg)
    logger.info(smsg)



def allows(action, **kwargs):

    allow = False

    isForced = False
    if kwargs.get('force') is True:
        isForced = True
        report('FORCED')

    if action == 'to_load_bids':
        moscow_time = now_in_moscow()
        time_to_work = True if moscow_time.hour in range(5, 15) else False
        if time_to_work or isForced:
            st = Status.get_today()
            if st.loader_started == st.loader_finished:
                allow = True
                st.loader_started += 1
                st.save()
                report('Starting to load bids')
                if st.loader_finished == 0:
                    Bid.objects.all().delete()
            else:
                report('Something went wrong last time', mail=True)
        else:
            report('Bed time! zzz...')

    if action == 'to_request_qpx':
        stats = Status.get_today()
        if stats.qpx_requests < 50:
            if stats.qpx_requests == 0:
                Trip.objects.all().delete()
            allow = True
            stats.qpx_requests += 1
            stats.save()
        else:
            report('REQUEST LIMIT EXCEEDED', mail=True)


    if action == 'to_run_planner':
        #isForced = options['force']
        syd = Status.get_yesterday(isForced)
        std = Status.get_today()
        if syd is not False or isForced:
            if not std.planner_started or isForced:
                if syd.planner_finished or isForced:
                    std.planner_started = True
                    std.save()
                    allow = True
                else:
                    report('planner has not finished ok yesterday')
            else:
                report('planner has already stared today')

    if action == 'to_make_bid_request':
        std = Status.get_today()
        allow = False if std.api_request_in_progress else True

    return allow


def inform(action, **kwargs):

    if action == 'started_trip_loader':
        report('Started trip loader task')
    elif action == 'finished_trip_loader':
        report('finished to load trips')
    elif action == 'build_complete':
        report('Улётные билеты готовы\nhttp://uletbilet.ru/letter?sort=price&new=1', mail=True)

    if 'extra' in kwargs.keys():
        report(kwargs['extra'])


def finish(action):
    if action == 'to_load_bids':
        st = Status.get_today()
        st.loader_finished += 1
        st.save()
        report('finished to load bids')

    if action == 'to_plan':
        std = Status.get_today()
        std.planner_finished = True
        std.save()

def have(action):
    res = False
    if action == 'to_run_planner':
        st = Status.get_today()
        if st.loader_started == 1:
            res = True
    return res





