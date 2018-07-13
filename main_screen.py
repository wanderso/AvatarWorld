import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

frame_root = tk.Frame(root)
frame_root.pack()


w = tk.Label(frame_root, font = "Helvetica 16 bold", text="Pinnacle Academy Interface 0.1")
w.pack(side=tk.TOP)

main_frame = tk.Frame(frame_root)
main_frame.pack(side=tk.TOP)

frame_tabs = tk.Frame(main_frame)
frame_tabs.pack(side=tk.LEFT)

view_switch = tk.Frame(frame_tabs)
view_switch.pack(side=tk.TOP)

chara_viewer_button = tk.Button(view_switch, text="Character Viewer", command=quit)
chara_viewer_button.pack(side=tk.TOP, fill=tk.X)

power_creator_button = tk.Button(view_switch, text="Power Creator", command=quit)
power_creator_button.pack(side=tk.TOP, fill=tk.X)

combat_simulator_button = tk.Button(view_switch, text="Combat Simulator", command=quit)
combat_simulator_button.pack(side=tk.TOP, fill=tk.X)

map_creator_button = tk.Button(view_switch, text="Map Creator", command=quit)
map_creator_button.pack(side=tk.TOP, fill=tk.X)

frame_display = tk.Frame(main_frame)
frame_display.pack(side=tk.RIGHT)

image = Image.open("Graphics/daphne_example.jpg")
daphne = ImageTk.PhotoImage(image)

daphne_display = tk.Label(frame_display, image=daphne)
daphne_display.pack()

root.mainloop()
