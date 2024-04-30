from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# Updated training data
training_data = [
    ("create a new file", "create_file"),
    ("delete the old file", "delete_file"),
    ("edit the document", "modify_file"),
    ("add a new slide", "add_slide"),
    ("remove a slide", "remove_slide"),
    ("add a slide with URL", "add_slide_url"),
    ("add an image with URL", "add_image_url"),
    ("change content in slide 2", "change_content_slide_2"),
]
texts, labels = zip(*training_data)

# Re-create TF-IDF vectorizer and Naive Bayes classifier
vectorizer = TfidfVectorizer()
clf = MultinomialNB()

# Train the classifier with the updated dataset
features = vectorizer.fit_transform(texts)
clf.fit(features, labels)

# Classify new user input
user_input = "add content to slide 4 from wikipedia.org"
features = vectorizer.transform([user_input])
intent = clf.predict(features)[0]
print(intent)  # Output: remove_slide
