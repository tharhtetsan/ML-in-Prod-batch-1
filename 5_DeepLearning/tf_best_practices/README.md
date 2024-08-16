

## Improving TensorFlow CNN Accuracy: Best Variables to Tune
When working with Convolutional Neural Networks (CNNs) in TensorFlow, there are several hyperparameters and variables that you can tune to improve model accuracy.

### 1. **Learning Rate**
   - **Description**: Controls how much to change the model in response to the estimated error each time the model weights are updated.
   - **Typical Range**: `1e-4` to `1e-2`
   - **Tuning Tips**: Start with a lower learning rate and gradually increase. You can also use learning rate schedulers or adaptive learning rates.

### 2. **Batch Size**
   - **Description**: Number of training samples utilized in one iteration.
   - **Typical Range**: `16`, `32`, `64`
   - **Tuning Tips**: Larger batch sizes may lead to faster training but can also result in lower generalization. Smaller batch sizes can help in regularizing the model.

### 3. **Number of Epochs**
   - **Description**: Number of times the entire dataset is passed forward and backward through the network.
   - **Typical Range**: `10` to `100`
   - **Tuning Tips**: Monitor the validation accuracy to avoid overfitting. Use early stopping to prevent excessive training.

### 4. **Optimizer**
   - **Description**: Algorithm to change the attributes of the neural network such as weights and learning rate.
   - **Common Options**: `Adam`, `SGD`, `RMSprop`
   - **Tuning Tips**: `Adam` is generally a good starting point. For fine-tuning, consider trying `SGD` with momentum or learning rate decay.

### 5. **Dropout Rate**
   - **Description**: Prevents overfitting by randomly setting a fraction of input units to 0 at each update during training time.
   - **Typical Range**: `0.2` to `0.5`
   - **Tuning Tips**: Start with `0.5` and adjust depending on overfitting signs.

### 6. **Number of Filters in Convolutional Layers**
   - **Description**: Determines the number of output channels in convolutional layers.
   - **Typical Range**: `32`, `64`, `128`
   - **Tuning Tips**: More filters can capture more features but increase computation. Adjust based on the complexity of the task.

### 7. **Filter Size (Kernel Size)**
   - **Description**: Size of the convolutional filters.
   - **Typical Range**: `(3, 3)`, `(5, 5)`
   - **Tuning Tips**: Smaller filters capture more local features, while larger ones can capture broader features. Start with `(3, 3)` and adjust.

### 8. **Number of Convolutional Layers**
   - **Description**: Number of convolutional layers stacked in the model.
   - **Typical Range**: `2` to `5`
   - **Tuning Tips**: More layers allow capturing more complex patterns but can also lead to overfitting. Use with caution.

### 9. **Activation Function**
   - **Description**: Function applied to the output of each layer.
   - **Common Options**: `ReLU`, `Leaky ReLU`, `ELU`
   - **Tuning Tips**: `ReLU` is standard. Experiment with `Leaky ReLU` or `ELU` if you encounter dead neurons.

### 10. **Pooling Strategy**
   - **Description**: Reduces the spatial size of the representation to decrease computation and prevent overfitting.
   - **Common Options**: `MaxPooling`, `AveragePooling`
   - **Tuning Tips**: MaxPooling is more common, but AveragePooling can be beneficial in some scenarios.

### 11. **L2 Regularization**
   - **Description**: Penalizes large weights to prevent overfitting.
   - **Typical Range**: `1e-5` to `1e-2`
   - **Tuning Tips**: Apply to densely connected layers if overfitting is an issue.

### 12. **Data Augmentation**
   - **Description**: Techniques to artificially expand the size of the training dataset by creating modified versions of images.
   - **Common Techniques**: Rotation, flipping, zooming, shifting
   - **Tuning Tips**: Use `ImageDataGenerator` to apply augmentations and increase generalization.

### 13. **Learning Rate Scheduler**
   - **Description**: Dynamically adjusts the learning rate during training.
   - **Common Schedulers**: `ReduceLROnPlateau`, `ExponentialDecay`
   - **Tuning Tips**: Use `ReduceLROnPlateau` to lower the learning rate when the model plateaus.

### 14. **Early Stopping**
   - **Description**: Stops training when the validation loss stops improving.
   - **Tuning Tips**: Set `patience` to a reasonable number to avoid stopping too early.

### 15. **Model Architecture Complexity**
   - **Description**: Overall depth and structure of the network.
   - **Tuning Tips**: Start simple and gradually increase complexity. Monitor for overfitting and adjust accordingly.




## How to Run
```bash
conda create -n ths python==3.10
conda activate ths
which python3.10

```


Solve pipenv
```bash
pipenv clean
pipenv run python --version
# remove wrong python path
pipenv --rm
# set python path
pipenv --python /opt/anaconda3/envs/ths/bin/python3.10
```
