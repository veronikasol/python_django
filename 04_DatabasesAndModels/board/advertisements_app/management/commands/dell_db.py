from django.core.management.base import BaseCommand, CommandError
from advertisements_app.models import Advertisement

class Command(BaseCommand):
    help = 'Deletes items from ads_list if there is more than 5'
    
    def handle(self, *args, **options):
        self.stdout.write("Deleting items from the Advertisements table....")
        count = Advertisement.objects.count()
        if count > 5:
            for i in range(5,count):
                del_ad = Advertisement(id=i)
                del_ad.delete()
        self.stdout.write("Complete!")