import numpy as np

cyan_dots1 = np.array([[x1, y1, z1], [x2, y2, z2], ...])  
cyan_dots2 = np.array([[x1, y1, z1], [x2, y2, z2], ...])
cyan_dots3 = np.array([[x1, y1, z1], [x2, y2, z2], ...])
cyan_dots4 = np.array([[x1, y1, z1], [x2, y2, z2], ...])

all_cyan_dots = [cyan_dots1, cyan_dots2, cyan_dots3, cyan_dots4]

ref_center = np.array([x_ref, y_ref, z_ref])  

def error(cyan_dots, ref_center=ref_center):
    distances = np.linalg.norm(cyan_dots - ref_center, axis=1) # Euclidean distances
    mean_displacement = np.mean(distances) # Average displacement
    std_displacement = np.std(distances) # Standard deviation
    return mean_displacement, std_displacement

for i, cyan_dots in enumerate(all_cyan_dots):
    mean_displacement, std_displacement = error(cyan_dots=cyan_dots)
    print(f"Average displacement {i+1}: {mean_displacement:.2f} mm")
    print(f"Standard deviation {i+1}: {std_displacement:.2f} mm")
