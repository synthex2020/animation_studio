import numpy as np
import matplotlib.pyplot as plt

class AlgebricProcessing:
    def __init__(self, head_diameter):
        self.diameter = head_diameter
        self.radius = head_diameter / 2

    def createSemicircle(self, x_0, y_0, r):
        theta = np.linspace(0, np.pi, 100)
        x = x_0 + r * np.cos(theta)
        y = y_0 + r * np.sin(theta)
        return x, y

    def createVerticalGuidelines(self, x_0, y_0, r):
        x = [x_0] * 2
        y = [y_0 - r, y_0 + r]
        return x, y

    def createHorizontalGuidelines(self, x_0, y_0, r, divisions=6):
        lines = []
        for i in range(divisions + 1):
            y = y_0 - r + (i * (2 * r / divisions))
            x = [x_0 - r, x_0 + r]
            lines.append((x, [y, y]))
        return lines

    def createEyes(self, x_0, y_0, r):
        eye_radius = r / 15
        eye_y = y_0 - r / 3
        left_eye_x = x_0 - r / 4
        right_eye_x = x_0 + r / 4
        return [(left_eye_x, eye_y), (right_eye_x, eye_y)]

    def createNose(self, x_0, y_0, r):
        nose_length = r / 6
        x = [x_0, x_0 - r / 15, x_0 + r / 15]
        y = [y_0 - r / 3 - nose_length, y_0 - r / 3, y_0 - r / 3]
        return x, y

    def createMouth(self, x_0, y_0, r):
        mouth_width = r / 3
        mouth_y = y_0 - 2 * r / 3
        x = np.linspace(x_0 - mouth_width / 2, x_0 + mouth_width / 2, 50)
        y = mouth_y + (r / 20) * np.sin(2 * np.pi * (x - x_0) / mouth_width)
        return x, y

    def createEars(self, x_0, y_0, r):
        ear_y = np.linspace(y_0 - r / 3, y_0, 50)
        left_ear_x = [x_0 - r] * len(ear_y)
        right_ear_x = [x_0 + r] * len(ear_y)
        return (left_ear_x, ear_y), (right_ear_x, ear_y)

    def drawLoomisHead(self):
        x_0, y_0 = 0, 0
        r = self.radius

        # Semicircle
        semi_circle_x, semi_circle_y = self.createSemicircle(x_0, y_0, r)

        # Guidelines
        vertical_guideline_x, vertical_guideline_y = self.createVerticalGuidelines(x_0, y_0, r)
        horizontal_guidelines = self.createHorizontalGuidelines(x_0, y_0, r)

        # Features
        eyes = self.createEyes(x_0, y_0, r)
        nose_x, nose_y = self.createNose(x_0, y_0, r)
        mouth_x, mouth_y = self.createMouth(x_0, y_0, r)
        ears = self.createEars(x_0, y_0, r)

        # Plot
        plt.figure(figsize=(8, 8))
        plt.plot(semi_circle_x, semi_circle_y, label="Semicircle (Top of Head)")
        plt.plot(vertical_guideline_x, vertical_guideline_y, 'k--', label="Vertical Guideline")
        for line in horizontal_guidelines:
            plt.plot(*line, 'k--', label="Horizontal Guideline")

        for eye in eyes:
            plt.scatter(*eye, color="blue", label="Eye")
        plt.plot(nose_x, nose_y, color="green", label="Nose")
        plt.plot(mouth_x, mouth_y, color="red", label="Mouth")
        for ear in ears:
            plt.plot(*ear, color="orange", label="Ear")

        plt.gca().set_aspect('equal', adjustable='box')
        plt.title("Loomis Head with Proportions")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.show()


# Call the function to plot the Loomis head

if __name__ == "__main__":
    # Example usage
    head = AlgebricProcessing(head_diameter=100)
    head.drawLoomisHead()