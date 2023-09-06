import tkinter as tk
import numpy as np
import math
import cv2

class Circle:
    def __init__(self, current_lines):
        self.points = None
        self.radius = None
        self.center = None
        self.current_lines = current_lines
        # print("circlr created....")   
    def check(self):
        distances = np.linalg.norm(self.points - self.center, axis=1)
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)

        # Set a threshold for variance to classify as a line or circle
        threshold = 3  # You may need to adjust this value based on your data
        #print(std_distance, self.radius, self.center, mean_distance)
        _, radius = cv2.minEnclosingCircle(self.points)
    
    # Calculate the convex hull of the points
        hull = cv2.convexHull(self.points)
        
        # Calculate the area of the convex hull
        hull_area = cv2.contourArea(hull)
        # print((np.pi * self.radius**2) / hull_area)

        area_thresh = abs(hull_area - (np.pi * self.radius**2))
        print(area_thresh, self.radius)
        # print(round(self.radius // std_distance, 3) )
        if std_distance < self.radius // 3 and (area_thresh < hull_area / 10):

            return True
        else:
            return False

    def scale_down(self, val):
        temp = []
        for i in range(len(self.points)):
            if(i % val != 0):
                temp.append(self.points[i])
        self.points = np.array(temp)


    def Centroid(self):
        x = np.mean(self.points[:, 0])
        y = np.mean(self.points[:, 1])
        self.center = [x, y]
        # if(self.points):
        #     x = np.mean(self.points[:, 0])
        #     y = np.mean(self.points[:, 1])
        #     self.centroid = [x, y]
    
    def Radius(self):
        distances = np.sqrt(np.sum((self.points - self.center)**2, axis=1))
        self.radius =  np.mean(distances)
        # print("eql -> ", np.std(distances))
        # if(self.center):
        #     distances = np.sqrt(np.sum((self.points - self.centroid)**2, axis=1))
        #     self.radius =  np.mean(distances)
    def draw(self, canvas):
        number_of_points = int(self.radius) * 10
        angle = np.linspace(0, 2 * np.pi, number_of_points)
        x = self.center[0] + self.radius * np.cos(angle)
        y = self.center[1] + self.radius * np.sin(angle)
        # print(x, y)
        # print(len(self.current_lines))
        for i in self.current_lines:
            canvas.delete(i)
        for i in range(number_of_points):
            canvas.create_line(x[i], y[i], x[i] + 1,  y[i] + 1, fill="black", width=2)

        pass

class Ellipse:
    def __init__(self, current_lines):
        self.minor = None
        self.major = None
        self.points = None
    
    def get_focal(self):
        if(self.points != None):
            self.major


class DrawingApp:
    def __init__(self, root, width , height):
        self.root = root
        #self.root.title("Drawing App with Point Recording")
        self.circle_list = []
        self.current_lines = []
        self.canvas = tk.Canvas(root, bg="white", width = width, height = height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.is_drawing = False
        self.last_x, self.last_y = None, None
        self.recorded_points = []
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

    def start_draw(self, event):
        self.is_drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            if self.last_x is not None and self.last_y is not None:
                self.draw_smooth_line(self.last_x, self.last_y, x, y)
            self.last_x, self.last_y = x, y

    def stop_draw(self, event):
        self.is_drawing = False
        self.last_x, self.last_y = None, None
        temp = Circle(self.current_lines)
        temp.points = np.array(self.recorded_points)
        
        temp.scale_down(10)
        temp.Centroid()
        temp.Radius()
        if(temp.check()):
            temp.draw(self.canvas)
        self.circle_list.append(temp)
        self.recorded_points = []
        self.current_lines = []
        #print("drawing done")

    def draw_smooth_line(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy

        points = []

        while x0 != x1 or y0 != y1:
            points.append((x0, y0))
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        for point in points:
            self.recorded_points.append(point)
            self.current_lines.append(self.canvas.create_line(point[0], point[1], point[0] + 1, point[1] + 1, fill="black", width=2))
        #print(self.recorded_points)
    
    def get_points(self):
        return self.recorded_points
    
    def clear_canvas(self):
        self.canvas.delete("all")


    def get_clicked_position(event):
        x = event.x
        y = event.y
        # print("Clicked position:", x, y)
        return [x,y]
    

width = 600
height = 600

root = tk.Tk()
root.title("auto_circle")



main_frame = tk.Frame(root, width=width, height=height)
main_frame.pack(side="right", padx=10, pady=10)
drawable = DrawingApp(main_frame, width, height)
root.geometry("800x600")
root.mainloop()
