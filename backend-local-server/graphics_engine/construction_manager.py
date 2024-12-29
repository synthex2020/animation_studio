
#   CREATES A CONSTRUCTION MODEL BASED OF MATHEMATICAL AND GRAPHICAL TECHNIQUES

import matplotlib.pyplot as plt
import numpy as np 

class ConstructionManager:

    def __init__(self, working_dir):
        self.working = working_dir

    
    #   GENERATE BASE CONSTRUCTION MODEL 
    def loomis_generation(self, head_height=1, body_ratios=None):
        try:
            """
            Generates a Loomis construction model on a canvas.

            :param head_height: The unit height of the head.
            :param body_ratios: A dictionary defining body part proportions relative to head height.
            """
            if body_ratios is None:
                body_ratios = {
                    "head_to_chin": 1,
                    "chin_to_sternum": 1.5,
                    "sternum_to_navel": 1.5,
                    "navel_to_pelvis": 1,
                    "pelvis_to_knee": 2,
                    "knee_to_foot": 2
                }
            
            # Calculate cumulative heights
            heights = np.cumsum(list(body_ratios.values()))
            total_height = heights[-1] + head_height
            
            # Initialize the canvas
            fig, ax = plt.subplots(figsize=(5, 10))
            ax.set_xlim(-2, 2)
            ax.set_ylim(0, total_height + 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Draw the head (circle and guideline)
            head_radius = head_height / 2
            head_center = (0, total_height - head_radius)
            head_circle = plt.Circle(head_center, head_radius, color="blue", fill=False)
            ax.add_artist(head_circle)
            
            # Draw facial guidelines
            ax.plot([head_center[0] - head_radius, head_center[0] + head_radius], 
                    [head_center[1], head_center[1]], 
                    color="red", linestyle="--")  # Horizontal guide
            ax.plot([head_center[0], head_center[0]], 
                    [head_center[1] - head_radius, head_center[1] + head_radius], 
                    color="red", linestyle="--")  # Vertical guide
            
            # Draw the body sections
            current_height = total_height - head_height
            for section, ratio in body_ratios.items():
                next_height = current_height - ratio
                ax.plot([-1, 1], [current_height, current_height], color="black", linestyle="-")
                ax.text(1.2, current_height - ratio / 2, section, fontsize=10)
                current_height = next_height
            
            # Final ground line
            ax.plot([-2, 2], [0, 0], color="black", linestyle="-")
            ax.text(-1.8, 0.2, "Ground", fontsize=10)
            
            plt.show()
        except Exception as error:
            print(error)

    def generate_default_female(self):
        try:
            """
            Replicates the default Loomis-style construction model for a female figure
            with geometric segmentation shown as lines and shapes, without color.
            """
            # Initialize the figure
            fig, ax = plt.subplots(figsize=(5, 10))
            ax.set_xlim(-2, 2)
            ax.set_ylim(-1, 10)
            ax.set_aspect('equal')
            ax.axis('off')

            # Helper functions for geometric shapes
            def draw_circle(center, radius, ax):
                circle = plt.Circle(center, radius, fill=False, color="black", linewidth=1)
                ax.add_artist(circle)
            
            def draw_rectangle(x, y, width, height, ax):
                rect = plt.Rectangle((x, y), width, height, fill=False, color="black", linewidth=1)
                ax.add_artist(rect)

            def draw_ellipse(center, width, height, angle, ax):
                ellipse = plt.matplotlib.patches.Ellipse(
                    center, width, height, angle=angle, fill=False, color="black", linewidth=1
                )
                ax.add_artist(ellipse)
    
            # Draw the head
            draw_circle((0, 9), 1, ax)  # Head circle
            ax.plot([0, 0], [8, 10], color="black", linestyle="--")  # Centerline for the face

            # Neck and shoulders
            ax.plot([-0.5, 0.5], [8, 8], color="black")  # Neck base
            ax.plot([-1.5, 1.5], [8, 7.5], color="black")  # Shoulders
            
            # Torso
            draw_ellipse((0, 6.5), 2.5, 3, 0, ax)  # Ribcage
            draw_ellipse((0, 5), 2, 1.5, 0, ax)  # Pelvis

            # Arms
            ax.plot([-1.5, -2], [7.5, 5], color="black")  # Left arm line
            ax.plot([1.5, 2], [7.5, 5], color="black")   # Right arm line

            # Legs
            ax.plot([-1, -1], [4, 2], color="black")  # Left thigh
            ax.plot([1, 1], [4, 2], color="black")    # Right thigh
            draw_ellipse((-1, 2), 0.8, 1.5, 0, ax)    # Left knee
            draw_ellipse((1, 2), 0.8, 1.5, 0, ax)     # Right knee
            ax.plot([-1, -1], [1, 0], color="black")  # Left calf
            ax.plot([1, 1], [1, 0], color="black")    # Right calf

            # Feet
            draw_rectangle(-1.5, -0.2, 1, 0.2, ax)    # Left foot
            draw_rectangle(0.5, -0.2, 1, 0.2, ax)     # Right foot

            # Final centerline
            ax.plot([0, 0], [-1, 10], color="black", linestyle="--")  # Vertical centerline
    
            plt.show()
        except Exception as error:
            print(error)

