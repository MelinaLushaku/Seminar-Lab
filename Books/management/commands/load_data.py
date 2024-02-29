from csv import DictReader
from django.core.management import BaseCommand

## Reference for creating `load_data` custom command to populate database with dataset: 
## https://adityakedawat.medium.com/importing-csv-file-into-django-models-using-django-management-command-716eda305e61

# Import the model 
from Books.models import Book, Rating, User
import names

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
        
        if Rating.objects.exists():
            print('rating data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        if User.objects.exists():
            print('user data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading book data...")

        limit = 1000
        count = 0
        reader = DictReader(open('books.csv', 'r'), delimiter=';')
        #Code to load the data into database
        for row in reader:
            if (count < limit):
                count +=1
                book = Book(
                    isbn = row['ISBN'],
                    title = row['Book-Title'],
                    author = row['Book-Author'],
                    imageUrl = row['Image-URL-M'],
                    yearOfPublication = row['Year-Of-Publication'],
                    publisher = row['Publisher'],
                )

                book.save()
        print("Loading Book Data...    DONE")
        
        count = 0
        print("Loading Users Data...")
        reader = DictReader(open('users.csv', 'r'), delimiter=';')
        #Code to load the data into database
        for row in reader:
            if (count < limit):
                count +=1
                user = User(
                    id = row['User-ID'],
                    firstName = names.get_first_name(),
                    lastName = names.get_last_name(),
                )

                user.save()
        print("Loading Users Data...   DONE")
        
        limit = 4000
        count = 0
        print("Loading Ratings Data...")
        reader = DictReader(open('ratings.csv', 'r'), delimiter=';')
        #Code to load the data into database
        for row in reader:
            if (count < limit):
                if (int(row['User-ID']) <= 1000):
                    count +=1
                    user = User.objects.get(id=row['User-ID'])
                    if (user is not None):
                        count +=1
                        rating = Rating(
                            user = user,
                            isbn = row['ISBN'],
                            rating = row['Book-Rating'],
                        )

                        rating.save()
        print("Loading Ratings Data...   DONE")
