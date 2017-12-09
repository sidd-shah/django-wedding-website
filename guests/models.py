from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun'),
    ('dimagi', 'dimagi'),
]


def _random_uuid():
    return uuid.uuid4().hex

class Function(models.Model):
    FUNCTIONS = (
        ('Shreya Mehendi', 'Shreya Mehendi'),
        ('Sid Mehendi', 'Sid Mehendi'),
        ('Wedding', 'Wedding'),
        ('Celebration', 'Celebration')
    )
    name = models.CharField(max_length=100,choices=FUNCTIONS)

    def __str__(self):
        return self.name

class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    function = models.ManyToManyField(Function)
    type = models.CharField(max_length=10, choices=ALLOWED_TYPES, blank=True, null=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(default=False)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    comments = models.TextField(null=True, blank=True)
    groom_invite = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('-date')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return filter(None, self.guest_set.values_list('email', flat=True))

    @property
    def invitation_link(self):
        return "http://sidheartshreya.com/invite/"+self.invitation_id



MEALS = [
    ('beef', 'cow'),
    ('fish', 'fish'),
    ('hen', 'hen'),
    ('vegetarian', 'vegetable'),
]


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey(Party)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(unique=True, validators=[phone_regex], max_length=15, blank=True)
    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    # @property
    # def unique_id(self):
    #     # convert to string so it can be used in the "add" templatetag
    #     return unicode(self.pk)
    #
    # def __unicode__(self):
    #     return 'Guest: {} {}'.format(self.first_name, self.last_name)

    @property
    def whatsapp_message(self):
        WHATSAPP_PREFIX = 'https://api.whatsapp.com/send?phone={0}&text={1}'
        INVITATION_SMS_TEMPLATE = 'Hi *_{0}_*. Siddharth and Shreya are getting hitched on 8th Jan. We would love to have you bless us with your presence. Kindly click on this link for your invitation here {1}'
        invite_message = INVITATION_SMS_TEMPLATE.format(self.party.name, self.party.invitation_link)
        invite_message = invite_message.replace(" ", "%20")
        invite_message = invite_message.replace("&", "%26")
        print invite_message
        return WHATSAPP_PREFIX.format(self.phone_number[1:], invite_message)

    @property
    def functions(self):
        functions = ",".join([function.name for function in self.party.function.all()])
        return functions