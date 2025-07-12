import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import time
import json
import os
from tkinter import font

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.tasks = []
        self.completed_tasks = []
        self.streak_count = 0
        self.last_completed_date = None
        self.water_reminder_active = True
        self.scheduled_tasks = []
        
        # Load data
        self.load_data()
        
        # Start background threads
        self.start_water_reminder()
        self.start_scheduler_check()
        
        # Create GUI
        self.create_widgets()
        
        # Start streak check
        self.update_streak_display()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(main_frame, text="📝 Advanced To-Do List Manager", 
                              font=title_font, bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=(0, 20))
        
        # Top frame for stats
        stats_frame = tk.Frame(main_frame, bg='#e6f3ff', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Streak display
        self.streak_label = tk.Label(stats_frame, text=f"🔥 Current Streak: {self.streak_count} days", 
                                    font=("Arial", 12, "bold"), bg='#e6f3ff', fg='#ff4444')
        self.streak_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Tasks count
        self.tasks_count_label = tk.Label(stats_frame, text=f"📋 Active Tasks: {len(self.tasks)}", 
                                         font=("Arial", 10), bg='#e6f3ff', fg='#333333')
        self.tasks_count_label.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Water reminder toggle
        self.water_var = tk.BooleanVar(value=self.water_reminder_active)
        water_check = tk.Checkbutton(stats_frame, text="💧 Water Reminder", 
                                    variable=self.water_var, command=self.toggle_water_reminder,
                                    bg='#e6f3ff', font=("Arial", 10))
        water_check.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tasks tab
        self.tasks_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.tasks_frame, text="📋 Tasks")
        
        # Scheduler tab
        self.scheduler_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.scheduler_frame, text="⏰ Scheduler")
        
        # Completed tab
        self.completed_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.completed_frame, text="✅ Completed")
        
        self.create_tasks_tab()
        self.create_scheduler_tab()
        self.create_completed_tab()
        
    def create_tasks_tab(self):
        # Add task frame
        add_frame = tk.Frame(self.tasks_frame, bg='#ffffff')
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(add_frame, text="New Task:", font=("Arial", 10, "bold"), 
                bg='#ffffff').pack(side=tk.LEFT, padx=(0, 10))
        
        self.task_entry = tk.Entry(add_frame, font=("Arial", 10), width=40)
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_btn = tk.Button(add_frame, text="Add Task", command=self.add_task, 
                           bg='#4CAF50', fg='white', font=("Arial", 10, "bold"))
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Priority selection
        tk.Label(add_frame, text="Priority:", font=("Arial", 10), 
                bg='#ffffff').pack(side=tk.LEFT, padx=(10, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(add_frame, textvariable=self.priority_var, 
                                     values=["High", "Medium", "Low"], width=10)
        priority_combo.pack(side=tk.LEFT)
        
        # Tasks list frame
        list_frame = tk.Frame(self.tasks_frame, bg='#ffffff')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable listbox
        self.tasks_listbox = tk.Listbox(list_frame, font=("Arial", 10), 
                                       selectmode=tk.SINGLE, height=15)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        self.tasks_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.tasks_frame, bg='#ffffff')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        complete_btn = tk.Button(buttons_frame, text="✅ Complete", 
                                command=self.complete_task, bg='#2196F3', fg='white',
                                font=("Arial", 10, "bold"))
        complete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = tk.Button(buttons_frame, text="🗑️ Delete", 
                              command=self.delete_task, bg='#f44336', fg='white',
                              font=("Arial", 10, "bold"))
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        edit_btn = tk.Button(buttons_frame, text="✏️ Edit", 
                            command=self.edit_task, bg='#FF9800', fg='white',
                            font=("Arial", 10, "bold"))
        edit_btn.pack(side=tk.LEFT)
        
        self.refresh_tasks_list()
        
    def create_scheduler_tab(self):
        # Schedule task frame
        schedule_frame = tk.Frame(self.scheduler_frame, bg='#ffffff')
        schedule_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(schedule_frame, text="Schedule Task:", font=("Arial", 12, "bold"), 
                bg='#ffffff').pack(anchor=tk.W, pady=(0, 10))
        
        # Task name
        task_frame = tk.Frame(schedule_frame, bg='#ffffff')
        task_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(task_frame, text="Task:", font=("Arial", 10), 
                bg='#ffffff', width=10).pack(side=tk.LEFT)
        self.schedule_task_entry = tk.Entry(task_frame, font=("Arial", 10), width=40)
        self.schedule_task_entry.pack(side=tk.LEFT, padx=10)
        
        # Date and time
        datetime_frame = tk.Frame(schedule_frame, bg='#ffffff')
        datetime_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(datetime_frame, text="Date:", font=("Arial", 10), 
                bg='#ffffff', width=10).pack(side=tk.LEFT)
        self.date_entry = tk.Entry(datetime_frame, font=("Arial", 10), width=15)
        self.date_entry.pack(side=tk.LEFT, padx=10)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(datetime_frame, text="Time:", font=("Arial", 10), 
                bg='#ffffff').pack(side=tk.LEFT, padx=(20, 10))
        self.time_entry = tk.Entry(datetime_frame, font=("Arial", 10), width=15)
        self.time_entry.pack(side=tk.LEFT, padx=10)
        self.time_entry.insert(0, "09:00")
        
        # Schedule button
        schedule_btn = tk.Button(schedule_frame, text="⏰ Schedule Task", 
                                command=self.schedule_task, bg='#9C27B0', fg='white',
                                font=("Arial", 10, "bold"))
        schedule_btn.pack(pady=10)
        
        # Scheduled tasks list
        scheduled_frame = tk.Frame(self.scheduler_frame, bg='#ffffff')
        scheduled_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(scheduled_frame, text="Scheduled Tasks:", font=("Arial", 12, "bold"), 
                bg='#ffffff').pack(anchor=tk.W, pady=(0, 10))
        
        self.scheduled_listbox = tk.Listbox(scheduled_frame, font=("Arial", 10), height=10)
        self.scheduled_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Remove scheduled task button
        remove_scheduled_btn = tk.Button(scheduled_frame, text="Remove Scheduled Task", 
                                        command=self.remove_scheduled_task, 
                                        bg='#f44336', fg='white', font=("Arial", 10, "bold"))
        remove_scheduled_btn.pack(pady=10)
        
        self.refresh_scheduled_list()
        
    def create_completed_tab(self):
        # Completed tasks list
        completed_frame = tk.Frame(self.completed_frame, bg='#ffffff')
        completed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(completed_frame, text="Completed Tasks:", font=("Arial", 12, "bold"), 
                bg='#ffffff').pack(anchor=tk.W, pady=(0, 10))
        
        self.completed_listbox = tk.Listbox(completed_frame, font=("Arial", 10), height=15)
        self.completed_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Clear completed button
        clear_btn = tk.Button(completed_frame, text="Clear Completed", 
                             command=self.clear_completed, bg='#607D8B', fg='white',
                             font=("Arial", 10, "bold"))
        clear_btn.pack(pady=10)
        
        self.refresh_completed_list()
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            priority = self.priority_var.get()
            task = {
                'text': task_text,
                'priority': priority,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks_list()
            self.save_data()
            self.update_tasks_count()
            
    def complete_task(self):
        selection = self.tasks_listbox.curselection()
        if selection:
            task = self.tasks.pop(selection[0])
            task['completed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.completed_tasks.append(task)
            self.refresh_tasks_list()
            self.refresh_completed_list()
            self.save_data()
            self.update_streak()
            self.update_tasks_count()
            messagebox.showinfo("Task Completed", f"Great job! Task completed: {task['text']}")
            
    def delete_task(self):
        selection = self.tasks_listbox.curselection()
        if selection:
            task = self.tasks[selection[0]]
            if messagebox.askyesno("Delete Task", f"Are you sure you want to delete: {task['text']}?"):
                self.tasks.pop(selection[0])
                self.refresh_tasks_list()
                self.save_data()
                self.update_tasks_count()
                
    def edit_task(self):
        selection = self.tasks_listbox.curselection()
        if selection:
            task = self.tasks[selection[0]]
            new_text = tk.simpledialog.askstring("Edit Task", "Enter new task text:", 
                                                initialvalue=task['text'])
            if new_text:
                task['text'] = new_text.strip()
                self.refresh_tasks_list()
                self.save_data()
                
    def schedule_task(self):
        task_text = self.schedule_task_entry.get().strip()
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        
        if task_text and date_str and time_str:
            try:
                scheduled_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                if scheduled_datetime <= datetime.now():
                    messagebox.showerror("Error", "Scheduled time must be in the future!")
                    return
                
                scheduled_task = {
                    'text': task_text,
                    'datetime': scheduled_datetime,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                self.scheduled_tasks.append(scheduled_task)
                self.schedule_task_entry.delete(0, tk.END)
                self.refresh_scheduled_list()
                self.save_data()
                messagebox.showinfo("Task Scheduled", f"Task scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
                
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format! Use YYYY-MM-DD for date and HH:MM for time.")
                
    def remove_scheduled_task(self):
        selection = self.scheduled_listbox.curselection()
        if selection:
            task = self.scheduled_tasks[selection[0]]
            if messagebox.askyesno("Remove Scheduled Task", f"Remove scheduled task: {task['text']}?"):
                self.scheduled_tasks.pop(selection[0])
                self.refresh_scheduled_list()
                self.save_data()
                
    def clear_completed(self):
        if messagebox.askyesno("Clear Completed", "Are you sure you want to clear all completed tasks?"):
            self.completed_tasks.clear()
            self.refresh_completed_list()
            self.save_data()
            
    def refresh_tasks_list(self):
        self.tasks_listbox.delete(0, tk.END)
        # Sort by priority
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(self.tasks, key=lambda x: priority_order[x['priority']])
        
        for task in sorted_tasks:
            priority_symbol = {"High": "🔥", "Medium": "⚡", "Low": "📝"}
            display_text = f"{priority_symbol[task['priority']]} {task['text']} ({task['created']})"
            self.tasks_listbox.insert(tk.END, display_text)
            
    def refresh_scheduled_list(self):
        self.scheduled_listbox.delete(0, tk.END)
        for task in sorted(self.scheduled_tasks, key=lambda x: x['datetime']):
            display_text = f"⏰ {task['text']} - {task['datetime'].strftime('%Y-%m-%d %H:%M')}"
            self.scheduled_listbox.insert(tk.END, display_text)
            
    def refresh_completed_list(self):
        self.completed_listbox.delete(0, tk.END)
        for task in reversed(self.completed_tasks):  # Show most recent first
            display_text = f"✅ {task['text']} - Completed: {task['completed']}"
            self.completed_listbox.insert(tk.END, display_text)
            
    def update_streak(self):
        today = datetime.now().date()
        if self.last_completed_date:
            last_date = datetime.strptime(self.last_completed_date, "%Y-%m-%d").date()
            if today == last_date:
                return  # Already updated today
            elif today == last_date + timedelta(days=1):
                self.streak_count += 1
            else:
                self.streak_count = 1
        else:
            self.streak_count = 1
            
        self.last_completed_date = today.strftime("%Y-%m-%d")
        self.update_streak_display()
        self.save_data()
        
    def update_streak_display(self):
        self.streak_label.config(text=f"🔥 Current Streak: {self.streak_count} days")
        
    def update_tasks_count(self):
        self.tasks_count_label.config(text=f"📋 Active Tasks: {len(self.tasks)}")
        
    def toggle_water_reminder(self):
        self.water_reminder_active = self.water_var.get()
        self.save_data()
        
    def start_water_reminder(self):
        def water_reminder():
            while True:
                time.sleep(1800)  # 30 minutes = 1800 seconds
                if self.water_reminder_active:
                    self.show_water_reminder()
                    
        thread = threading.Thread(target=water_reminder, daemon=True)
        thread.start()
        
    def show_water_reminder(self):
        def show_popup():
            messagebox.showinfo("Water Reminder", "💧 Time to drink water! Stay hydrated! 💧")
        
        self.root.after(0, show_popup)
        
    def start_scheduler_check(self):
        def check_scheduled_tasks():
            while True:
                time.sleep(60)  # Check every minute
                current_time = datetime.now()
                
                for task in self.scheduled_tasks[:]:  # Create a copy to iterate
                    if current_time >= task['datetime']:
                        self.show_scheduled_task_alarm(task)
                        self.scheduled_tasks.remove(task)
                        self.root.after(0, self.refresh_scheduled_list)
                        self.root.after(0, self.save_data)
                        
        thread = threading.Thread(target=check_scheduled_tasks, daemon=True)
        thread.start()
        
    def show_scheduled_task_alarm(self, task):
        def show_alarm():
            result = messagebox.askyesno("⏰ Scheduled Task Alert", 
                                       f"Time for your scheduled task:\n\n'{task['text']}'\n\nAdd to active tasks?")
            if result:
                new_task = {
                    'text': task['text'],
                    'priority': 'High',
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                self.tasks.append(new_task)
                self.root.after(0, self.refresh_tasks_list)
                self.root.after(0, self.update_tasks_count)
                self.root.after(0, self.save_data)
                
        self.root.after(0, show_alarm)
        
    def save_data(self):
        data = {
            'tasks': self.tasks,
            'completed_tasks': self.completed_tasks,
            'streak_count': self.streak_count,
            'last_completed_date': self.last_completed_date,
            'water_reminder_active': self.water_reminder_active,
            'scheduled_tasks': []
        }
        
        # Convert scheduled tasks datetime objects to strings
        for task in self.scheduled_tasks:
            task_copy = task.copy()
            task_copy['datetime'] = task['datetime'].strftime("%Y-%m-%d %H:%M:%S")
            data['scheduled_tasks'].append(task_copy)
            
        try:
            with open('todo_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_data(self):
        try:
            if os.path.exists('todo_data.json'):
                with open('todo_data.json', 'r') as f:
                    data = json.load(f)
                    
                self.tasks = data.get('tasks', [])
                self.completed_tasks = data.get('completed_tasks', [])
                self.streak_count = data.get('streak_count', 0)
                self.last_completed_date = data.get('last_completed_date', None)
                self.water_reminder_active = data.get('water_reminder_active', True)
                
                # Convert scheduled tasks strings back to datetime objects
                scheduled_data = data.get('scheduled_tasks', [])
                for task_data in scheduled_data:
                    task = task_data.copy()
                    task['datetime'] = datetime.strptime(task_data['datetime'], "%Y-%m-%d %H:%M:%S")
                    self.scheduled_tasks.append(task)
                    
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def on_closing(self):
        self.save_data()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Make the window resizable
    root.minsize(800, 600)
    
    root.mainloop()

if __name__ == "__main__":
    main()