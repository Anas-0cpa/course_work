import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
from datetime import datetime
import json
import os


class Reminder(ABC):
    @abstractmethod
    def send_reminder(self, birthday):
        pass


class Birthday:
    def __init__(self, name, dob, contact):
        self.__name = name
        self.__dob = datetime.strptime(dob, "%Y-%m-%d")
        self.__contact = contact

    def get_name(self):
        return self.__name

    def get_contact(self):
        return self.__contact

    def get_dob(self):
        return self.__dob

    def days_until_birthday(self):
        today = datetime.today()
        next_birthday = self.__dob.replace(year=today.year)
        if next_birthday < today:
            next_birthday = self.__dob.replace(year=today.year + 1)
        return (next_birthday - today).days

    def to_dict(self):
        return {
            "name": self.__name,
            "dob": self.__dob.strftime("%Y-%m-%d"),
            "contact": self.__contact
        }


class GuiReminder(Reminder):
    def __init__(self, master):
        self.master = master
        self.birthdays = []
        self.load_data()

        master.title("🎂 Birthday Reminder App")
        master.geometry("400x400")

        tk.Label(master, text="Name:").pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        tk.Label(master, text="Date of Birth (YYYY-MM-DD):").pack()
        self.dob_entry = tk.Entry(master)
        self.dob_entry.pack()

        tk.Label(master, text="Contact:").pack()
        self.contact_entry = tk.Entry(master)
        self.contact_entry.pack()

        tk.Button(master, text="Add Birthday", command=self.add_birthday).pack(pady=10)
        tk.Button(master, text="Show Reminders", command=self.show_reminders).pack(pady=10)

    def send_reminder(self, birthday):
        days_left = birthday.days_until_birthday()
        if days_left == 0:
            message = f"🎉 Today is {birthday.get_name()}'s birthday!"
        elif days_left <= 7:
            message = f"🔔 {birthday.get_name()}'s birthday is in {days_left} day(s)!"
        else:
            return
        messagebox.showinfo("Birthday Reminder", message)

    def add_birthday(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        contact = self.contact_entry.get()

        try:
            birthday = Birthday(name, dob, contact)
            self.birthdays.append(birthday)
            self.save_data()
            messagebox.showinfo("Success", "Birthday added successfully!")
            self.name_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.contact_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_reminders(self):
        if not self.birthdays:
            messagebox.showinfo("Reminders", "No birthdays saved.")
            return
        for birthday in self.birthdays:
            self.send_reminder(birthday)

    def save_data(self):
        with open("birthdays.json", "w") as f:
            json.dump([b.to_dict() for b in self.birthdays], f)

    def load_data(self):
        if os.path.exists("birthdays.json"):
            with open("birthdays.json", "r") as f:
                data = json.load(f)
                for item in data:
                    self.birthdays.append(Birthday(item["name"], item["dob"], item["contact"]))
        else:
            # Add default sample data if file doesn't exist
            self.birthdays = [
                Birthday("Alice", "2000-05-15", "alice@example.com"),
                Birthday("Bob", "1998-05-18", "bob@example.com"),
                Birthday("Charlie", "2001-05-20", "charlie@example.com")
            ]
            self.save_data()


if __name__ == "__main__":
    root = tk.Tk()
    app = GuiReminder(root)
    root.mainloop()