import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
from threading import Thread


class VectorVisualization:
    def __init__(self):
        self.vectors = []
        self.show_plane = False
        self.show_cross_product = False
        self.show_dot_product = False
        self.fig = None
        self.ax = None

    def set_vectors(self, vectors):
        self.vectors = np.array(vectors)

    def update_visualization(self, frame):
        self.ax.clear()

        # Set limits for the plot
        max_val = np.max(np.abs(self.vectors))
        self.ax.set_xlim([-max_val, max_val])
        self.ax.set_ylim([-max_val, max_val])
        self.ax.set_zlim([-max_val, max_val])

        # Plot vectors
        for vector in self.vectors:
            self.ax.quiver(0, 0, 0, vector[0], vector[1], vector[2])

        if self.show_plane and len(self.vectors) >= 2:
            normal = np.cross(self.vectors[0], self.vectors[1])
            if np.allclose(normal, 0):
                self.ax.text2D(0.5, 0.5, 'No plane exists', transform=self.ax.transAxes, ha='center',
                               va='center', fontsize=12, color='red')
            else:
                point = self.vectors[0]
                xx, yy = np.meshgrid(point[0] + self.vectors[1][0] * np.array([-1, 1]),
                                     point[1] + self.vectors[1][1] * np.array([-1, 1]))
                zz = point[2] - (normal[0] * (xx - point[0]) + normal[1] * (yy - point[1])) / normal[2]
                self.ax.plot_surface(xx, yy, zz, alpha=0.5, color='gray')

        if self.show_cross_product and len(self.vectors) >= 2:
            cross_product = np.cross(self.vectors[0], self.vectors[1])
            self.ax.quiver(0, 0, 0, cross_product[0], cross_product[1], cross_product[2], color='red')

        if self.show_dot_product and len(self.vectors) >= 2:
            dot_product = np.dot(self.vectors[0], self.vectors[1])
            self.ax.text2D(0.1, 0.1, f'Dot Product: {dot_product}', transform=self.ax.transAxes, ha='left',
                           va='center', fontsize=12)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Vector Visualization')

    def toggle_plane(self, label):
        self.show_plane = not self.show_plane
        self.update_visualization(0)  # Call update_visualization to update the visualization
        self.fig.canvas.draw_idle()  # Update the canvas

    def toggle_cross_product(self, label):
        self.show_cross_product = not self.show_cross_product
        self.update_visualization(0)  # Call update_visualization to update the visualization
        self.fig.canvas.draw_idle()  # Update the canvas

    def toggle_dot_product(self, label):
        self.show_dot_product = not self.show_dot_product
        self.update_visualization(0)  # Call update_visualization to update the visualization
        self.fig.canvas.draw_idle()  # Update the canvas


    def create_interactive_plot(self, vectors):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.set_vectors(vectors)
        self.update_visualization(0)  # Call update_visualization to display the vectors

        # Create interactive checkboxes
        ax_options = plt.axes([0.05, 0.1, 0.1, 0.1])
        checkbox_plane = CheckButtons(ax_options, ['Plane'], [False])
        checkbox_plane.on_clicked(self.toggle_plane)

        ax_cross_product = plt.axes([0.05, 0.2, 0.1, 0.1])
        checkbox_cross_product = CheckButtons(ax_cross_product, ['Cross Product'], [False])
        checkbox_cross_product.on_clicked(self.toggle_cross_product)

        ax_dot_product = plt.axes([0.05, 0.3, 0.1, 0.1])
        checkbox_dot_product = CheckButtons(ax_dot_product, ['Dot Product'], [False])
        checkbox_dot_product.on_clicked(self.toggle_dot_product)

        plt.show()


def get_vector_input():
    try:
        vector_input = input("Enter vector components (comma-separated): ")
        vector_components = [float(x.strip()) for x in vector_input.split(',')]
        if len(vector_components) == 2:
            vector = np.array([vector_components[0], vector_components[1], 0])
        elif len(vector_components) == 3:
            vector = np.array([vector_components[0], vector_components[1], vector_components[2]])
        else:
            raise ValueError("Invalid number of vector components")
    except ValueError:
        print("Invalid input. Please enter valid vector components.")
        return None
    return vector


def visualize_vectors(vectors):
    visualization = VectorVisualization()
    visualization.create_interactive_plot(vectors)


def submit_vectors(v1_entry, v2_entry):
    v1 = v1_entry.get()
    v2 = v2_entry.get()

    try:
        v1_components = [float(x.strip()) for x in v1.split(',')]
        v2_components = [float(x.strip()) for x in v2.split(',')]
        if len(v1_components) != 3 or len(v2_components) != 3:
            raise ValueError("Invalid number of vector components")
    except ValueError:
        messagebox.showerror("Error", "Invalid vector components. Please enter valid numbers.")
        return

    vectors = [np.array(v1_components), np.array(v2_components)]
    thread = Thread(target=visualize_vectors, args=(vectors,))
    thread.start()


def main():
    root = tk.Tk()
    root.title("Vector Visualization")
    root.geometry("400x200")

    v1_label = tk.Label(root, text="Vector 1 (x, y, z):")
    v1_label.pack()
    v1_entry = tk.Entry(root)
    v1_entry.pack()

    v2_label = tk.Label(root, text="Vector 2 (x, y, z):")
    v2_label.pack()
    v2_entry = tk.Entry(root)
    v2_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=lambda: submit_vectors(v1_entry, v2_entry))
    submit_button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
