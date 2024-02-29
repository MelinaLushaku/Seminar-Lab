import numpy
import pandas
from .models import Book, User, Rating
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    books = []
    users = []
    ratings = []
    ratignsWithBooks = None
    pivotTable = []
    similarityScores = []

    def __init__(self):
        self.books = pandas.DataFrame(list(Book.objects.all().values()))
        self.users = pandas.DataFrame(list(User.objects.all().values()))
        self.ratings = pandas.DataFrame(list(Rating.objects.all().values()))
        self.ratignsWithBooks = self.ratings.merge(self.books, on='isbn')

    def getPopularBooks(self):
        numberOfRatingsDF = self.ratignsWithBooks.groupby('title').count()['rating'].reset_index()
        numberOfRatingsDF.rename(columns={'rating': 'Num-of-ratings'}, inplace=True)
        
        averageRatingsDf = self.ratignsWithBooks.groupby('title')['rating'].mean().reset_index()
        averageRatingsDf.rename(columns={'rating': 'avg_rating'}, inplace=True)
        
        popularDf = numberOfRatingsDF.merge(averageRatingsDf, on="title")
        popularDf = popularDf[popularDf['Num-of-ratings']>=250].sort_values('avg_rating', ascending=False).head(50)
        popularDf = popularDf.merge(self.books, on='title').drop_duplicates('title')[['title', 'author', 'Num-of-ratings', 'avg_rating']]
        return popularDf
    
    def calculateSimilarityScores(self):
        x = self.ratignsWithBooks.groupby('user_id').count()['rating'] > 0
        usersWithRatings = x[x].index
        filteredRatings = self.ratignsWithBooks[self.ratignsWithBooks['user_id'].isin(usersWithRatings)]
        y = filteredRatings.groupby('title').count()['rating']>0
        popularBooks = y[y].index
        finalRatings = filteredRatings[filteredRatings['title'].isin(popularBooks)]
        self.pivotTable = finalRatings.pivot_table(index='title', columns='user_id', values='rating')
        self.pivotTable.fillna(0, inplace=True)
        self.similarityScores = cosine_similarity(self.pivotTable)

    def getRecommendedBooks(self, bookName):
        self.calculateSimilarityScores()
        bookIndex = numpy.where(self.pivotTable.index == bookName)
        recommended_books = []
        if (len(bookIndex[0]) == 0):
            print('No such book, check your spelling')
        else: 
            similar_items = sorted(list(enumerate(self.similarityScores[bookIndex[0][0]])), key= lambda x:x[1], reverse=True)[1:6]
            for item in similar_items:
                book = Book.objects.get(title=self.pivotTable.index[item[0]])
                recommended_books.append(book)
        return recommended_books
