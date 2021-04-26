from django.core.management.base import BaseCommand, CommandError
from advertisements_app.models import Advertisement

class Command(BaseCommand):
    help = 'Adds items to ads_list'
    
    def handle(self, *args, **options):
        self.stdout.write("Adding items to the Advertisements table....")
        count = Advertisement.objects.count()
        for i in range(count+1,count+501):
            new_ad = Advertisement(title="Объявление %s"%(str(i)))
            new_ad.save()
        self.stdout.write("Complete!")