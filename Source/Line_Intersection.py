# python
"""
Module: Line_Intersection.py

This module provides several methods to determine whether two line segments intersect.
It implements three approaches:
    1. CCW-based intersection check.
    2. Vector cross product based intersection check.
    3. Line sweep algorithm based intersection check.

The module also provides a Tkinter-based GUI application to visualize and test these
line intersection methods interactively.

Target Users: Developers and researchers in computational geometry.
"""

import tkinter as tk


def do_intersect_ccw(A, B, C, D):
    """
    Determine if two line segments (A,B) and (C,D) intersect using the CCW method.
    
    The function defines a nested ccw() function that calculates the orientation of three points.
    If the orientations of the pairs (A, B, C) and (A, B, D) differ, and the orientations
    of (C, D, A) and (C, D, B) differ, the segments intersect in the general case.
    It also handles special collinear cases where the segments may overlap.

    Args:
        A, B, C, D (tuple): Points represented as (x, y).

    Returns:
        bool: True if the line segments intersect; otherwise, False.
    """
    def ccw(A, B, C):
        # Compute the cross product to determine the orientation of triangle ABC
        val = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    # Compute orientations needed for general and collinear cases.
    orientation1 = ccw(A, B, C)
    orientation2 = ccw(A, B, D)
    orientation3 = ccw(C, D, A)
    orientation4 = ccw(C, D, B)

    # General case: segments intersect if they have different orientations.
    if orientation1 != orientation2 and orientation3 != orientation4:
        return True

    # Special case: segments are collinear. Check for overlapping segments.
    if orientation1 == orientation2 == orientation3 == 0:
        if (min(A[0], B[0]) <= C[0] <= max(A[0], B[0]) or
            min(A[0], B[0]) <= D[0] <= max(A[0], B[0]) or
            min(C[0], D[0]) <= A[0] <= max(C[0], D[0]) or
            min(C[0], D[0]) <= B[0] <= max(C[0], D[0])):
            return True

    return False


def vecotr_cross_product(p1, p2, p3, p4):
    """
    Check intersection of two line segments (p1, p2) and (p3, p4) using the vector cross product approach.

    This method calculates the directional cross products to determine the relative positions of the points,
    and then checks the special cases where a point lies exactly on the segment.

    Args:
        p1, p2, p3, p4 (tuple): Endpoints of the two line segments.

    Returns:
        bool: True if the segments intersect; otherwise, False.
    """
    def direction(p1, p2, p3):
        # Compute cross product to determine the direction of p3 relative to line p1-p2.
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def on_segment(p, q, r):
        # Check if point q lies on segment pr.
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

    # Compute direction values for all combinations using cross product.
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    # Check general intersection condition using sign changes.
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    # Check for collinear intersection cases.
    elif d1 == 0 and on_segment(p3, p1, p4):
        return True
    elif d2 == 0 and on_segment(p3, p2, p4):
        return True
    elif d3 == 0 and on_segment(p1, p3, p2):
        return True
    elif d4 == 0 and on_segment(p1, p4, p2):
        return True
    else:
        return False


def line_sweep(p1, p2, p3, p4):
    """
    Check for intersection of two line segments using a line sweep approach.

    This function first verifies if the bounding boxes of the two segments overlap.
    Then, using the determinant method, it checks whether the segments cross each other.

    Args:
        p1, p2, p3, p4 (tuple): Endpoints of the two line segments.

    Returns:
        bool: True if the segments intersect; otherwise, False.
    """
    def calculate_determinant(point_1, point_2, point_3):
        # Calculate the determinant (similar to cross product) for three points.
        return (point_1[0] * point_2[1] +
                point_1[1] * point_3[0] +
                point_2[0] * point_3[1] -
                point_3[0] * point_2[1] -
                point_3[1] * point_1[0] -
                point_2[0] * point_1[1])

    def intersect(p1, p2, p3, p4):
        """
        Internal function to determine intersection using bounding box and cross product tests.
        
        Returns:
            bool: True if segments intersect; otherwise, False.
        """
        # Quick rejection: check if bounding boxes of segments do not overlap.
        if max(p1[0], p2[0]) < min(p3[0], p4[0]) or min(p1[0], p2[0]) > max(p3[0], p4[0]):
            return False
        if max(p1[1], p2[1]) < min(p3[1], p4[1]) or min(p1[1], p2[1]) > max(p3[1], p4[1]):
            return False

        # Check the positional relationship using determinants.
        if (calculate_determinant(p1, p3, p4) * calculate_determinant(p2, p3, p4) < 0 and
                calculate_determinant(p3, p1, p2) * calculate_determinant(p4, p1, p2) < 0):
            return True

        return False

    return intersect(p1, p2, p3, p4)


class LineIntersectionApp:
    """
    A Tkinter-based GUI application to test line-segment intersection methods.

    Users can click on the canvas to define endpoints of two line segments.
    Once four points are defined, the selected intersection algorithm is applied,
    and the result is displayed and visually represented on the canvas.
    """

    def __init__(self, root):
        """
        Initialize the GUI, bind events, and set up widgets.

        Args:
            root (tk.Tk): Root window for the Tkinter application.
        """
        self.root = root
        self.root.title("Line Intersection Checker")

        # Create a canvas to display points and line segments.
        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        # Store clicked points from the user.
        self.points = []

        # Bind left-mouse click event to collect point coordinates.
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Button to reset the canvas.
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_canvas)
        self.reset_button.pack()

        # Option menu to select which algorithm to use.
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("CCW")  # Default algorithm is CCW.
        self.algorithm_menu = tk.OptionMenu(
            root,
            self.algorithm_var,
            "CCW",
            "Vector Cross Product",
            "Line Sweep Algorithm"
        )
        self.algorithm_menu.pack()

        # Label to display the intersection result.
        self.intersect_label = tk.Label(root, text="", fg="green", font="Helvetica 12 bold")
        self.intersect_label.pack()

    def on_canvas_click(self, event):
        """
        Handle canvas click events by recording click positions and triggering
        the intersection check when four points are collected.

        Args:
            event (tk.Event): Event containing the x and y coordinates of the click.
        """
        x, y = event.x, event.y
        self.points.append((x, y))
        # Draw a small circle for visual feedback when a point is clicked.
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")

        # Once four points are present, check for intersection using the selected algorithm.
        if len(self.points) == 4:
            algorithm_choice = self.algorithm_var.get()
            if algorithm_choice == "CCW":
                result = do_intersect_ccw(self.points[0], self.points[1],
                                          self.points[2], self.points[3])
            elif algorithm_choice == "Vector Cross Product":
                result = vecotr_cross_product(self.points[0], self.points[1],
                                              self.points[2], self.points[3])
            elif algorithm_choice == "Line Sweep Algorithm":
                result = line_sweep(self.points[0], self.points[1],
                                    self.points[2], self.points[3])

            # Log the result to the console for debugging.
            print(f"Segments {'intersect' if result else 'do not intersect'}.")
            
            # Draw the segments in blue if they intersect; otherwise, in red.
            color = "blue" if result else "red"
            self.draw_line(self.points[0], self.points[1], color)
            self.draw_line(self.points[2], self.points[3], color)

            # Update the intersection label with user-friendly text.
            self.intersect_label.config(
                text="Segments Intersect" if result else "Segments Do Not Intersect",
                fg="green" if result else "red"
            )

    def draw_line(self, p1, p2, color):
        """
        Draw a line between two points on the canvas.
        
        Args:
            p1, p2 (tuple): Endpoints of the line.
            color (str): Color in which to draw the line.
        """
        self.canvas.create_line(p1, p2, fill=color)

    def reset_canvas(self):
        """
        Reset the canvas and clear any stored points and displayed messages.
        """
        self.points = []
        self.canvas.delete("all")
        self.intersect_label.config(text="", fg="green")


if __name__ == "__main__":
    # Create and start the Tkinter application.
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()