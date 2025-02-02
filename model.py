from tensorflow import keras
import numpy as np 
from sklearn.model_selection import train_test_split
from keras import layers

def predict_land_use(self, name, place_type):
        """Predict land use using the trained RNN model"""
        try:
            if self.model is None or self.tokenizer is None:
                prediction = self.classify_land_use(name, place_type)
                return prediction, 'rule-based'

            # Prepare input
            combined_text = f"{name} {place_type}"
            
            # Convert text to sequence
            X_sequence = self.tokenizer.texts_to_sequences([combined_text])
            
            # Pad sequence to match the training length
            X_padded = keras.preprocessing.sequence.pad_sequences(
                X_sequence,
                maxlen=20,  # Should match the max_sequence_length used in training
                padding='post'
            )
            
            # Get prediction
            pred = self.model.predict(X_padded, verbose=0)
            pred_class = np.argmax(pred[0])
            
            # Get confidence score
            confidence = float(pred[0][pred_class])
            
            # Use rule-based fallback if confidence is too low
            confidence_threshold = 0.5  # Adjust this threshold as needed
            if confidence < confidence_threshold:
                prediction = self.classify_land_use(name, place_type)
                return prediction, 'rule-based'
            
            prediction = self.reverse_mapping.get(pred_class, "Others")
            return prediction, 'model'
        
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            prediction = self.classify_land_use(name, place_type)
            return prediction, 'rule-based'


def initialize_model(self):
        try:
            if self.df is None or len(self.df) == 0:
                print("No data available for model initialization")
                return

            # Feature Extraction
            self.df['land_use'] = self.df.apply(lambda row: self.classify_land_use(row['name'], row['place_type']), axis=1)
            self.df['name_place'] = self.df['name'] + " " + self.df['place_type'].fillna('')
            
            # Convert text to sequences using tokenizer
            self.tokenizer = keras.preprocessing.text.Tokenizer(num_words=1000)
            self.tokenizer.fit_on_texts(self.df['name_place'])
            X_sequences = self.tokenizer.texts_to_sequences(self.df['name_place'])
            
            # Pad sequences to ensure uniform length
            max_sequence_length = 20  # You can adjust this based on your data
            X_padded = keras.preprocessing.sequence.pad_sequences(
                X_sequences, 
                maxlen=max_sequence_length,
                padding='post'
            )
            
            # Ensure land_use column exists and has values
            if 'land_use' not in self.df.columns or self.df['land_use'].isna().all():
                self.df['land_use'] = self.df.apply(
                    lambda x: self.classify_land_use(x['name'], x['place_type']), 
                    axis=1
                )
            
            # Get unique land use categories and create label mapping
            unique_land_uses = sorted(self.df['land_use'].unique())
            self.label_mapping = {label: idx for idx, label in enumerate(unique_land_uses)}
            class_counts = self.df['land_use'].value_counts()
            
            # Convert labels to numeric values
            y = np.array([self.label_mapping[label] for label in self.df['land_use']])
            
            # Ensure we have enough samples and more than one class
            if len(y) < 32 or len(unique_land_uses) < 2:
                print(f"Warning: Insufficient data for training. Samples: {len(y)}, Classes: {len(unique_land_uses)}")
                return

            # Train-test split
            X_train, self.X_test, y_train, self.y_test = train_test_split(
                X_padded, y, 
                train_size=0.7, 
                test_size=0.3, 
                random_state=42,
                stratify=y
            )

            # Define RNN model architecture
            num_classes = len(unique_land_uses)
            vocab_size = len(self.tokenizer.word_index) + 1  # Add 1 for padding token
            
            self.model = keras.Sequential([
                layers.Embedding(vocab_size, 100, input_length=max_sequence_length),
                layers.Bidirectional(layers.LSTM(128, return_sequences=True)),
                layers.Dropout(0.3),
                layers.Bidirectional(layers.LSTM(64)),
                layers.Dropout(0.2),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.1),
                layers.Dense(num_classes, activation='softmax')
            ])

            # Compile model
            self.model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )

            # Save initial model architecture summary
            self.model_summary = []
            self.model.summary(print_fn=lambda x: self.model_summary.append(x))

            # Use class weights to handle imbalanced data
            class_weights = {}
            class_counts = np.bincount(y_train)
            total_samples = len(y_train)
            for i in range(len(class_counts)):
                class_weights[i] = total_samples / (len(class_counts) * class_counts[i])

            # Training with early stopping and history tracking
            early_stopping = keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )

            self.history = self.model.fit(
                X_train,
                y_train,
                epochs=2,
                batch_size=32,
                validation_split=0.2,
                callbacks=[early_stopping],
                class_weight=class_weights,
                verbose=1
            )

            # Evaluate model
            self.test_loss, self.test_accuracy = self.model.evaluate(self.X_test, self.y_test, verbose=0)
            print(f"\nModel Training Completed Successfully!")
            print(f"Test Accuracy: {self.test_accuracy:.4f}")

            # Generate predictions for confusion matrix
            y_pred = self.model.predict(self.X_test)
            self.y_pred_classes = np.argmax(y_pred, axis=1)

            # Save reverse mapping for later use
            self.reverse_mapping = {v: k for k, v in self.label_mapping.items()}

        except Exception as e:
            print(f"Model initialization error: {str(e)}")
            self.model = None