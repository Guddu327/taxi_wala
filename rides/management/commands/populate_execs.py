import random
from faker import Faker
from django.core.management.base import BaseCommand
from rides.models import Executive, Cab, User
from rides.utils.generator_util import GeneratorMod
from rides.utils.license_plate import License

class Command(BaseCommand):

    shift_options = (('M','08:00 - 17:00'),('E','16:00 - 01:00'),('N','00;00 - 09:00'))
    fakegen = Faker()

    # topics = ['Search','Social','Marketplace','News','Games']

    # def add_topic():
    #     s = random.randint(0,3)
    #     return s
    lic = License() 
    gu = GeneratorMod()
    def populate(self, n=2):

        for _ in range(n):

            shift = self.shift_options[random.randint(0, 2)]
            name = self.fakegen.name()
            pas_ = self.gu.get_random_string(10)
            uname = self.gu.generate_username(name)
            car_number = self.lic.generate_license_plate()
            cab = Cab.objects.create(number=car_number)

            user = User.objects.create(username=uname, name=name, password=pas_, is_ex=True, is_rider=False)

            Executive.objects.create(user=user, car=cab, shift=shift)

    def handle(self, **kwargs):
        self.populate(15)