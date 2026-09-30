import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
 
 
# ==========================================================
# EMPLOYEE
# ==========================================================
 
class Employee:
    def __init__(self, emp_id, name, age, position, salary):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary
 
 
# ==========================================================
# MAIN SYSTEM
# ==========================================================
 
class EmployeeManagementSystem:
 
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#f4f6f8")
 
        # DSA
        self.employees = {}          # Dictionary
        self.employee_queue = deque() # Queue
        self.deleted_stack = []      # Stack
 
        # Colors
        self.bg = "#f4f6f8"
        self.sidebar = "#1e293b"
        self.blue = "#2563eb"
        self.green = "#16a34a"
        self.red = "#dc2626"
        self.yellow = "#f59e0b"
        self.text = "#1e293b"
 
        self.setup_style()
        self.create_interface()
        self.load_sample_data()
        self.refresh_table()
 
    # ======================================================
    # STYLE
    # ======================================================
 
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
 
        style.configure(
            "Treeview",
            background="white",
            foreground=self.text,
            rowheight=35,
            fieldbackground="white",
            font=("Arial", 10)
        )
 
        style.configure(
            "Treeview.Heading",
            background="#e2e8f0",
            foreground=self.text,
            font=("Arial", 10, "bold"),
            padding=8
        )
 
        style.map(
            "Treeview",
            background=[("selected", "#bfdbfe")],
            foreground=[("selected", "#1e3a8a")]
        )
 
    # ======================================================
    # MAIN INTERFACE
    # ======================================================
 
    def create_interface(self):
 
        # ---------- SIDEBAR ----------
 
        self.sidebar_frame = tk.Frame(
            self.root,
            bg=self.sidebar,
            width=230
        )
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
 
        tk.Label(
            self.sidebar_frame,
            text="EMPLOYEE",
            bg=self.sidebar,
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(pady=(35, 0))
 
        tk.Label(
            self.sidebar_frame,
            text="MANAGEMENT SYSTEM",
            bg=self.sidebar,
            fg="#94a3b8",
            font=("Arial", 9, "bold")
        ).pack(pady=(0, 30))
 
        buttons = [
            ("🏠  Dashboard", self.show_dashboard),
            ("👥  Employees", self.show_employees),
            ("➕  Add Employee", self.show_add_employee),
            ("🔍  Search", self.show_search),
            ("📋  Queue", self.show_queue),
            ("↩  Deleted Stack", self.show_stack)
        ]
 
        for text, command in buttons:
            self.sidebar_button(text, command)
 
        tk.Label(
            self.sidebar_frame,
            text="Python + Tkinter",
            bg=self.sidebar,
            fg="#64748b",
            font=("Arial", 9)
        ).pack(side="bottom", pady=(0, 20))
 
        tk.Label(
            self.sidebar_frame,
            text="DSA PROJECT",
            bg=self.sidebar,
            fg="#64748b",
            font=("Arial", 9, "bold")
        ).pack(side="bottom")
 
        # ---------- CONTENT ----------
 
        self.content = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.content.pack(side="left", fill="both", expand=True)
 
        self.show_dashboard()
 
    # ======================================================
    # SIDEBAR BUTTON
    # ======================================================
 
    def sidebar_button(self, text, command):
        tk.Button(
            self.sidebar_frame,
            text=text,
            command=command,
            bg=self.sidebar,
            fg="#cbd5e1",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            anchor="w",
            padx=25,
            font=("Arial", 11),
            cursor="hand2"
        ).pack(fill="x", pady=2, ipady=10)
 
    # ======================================================
    # COMMON FUNCTIONS
    # ======================================================
 
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
 
    def page_title(self, title, subtitle=""):
        frame = tk.Frame(self.content, bg=self.bg)
        frame.pack(fill="x", padx=30, pady=(25, 15))
 
        tk.Label(
            frame,
            text=title,
            bg=self.bg,
            fg=self.text,
            font=("Arial", 24, "bold")
        ).pack(anchor="w")
 
        if subtitle:
            tk.Label(
                frame,
                text=subtitle,
                bg=self.bg,
                fg="#64748b",
                font=("Arial", 10)
            ).pack(anchor="w", pady=5)
 
    def button(self, parent, text, command, color, side="left"):
        tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=side, padx=5)
 
    def make_table(self, parent):
        columns = ("ID", "Name", "Age", "Position", "Salary")
 
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings"
        )
 
        widths = {
            "ID": 100,
            "Name": 200,
            "Age": 80,
            "Position": 200,
            "Salary": 150
        }
 
        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                width=widths[column],
                anchor="center"
            )
 
        return tree
 
    def employee_values(self, employee):
        return (
            employee.emp_id,
            employee.name,
            employee.age,
            employee.position,
            f"₱{employee.salary:,.2f}"
        )
 
    # ======================================================
    # DASHBOARD
    # ======================================================
 
    def show_dashboard(self):
        self.clear_content()
        self.page_title(
            "Dashboard",
            "Employee Management System Overview"
        )
 
        cards = tk.Frame(self.content, bg=self.bg)
        cards.pack(fill="x", padx=30, pady=10)
 
        total = len(self.employees)
        salary = sum(e.salary for e in self.employees.values())
        average = salary / total if total else 0
 
        data = [
            ("👥", "Total Employees", total, self.blue),
            ("💰", "Total Salary", f"₱{salary:,.2f}", self.green),
            ("📊", "Average Salary", f"₱{average:,.2f}", self.yellow),
            ("📋", "Queue", len(self.employee_queue), "#8b5cf6")
        ]
 
        for i, item in enumerate(data):
            self.stat_card(cards, *item, i)
 
        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=20)
 
        tk.Label(
            frame,
            text="Recent Employees",
            bg="white",
            fg=self.text,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=15)
 
        tree = self.make_table(frame)
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
 
        for employee in list(self.employees.values())[-8:]:
            tree.insert("", "end", values=self.employee_values(employee))
 
    def stat_card(self, parent, icon, title, value, color, column):
        card = tk.Frame(parent, bg="white", height=120)
        card.grid(row=0, column=column, sticky="nsew", padx=7)
 
        parent.columnconfigure(column, weight=1)
 
        tk.Label(
            card,
            text=icon,
            bg="white",
            fg=color,
            font=("Arial", 24)
        ).pack(anchor="w", padx=18, pady=(15, 0))
 
        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#64748b",
            font=("Arial", 9)
        ).pack(anchor="w", padx=20)
 
        tk.Label(
            card,
            text=value,
            bg="white",
            fg=self.text,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=20)
 
    # ======================================================
    # EMPLOYEE PAGE
    # ======================================================
 
    def show_employees(self):
        self.clear_content()
        self.page_title(
            "Employees",
            "Manage employee records"
        )
 
        toolbar = tk.Frame(self.content, bg=self.bg)
        toolbar.pack(fill="x", padx=30)
 
        self.button(
            toolbar,
            "➕ Add Employee",
            self.show_add_employee,
            self.blue
        )
 
        self.button(
            toolbar,
            "↕ Sort by Name",
            self.sort_by_name,
            "#64748b"
        )
 
        self.button(
            toolbar,
            "💰 Sort by Salary",
            self.sort_by_salary,
            "#64748b"
        )
 
        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=15)
 
        self.employee_tree = self.make_table(frame)
        self.employee_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
 
        buttons = tk.Frame(self.content, bg=self.bg)
        buttons.pack(fill="x", padx=30, pady=(0, 20))
 
        self.button(
            buttons,
            "✏ Edit",
            self.edit_selected,
            self.yellow
        )
 
        self.button(
            buttons,
            "🗑 Delete",
            self.delete_selected,
            self.red
        )
 
        self.button(
            buttons,
            "📋 Add to Queue",
            self.queue_selected,
            "#8b5cf6"
        )
 
        self.refresh_table()
 
    def refresh_table(self):
        if not hasattr(self, "employee_tree"):
            return
 
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
 
        for employee in self.employees.values():
            self.employee_tree.insert(
                "",
                "end",
                values=self.employee_values(employee)
            )
 
    # ======================================================
    # ADD / EDIT FORM
    # ======================================================
 
    def show_add_employee(self):
        self.clear_content()
        self.page_title(
            "Add Employee",
            "Create a new employee record"
        )
 
        self.create_form()
 
    def create_form(self, employee=None):
        form = tk.Frame(self.content, bg="white")
        form.pack(padx=80, pady=20, fill="x")
 
        fields = [
            ("Employee ID", "emp_id"),
            ("Full Name", "name"),
            ("Age", "age"),
            ("Position", "position"),
            ("Salary", "salary")
        ]
 
        self.entries = {}
 
        for row, (label, key) in enumerate(fields):
 
            tk.Label(
                form,
                text=label,
                bg="white",
                fg=self.text,
                font=("Arial", 10, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=30,
                pady=12
            )
 
            entry = tk.Entry(
                form,
                font=("Arial", 11),
                relief="solid"
            )
 
            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=30,
                pady=12,
                ipady=7
            )
 
            self.entries[key] = entry
 
        form.columnconfigure(1, weight=1)
 
        if employee:
            values = {
                "emp_id": employee.emp_id,
                "name": employee.name,
                "age": employee.age,
                "position": employee.position,
                "salary": employee.salary
            }
 
            for key, value in values.items():
                self.entries[key].insert(0, value)
 
            self.entries["emp_id"].configure(state="disabled")
 
            command = lambda: self.update_employee(employee.emp_id)
            text = "💾 Update Employee"
 
        else:
            command = self.add_employee
            text = "➕ Add Employee"
 
        tk.Button(
            form,
            text=text,
            command=command,
            bg=self.blue,
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        ).grid(
            row=5,
            column=1,
            sticky="e",
            padx=30,
            pady=25
        )
 
    def get_form_data(self):
        return (
            self.entries["emp_id"].get().strip(),
            self.entries["name"].get().strip(),
            int(self.entries["age"].get()),
            self.entries["position"].get().strip(),
            float(self.entries["salary"].get())
        )
 
    # ======================================================
    # ADD EMPLOYEE
    # ======================================================
 
    def add_employee(self):
        try:
            emp_id, name, age, position, salary = self.get_form_data()
 
            if not emp_id or not name or not position:
                raise ValueError("Please fill in all fields.")
 
            if emp_id in self.employees:
                messagebox.showerror(
                    "Error",
                    "Employee ID already exists."
                )
                return
 
            if age <= 0 or salary < 0:
                raise ValueError("Invalid age or salary.")
 
            self.employees[emp_id] = Employee(
                emp_id, name, age, position, salary
            )
 
            messagebox.showinfo(
                "Success",
                "Employee added successfully!"
            )
 
            self.show_employees()
 
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
 
    # ======================================================
    # EDIT
    # ======================================================
 
    def edit_selected(self):
        selected = self.employee_tree.selection()
 
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an employee first."
            )
            return
 
        emp_id = self.employee_tree.item(
            selected[0],
            "values"
        )[0]
 
        employee = self.employees[emp_id]
 
        self.clear_content()
        self.page_title(
            "Edit Employee",
            "Update employee information"
        )
 
        self.create_form(employee)
 
    def update_employee(self, emp_id):
        try:
            _, name, age, position, salary = self.get_form_data()
 
            if not name or not position:
                raise ValueError("Please fill in all fields.")
 
            if age <= 0 or salary < 0:
                raise ValueError("Invalid age or salary.")
 
            employee = self.employees[emp_id]
 
            employee.name = name
            employee.age = age
            employee.position = position
            employee.salary = salary
 
            messagebox.showinfo(
                "Success",
                "Employee updated successfully!"
            )
 
            self.show_employees()
 
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
 
    # ======================================================
    # DELETE
    # ======================================================
 
    def delete_selected(self):
        selected = self.employee_tree.selection()
 
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an employee."
            )
            return
 
        emp_id = self.employee_tree.item(
            selected[0],
            "values"
        )[0]
 
        employee = self.employees[emp_id]
 
        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete {employee.name}?"
        ):
            # STACK
            self.deleted_stack.append(employee)
 
            del self.employees[emp_id]
 
            if emp_id in self.employee_queue:
                self.employee_queue.remove(emp_id)
 
            messagebox.showinfo(
                "Deleted",
                "Employee deleted successfully."
            )
 
            self.refresh_table()
 
    # ======================================================
    # SEARCH
    # ======================================================
 
    def show_search(self):
        self.clear_content()
        self.page_title(
            "Search Employee",
            "Linear search and binary search"
        )
 
        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="x", padx=50, pady=20)
 
        tk.Label(
            frame,
            text="Search:",
            bg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=15, pady=20)
 
        self.search_entry = tk.Entry(
            frame,
            font=("Arial", 11),
            width=35
        )
        self.search_entry.pack(side="left", ipady=7)
 
        self.button(
            frame,
            "🔍 Search Name",
            self.search_name,
            self.blue
        )
 
        self.button(
            frame,
            "⚡ Binary Search ID",
            self.binary_search,
            "#8b5cf6"
        )
 
        result = tk.Frame(self.content, bg="white")
        result.pack(fill="both", expand=True, padx=50, pady=10)
 
        self.search_tree = self.make_table(result)
        self.search_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
 
    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
 
    def search_name(self):
        target = self.search_entry.get().lower()
        self.clear_tree(self.search_tree)
 
        found = False
 
        # LINEAR SEARCH
        for employee in self.employees.values():
            if target in employee.name.lower():
                self.search_tree.insert(
                    "",
                    "end",
                    values=self.employee_values(employee)
                )
                found = True
 
        if not found:
            messagebox.showinfo(
                "Search",
                "No employee found."
            )
 
    def binary_search(self):
        target = self.search_entry.get().strip()
 
        employees = sorted(
            self.employees.values(),
            key=lambda e: e.emp_id
        )
 
        left, right = 0, len(employees) - 1
 
        while left <= right:
            middle = (left + right) // 2
            current = employees[middle].emp_id
 
            if current == target:
                self.clear_tree(self.search_tree)
 
                self.search_tree.insert(
                    "",
                    "end",
                    values=self.employee_values(
                        employees[middle]
                    )
                )
                return
 
            if current < target:
                left = middle + 1
            else:
                right = middle - 1
 
        messagebox.showinfo(
            "Binary Search",
            "Employee ID not found."
        )
 
    # ======================================================
    # QUEUE
    # ======================================================
 
    def show_queue(self):
        self.clear_content()
        self.page_title(
            "Employee Queue",
            "FIFO - First In, First Out"
        )
 
        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="both", expand=True, padx=50, pady=20)
 
        self.queue_listbox = tk.Listbox(
            frame,
            font=("Arial", 12),
            bg="white"
        )
        self.queue_listbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
 
        buttons = tk.Frame(frame, bg="white")
        buttons.pack(pady=(0, 20))
 
        self.button(
            buttons,
            "▶ Process First",
            self.process_queue,
            self.green
        )
 
        self.button(
            buttons,
            "🔄 Refresh",
            self.refresh_queue,
            self.blue
        )
 
        self.refresh_queue()
 
    def queue_selected(self):
        selected = self.employee_tree.selection()
 
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Select an employee first."
            )
            return
 
        emp_id = self.employee_tree.item(
            selected[0],
            "values"
        )[0]
 
        if emp_id in self.employee_queue:
            messagebox.showinfo(
                "Queue",
                "Employee is already in the queue."
            )
            return
 
        # ENQUEUE
        self.employee_queue.append(emp_id)
 
        messagebox.showinfo(
            "Queue",
            "Employee added to queue."
        )
 
    def refresh_queue(self):
        self.queue_listbox.delete(0, tk.END)
 
        for i, emp_id in enumerate(
            self.employee_queue,
            1
        ):
            employee = self.employees.get(emp_id)
 
            if employee:
                self.queue_listbox.insert(
                    tk.END,
                    f"{i}.  {employee.emp_id}  |  "
                    f"{employee.name}  |  "
                    f"{employee.position}"
                )
 
    def process_queue(self):
        if not self.employee_queue:
            messagebox.showinfo(
                "Queue",
                "The queue is empty."
            )
            return
 
        # DEQUEUE
        emp_id = self.employee_queue.popleft()
        employee = self.employees.get(emp_id)
 
        if employee:
            messagebox.showinfo(
                "Processing Employee",
                f"Processing:\n\n"
                f"ID: {employee.emp_id}\n"
                f"Name: {employee.name}\n"
                f"Position: {employee.position}"
            )
 
        self.refresh_queue()
 
    # ======================================================
    # STACK
    # ======================================================
 
    def show_stack(self):
        self.clear_content()
        self.page_title(
            "Deleted Employee Stack",
            "LIFO - Last In, First Out"
        )
 
        frame = tk.Frame(self.content, bg="white")
        frame.pack(fill="both", expand=True, padx=50, pady=20)
 
        listbox = tk.Listbox(
            frame,
            font=("Arial", 12),
            bg="white"
        )
        listbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
 
        # TOP OF STACK FIRST
        for employee in reversed(self.deleted_stack):
            listbox.insert(
                tk.END,
                f"{employee.emp_id}  |  "
                f"{employee.name}  |  "
                f"{employee.position}"
            )
 
        self.button(
            frame,
            "↩ Restore Last Deleted",
            self.undo_delete,
            self.green
        )
 
    def undo_delete(self):
        if not self.deleted_stack:
            messagebox.showinfo(
                "Stack",
                "No deleted employee to restore."
            )
            return
 
        # POP
        employee = self.deleted_stack.pop()
 
        self.employees[employee.emp_id] = employee
 
        messagebox.showinfo(
            "Restored",
            f"{employee.name} has been restored."
        )
 
        self.show_stack()
 
    # ======================================================
    # SORTING
    # ======================================================
 
    def sort_by_name(self):
        employees = sorted(
            self.employees.values(),
            key=lambda e: e.name.lower()
        )
 
        self.employees = {
            e.emp_id: e
            for e in employees
        }
 
        self.refresh_table()
 
    def sort_by_salary(self):
        employees = sorted(
            self.employees.values(),
            key=lambda e: e.salary,
            reverse=True
        )
 
        self.employees = {
            e.emp_id: e
            for e in employees
        }
 
        self.refresh_table()
 
    # ======================================================
    # SAMPLE DATA
    # ======================================================
 
    def load_sample_data(self):
 
        data = [
            ("EMP001", "Juan Dela Cruz", 25,
             "Software Developer", 35000),
 
            ("EMP002", "Maria Santos", 28,
             "HR Manager", 45000),
 
            ("EMP003", "Pedro Reyes", 30,
             "Accountant", 40000),
 
            ("EMP004", "Ana Garcia", 24,
             "UI Designer", 32000),
 
            ("EMP005", "Mark Lopez", 35,
             "Project Manager", 55000)
        ]
 
        for emp_id, name, age, position, salary in data:
            self.employees[emp_id] = Employee(
                emp_id,
                name,
                age,
                position,
                salary
            )
 
 
# ==========================================================
# PROGRAM START
# ==========================================================
 
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()