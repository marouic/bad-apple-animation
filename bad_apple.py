import cv2
import pygame
import numpy as np
import random

# =========================
# SETTINGS
# =========================
VIDEO_PATH = "bad_apple.mp4"
SCALE = 6              # Higher = fewer objects, faster
FPS = 30
THRESHOLD = 100        # Lower = more white

# =========================
# LOAD VIDEO
# =========================
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

grid_w = width // SCALE
grid_h = height // SCALE

# =========================
# INIT PYGAME
# =========================
pygame.init()
screen = pygame.display.set_mode((grid_w * SCALE, grid_h * SCALE))
pygame.display.set_caption("Bad Apple - Random Object Renderer")
clock = pygame.time.Clock()

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Downscale
    small = cv2.resize(gray, (grid_w, grid_h))

    # Threshold (black & white)
    _, bw = cv2.threshold(small, THRESHOLD, 255, cv2.THRESH_BINARY)

    screen.fill((0, 0, 0))

    # Draw "random objects"
    for y in range(grid_h):
        for x in range(grid_w):
            value = bw[y, x]

            # Skip black pixels (optional optimization)
            if value == 0:
                continue

            # Random variation
            jitter_x = random.randint(-1, 1)
            jitter_y = random.randint(-1, 1)

            # Brightness affects size
            v = int(value)
            radius = int((v / 255) * (SCALE / 1.5))
            radius = max(1, radius)

            # Slight randomness in brightness
            color_variation = random.randint(-30, 30)
            color_val = int(value) + color_variation
            color_val = max(0, min(255, color_val))

            color = (color_val, color_val, color_val)

            # Position
            px = x * SCALE + SCALE // 2 + jitter_x
            py = y * SCALE + SCALE // 2 + jitter_y

            pygame.draw.circle(screen, color, (px, py), radius)

    pygame.display.flip()
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# =========================
# CLEANUP
# =========================
cap.release()
pygame.quit()