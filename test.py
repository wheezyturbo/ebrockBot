import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Flatten
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Sample dataset with names and labels (0 for male, 1 for female)
names = ["John", "Jane", "Michael", "Emma", "William", "Olivia"]
labels = [0, 1, 0, 1, 0, 1]

# Tokenize and pad names
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(names)
vocab_size = len(tokenizer.word_index) + 1
max_length = max([len(name) for name in names])

# Convert names to sequences and pad them
sequences = tokenizer.texts_to_sequences(names)
padded_names = pad_sequences(sequences, maxlen=max_length, padding='post')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(padded_names, labels, test_size=0.2, random_state=42)

# Build a simple neural network model
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=8, input_length=max_length))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=2, verbose=1)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Predict gender based on a new name
new_names = ["Sophia", "Jacob"]
new_sequences = tokenizer.texts_to_sequences(new_names)
new_padded_names = pad_sequences(new_sequences, maxlen=max_length, padding='post')
predictions = model.predict(new_padded_names)
for name, prediction in zip(new_names, predictions):
    gender = "Female" if prediction >= 0.5 else "Male"
    print(f"Name: {name}, Predicted Gender: {gender}")
