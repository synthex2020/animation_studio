import numpy as np 
import matplotlib.pyplot as plt 


class AlgebricProcessing:

    def __init__(self, head_diameter):
        self.diameter = head_diameter
        self.radius = head_diameter/2


    #   FACIAL CONSTRUCTION FOWARD FACING 

    #   BASE - HEAD ( SEMI-CIRCLE AND HEXAGON )
    def buildBaseForProfile2D(self, chin_start, chin_end):
        #   DEFINING THE VALUES 
        #       r - Radius of semi-circle 
        #       d - Diameter of semi-circle 
        #       r1 - Initial radius from top of semi circle 
        #       r2 - The vertical distance of r from the center of semi-circle 
        #       r3 - The vertical distance of r from the end point of r2
        #       k0 - The starting point for the chin 
        #       kf - The end point for the chin 
        #       x0 - X - center of semi circle 
        #       y0 - Y - center of semi circle 
        #   Note k0 and kf determine the angle of the cheeks 

        k_0 = chin_start
        k_f = chin_end

        r = self.radius
        d = self.diameter
        r_1 = r
        r_2 = r
        #   Take user input to determine face shape ( r_2_ and r_3 )
        r_2_ = r/1.5
        r_3 = (r/2)

        x_0 = 50
        y_0 = 50

        #   FUNCTION FOR SEMI-CIRCLE 
        #       f(x) => y = (+/-) sqrt(r^2 - x^2) 

        #   angles from 0 to PI 
        theta = np.linspace(0, np.pi, 100)
        semi_circle_x = x_0 + r * np.cos(theta)
        semi_circle_y = y_0 + r * np.sin(theta)


        #   FUNCTION FOR THE HEXAGON 
        #       f(x) => : 
        #               Top Base -> y = y_0 for {(x_0 - r) < x < (x_0 + r)}
        #               Left Side -> x = x_0 - r for {y_0 < y < y_0 + r}
        #               Right Side -> x = x_0 + r for {y_0 < y < y_o + r}
        #               Bottom Base -> y = y_0 - (r1 + r2) for {k_o < x < k_f}
        #               Cheek left -> y = mx + c for {(x_0 -r) < x < k_0 | (y_0 - r2) < y < (y_0 - d) }
        #               Cheek right -> y = mx + c for {(x_0 + r) < x < k_f | (y_0 -r) < y < (y_0 - d) }
        hexagon_x = [
            #   left base 
            x_0 - r , 
            #   left side 
            x_0 - r, 
            #   bottom left 
            k_0,
            #   bottom right 
            k_f,
            #   right side 
            x_0 + r, 
            #   right base 
            x_0 + r
        ]

        hexagon_y = [
            #   left base 
            y_0,
            #   left side 
            y_0 - r_2_,
            #   bottom left 
            y_0 - r_2 - r_3 , 
            #   bottom right 
            y_0 - r_2- r_3 ,
            #   right side 
            y_0 - r_2_,
            #   right base 
            y_0
        ]

        #   CRAFTING CORDINATES 
        plt.figure(figsize=(8,8))
        plt.plot(semi_circle_x, semi_circle_y, label="Semicircle (Top of Head)")
        plt.plot(hexagon_x + [hexagon_x[0]], hexagon_y + [hexagon_y[0]], label="Hexagon (Face Base)")
        plt.scatter(x_0, y_0, color="red", label="Center of Head")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.title('Loomis')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()

        self.buildForehead(circle_x=x_0, circle_y=y_0, circle_diameter=d ,arc_theta=45, eye_length=self.radius * 1/3)

        self.plot_slanted_lines_with_spacing(
            x_b_start=-20, y_b_start=60, 
            x_b_end=-15, y_b_end=50, 
            slope_a=2, spacing=5
        )
    def buildForehead(self, circle_x, circle_y, circle_diameter, arc_theta, eye_length):
        #   DEFINING SOME VARIABLES
        #       c -> eye_length
        #       Ed -> nose length
        #       l -> length of the arc 
        #       radius_circle -> circle_diameter / 2
        #       radius_arc -> (3/4) * radius_circle
        #       x_s -> circle_x - ((2/4) * radius_circle) [starting x-cordinate for arc]  
        #       x_f -> circle_x + ((2/4) * radius_circle) [starting y-cordinate for arc]  
        #       arc_theta -> the angle of the arc 
        #       c_x_1 -> x_s + (l/3)
        #       c_x_2 -> x_f - (l/3)
        #       x_0 -> circle_x
        #       y_0 -> circle_y + ((1/3) * circle_diameter) 
        #       z -> y_0  + ((2/3) * radius_arc)
        radius_circle = circle_diameter/2
        radius_arc = (3/4) * radius_circle
        y_0 = circle_y + ((1/3) * circle_diameter)
        z = y_0 + ((2/3) * radius_arc)
        x_s = circle_x - ((2/4) * radius_circle)
        x_f = circle_x + ((2/4) *radius_circle)
        #   CREATING THE ARC 
        #   f(arc) -> {x_s < x < x_f} | {y = z}

        #   CREATING FOREHEAD - b is a reflection of a 
        #   f(a1) --->  Right side 
        #   f(a1) -> y = mx + c for {xs < x < xs - c} | {z < y < c - z}
        #   f(b1) ---> Left side refelection of a1
        #   f(b1) -> y = mx + c for {xf < x < xf - c } | {z < y < c - z}

        #   f(a2) -> y = mx + c for {x_s - c < x < x_0 - (Ed/2) } | {c - z < y < y_0 + (radius_arc/2)}
        #   f(b2) ---> Left side reflection of b2 
        #   f(b2) -> y = mx + c for {x_f + c < x < x_0 + (Ed/2)} | {c - z < y < y_0 + (radius_arc/2)}

        #   f(a3) -> y = mx + c for {x_0 - (Ed/2) < x < x_0 + (Ed/2)} | {y = circle_y + (radius_arc/2)}

        #   f(c1) -> where c2 is a reflection of c1
        #         -> y = mx + c for {c_x_1 < x < x_0 + (Ed/2)} | {(centre_y) + radius_arc/2 < y < ((centre_y + (radius_arc/2)) + (0.9 * radius_arc))}
        #   f(c2) -> y = mx + c  for {c_x_2 < x < x_0 - (Ed/2)} | {(centre_y) + radius_arc/2 < y < ((centre_y + (radius_arc/2)) + (0.9 * radius_arc))}

        self.plot_arc(x_s=x_s, x_f=x_f, radius=radius_arc, z=z, theta_degrees=arc_theta)

    def plot_arc(self, x_s, x_f, radius, z, theta_degrees):
        """
        Plots a horizontal arc between x_s and x_f with a given radius, height z,
        and angle in degrees (theta).
        
        Parameters:
        x_s - Starting x-coordinate
        x_f - Ending x-coordinate
        radius - Radius of the arc
        z - Vertical center position of the arc
        theta_degrees - Angle in degrees for the arc
        """
        # Convert theta from degrees to radians
        theta = np.radians(theta_degrees)
        
        # Calculate the angle range for the arc
        arc_theta = np.linspace(-theta / 2, theta / 2, 100)
        
        # Calculate the center of the arc
        center_x = (x_s + x_f) / 2  # Horizontal center of the arc
        center_y = z                # Vertical center of the arc
        
        # Generate arc points
        arc_x = center_x + radius * np.sin(arc_theta)  # Horizontal arc
        arc_y = center_y + radius * np.cos(arc_theta)  # Vertical arc

        # Plot the arc
        plt.figure(figsize=(8, 8))
        plt.plot(arc_x, arc_y, label="Horizontal Arc")
        plt.scatter([x_s, x_f], [z, z], color="red", label="Arc Start/End Points")
        plt.axhline(y=z, color="gray", linestyle="--", label="Horizontal Center Line")
        plt.axvline(x=center_x, color="blue", linestyle="--", label="Arc Center Line")
        plt.scatter([center_x], [center_y], color="green", label="Arc Center")
        
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.title("Horizontal Arc Plot")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()
    

    def plot_slanted_lines_with_spacing(self, x_b_start, y_b_start, x_b_end, y_b_end, slope_a, spacing):
        """
        Plots two slanted lines where Line A starts after Line B ends with a given spacing.

        Parameters:
        x_b_start - Starting x-coordinate of Line B
        y_b_start - Starting y-coordinate of Line B
        x_b_end - Ending x-coordinate of Line B
        y_b_end - Ending y-coordinate of Line B
        slope_a - Slope of Line A
        spacing - Horizontal spacing between the end of Line B and the start of Line A
        """
        # Line B (going downwards)
        x_b = np.linspace(x_b_start, x_b_end, 100)
        m_b = (y_b_end - y_b_start) / (x_b_end - x_b_start)  # Slope of Line B
        y_b = m_b * (x_b - x_b_start) + y_b_start

        # Line A (going upwards, starting after spacing)
        x_a_start = x_b_end + spacing
        y_a_start = y_b_end
        x_a_end = x_a_start + 5  # Define the horizontal range for Line A
        x_a = np.linspace(x_a_start, x_a_end, 100)
        y_a = slope_a * (x_a - x_a_start) + y_a_start

        # Plotting
        plt.figure(figsize=(8, 8))
        plt.plot(x_b, y_b, label="Line B (Left Side)", color="green")
        plt.plot(x_a, y_a, label="Line A (Right Side)", color="blue")

        # Highlight key points
        plt.scatter([x_b_start, x_b_end], [y_b_start, y_b_end], color="red", label="Line B Start/End")
        plt.scatter([x_a_start, x_a_end], [y_a_start, y_a[-1]], color="orange", label="Line A Start/End")

        # Annotate spacing
        #plt.arrow(
        #    x_b_end, y_b_end, spacing, 0, 
        #    head_width=1, head_length=0.5, fc="purple", ec="purple", label="Spacing"
        #)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.title("Slanted Lines with Spacing Between Them")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()
    
    def plot_a2_b2(self):
        #   f(a2) is a mirror reflection of f(b2)
        #   f(a2) --> 
        #       y = mx + c for {x_s - c < x < x_0 - [Ed/2] } | {c-z < y < y_0 + (radius_arc/2)}
        #   f(b2) --> 
        #       y = mx + c for {x_f + c < x < x_0 + (Ed/2) } | {c-z < y < y_0 + (radius_arc/2)}
        pass
   
    #   FACIAL CONTRSTUCTION SIDE PROFILES 


