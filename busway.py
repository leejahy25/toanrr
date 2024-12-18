import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar
import networkx as nx
import random


class BusWayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BusWay")
        self.root.geometry("900x700")
        self.graph = self.load_bus_data("input.txt")
        self.current_screen = None
        self.screen_stack = []
        self.initialize_ui()

    def initialize_ui(self):
        self.start_screen()

    def load_bus_data(self, file_name):
        G = nx.DiGraph()
        with open(file_name, encoding="utf-8") as file:
            data = file.read().strip().split("||")
        for line in data:
            bus_info = line.split(";")
            bus_name = bus_info[0].strip()
            stations = bus_info[1].split("-")
            for i in range(len(stations)):
                station = stations[i].strip()
                if i < len(stations) - 1:
                    G.add_edge(station, stations[i + 1].strip(), bus=bus_name)
        return G

    def change_screen(self, screen, save_previous=True):
        if self.current_screen:
            self.current_screen.pack_forget()
            if save_previous:
                self.screen_stack.append(self.current_screen)
        self.current_screen = screen
        self.current_screen.pack(fill="both", expand=True)

    def go_back(self):
        if self.screen_stack:
            screen = self.screen_stack.pop()
            self.current_screen.pack_forget()
            self.current_screen = screen
            self.current_screen.pack(fill="both", expand=True)

            if isinstance(self.current_screen, tk.Frame) and self.current_screen.winfo_children():
                for widget in self.current_screen.winfo_children():
                    if isinstance(widget, tk.Entry):
                        widget.delete(0, tk.END)

    def add_back_button(self, screen):
        back_button = tk.Button(
            screen,
            text="<",
            font=("Helvetica", 14, "bold"),
            bg="#D32F2F",
            fg="white",
            command=self.go_back,
        )
        back_button.place(x=10, y=10, width=40, height=40)

    def start_screen(self):
        screen = tk.Frame(self.root, bg="#2C3E50")
        title_label = tk.Label(
            screen,
            text="🚍 Welcome to BusWay! Ready for your next journey? 🌟",
            font=("Helvetica", 22, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        title_label.pack(pady=50)

        button_frame = tk.Frame(screen, bg="#2C3E50")
        button_frame.pack(pady=175)

        yes_button = tk.Button(
            button_frame,
            text="Yes, I wanna travel with buses",
            font=("Helvetica", 16),
            bg="#4CAF50",
            fg="white",
            command=self.choices_screen,
            wraplength=200,
            width=20,
            height=3
        )
        yes_button.grid(row=0, column=0, padx=20)

        no_button = tk.Button(
            button_frame,
            text="No, thanks",
            font=("Helvetica", 16),
            bg="#D32F2F",
            fg="white",
            command=self.root.quit,
            width=20,
            height=3
        )
        no_button.grid(row=0, column=1, padx=20)

        credit_button = tk.Button(
            screen,
            text="Credit",
            font=("Helvetica", 14),
            bg="#90CAF9",
            fg="black",
            command=self.credit_screen,
            width=12,
            height=2
        )
        credit_button.place(relx=1.0, rely=1.0, x=-15, y=-15, anchor="se")

        self.change_screen(screen, save_previous=False)

    def credit_screen(self):
        screen = tk.Frame(self.root, bg="#2C3E50")
        credit_label = tk.Label(
            screen,
            text="CREDIT",
            font=("Helvetica", 22, "bold"),
            fg="Red",
            bg="#2C3E50"
        )
        credit_label.pack(pady=20)

        credit_text = (
            "Author: Ho Thanh Dat - 22110020 || Le Gia Huy - 22110032\n"
            "Course: Discrete Mathematics and Graph Theory | Semester 1 (2024 - 2025)\n"
            "Lecturer: M.Sc. Nguyen Thi Phuong"
        )
        credit_info = tk.Label(
            screen,
            text=credit_text,
            font=("Helvetica", 16),
            fg="white",
            bg="#2C3E50",
            justify="center"
        )
        credit_info.pack(pady=50)

        self.add_back_button(screen)
        self.change_screen(screen)

    def choices_screen(self):
        screen = tk.Frame(self.root, bg="#2C3E50")
        title_label = tk.Label(
            screen,
            text="What do you want to do? Select an action below.",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        title_label.pack(pady=50)
        button_frame = tk.Frame(screen, bg="#2C3E50")
        button_frame.pack(pady=150)
        search_routes_button = tk.Button(
            button_frame,
            text="Search for buses routes",
            font=("Helvetica", 14),
            bg="#90CAF9",
            fg="black",
            command=self.display_buses,
        )
        search_routes_button.pack(padx=10, pady=10, fill="x")
        find_routes_button = tk.Button(
            button_frame,
            text="Find routes between two stations",
            font=("Helvetica", 14),
            bg="#90CAF9",
            fg="black",
            command=self.find_routes_screen1,
        )
        find_routes_button.pack(padx=10, pady=10, fill="x")
        self.add_back_button(screen)
        self.change_screen(screen)

    def display_buses(self):
        screen = tk.Frame(self.root, bg="#2C3E50")
        title_label = tk.Label(
            screen,
            text="Choose a bus",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        title_label.pack(pady=10)

        buses = set()
        for u, v, data in self.graph.edges(data=True):
            buses.add(data["bus"])

        button_frame = tk.Frame(screen, bg="#2C3E50")
        button_frame.pack(fill="both", expand=True)

        columns = 6
        rows = (len(buses) + columns - 1) // columns

        for index, bus in enumerate(sorted(buses)):
            row = index // columns
            column = index % columns
            btn = tk.Button(
                button_frame,
                text=bus,
                font=("Helvetica", 12),
                bg="#90CAF9",
                fg="black",
                command=lambda bus_name=bus: self.show_bus_route(bus_name),
                width=15,
                height=2,
                wraplength=150,
            )
            btn.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        for i in range(columns):
            button_frame.grid_columnconfigure(i, weight=1, uniform="button")
        for i in range(rows):
            button_frame.grid_rowconfigure(i, weight=1, uniform="button")

        self.add_back_button(screen)
        self.change_screen(screen)

    def show_bus_route(self, bus_name):
        screen = tk.Frame(self.root, bg="#2C3E50")
        route_info_label = tk.Label(
            screen,
            text=f"Routes for bus {bus_name}:",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        route_info_label.pack(pady=20)

        canvas_frame = tk.Frame(screen)
        canvas_frame.pack(fill="both", expand=True)

        canvas = Canvas(canvas_frame, bg="#2C3E50", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll_y.set)

        path = []
        for u, v, data in self.graph.edges(data=True):
            if data["bus"] == bus_name:
                path.append((u, v))

        route_str = " → ".join([f"{u} → {v}" for u, v in path])

        text_widget = tk.Text(canvas, wrap="word", font=("Helvetica", 18), bg="#2C3E50", fg="white", height=22, width=160)
        text_widget.insert(tk.END, route_str)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=20, pady=20)

        self.add_back_button(screen)
        self.change_screen(screen)

    def find_routes_screen1(self):
        screen = tk.Frame(self.root, bg="#2C3E50")
        title_label = tk.Label(
            screen,
            text="Enter your starting station and your destination.",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#2C3E50",
        )
        title_label.pack(pady=20)
        start_label = tk.Label(screen, text="Starting Station:", font=("Helvetica", 14), fg="white", bg="#2C3E50")
        start_label.pack(pady=5)
        start_entry = tk.Entry(screen, font=("Helvetica", 14))
        start_entry.pack(pady=5)
        end_label = tk.Label(screen, text="Destination:", font=("Helvetica", 14), fg="white", bg="#2C3E50")
        end_label.pack(pady=5)
        end_entry = tk.Entry(screen, font=("Helvetica", 14))
        end_entry.pack(pady=5)

        recommend_frame = tk.Frame(screen, bg="#2C3E50")
        recommend_frame.pack(pady=10)

        def populate_recommendations():
            for widget in recommend_frame.winfo_children():
                widget.destroy()
            stations = list(self.graph.nodes)
            random.shuffle(stations)
            rows = 4
            cols = 5
            for i in range(rows):
                for j in range(cols):
                    index = i * cols + j
                    if index < len(stations):
                        station = stations[index]
                        btn = tk.Button(
                            recommend_frame,
                            text=station,
                            font=("Helvetica", 12),
                            bg="#90CAF9",
                            fg="black",
                            command=lambda s=station: self.handle_recommendation(s, start_entry, end_entry),
                            width=15,
                            height=4,
                            wraplength=120
                        )
                        btn.grid(row=i, column=j, padx=5, pady=5)

        populate_recommendations()

        def randomize_recommendations():
            populate_recommendations()

        randomize_button = tk.Button(
            screen,
            text="Re-Randomize Recommendations",
            font=("Helvetica", 14),
            bg="#FFEB3B",
            fg="black",
            command=randomize_recommendations
        )
        randomize_button.pack(pady=10)

        def submit():
            start_station = start_entry.get().strip()
            end_station = end_entry.get().strip()
            if start_station and end_station:
                self.find_routes_screen2(start_station, end_station)
            else:
                messagebox.showerror("Error", "Please enter both stations.")

        submit_button = tk.Button(screen, text="Find route", font=("Helvetica", 14), command=submit, bg="#4CAF50", fg="white")
        submit_button.pack(pady=20)
        self.add_back_button(screen)
        self.change_screen(screen)

    def handle_recommendation(self, station, start_entry, end_entry):
        if start_entry.get().strip() and end_entry.get().strip():
            messagebox.showerror("Error", "Please delete one station before selecting a recommended one.")
            return
        if not start_entry.get().strip():
            start_entry.delete(0, tk.END)
            start_entry.insert(0, station)
        elif not end_entry.get().strip():
            end_entry.delete(0, tk.END)
            end_entry.insert(0, station)

    def find_routes_screen2(self, start_station, end_station):
        screen = tk.Frame(self.root, bg="#2C3E50")
        result_label = tk.Label(
            screen,
            text="Result",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#34495E",
        )
        result_label.pack(pady=20)
        try:
            path = nx.shortest_path(self.graph, source=start_station, target=end_station)
            bus_name = self.graph[path[0]][path[1]]["bus"]
            result_text = f"You can travel with bus '{bus_name}' through this route: " + " → ".join(path)
        except nx.NetworkXNoPath:
            result_text = "Sorry! No route found between these stations."
        result = tk.Label(screen, text=result_text, font=("Helvetica", 14), fg="white", bg="#2C3E50", wraplength=700)
        result.pack(pady=20)
        self.add_back_button(screen)
        self.change_screen(screen)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusWayApp(root)
    root.mainloop()