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
    headers = [
        'party_name', 'first_name', 'last_name', 'party_type',
        'is_child', 'category', 'is_invited', 'is_attending',
        'rehearsal_dinner', 'meal', 'email', 'comments'
    ]
    file = StringIO.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    party.type,
                    guest.is_child,
                    party.category,
                    party.is_invited,
                    guest.is_attending,
                    party.rehearsal_dinner,
                    guest.meal,
                    guest.email,
                    party.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
