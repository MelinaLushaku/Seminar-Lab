from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from Books.models import Book


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the books data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from books.csv, users.csv, ratings.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Book.objects.exists():
            print('book data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading book data")
        reader = DictReader(open('books.csv', 'r'), delimiter=';')
        #Code to load the data into database
     
        for row in reader:
            book = Book(
                isbn = row['ISBN'],
                title = row['Book-Title'],
                author = row['Book-Author'],
                yearOfPublication = row['Year-Of-Publication'],
                publisher = row['Publisher'],
            )

            book.save()