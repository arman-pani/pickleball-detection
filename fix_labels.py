import csv
import sys

import pandas as pd

try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    if not inputFile or not outputFile:
        raise ValueError("Missing input or output file")
except:
    print('Usage: python3 Rearrange_Label.py <inputFile> <outputFile>')
    sys.exit(1)

# Read CSV
df = pd.read_csv(inputFile)

# Extract frame numbers
frames = df["Frame"].tolist()
ball_status = df["Ball"].tolist()
x_values = df["x"].tolist()
y_values = df["y"].tolist()

# Define visibility based on 'Ball' column
visibility = [1 if ball == 1 else 0 for ball in ball_status]

# Create DataFrame
df_label = pd.DataFrame({
    "Frame": frames,
    "Visibility": visibility,
    "X": x_values,
    "Y": y_values
})

# Ensure missing frames are handled
all_frames = list(range(0, max(frames) + 1))
existing_frames = set(frames)

for frame in all_frames:
    if frame not in existing_frames:
        df_label = df_label.append({
            "Frame": frame,
            "Visibility": 0,
            "X": -1.000,
            "Y": -1.000
        }, ignore_index=True)

# Sort by frame number
df_label = df_label.sort_values(by="Frame")

# Convert Frame column to integer
df_label["Frame"] = df_label["Frame"].astype(int)

# Save to CSV
df_label.to_csv(outputFile, index=False)

print(f"Processed labels saved to {outputFile}")
