import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def get_sample_image(sample_x: np.ndarray, sample_y: np.ndarray) -> bytes:
    sample_x = sample_x.reshape(28, 28)
    sample_y = sample_y.reshape(28, 28)

    _, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(sample_x, cmap='gray')
    axs[0].set_title('Sample X')
    axs[0].axis('off')

    axs[1].imshow(sample_y, cmap='gray')
    axs[1].set_title('Sample Y')
    axs[1].axis('off') 

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()