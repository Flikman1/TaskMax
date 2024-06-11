import tkinter as tk
from tkinter import filedialog
import trimesh
import numpy as np


def laplacian_smoothing(mesh, iterations, smoothing_factor):
    vertices = mesh.vertices.copy()
    adjacency_list = mesh.vertex_neighbors

    for _ in range(iterations):
        new_vertices = vertices.copy()
        for i, neighbors in enumerate(adjacency_list):
            if mesh.is_vertex_boundary(i):
                continue
            new_vertices[i] = vertices[i] + smoothing_factor * (np.mean(vertices[neighbors], axis=0) - vertices[i])
        vertices = new_vertices
    return vertices


def load_mesh():
    filepath = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")])
    if filepath:
        mesh = trimesh.load_mesh(filepath)
        mesh.show()
        return mesh
    return None


def apply_smoothing():
    if not mesh:
        return

    smoothing_factor = smoothing_scale.get()
    smoothed_vertices = laplacian_smoothing(mesh, iterations=10, smoothing_factor=smoothing_factor)

    smoothed_mesh = mesh.copy()
    smoothed_mesh.vertices = smoothed_vertices
    smoothed_mesh.show()


# Создание интерфейса
root = tk.Tk()
root.title("Laplacian Smoothing")

load_button = tk.Button(root, text="Load OBJ File", command=load_mesh)
load_button.pack()

smoothing_scale = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Smoothing Factor")
smoothing_scale.pack()

smooth_button = tk.Button(root, text="Apply Smoothing", command=apply_smoothing)
smooth_button.pack()

root.mainloop()

