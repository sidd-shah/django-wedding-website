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
            party_name, first_name, last_name, party_type, function, phone_number, email = row[:8]
            if not party_name:
                print 'skipping row {}'.format(row)
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            functions = function.split('+')
            print functions
            for function in functions:
                found_function = Function.objects.get(name=function)
                party.function.add(found_function)
            party.type = party_type
            # party.category = category
            party.is_invited = True
            if not party.invitation_id:
                party.invitation_id = uuid.uuid4().hex
            party.save()
            if email:
                guest, created = Guest.objects.get_or_create(party=party, email=email)
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            if phone_number:
                guest.phone_number = phone_number
            # guest.is_child = _is_true(is_child)
            guest.save()


def export_guests():
    INVITATION_SMS_TEMPLATE = 'Hi *_{0}_*. Siddharth and Shreya are getting hitched on 8th Jan. We would love to have you bless us with your presence. Kindly click on this link for your invitation here {1}.'
    headers = [
        'party_name', 'first_name', 'last_name', 'email', 'comments', 'invite_message'
    ]
    file = StringIO.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        invite_message = INVITATION_SMS_TEMPLATE.format(party.name, party.invitation_link)
        for guest in party.guest_set.all():
            if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    guest.email,
                    party.comments,
                    invite_message,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
