import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
# Fix import path for backend classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/classes')))

from CinemaManager import CinemaManager
from Film import Film
from Screen import Screen
from Cinema import Cinema
from Booking import Booking

class HorizonCinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horizon Cinema Booking System")
        self.manager = CinemaManager()
        self.current_user = None

        self.login_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Sign Up", command=self.signup_screen).pack()

    def signup_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Create Username:").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()

        tk.Label(self.root, text="Create Password:").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()

        tk.Button(self.root, text="Register", command=self.register_user).pack()
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        success = self.manager.add_user(username, password)
        if success:
            messagebox.showinfo("Success", "User registered successfully. Please login.")
            self.login_screen()
        else:
            messagebox.showerror("Error", "Username already exists. Please choose another.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Login Success", f"Welcome {user.username}!")
            self.main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text=f"Welcome {self.current_user.username} ({self.current_user.role})").pack()

        tk.Button(self.root, text="View Cinemas", command=self.view_cinemas).pack()
        tk.Button(self.root, text="Add Cinema", command=self.add_cinema).pack()
        tk.Button(self.root, text="Book Tickets", command=self.book_tickets).pack()
        tk.Button(self.root, text="Logout", command=self.logout).pack()

    def view_cinemas(self):
        self.clear_window()
        tk.Label(self.root, text="Cinemas:").pack()
        for cinema in self.manager.cinemas:
            tk.Label(self.root, text=f"{cinema.name} - {cinema.city}").pack()
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def add_cinema(self):
        cinema_name = simpledialog.askstring("Add Cinema", "Enter cinema name:")
        city = simpledialog.askstring("Add Cinema", "Enter city:")
        if cinema_name and city:
            self.manager.add_cinema(cinema_name, city)
            messagebox.showinfo("Success", "Cinema added successfully")
        self.main_menu()

    def book_tickets(self):
        self.clear_window()
        tk.Label(self.root, text="Select Cinema:").pack()
        self.cinema_var = tk.StringVar(self.root)
        cinema_names = [cinema.name for cinema in self.manager.cinemas]
        if not cinema_names:
            messagebox.showinfo("No Cinemas", "No cinemas available to book.")
            self.main_menu()
            return
        self.cinema_var.set(cinema_names[0])
        cinema_menu = tk.OptionMenu(self.root, self.cinema_var, *cinema_names)
        cinema_menu.pack()

        tk.Button(self.root, text="Next", command=self.select_film).pack()
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def select_film(self):
        selected_cinema_name = self.cinema_var.get()
        self.selected_cinema = next((c for c in self.manager.cinemas if c.name == selected_cinema_name), None)
        if not self.selected_cinema:
            messagebox.showerror("Error", "Selected cinema not found.")
            self.book_tickets()
            return

        self.clear_window()
        tk.Label(self.root, text="Select Film and Show Time:").pack()

        self.film_showings = []
        for screen in self.selected_cinema.screens:
            for film, show_time in screen.showings:
                self.film_showings.append((film, show_time, screen))

        if not self.film_showings:
            messagebox.showinfo("No Showings", "No films available for booking in this cinema.")
            self.book_tickets()
            return

        self.film_var = tk.StringVar(self.root)
        film_options = [f"{film.title} at {show_time}" for film, show_time, _ in self.film_showings]
        self.film_var.set(film_options[0])
        film_menu = tk.OptionMenu(self.root, self.film_var, *film_options)
        film_menu.pack()

        tk.Button(self.root, text="Next", command=self.select_seats).pack()
        tk.Button(self.root, text="Back", command=self.book_tickets).pack()

    def select_seats(self):
        selected_option = self.film_var.get()
        index = [f"{film.title} at {show_time}" for film, show_time, _ in self.film_showings].index(selected_option)
        self.selected_film, self.selected_show_time, self.selected_screen = self.film_showings[index]

        self.clear_window()
        tk.Label(self.root, text=f"Selected: {self.selected_film.title} at {self.selected_show_time}").pack()

        tk.Label(self.root, text="Number of Tickets:").pack()
        self.tickets_entry = tk.Entry(self.root)
        self.tickets_entry.pack()

        tk.Label(self.root, text="Seat Numbers (comma separated):").pack()
        self.seats_entry = tk.Entry(self.root)
        self.seats_entry.pack()

        tk.Button(self.root, text="Confirm Booking", command=self.confirm_booking).pack()
        tk.Button(self.root, text="Back", command=self.select_film).pack()

    def confirm_booking(self):
        try:
            num_tickets = int(self.tickets_entry.get())
            seat_numbers = [seat.strip() for seat in self.seats_entry.get().split(',')]
            if len(seat_numbers) != num_tickets:
                messagebox.showerror("Error", "Number of seats does not match number of tickets.")
                return
            booking = Booking(self.selected_film, self.selected_screen, self.selected_show_time, num_tickets, seat_numbers)
            self.manager.add_booking(booking)
            messagebox.showinfo("Success", f"Booking confirmed! Reference: {booking.booking_reference}")
            self.main_menu()
        except ValueError:
            messagebox.showerror("Error", "Invalid number of tickets.")

    def logout(self):
        self.current_user = None
        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HorizonCinemaApp(root)
    root.mainloop()
