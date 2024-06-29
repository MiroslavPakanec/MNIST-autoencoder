### Common Issue Log: 
Torch doesn't recognize GPU in a container
- Error: CUDA initialization: Unexpected error from cudaGetDeviceCount()
- Context: 'nvidia-smi' and 'nvcc --version' worked, but 'torch.cuda.is_available()' did not.
- Solution: Downgrading Nvidia GPU driver from 556.12 to 552.44
