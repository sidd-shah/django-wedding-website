import csv
import StringIO
import uuid
from guests.models import Party, Guest, Function


def import_guests(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            party_name, guests, function, groom_invite = row[:4]
            phone_numbers = row[4:]
            party_name = party_name.title()
            if guests == 'Couple':
                party_name = 'Mr. & Mrs. ' + party_name
            elif guests == 'Family':
                party_name = party_name + ' and Family'
            print phone_numbers
            if not party_name:
                print 'skipping row {}'.format(row)
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            functions = function.split('+')
            print functions
            for function in functions:
                found_function = Function.objects.get(name=function)
                party.function.add(found_function)
            # party.type = party_type
            # party.category = category
            party.is_invited = True
            party.groom_invite = True if groom_invite == 'TRUE' else False
            if not party.invitation_id:
                party.invitation_id = uuid.uuid4().hex
            party.save()
            for number in phone_numbers:
                if not number == '':
                    guest, create = Guest.objects.get_or_create(party=party, phone_number=number)
                    guest.save()


def export_guests():
    WHATSAPP_PREFIX = 'https://api.whatsapp.com/send?phone={0}&text={1}'
    INVITATION_SMS_TEMPLATE = 'Hi *_{0}_*. Siddharth and Shreya are getting hitched on 8th Jan. We would love to have you bless us with your presence. Kindly click on this link for your invitation here {1}.'
    headers = [
        'party_name', 'phone_number', 'invite_message', 'whatsapp_link'
    ]
    file = StringIO.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        print party.name
        invite_message = INVITATION_SMS_TEMPLATE.format(party.name, party.invitation_link)
        for guest in party.guest_set.all():
            whatsapp_link = WHATSAPP_PREFIX.format(guest.phone_number, invite_message)
            writer.writerow([
                party.name,
                guest.phone_number[1:],
                invite_message,
                whatsapp_link
            ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
