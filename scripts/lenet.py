"""
# LeNet-5 Implementation on MNIST
# =============================================================================
#
# This script demonstrates how to train a LeNet-5 Convolutional Neural Network (CNN) 
# on the MNIST dataset using PyTorch. The MNIST dataset consists of 28x28 grayscale 
# images of handwritten digits (0-9).
#
# The LeNet-5 architecture is a classic CNN designed by Yann LeCun et al. (1998).
# It consists of two convolutional layers, each followed by a pooling layer, and 
# then three fully connected layers.
#
# This implementation covers:
# 1. Setting up the environment and hyperparameters
# 2. Defining the LeNet neural network architecture
# 3. Loading and transforming the MNIST dataset
# 4. Defining the training loop
# 5. Training the model and tracking accuracy
# 6. Saving the trained model
"""

import torch
import os
import torch.nn as nn

# This is here simply to demonstrate installing new package
# import cowsay

from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import v2 as transforms
from torchmetrics.classification import MulticlassAccuracy

# -----------------------------------------------------------------------------
# 2. Hyperparameters and Device Configuration
# -----------------------------------------------------------------------------
# These parameters control the training process:
# - LEARNING_RATE: How much the model weights are adjusted during each step.
# - EPOCHS: Number of times the entire dataset is passed through the network.
# - BATCH_SIZE: Number of samples processed before the model is updated.
#
# We also check for CUDA availability to ensure we are training on a GPU, 
# which is much faster than a CPU for these tasks.
# -----------------------------------------------------------------------------

LEARNING_RATE = 0.01
EPOCHS = 20
BATCH_SIZE = 128
NUM_CPU = os.cpu_count()

print('torch.__version__:', torch.__version__)
assert torch.cuda.is_available(), "CUDA is not available. Training on CPU is for dimwits. Exiting."
device = "cuda:0"

DATA_PATH = os.environ.get("LOCAL_SCRATCH", "./data")
DATA_PATH = os.path.expandvars(DATA_PATH)
print(f"Using data path: {DATA_PATH}")

# -----------------------------------------------------------------------------
# 3. Defining the Neural Network Architecture (LeNet-5)
# -----------------------------------------------------------------------------
# We define the LeNet model class which inherits from nn.Module. 
# It consists of sequential layers that transform the input image into predictions. 
#
# Key components:
# - Conv2d: Convolutional layers for feature extraction (filters slide over the image).
# - ReLU: Activation function to introduce non-linearity.
# - MaxPool2d: Pooling layers to reduce spatial dimensions (downsampling).
# - Linear: Fully connected layers for the final classification.
# -----------------------------------------------------------------------------

class LeNet(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()

        # Conv1: 28x28x1 -> 28x28x20
        # Padding=2 to maintain 28x28 size with 5x5 kernel
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=20, kernel_size=5, padding=2)
        self.act1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Conv2: 14x14x20 -> 14x14x50
        # Padding=2 to maintain 14x14 size with 5x5 kernel
        self.conv2 = nn.Conv2d(in_channels=20, out_channels=50, kernel_size=5, padding=2)
        self.act2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # FC1: 7x7x50 -> 500
        self.fc1 = nn.Linear(in_features=50 * 7 * 7, out_features=500)
        self.act3 = nn.ReLU()

        # FC2: 500 -> 10
        self.fc2 = nn.Linear(in_features=500, out_features=num_classes)

    def forward(self, x):
        # Block 1
        x = self.pool1(self.act1(self.conv1(x)))

        # Block 2
        x = self.pool2(self.act2(self.conv2(x)))

        # FC Layers
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.act3(x)
        x = self.fc2(x)

        return x

# -----------------------------------------------------------------------------
# 4. Model Instantiation & Device Placement
# -----------------------------------------------------------------------------
# We create an instance of the LeNet class and move the model to the target device.
# For neural networks, moving computations to a GPU (cuda) significantly speeds up 
# training.
# -----------------------------------------------------------------------------

model = LeNet(num_classes=10)
model = model.to(device)


# -----------------------------------------------------------------------------
# 5. Data Augmentation and Normalization
# -----------------------------------------------------------------------------
# Data preprocessing is crucial for effective training. We define transformations:
# - Normalization: Scales pixel values (0-255) to a standard range (using mean/std).
# - Data Augmentation (Train only): Applies random transformations (e.g. rotation) 
#   to artificially increase the training set size and improve robustness.
# -----------------------------------------------------------------------------

# MNIST stats (mean and std for normalization)
MNIST_MEAN = (0.1307,)
MNIST_STD = (0.3081,)

train_transform = transforms.Compose(
    [
        transforms.RandomRotation(10),  # Slight rotation for augmentation
        transforms.ToImage(),  # convert PIL/ndarray -> v2 image
        transforms.ToDtype(torch.float32, scale=True),
        transforms.Normalize(MNIST_MEAN, MNIST_STD),
    ]
)

test_transform = transforms.Compose(
    [
        transforms.ToImage(),
        transforms.ToDtype(torch.float32, scale=True),
        transforms.Normalize(MNIST_MEAN, MNIST_STD),
    ]
)

# -----------------------------------------------------------------------------
# 6. MNIST Dataset and DataLoaders
# -----------------------------------------------------------------------------
# We load the MNIST dataset from torchvision.datasets.
# - trainset: Includes training images and labels.
# - testset: Used to evaluate the model's performance on unseen data.
#
# DataLoader:
# Wraps the dataset and provides an iterable over the given dataset.
# It supports automatic batching, sampling, shuffling and multiprocess data loading.
#
# - batch_size: Number of samples per batch (e.g., 128 images at once).
# - shuffle=True: Shuffles the training data at every epoch to prevent the model 
#   from learning the order of the data.
# -----------------------------------------------------------------------------

# Download and load the training data
print("[INFO] accessing MNIST...")
trainset = datasets.MNIST(
    DATA_PATH, download=True, train=True, transform=train_transform
)
testset = datasets.MNIST(
    DATA_PATH, download=True, train=False, transform=test_transform
)

# Create data loaders
trainloader = DataLoader(
    trainset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    persistent_workers=True,
    num_workers=NUM_CPU,
)
testloader = DataLoader(
    testset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    persistent_workers=True,
    num_workers=NUM_CPU,
)

# -----------------------------------------------------------------------------
# 7. Training Function (Single Epoch)
# -----------------------------------------------------------------------------
# This function handles the training process for one full pass through the dataset.
# It iterates over the DataLoader, computes the loss, performs backpropagation, 
# and updates the model's weights.
#
# Key Steps:
# 1. model.train(): Set the model to training mode (important for certain layers).
# 2. optimizer.zero_grad(): Clear gradients from the previous step.
# 3. outputs = model(inputs): Forward pass (compute predictions).
# 4. loss = criterion(...): Calculate the error (loss) between predictions and labels.
# 5. loss.backward(): Compute gradients (how much each weight contributed to error).
# 6. optimizer.step(): Update weights using the optimizer and computed gradients.
# -----------------------------------------------------------------------------

def train_epoch(model, train_loader, criterion, optimizer, metric, device):
    """Train the model for one epoch.

    Args:
        metric: A torchmetrics metric instance (e.g., MulticlassAccuracy)

    Returns:
        tuple: (average_loss, accuracy)
    """
    model.train()
    metric.reset()
    total_loss = 0.0

    for batch_idx, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        # Update metric with predictions
        metric.update(outputs, labels)

        # Print batch loss every 50 batches
        if batch_idx % 50 == 0:
            print(f"Batch {batch_idx}/{len(train_loader)} - Loss: {loss.item():.4f}")

    avg_loss = total_loss / len(train_loader)
    accuracy = metric.compute().item()
    return avg_loss, accuracy

# -----------------------------------------------------------------------------
# 8. Loss Function and Optimizer Setup
# -----------------------------------------------------------------------------
# We define how the model's errors are calculated and how its weights are updated.
#
# - CrossEntropyLoss: Standard loss for multi-class classification problems.
#   (It effectively combines LogSoftmax and NLLLoss).
# - SGD (Stochastic Gradient Descent): The optimization algorithm.
#    Momentum helps accelerate gradient vectors in the right directions.
# - MulticlassAccuracy: A metric to track the proportion of correct predictions.
# -----------------------------------------------------------------------------

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=0.9)
accuracy_metric = MulticlassAccuracy(num_classes=10).to(device)

# -----------------------------------------------------------------------------
# 9. Main Training Loop
# -----------------------------------------------------------------------------
# We loop over the dataset multiple times (EPOCHS). In each epoch:
# 1. We call train_epoch() to perform forward and backward passes.
# 2. We print the average loss and accuracy to monitor progress.
#
# Note: For a real-world scenario, you would also evaluate on the test set 
# (testloader) after every epoch to check for overfitting.
# -----------------------------------------------------------------------------

print("[INFO] training network...")
for epoch in range(EPOCHS):
    # Training phase
    train_loss, train_acc = train_epoch(
        model, trainloader, criterion, optimizer, accuracy_metric, device
    )

    # Print progress every epoch since
    # the model is expected to find a proper solution fairly quickly.
    print(f"Epoch [{epoch+1}/{EPOCHS}] - "
          f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")

trained_model = model
print("[INFO] training complete!")

# -----------------------------------------------------------------------------
# 10. Saving the Model Checkpoint
# -----------------------------------------------------------------------------
# After training completes, we save the application state to a file.
# The checkpoint dictionary contains:
# - 'epoch': The total number of epochs run.
# - 'model_state_dict': The trained weights and biases of the model.
#
# This allows us to reload the model later for inference (predictions) or 
# to resume training from this point.
# -----------------------------------------------------------------------------

# Define a path for the full checkpoint
checkpoint_path = 'models/MNIST_make_your_own_versioning_stragegy.pth'

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

# Save a dictionary containing all necessary state
torch.save({
    'epoch': EPOCHS,
    'model_state_dict': trained_model.state_dict(),
}, checkpoint_path)

print(f"Trained model saved to: {checkpoint_path}")