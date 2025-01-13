import pygame
import time

from ffrontier.managers import asset_manager

pygame.init()

am = asset_manager.AssetManager()
# Load grasslands image 50 times
scale = 100
number = 100
in_use = 90
start_time = time.time()
for i in range(number):
    am.load_image('tests/testing_assets/grasslands.png', f'grasslands{i}', scale=scale)
end_time = time.time()

print(f"Time to load {number} images: {end_time - start_time:.4f} seconds")

for i in range(10):
    scale += 5
    # Measure rescaling time
    for j in range(in_use):
        am.in_use.add(f'grasslands{j}')
    start_time = time.time()
    am.rescale_images(scale=scale)
    end_time = time.time()

    print(f"Time to rescale {number} images: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    for j in range(in_use):
        am.get_scaled_image(f'grasslands{j}')
        for t in range(5):
            am.get_scaled_image(f'grasslands{t+in_use}')
    end_time = time.time()

    am.reset_in_use()

    print(f"Time to get {in_use} images: {end_time - start_time:.4f} seconds")


pygame.quit()
