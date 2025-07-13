import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Blog


class Command(BaseCommand):
    help = 'Create dummy blog data using Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Number of blog entries to create'
        )

    def handle(self, *args, **options):
        fake = Faker('ja_JP')
        count = options['count']
        
        categories = ['news', 'poem']
        
        for i in range(count):
            category = random.choice(categories)
            
            if category == 'news':
                title = fake.sentence(nb_words=6)
                content = fake.text(max_nb_chars=1000)
            else:
                title = fake.sentence(nb_words=4)
                content = '\n'.join([fake.sentence(nb_words=8) for _ in range(4)])
            
            Blog.objects.create(
                title=title,
                content=content,
                category=category
            )
            
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Created {i + 1} blog entries...')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} blog entries')
        )
