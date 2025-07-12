import tkinter as tk
from tkinter import messagebox, ttk
import re
import json  
import os
from tkinter import font

class ModernContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure modern colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'text': '#2c3e50',
            'muted': '#7f8c8d'
        }
        
        # Configure fonts
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'body': ('Segoe UI', 11),
            'small': ('Segoe UI', 9)
        }
        
        # File to store contacts
        self.contacts_file = "contacts.json"
        self.contacts = self.load_contacts()
        
        # Search variable
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_contacts)
        
        self.setup_styles()
        self.setup_ui()
        self.refresh_contact_list()
    
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['body'])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['body'])
        
        style.configure('Danger.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['body'])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['body'])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='solid',
                       font=self.fonts['body'])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=1)
        
        style.configure('Header.TFrame',
                       background=self.colors['primary'],
                       relief='flat')
        
        # Configure treeview
        style.configure('Modern.Treeview',
                       background='white',
                       foreground=self.colors['text'],
                       rowheight=40,
                       fieldbackground='white',
                       font=self.fonts['body'])
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       font=self.fonts['heading'])
    
    def setup_ui(self):
        """Set up the modern user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Left panel (form)
        left_panel = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Right panel (contact list)
        right_panel = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_form_panel(left_panel)
        self.create_list_panel(right_panel)
    
    def create_header(self, parent):
        """Create modern header"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=70)#
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="📱 Contact Book",
                              font=self.fonts['title'],
                              bg=self.colors['primary'],
                              fg='white')
        title_label.pack(side='left', padx=20, pady=20)
        
        # Stats
        stats_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        stats_frame.pack(side='right', padx=20, pady=20)
        
        self.stats_label = tk.Label(stats_frame,
                                   text=f"Total Contacts: {len(self.contacts)}",
                                   font=self.fonts['body'],
                                   bg=self.colors['primary'],
                                   fg='white')
        self.stats_label.pack()
    
    def create_form_panel(self, parent):
        """Create the form panel"""
        parent.configure(width=400)
        parent.pack_propagate(False)
        
        
        # Form content
        form_content = tk.Frame(parent, bg='white')
        form_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Name field
        self.create_field(form_content, "Full Name", "name_entry", 0, required=True)
        
        # Phone field with hint
        self.create_field_with_hint(form_content, "Phone Number", "phone_entry", 1, 
                                   required=True)
        
        # Email field with hint
        self.create_field_with_hint(form_content, "Email Address", "email_entry", 2, 
                                   )
        
        # Address field
        tk.Label(form_content,
                text="Address",
                font=self.fonts['body'],
                bg='white',
                fg=self.colors['text']).grid(row=8, column=0, sticky='w', pady=(15, 5))
        
        self.address_text = tk.Text(form_content,
                                   height=4,
                                   width=35,
                                   font=self.fonts['body'],
                                   relief='solid',
                                   bd=2,
                                   bg='white')
        self.address_text.grid(row=9, column=0, sticky='ew', pady=(0, 15))
        
        # Action buttons
        self.create_action_buttons(form_content)
        
        # Configure grid weights
        form_content.columnconfigure(0, weight=1)
    
    def create_field(self, parent, label, attr_name, row, required=False):
        """Create a form field"""
        label_text = f"{label} {'*' if required else ''}"
        tk.Label(parent,
                text=label_text,
                font=self.fonts['body'],
                bg='white',
                fg=self.colors['accent'] if required else self.colors['text']).grid(row=row*2, column=0, sticky='w', pady=(15, 5))
        
        entry = tk.Entry(parent,
                        font=self.fonts['body'],
                        relief='solid',
                        bd=2,
                        bg='white',
                        width=35)
        entry.grid(row=row*2+1, column=0, sticky='ew', pady=(0, 10))
        
        setattr(self, attr_name, entry)
    
    def create_field_with_hint(self, parent, label, attr_name, row, hint="", required=False):
        """Create a form field with hint text"""
        label_text = f"{label} {'*' if required else ''}"
        tk.Label(parent,
                text=label_text,
                font=self.fonts['body'],
                bg='white',
                fg=self.colors['accent'] if required else self.colors['text']).grid(row=row*2, column=0, sticky='w', pady=(15, 5))
        
        entry = tk.Entry(parent,
                        font=self.fonts['body'],
                        relief='solid',
                        bd=2,
                        bg='white',
                        width=35)
        entry.grid(row=row*2+1, column=0, sticky='ew', pady=(0, 5))
        
        # Add hint label
        if hint:
            hint_label = tk.Label(parent,
                                text=hint,
                                font=self.fonts['small'],
                                bg='white',
                                fg=self.colors['muted'])
            hint_label.grid(row=row*2+2, column=0, sticky='w', pady=(0, 10))
        
        setattr(self, attr_name, entry)
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.grid(row=12, column=0, pady=20, sticky='ew')
        
        # Add button
        add_btn = tk.Button(button_frame,
                           text="➕ Add Contact",
                           command=self.add_contact,
                           bg=self.colors['success'],
                           fg='white',
                           font=self.fonts['body'],
                           relief='flat',
                           cursor='hand2',
                           pady=10)
        add_btn.pack(fill='x', pady=5)
        
        # Update button
        update_btn = tk.Button(button_frame,
                              text="✏️ Update Contact",
                              command=self.update_contact,
                              bg=self.colors['secondary'],
                              fg='white',
                              font=self.fonts['body'],
                              relief='flat',
                              cursor='hand2',
                              pady=10)
        update_btn.pack(fill='x', pady=5)
        
        # Delete button
        delete_btn = tk.Button(button_frame,
                              text="🗑️ Delete Contact",
                              command=self.delete_contact,
                              bg=self.colors['accent'],
                              fg='white',
                              font=self.fonts['body'],
                              relief='flat',
                              cursor='hand2',
                              pady=10)
        delete_btn.pack(fill='x', pady=5)
        
        # Clear button
        clear_btn = tk.Button(button_frame,
                             text="🗃️ Clear Fields",
                             command=self.clear_fields,
                             bg=self.colors['warning'],
                             fg='white',
                             font=self.fonts['body'],
                             relief='flat',
                             cursor='hand2',
                             pady=10)
        clear_btn.pack(fill='x', pady=5)
    
    def create_list_panel(self, parent):
        """Create the contact list panel"""
        # List header
        list_header = tk.Frame(parent, bg=self.colors['primary'], height=50)
        list_header.pack(fill='x')
        list_header.pack_propagate(False)
        
        # Search frame
        search_frame = tk.Frame(list_header, bg=self.colors['primary'])
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame,
                text="🔍",
                font=self.fonts['heading'],
                bg=self.colors['primary'],
                fg='white').pack(side='left')
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=self.fonts['body'],
                               relief='solid',
                               bd=2,
                               bg='white')
        search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # List content
        list_content = tk.Frame(parent, bg='white')
        list_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(list_content, bg='white')
        tree_frame.pack(fill='both', expand=True)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame,
                                columns=("Name", "Phone", "Email", "Address"),
                                show="headings",
                                style='Modern.Treeview')
        
        # Configure columns
        self.tree.heading("Name", text="👤 Name")
        self.tree.heading("Phone", text="📞 Phone")
        self.tree.heading("Email", text="📧 Email")
        self.tree.heading("Address", text="🏠 Address")
        
        self.tree.column("Name", width=200)
        self.tree.column("Phone", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Address", width=250)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self.on_contact_select)
        self.tree.bind("<Double-1>", self.on_contact_double_click)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='white')
    
    def search_contacts(self, *args):
        """Search contacts based on search term"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and add contacts
        for i, contact in enumerate(self.contacts):
            if (search_term in contact['name'].lower() or
                search_term in contact['phone'].lower() or
                search_term in contact['email'].lower() or
                search_term in contact['address'].lower()):
                
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END,
                                values=(contact['name'], contact['phone'], 
                                       contact['email'], contact['address']),
                                tags=(tag,))
    
    def validate_phone(self, phone):
        """Validate phone number format with international support"""
        if not phone:
            return False, "Phone number is required"
        
        # Clean the phone number for validation
        phone = phone.strip()
        
        # Remove common separators for digit counting
        digits_only = re.sub(r'[^\d]', '', phone)
        
        # Check if it's a valid international format
        # Pattern for international phone numbers:
        # - Must start with + (optional)
        # - Country code (1-4 digits)
        # - Area/city code and number (6-14 digits)
        # - Total digits should be 7-15
        
        # Valid characters: digits, spaces, hyphens, parentheses, plus sign, dots
        if not re.match(r'^[\d\s\-\(\)\+\.]+$', phone):
            return False, "Phone number can only contain digits, spaces, hyphens, parentheses, plus sign, and dots"
        
        # Check digit count
        if len(digits_only) < 7:
            return False, "Phone number must have at least 7 digits"
        elif len(digits_only) > 15:
            return False, "Phone number cannot have more than 15 digits"
        
        # Check for valid international format patterns
        international_patterns = [
            r'^\+\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{0,4}$',  # +1-123-456-7890
            r'^\+\d{1,4}\s?\(\d{1,4}\)\s?\d{1,4}[\s\-]?\d{1,4}$',  # +1 (123) 456-7890
            r'^\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{0,4}$',  # 123-456-7890
            r'^\(\d{1,4}\)\s?\d{1,4}[\s\-]?\d{1,4}$',  # (123) 456-7890
            r'^\d{10,15}$',  # 1234567890
        ]
        
        is_valid_format = any(re.match(pattern, phone) for pattern in international_patterns)
        
        if not is_valid_format:
            return False, "Invalid phone number format."
        
        return True, "Valid phone number"
    
    def validate_email(self, email):
        """Validate email format with comprehensive checks"""
        if not email:
            return True, "Email is optional"
        
        email = email.strip()
        
        # Check length
        if len(email) > 254:
            return False, "Email address is too long (max 254 characters)"
        
        # Check for basic format
        if email.count('@') != 1:
            return False, "Email must contain exactly one @ symbol"
        
        local_part, domain_part = email.split('@')
        
        # Validate local part (before @)
        if not local_part or len(local_part) > 64:
            return False, "Email local part (before @) must be 1-64 characters"
        
        # Validate domain part (after @)
        if not domain_part or len(domain_part) > 253:
            return False, "Email domain part (after @) must be 1-253 characters"
        
        # Check for valid characters in local part
        if not re.match(r'^[a-zA-Z0-9._%+-]+$', local_part):
            return False, "Email local part contains invalid characters"
        
        # Check for valid domain format
        if not re.match(r'^[a-zA-Z0-9.-]+$', domain_part):
            return False, "Email domain contains invalid characters"
        
        # Check for valid domain structure
        if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain_part):
            return False, "Email domain must have a valid top-level domain (e.g., .com, .org)"
        
        # Check for consecutive dots
        if '..' in email:
            return False, "Email cannot contain consecutive dots"
        
        # Check for dots at the beginning or end of local part
        if local_part.startswith('.') or local_part.endswith('.'):
            return False, "Email local part cannot start or end with a dot"
        
        # Additional comprehensive check
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format. Use format: example@domain.com"
        
        return True, "Valid email"
    
    def show_success_message(self, title, message):
        """Show success message with custom styling"""
        messagebox.showinfo(title, message)
    
    def show_error_message(self, title, message):
        """Show error message with custom styling"""
        messagebox.showerror(title, message)
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        if not name:
            self.show_error_message("Validation Error", "Name is required")
            return
        
        phone_valid, phone_msg = self.validate_phone(phone)
        if not phone_valid:
            self.show_error_message("Phone Validation Error", phone_msg)
            return
        
        email_valid, email_msg = self.validate_email(email)
        if not email_valid:
            self.show_error_message("Email Validation Error", email_msg)
            return
        
        # Check for duplicate names
        if any(contact['name'].lower() == name.lower() for contact in self.contacts):
            self.show_error_message("Duplicate Contact", "Contact with this name already exists")
            return
        
        # Check for duplicate phone numbers
        if any(contact['phone'] == phone for contact in self.contacts):
            self.show_error_message("Duplicate Contact", "Contact with this phone number already exists")
            return
        
        # Check for duplicate email addresses (if provided)
        if email and any(contact['email'].lower() == email.lower() for contact in self.contacts):
            self.show_error_message("Duplicate Contact", "Contact with this email address already exists")
            return
        
        contact = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        
        self.contacts.append(contact)
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_fields()
        self.update_stats()
        
        self.show_success_message("Success", "Contact added successfully! 🎉")
    
    def update_contact(self):
        """Update selected contact"""
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_error_message("Selection Error", "Please select a contact to update")
            return
        
        contact_index = self.tree.index(selected_item[0])
        
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        if not name:
            self.show_error_message("Validation Error", "Name is required")
            return
        
        phone_valid, phone_msg = self.validate_phone(phone)
        if not phone_valid:
            self.show_error_message("Phone Validation Error", phone_msg)
            return
        
        email_valid, email_msg = self.validate_email(email)
        if not email_valid:
            self.show_error_message("Email Validation Error", email_msg)
            return
        
        # Find the actual contact in the filtered list
        visible_contacts = []
        search_term = self.search_var.get().lower()
        
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or
                search_term in contact['phone'].lower() or
                search_term in contact['email'].lower() or
                search_term in contact['address'].lower()):
                visible_contacts.append(contact)
        
        if contact_index < len(visible_contacts):
            # Find the original index
            original_contact = visible_contacts[contact_index]
            original_index = self.contacts.index(original_contact)
            
            # Check for duplicates (excluding the current contact)
            for i, contact in enumerate(self.contacts):
                if i != original_index:
                    if contact['name'].lower() == name.lower():
                        self.show_error_message("Duplicate Contact", "Another contact with this name already exists")
                        return
                    if contact['phone'] == phone:
                        self.show_error_message("Duplicate Contact", "Another contact with this phone number already exists")
                        return
                    if email and contact['email'].lower() == email.lower():
                        self.show_error_message("Duplicate Contact", "Another contact with this email address already exists")
                        return
            
            self.contacts[original_index] = {
                'name': name,
                'phone': phone,
                'email': email,
                'address': address
            }
        
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_fields()
        
        self.show_success_message("Success", "Contact updated successfully! ✅")
    
    def delete_contact(self):
        """Delete selected contact"""
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_error_message("Selection Error", "Please select a contact to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            contact_index = self.tree.index(selected_item[0])
            
            # Find the actual contact in the filtered list
            visible_contacts = []
            search_term = self.search_var.get().lower()
            
            for contact in self.contacts:
                if (search_term in contact['name'].lower() or
                    search_term in contact['phone'].lower() or
                    search_term in contact['email'].lower() or
                    search_term in contact['address'].lower()):
                    visible_contacts.append(contact)
            
            if contact_index < len(visible_contacts):
                # Find the original index and remove
                original_contact = visible_contacts[contact_index]
                self.contacts.remove(original_contact)
            
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_fields()
            self.update_stats()
            
            self.show_success_message("Success", "Contact deleted successfully! 🗑️")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
    
    def on_contact_select(self, event):
        """Handle contact selection"""
        selected_item = self.tree.selection()
        if selected_item:
            contact_index = self.tree.index(selected_item[0])
            
            # Get the visible contact based on search
            visible_contacts = []
            search_term = self.search_var.get().lower()
            
            for contact in self.contacts:
                if (search_term in contact['name'].lower() or
                    search_term in contact['phone'].lower() or
                    search_term in contact['email'].lower() or
                    search_term in contact['address'].lower()):
                    visible_contacts.append(contact)
            
            if contact_index < len(visible_contacts):
                contact = visible_contacts[contact_index]
                
                self.clear_fields()
                self.name_entry.insert(0, contact['name'])
                self.phone_entry.insert(0, contact['phone'])
                self.email_entry.insert(0, contact['email'])
                self.address_text.insert("1.0", contact['address'])
    
    def on_contact_double_click(self, event):
        """Handle double-click on contact"""
        self.on_contact_select(event)
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        self.search_contacts()
    
    def update_stats(self):
        """Update the statistics display"""
        self.stats_label.config(text=f"Total Contacts: {len(self.contacts)}")
    
    def load_contacts(self):
        """Load contacts from file"""
        try:
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
            return []
    
    def save_contacts(self):
        """Save contacts to file"""
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(self.contacts, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")

def main():
    root = tk.Tk()
    app = ModernContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()