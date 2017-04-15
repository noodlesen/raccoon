from datetime import datetime
from enot_app.toolbox import now_in_moscow
from enot_app.models import Status
import logging
from django.core.mail import send_mail
from enot.settings import ADMINS, DEFAULT_FROM_EMAIL

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
    if 'mail' in kwargs and kwargs['mail'] is True:
        if 'subj' in kwargs:
            subj = kwargs['subj']
        else:
            subj = ''
        inform_admin(msg, subj)
    print (msg)



def allows(action, **kwargs):

    allow = False

    if action == 'to_load_bids':
        moscow_time = now_in_moscow()
        time_to_work = True if moscow_time.hour < 19 else False
        if time_to_work:  
            st = Status.get_today()
            if st.loader_started == st.loader_finished:
                allow = True
                st.loader_started += 1
                st.save()
                report('Starting to load bids')
            else:
                report('Something went wrong last time', mail=True)
        else:
            report('Bed time! zzz...') 

    if action == 'to_request_qpx':
        stats = Status.get_today()
        if stats.qpx_requests < 50:
            allow = True
            print('ALLOWED')
            stats.qpx_requests += 1
            stats.save()
        else:
            report('REQUEST LIMIT EXCEEDED', mail=True)

    return allow


def inform(action, **kwargs):

    if action == 'started_trip_loader':
        report('Started trip loader task')
    elif action == 'finished_trip_loader':
        report('finished to load trips')

    if 'extra' in kwargs.keys():
        report(kwargs['extra'])


def finish(action):
    if action == 'to_load_bids':
        st = Status.get_today()
        st.loader_finished += 1
        st.save()
        report('finished to load bids')




