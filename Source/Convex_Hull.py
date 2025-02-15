# python
"""
Module: Convex_Hull.py

This module implements a graphical application to compute the convex hull
of a set of points provided by the user. It supports multiple algorithms,
including Graham Scan, Jarvis March, Quick Hull, Andrew's Monotone Chain, 
and Brute Force, to accommodate different input characteristics.

Project Type: Geometric Algorithms Visualization
Target Users: Developers and researchers working on computational geometry.
"""

import tkinter as tk
import time
import numpy as np
import math
import random

class ConvexHullApp:
    """
    A Tkinter-based application that allows users to interactively add points
    on a canvas and view the computed convex hull using various algorithms.

    Attributes:
        master (tk.Tk): Parent Tkinter window.
        canvas (tk.Canvas): Canvas widget for drawing points and hull edges.
        points (list): List of (x, y) tuples representing the user-defined points.
        convex_hull (list): Points composing the convex hull in sequence.
        start_time (float): Timestamp to calculate elapsed time for computations.
        algorithm_var (tk.StringVar): Holds the currently selected convex hull algorithm.
    """
    
    def __init__(self, master, width, height):
        """
        Initialize the ConvexHullApp with a GUI interface.

        Args:
            master (tk.Tk): The root Tkinter window.
            width (int): Width of the drawing canvas.
            height (int): Height of the drawing canvas.
        """
        self.master = master
        self.master.title("Convex Hull Algorithms")
        
        # Set up the canvas for drawing points and hull edges.
        self.canvas = tk.Canvas(master, width=width, height=height, bg="white")
        self.canvas.pack()
        
        self.points = []         # Stores points as (x, y)
        self.convex_hull = []    # Stores the currently computed convex hull
        self.start_time = time.time()
        
        # Bind a mouse-click event to adding a new point
        self.canvas.bind("<Button-1>", self.add_point)

        # Dropdown menu for algorithm selection
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Graham Scan")  # Set default algorithm
        algorithms = ["Graham Scan", "Jarvis March", "Quick Hull", "Montone's Chain", "Brute Force"]
        self.algorithm_menu = tk.OptionMenu(master, self.algorithm_var, *algorithms)
        self.algorithm_menu.pack()
        
        # Button to trigger convex hull drawing
        self.draw_button = tk.Button(master, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()
        
        # Label to display elapsed computation time
        self.time_label = tk.Label(master, text="Time Elapsed: 0 seconds")
        self.time_label.pack()
        
        # Button to reset the canvas and clear all data
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_canvas)
        self.reset_button.pack()

        # Uncomment the following block if you wish to draw coordinate axes on the canvas.
        # gap = 10
        # self.canvas.create_line(gap, height - gap, width, height - gap, fill="black", width=2)  # x-axis
        # self.canvas.create_line(gap, gap, gap, height - gap, fill="black", width=2)          # y-axis
        # self.canvas.create_text(width - 20, height - gap + 20, text="X", anchor="w", fill="black",
        #                        font=("Helvetica", 12, "bold"))
        # self.canvas.create_text(gap + 20, gap + 20, text="Y", anchor="w", fill="black", font=("Helvetica", 12, "bold"))

    def update_time_label(self):
        """
        Update the label with the elapsed time since the last reset or start.
        The elapsed time helps in understanding the computational cost.
        """
        elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"Time Elapsed: {round(elapsed_time, 10)} seconds")
    
    def draw_line_segment(self, p1, p2, color="red"):
        """
        Draws a line segment between two given points.

        Args:
            p1 (tuple): The starting point (x, y).
            p2 (tuple): The ending point (x, y).
            color (str): The color of the line segment.
        """
        x1, y1 = p1
        x2, y2 = p2
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, tags="convex_hull")
    
    def add_point(self, event):
        """
        Event handler for adding a new point to the canvas.
        Captures the x and y screen coordinates from the mouse event,
        updates the points list, and visually represents the point.

        Args:
            event (tk.Event): The event object containing x and y coordinates.
        """
        x, y = event.x, event.y
        self.points.append((x, y))
        # Draw a small circle representing the point
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")
        # Display coordinates next to the point for clarity
        self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="w", fill="blue")
    
    def draw_convex_hull(self):
        """
        Compute and animate the drawing of the convex hull based on the selected algorithm.
        Validates that there are enough points and clears previous hull drawings before proceeding.
        """
        if len(self.points) < 3:
            return  # Not enough points to form a convex hull

        # Clear any previous convex hull lines from the canvas
        self.canvas.delete("convex_hull")
        
        # Select the algorithm based on the user's choice
        algorithm = self.algorithm_var.get()
        if algorithm == "Graham Scan":
            self.convex_hull = self.graham_scan()
        elif algorithm == "Jarvis March":
            self.convex_hull = self.jarvis_march_convex_hull()
        elif algorithm == "Quick Hull":
            self.convex_hull = self.quickhull()
        elif algorithm == "Montone's Chain":
            self.convex_hull = self.andrews_monotone_chain()
        elif algorithm == "Brute Force":
            self.convex_hull = self.brute_force()
        
        # Animate the drawing of convex hull edges
        if self.convex_hull is not None:
            # Use an animation effect by delaying the drawing of each edge
            for frame in range(1, len(self.convex_hull) + 1):
                # For the last edge, connect to the first point to close the hull
                if frame == len(self.convex_hull):
                    frame = 0

                def update(frame):
                    c0 = self.convex_hull[frame - 1]
                    c1 = self.convex_hull[frame]
                    # Draw an edge between consecutive hull points
                    self.canvas.create_line(c0[0], c0[1], c1[0], c1[1],
                                            fill='red', width=2)
                # Schedule the drawing of the edge with a slight delay for effect
                self.canvas.after(500 * frame, update, frame)
    
    def reset_canvas(self):
        """
        Reset the canvas to a clean state by clearing all points and convex hull drawings.
        Also resets the timer and updates the displayed elapsed time.
        """
        self.canvas.delete("all")
        self.points = []
        self.convex_hull = []
        self.start_time = time.time()
        self.update_time_label()

        # Uncomment the following block if coordinate axes should be redrawn after reset.
        # gap = 10
        # self.canvas.create_line(gap, self.canvas.winfo_reqheight() - gap, self.canvas.winfo_reqwidth(),
        #                         self.canvas.winfo_reqheight() - gap, fill="black", width=2)  # x-axis
        # self.canvas.create_line(gap, gap, gap, self.canvas.winfo_reqheight() - gap, fill="black", width=2)  # y-axis
        # self.canvas.create_text(self.canvas.winfo_reqwidth() - 20, self.canvas.winfo_reqheight() - gap + 20,
        #                         text="X", anchor="w", fill="black", font=("Helvetica", 12, "bold"))
        # self.canvas.create_text(gap + 20, gap + 20, text="Y", anchor="w", fill="black", font=("Helvetica", 12, "bold"))
    
    def graham_scan(self):
        """
        Compute the convex hull using the Graham Scan algorithm.
        The function defines helper functions to calculate polar angles, distances,
        and determinants to efficiently determine the hull boundary.

        Returns:
            list: A list of points (tuples) representing the convex hull in order.
        """
        start = time.time()

        # Global anchor used for polar angle calculations
        global anchor

        def polar_angle(p0, p1=None):
            """
            Compute the polar angle (in radians) between p1 and p0.
            Defaults to using the anchor as the reference point.
            """
            if p1 is None: 
                p1 = anchor
            y_span = p0[1] - p1[1]
            x_span = p0[0] - p1[0]
            return math.atan2(y_span, x_span)

        def distance(p0, p1=None):
            """
            Compute the squared Euclidean distance between p0 and p1.
            Using the squared distance avoids an unnecessary square root.
            """
            if p1 is None:
                p1 = anchor
            y_span = p0[1] - p1[1]
            x_span = p0[0] - p1[0]
            return y_span**2 + x_span**2

        def quicksort(a):
            """
            Sort points based on their polar angle relative to the anchor using a quicksort approach.
            The sorted order is then refined by distance for points with identical angles.
            """
            if len(a) <= 1:
                return a
            smaller = []
            equal = []
            larger = []
            piv_ang = polar_angle(a[random.randint(0, len(a) - 1)])  # Random pivot to avoid worst-case
            for pt in a:
                pt_ang = polar_angle(pt)
                if pt_ang < piv_ang:
                    smaller.append(pt)
                elif pt_ang == piv_ang:
                    equal.append(pt)
                else:
                    larger.append(pt)
            return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)
        
        # Identify the point with the lowest y-coordinate (and smallest x if tied)
        min_idx = None
        for i, (x, y) in enumerate(self.points):
            if min_idx is None or y < self.points[min_idx][1]:
                min_idx = i
            if y == self.points[min_idx][1] and x < self.points[min_idx][0]:
                min_idx = i

        anchor = self.points[min_idx]  # Set the global anchor for sorting
        
        # Sort the points based on their angle relative to the anchor
        sorted_pts = quicksort(self.points)
        # Remove the anchor from the sorted list to avoid duplicate entry in the hull
        del sorted_pts[sorted_pts.index(anchor)]

        def det(p1, p2, p3):
            """
            Calculate the determinant to check turn direction.
            A non-positive determinant indicates a non-left turn.
            """
            return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

        # Start the convex hull with the anchor and the first sorted point
        hull = [anchor, sorted_pts[0]]
        # Process each point to determine if it forms a left turn
        for s in sorted_pts[1:]:
            # Backtrack if the last segment does not make a left turn
            while len(hull) >= 2 and det(hull[-2], hull[-1], s) <= 0:
                del hull[-1]
            hull.append(s)
        self.update_time_label()
        return hull

    def jarvis_march_convex_hull(self):
        """
        Compute the convex hull using the Jarvis March (Gift Wrapping) algorithm.
        This method iteratively selects the next hull point by determining the
        most counterclockwise point relative to the current point.

        Returns:
            list: A list of points representing the convex hull.
        
        Raises:
            ValueError: If fewer than 3 points are provided.
        """
        start = time.time()

        def orientation(p, q, r):
            """
            Determine the orientation of the triplet (p, q, r).
            Returns:
                0  -> Collinear
                1  -> Clockwise
               -1  -> Counterclockwise
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        n = len(self.points)
        if n < 3:
            raise ValueError("Convex hull not possible with less than 3 points")

        # Initialize pivot to the point with the lowest y-coordinate (and leftmost if tied)
        pivot = min(self.points, key=lambda p: (p[1], p[0]))
        hull = []

        # Wrap around the set of points until we return to the starting point
        while True:
            hull.append(pivot)
            endpoint = self.points[0]  # Start comparing with the first point

            for i in range(1, n):
                # Select the most counterclockwise point relative to current pivot
                if endpoint == pivot or orientation(pivot, endpoint, self.points[i]) == -1:
                    endpoint = self.points[i]

            if endpoint == hull[0]:
                break  # Hull is complete after coming back to the start

            pivot = endpoint
        self.update_time_label()
        return hull

    def quickhull(self):
        """
        Compute the convex hull using the Quick Hull algorithm.
        Quick Hull is a divide-and-conquer approach that recursively finds
        the farthest points from a line and partitions the set of points.

        Returns:
            list: A list of line segments, where each segment is represented
                  as a pair of points joining consecutive hull edges.
        """
        start = time.time()
        points = self.points

        def calculate_determinant(point_1, point_2, point_3):
            """
            Calculate the determinant for three points.
            A positive value indicates that point_3 is to the left of the line formed by point_1->point_2.
            """
            return (point_1[0] * point_2[1] + point_1[1] * point_3[0] + point_2[0] * point_3[1] -
                    point_3[0] * point_2[1] - point_3[1] * point_1[0] - point_2[0] * point_1[1])

        def find_min_and_max(points):
            """
            Identify the leftmost and rightmost points based on the x-coordinate.
            These points are used as the starting boundary for partitioning.
            """
            minimum_point = points[0]
            maximum_point = points[0]
            for point in points:
                if point[0] <= minimum_point[0]:
                    minimum_point = point
                if point[0] >= maximum_point[0]:
                    maximum_point = point
            return minimum_point, maximum_point

        def calc_line_dist(min_absis, max_absis, point):
            """
            Compute the perpendicular distance from a point to the line defined by min_absis and max_absis.
            This distance helps to determine which point is farthest from the line.
            """
            return abs((point[1] - min_absis[1]) * (max_absis[0] - min_absis[0]) -
                       (max_absis[1] - min_absis[1]) * (point[0] - min_absis[0]))

        def divide_side(points, min_absis, max_absis):
            """
            Partition points into those lying on the left side and right side of the line.
            Only points not equal to the boundary points are considered.
            """
            left_hull = []
            right_hull = []
            for point in points:
                if point != min_absis and point != max_absis:
                    if calculate_determinant(min_absis, max_absis, point) > 0:
                        left_hull.append(point)
                    if calculate_determinant(min_absis, max_absis, point) < 0:
                        right_hull.append(point)
            return left_hull, right_hull

        def find_max_distance(points, min_absis, max_absis):
            """
            Find the point that is farthest from the line defined by min_absis and max_absis.
            """
            max_distance = 0
            index_of_max = 0
            for i in range(len(points)):
                curr_distance = calc_line_dist(min_absis, max_absis, points[i])
                if curr_distance > max_distance:
                    index_of_max = i
                    max_distance = curr_distance
            return points[index_of_max]

        def quick_hull_left(points, min_absis, max_absis):
            """
            Recursively compute the left part of the convex hull.
            Points are further partitioned until no eligible point remains.
            """
            if len(points) == 0:
                return
            else:
                max_point = find_max_distance(points, min_absis, max_absis)
                points.remove(max_point)
                list_of_hull.append(max_point)
                first_side, _ = divide_side(points, min_absis, max_point)
                second_side, _ = divide_side(points, max_point, max_absis)
                quick_hull_left(first_side, min_absis, max_point)
                quick_hull_left(second_side, max_point, max_absis)

        def quick_hull_right(points, min_absis, max_absis):
            """
            Recursively compute the right part of the convex hull.
            Similar to quick_hull_left but for the other side of the initial line.
            """
            if len(points) == 0:
                return
            else:
                max_point = find_max_distance(points, min_absis, max_absis)
                points.remove(max_point)
                list_of_hull.append(max_point)
                _, first_side = divide_side(points, min_absis, max_point)
                _, second_side = divide_side(points, max_point, max_absis)
                quick_hull_right(first_side, min_absis, max_point)
                quick_hull_right(second_side, max_point, max_absis)

        if len(points) <= 1:
            return points

        min_absis, max_absis = find_min_and_max(points)
        left_hull, right_hull = divide_side(points, min_absis, max_absis)
        list_of_hull = [min_absis, max_absis]
        quick_hull_left(left_hull, min_absis, max_absis)
        quick_hull_right(right_hull, min_absis, max_absis)

        # Sort the resulting hull points based on their angle around the center
        central_x = sum(point[0] for point in list_of_hull) / len(list_of_hull)
        central_y = sum(point[1] for point in list_of_hull) / len(list_of_hull)
        list_of_hull.sort(key=lambda point: math.atan2(point[0] - central_x, point[1] - central_y))

        # Convert the list of points to tuple segments to depict edges
        tuple_of_hull = []
        for i in range(len(list_of_hull)):
            if i == len(list_of_hull) - 1:
                tuple_of_hull.append([list_of_hull[i], list_of_hull[0]])
            else:
                tuple_of_hull.append([list_of_hull[i], list_of_hull[i + 1]])
        self.update_time_label()
        return tuple_of_hull

    def brute_force(self):
        """
        Compute the convex hull using a brute-force approach.
        The algorithm tests every combination of points to check whether a point
        lies on the boundary of the convex hull.

        Returns:
            list: A list of points in order that form the convex hull.
        """
        points = self.points
        start = time.time()

        def orientation(p, q, r):
            """
            Determine the orientation of the ordered triplet (p, q, r).
            Returns:
                0  for collinear points,
                1  for clockwise direction,
                2  for counterclockwise direction.
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            elif val > 0:
                return 1
            else:
                return 2

        n = len(points)
        if n < 3:
            return []

        hull = []
        # Start from the leftmost point which must be on the hull
        l = 0
        for i in range(1, n):
            if points[i][0] < points[l][0]:
                l = i

        p = l
        q = None
        # Continue wrapping until we return to starting point 'l'
        while True:
            hull.append(points[p])
            q = (p + 1) % n
            for r in range(n):
                if orientation(points[p], points[q], points[r]) == 2:
                    q = r
            p = q
            if p == l:
                break
        self.update_time_label()
        return hull

    def andrews_monotone_chain(self):
        """
        Compute the convex hull using Andrew's Monotone Chain algorithm.
        The procedure sorts the points lexicographically and constructs the
        lower and upper parts of the hull separately before merging.

        Returns:
            list: A list of points representing the convex hull.
        
        Raises:
            ValueError: If fewer than 3 points are provided.
        """
        start = time.time()

        def orientation(p, q, r):
            """
            Compute orientation using the cross product.
            Returns:
                0 for collinear, 1 for clockwise, and -1 for counterclockwise.
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        points = self.points
        n = len(points)
        if n < 3:
            raise ValueError("Convex hull not possible with less than 3 points")

        # Sort points lexicographically (first by x, then by y)
        points = sorted(points)

        # Build the lower hull of the convex hull
        lower_hull = []
        for p in points:
            while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], p) != -1:
                lower_hull.pop()
            lower_hull.append(p)

        # Build the upper hull of the convex hull
        upper_hull = []
        for p in reversed(points):
            while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], p) != -1:
                upper_hull.pop()
            upper_hull.append(p)

        # Merge both hulls, omitting the duplicate endpoints
        convex_hull = lower_hull[:-1] + upper_hull[:-1]
        self.update_time_label()
        return convex_hull

if __name__ == "__main__":
    # Main execution: instantiate and run the ConvexHullApp.
    root = tk.Tk()
    app = ConvexHullApp(root, width=900, height=500)
    root.mainloop()