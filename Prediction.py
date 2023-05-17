#import important Liraries
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import requests

#convert csv file into pandas dataframe
df = pd.read_csv('BBC_News_Train.csv')

# Split the dataset into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)


# Convert the raw text into numerical features using TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust the number of features as needed

# Fit the vectorizer on the training data and transform the training data
X_train = vectorizer.fit_transform(train_df['Text'])

# Transform the testing data using the fitted vectorizer
X_test = vectorizer.transform(test_df['Text'])


# Train a classification model, such as logistic regression, using the vectorized data
model = LogisticRegression()

# Fit the model on the training data
model.fit(X_train, train_df['Category'])


# Now, given a new news article, you can predict its category
def predict_category(article_url):

    # Scrape the article content from the provided URL
    # Use requests library to retrieve the HTML content of the article page
    response = requests.get(article_url)

    # Use BeautifulSoup library to extract the article text from the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    article_text = soup.get_text()

    # Transform the article text using the fitted vectorizer
    article_vectorized = vectorizer.transform([article_text])

    # Predict the category of the article using the trained model
    predicted_category = model.predict(article_vectorized)[0]

    return predicted_category
