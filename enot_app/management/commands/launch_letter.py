from django.core.management.base import BaseCommand, CommandError
from enot_app.mandrill import send_email
from enot_app.models import Trip
from enot.settings import DEBUG


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        trips = Trip.objects.filter(expose=True, price__lt=35000, rating__gt=50).order_by('price')[:15]

        addresses = ["k.lapshov@gmail.com", "000sergey@gmail.com", "Drugula@mail.ru", "ac.igoris@gmail.com", "19721129@mail.ru", "Lybafka@ya.ru", "juicegbox@gmail.com", "mispar@mail.ru", "Speck@inbox.ru", "alexei.sulin@gmail.com", "iva19742006@yandex.ru", "helens-5@yandex.ru", "Kitchatovampd@mail.ru", "avkrav@gmail.com", "Sauzza@bk.ru", "irinakirichek@ya.ru", "ainur.khannanov@gmail.com", "murzax@gmail.com", "aptncatrckp@gmail.com", "Privetps@gmail.com", "elenakiseleva2011@mail.ru", "Yuri1990@mail.ru", "gregklepcov@gmail.com", "Poe@inbox.ru", "Verdantmary@gmail.com", "hendhrix@gmail.com", "mariabrauns@gmail.com", "Ledi_olgar@mail.ru", "Spk@live.ru", "ussaction@gmail.com", "paulaplanta@gmail.com", "abotsina@gmail.com", "Verdesie@gmail.com", "milasa@rambler.ru", "kolomiytsevam@gmail.com", "iskanderartheart@gmail.com", "andreysoloweb@gmail.com", "Waleriazl@gmail.com", "Jm9104223241@gmail.com", "7733910@gmail.com", "ezhempalukh@mail.ru", "jmelkum@yandex.ru", "akadiakr@gmail.com", "Mabox@mail.ru", "A.gavrilina@gmail.com", "cobarudo@mail.ru", "vasily.rybak1211@gmail.com", "Anna@galkina.ru", "Kc-ovcharenko@yandex.ru", "dmitry.selikhov@gmail.com", "Nata_1020@mail.ru", "Edbaryshev@gmail.com", "Booking@ikon.su", "Salnikov.leo@gmail.com", "mariyapetrova_87@mail.ru", "archirodmen@gmail.com", "kadikova@gmail.com", "Tatyanaisoft@gmail.com", "ealtakimov@mail.ru", "k-nash@mail. ru", "Odyshkant@list.ru", "artlili@ya.ru", "Fortunata35@gmail.com", "elsorochenko@gmail.com", "Zamyatin.ap@gmail.com", "Vovakli@mail.ru", "Tagir747@mail.ru", "Egorov.a.g@gmail.com", "camilalala@yandex.ru", "mail@dsviridov.com", "ulenka83@mail.ru", "sergey@kovalev.org", "Vays@mail.ru", "heyguy@mail.ru", "Nshegay@newmail.ru", "morozova@di-house.ru", "Begun.m@mail.ru", "Evteeva-ay@yandex.ru", "latreillena@gmail.com", "Liluu-o@mail.ru", "heyguy@mail.ru", "kula4enko13@gmail.com", "maxagoni@mail.ru", "aysina.dr@gmail.com", "Agent_pomidor@mail.ru", "Ezhivikh@gmail.com", "olesia300989@mail.ru", "k.kruglikoff@gmail.com", "89028953847@mail.ru", "leouli@mail.ru", "Milavershko@gmail.com", "princessa2808@mail.ru", "44pomidora@gmail.com", "maxoon@yandex.ru", "moldavanova@mail.ru", "lyalinaksenia@mail.ru", "budilov.alex@gmail.com", "blackyak@bk.ru", "Novikova_T@bk.ru", "david_korolev@mail.ru", "igokartavykh@gmail.com", "alex.k.1976@gmail.com", "2546709@gmail.com", "Kurgasheva@gmail.com", "vengera@mail.ru", "vip-s@ya.ru", "Dmitry.Gluhov@gmail.com", "ilya.brait@gmail.com"]


        #places = [t.destination_name+': '+str(t.price) for t in trips][:6]
        subj = "Улётные билеты от разработчиков FlyFromMoscow.ru"
        for addr in addresses:
            print (addr)
            _send_email(sender="Улётные Билеты<mail@uletbilet.ru>",
                       to=addr,
                       subject=subj,
                       context={'trips': trips, 'debug': DEBUG},
                       template='enot_app/launch_letter.html')
