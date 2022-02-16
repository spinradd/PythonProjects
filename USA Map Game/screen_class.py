from border_class import WINDOW_WIDTH, WINDOW_HEIGHT
import turtle
import tkinter as tk

class Window():
   def __init__(self, master):
      """initialize window with background of USA map"""
      self.master = master
      self.master.title("USA Quiz")
      self.canvas = tk.Canvas(master)
      self.canvas.config(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)
      self.canvas.pack(side="left")
      self.screen = turtle.TurtleScreen(self.canvas)
      self.screen.bgcolor("white")
      self.main_turtle = turtle.RawTurtle(self.screen, visible=True)
      photo = "blank_states_img.gif"
      self.screen.register_shape(photo)
      self.main_turtle.shape(photo)