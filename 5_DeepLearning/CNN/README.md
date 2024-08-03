### Convolutional Neural Network (CNN)
Please see this for Slides
https://github.com/tharhtetsan/zero_2_hero_ml/tree/main/7_Deep_Learning/CNN




### Convolutional Layers
```bash
  parameters=( F×F × C_in +1 ) × C_out
```
​

- F: Filter size (height and width, assuming square filters).
- C_in : Number of input channels.
- 𝐶_out: Number of output channels (or filters).
- 1: This accounts for the bias term for each output channel.


###  Fully Connected (Dense) Layers
```bash
  parameters=( N_in + 1 ) × N_out
```
​- N_in: Number of input neurons.
- 𝑁_out : Number of output neurons.
- 1: This accounts for the bias term for each output neuron.