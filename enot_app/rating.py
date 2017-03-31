
def prerate(bid):
    """ Evaluate pre-rating of the bid
    :prop bid: Bid object
    return pre-rating number
    """
    rt =0
    d = bid.distance
    days = (bid.return_date-bid.departure_date).days
    if d > 1200 and d <= 2100:
        rt += 100
    if d > 2100 and d <= 4000:
        rt += 300
        if days>21:
            rt-=200
    if d > 4000 and d <= 8000:
        rt += 200
        if days>40 or days<7:
            rt-=200
    if d > 8000:
        rt += 100
        if days>60 or days<14:
            rt-=200

    rt += int(d/bid.price*1000)

    if days<3:
        rt-=300

    wd = bid.departure_date.weekday()
    if wd == 3:
        rt+=50
    elif wd == 4 or wd == 5:
        rt+=100

    rt = rt-bid.stops*100

    ap = bid.destination.average_price

    rt = rt + int((ap-bid.price)/ap*1000)

    return rt