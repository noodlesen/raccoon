from datetime import datetime
from enot_app.toolbox import now_in_moscow
from enot_app.models import Status

def report(msg):
    print (msg)

def report_start(task):

    print()
    print('===================================')
    print('##', task)
    print('## started: ', now_in_moscow())
    print()

def report_finish(task):

    print()
    print('##', task)
    print('## finished: ', now_in_moscow())
    print('===================================')
    print()


def allows(action):

    if action == 'to_load_bids':
        allow = False
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
                report('Something went wrong last time')
        else:
            report('Bed time! zzz...')
        return allow

def finish(action):
    if action == 'to_load_bids':
        st = Status.get_today()
        st.loader_finished += 1
        st.save()
        report('finished to load bids')