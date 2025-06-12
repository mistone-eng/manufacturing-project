from scipy.spatial.transform import Rotation as R
import numpy as np

# Example rotation vector [rx, ry, rz] from UR5e or RTDE
rotation_vector = np.array([0.1, -0.2, 0.3])  # Replace with your values

# Step 1: Convert rotation vector to rotation matrix
rotation = R.from_rotvec(rotation_vector)

# Step 2: Convert rotation matrix to Euler angles (RPY)
# 'xyz' -> Roll (X), Pitch (Y), Yaw (Z)
rpy_angles = rotation.as_euler('xyz', degrees=False)

# Print result
roll, pitch, yaw = rpy_angles
print(f"Roll: {roll:.4f}, Pitch: {pitch:.4f}, Yaw: {yaw:.4f}")
