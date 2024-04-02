import tensorflow as tf
import os
import random
import keras
from sklearn.model_selection import train_test_split
from keras import layers, models, optimizers

def load_and_preprocess_data(category1, category2, base_dir='./static/images/album', img_size=(128, 128)):
    """
    Load images from the directories of two categories, preprocess and augment them,
    and prepare training and validation datasets.

    Parameters:
    - category1: Name of the first category.
    - category2: Name of the second category.
    - base_dir: Base directory where the category folders are located.
    - img_size: Tuple indicating the size of the images after resizing.

    Returns:
    - train_ds: Training dataset with data augmentation.
    - val_ds: Validation dataset without data augmentation.
    """
    # Paths to category directories
    cat1_dir = os.path.join(base_dir, category1)
    cat2_dir = os.path.join(base_dir, category2)


    # Assuming target_size=(128, 128) as the desired size for all images

    # Data augmentation for the training data
    train_data_gen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2  # Use 20% of images as a validation set
    )
    
    # Only rescaling for the validation data, but resizing is implied in the flow_from_directory method
    val_data_gen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_ds = train_data_gen.flow_from_directory(
        base_dir,
        classes=[category1, category2],
        target_size=img_size,
        batch_size=32,
        class_mode='binary',
        subset='training'
    )

    val_ds = val_data_gen.flow_from_directory(
        base_dir,
        classes=[category1, category2],
        target_size=img_size,
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )

    return train_ds, val_ds



def build_model():
    model = models.Sequential()
    # Assuming images are 128x128 RGB
    model.add(layers.InputLayer(input_shape=(128, 128, 3)))
    
    # First Convolutional Layer
    model.add(layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    
    # Second Convolutional Layer
    model.add(layers.Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    
    # Third Convolutional Layer
    model.add(layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    
    # Flatten the output to feed into the Dense layer
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))  # Dense layer
    model.add(layers.Dense(1, activation='sigmoid'))  # Output layer for binary classification
    
    return model


def train_and_get_info(category1, category2):
    # Build the model
    model = build_model()

    # Compile the model
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

    # Summary of the model
    model.summary()

    train_ds, val_ds = load_and_preprocess_data(category1, category2)

    # Train the model
    history = model.fit(train_ds, validation_data=val_ds, epochs=32, batch_size=32)  # Adjust epochs and batch_size as necessary

    mod_name = f"Mod_{category1}_{category2}"
    model.save(f'./static/models/{mod_name}.keras')
    # For training accuracy of the last epoch
    final_train_accuracy = history.history['accuracy'][-1]
    print(f"Final Training Accuracy: {final_train_accuracy:.4f}")
    
    # For validation accuracy of the last epoch, if you have a validation set
    final_val_accuracy = history.history['val_accuracy'][-1]
    accuracy_model = f'{final_val_accuracy:.4}'
    return accuracy_model
    


# mod = keras.models.load_model(f'./static/models/{mod_name}.keras')

