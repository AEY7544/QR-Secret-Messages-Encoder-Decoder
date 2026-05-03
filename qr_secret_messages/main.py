import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from crypto_utils import encrypt_message, decrypt_message
from qr_utils import generate_qr_code, read_qr_code, save_qr_code
from auth_system import AuthSystem
from password_strength import check_password_strength, is_password_strong


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Secret Messages")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_register_tab()
        self._create_login_tab()
        self._create_encrypt_tab()
        self._create_decrypt_tab()
    
    def _create_register_tab(self):
        register_frame = ttk.Frame(self.notebook)
        self.notebook.add(register_frame, text="Register")
        
        tk.Label(register_frame, text="Create New Account", font=("Arial", 16, "bold"), pady=10).pack()
        
        user_frame = ttk.LabelFrame(register_frame, text="Username", padding=10)
        user_frame.pack(fill=tk.X, padx=20, pady=5)
        self.register_username_entry = ttk.Entry(user_frame, width=40, font=("Arial", 10))
        self.register_username_entry.pack(pady=5)
        
        pwd_frame = ttk.LabelFrame(register_frame, text="Password", padding=10)
        pwd_frame.pack(fill=tk.X, padx=20, pady=5)
        self.register_password_entry = ttk.Entry(pwd_frame, show="*", width=40, font=("Arial", 10))
        self.register_password_entry.pack(pady=5)
        
        self.register_strength_label = tk.Label(pwd_frame, text="", font=("Arial", 9), fg="gray")
        self.register_strength_label.pack(pady=2)
        
        self.register_feedback_text = scrolledtext.ScrolledText(pwd_frame, height=6, width=50, wrap=tk.WORD, font=("Arial", 8), state=tk.DISABLED)
        self.register_feedback_text.pack(pady=5)
        
        register_btn = ttk.Button(register_frame, text="Register", style="Accent.TButton")
        register_btn.pack(pady=10)
        self.register_button = register_btn
    
    def _create_login_tab(self):
        login_frame = ttk.Frame(self.notebook)
        self.notebook.add(login_frame, text="Login")
        
        tk.Label(login_frame, text="Login to Your Account", font=("Arial", 16, "bold"), pady=10).pack()
        
        self.login_status_label = tk.Label(login_frame, text="Not logged in", font=("Arial", 10), fg="red", pady=5)
        self.login_status_label.pack()
        
        user_frame = ttk.LabelFrame(login_frame, text="Username", padding=10)
        user_frame.pack(fill=tk.X, padx=20, pady=5)
        self.login_username_entry = ttk.Entry(user_frame, width=40, font=("Arial", 10))
        self.login_username_entry.pack(pady=5)
        
        pwd_frame = ttk.LabelFrame(login_frame, text="Password", padding=10)
        pwd_frame.pack(fill=tk.X, padx=20, pady=5)
        self.login_password_entry = ttk.Entry(pwd_frame, show="*", width=40, font=("Arial", 10))
        self.login_password_entry.pack(pady=5)
        
        self.failed_attempts_label = tk.Label(login_frame, text="", font=("Arial", 9), fg="orange")
        self.failed_attempts_label.pack(pady=2)
        
        login_btn = ttk.Button(login_frame, text="Login", style="Accent.TButton")
        login_btn.pack(pady=10)
        self.login_button = login_btn
        
        logout_btn = ttk.Button(login_frame, text="Logout")
        logout_btn.pack(pady=5)
        self.logout_button = logout_btn
    
    def _create_encrypt_tab(self):
        encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(encrypt_frame, text="Encrypt")
        
        tk.Label(encrypt_frame, text="Encrypt Message to QR Code", font=("Arial", 16, "bold"), pady=10).pack()
        
        self.encrypt_auth_label = tk.Label(encrypt_frame, text="Please login to use encryption features", font=("Arial", 10), fg="red", pady=5)
        self.encrypt_auth_label.pack()
        
        msg_frame = ttk.LabelFrame(encrypt_frame, text="Message Input", padding=10)
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.message_text = scrolledtext.ScrolledText(msg_frame, height=8, width=60, wrap=tk.WORD, font=("Arial", 10))
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        load_file_btn = ttk.Button(msg_frame, text="Load from .txt File")
        load_file_btn.pack(pady=5)
        self.load_file_button = load_file_btn
        
        pwd_frame = ttk.LabelFrame(encrypt_frame, text="Encryption Password", padding=10)
        pwd_frame.pack(fill=tk.X, padx=10, pady=5)
        self.password_entry = ttk.Entry(pwd_frame, show="*", width=50, font=("Arial", 10))
        self.password_entry.pack(pady=5)
        
        generate_btn = ttk.Button(encrypt_frame, text="Generate QR Code", style="Accent.TButton")
        generate_btn.pack(pady=10)
        self.generate_button = generate_btn
        
        qr_preview_frame = ttk.LabelFrame(encrypt_frame, text="QR Code Preview", padding=10)
        qr_preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.qr_label = tk.Label(qr_preview_frame, text="QR code will appear here", bg="white", relief=tk.SUNKEN, width=50, height=20)
        self.qr_label.pack(pady=10)
        
        save_frame = ttk.Frame(encrypt_frame)
        save_frame.pack(pady=10)
        save_qr_btn = ttk.Button(save_frame, text="Save QR as PNG")
        save_qr_btn.pack(side=tk.LEFT, padx=5)
        self.save_qr_button = save_qr_btn
        
        save_bin_btn = ttk.Button(save_frame, text="Save Encrypted Data (.bin)")
        save_bin_btn.pack(side=tk.LEFT, padx=5)
        self.save_bin_button = save_bin_btn
    
    def _create_decrypt_tab(self):
        decrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(decrypt_frame, text="Decrypt")
        
        tk.Label(decrypt_frame, text="Decrypt QR Code to Message", font=("Arial", 16, "bold"), pady=10).pack()
        
        self.decrypt_auth_label = tk.Label(decrypt_frame, text="Please login to use decryption features", font=("Arial", 10), fg="red", pady=5)
        self.decrypt_auth_label.pack()
        
        load_frame = ttk.LabelFrame(decrypt_frame, text="Load QR Code", padding=10)
        load_frame.pack(fill=tk.X, padx=10, pady=5)
        load_qr_btn = ttk.Button(load_frame, text="Load QR Code Image")
        load_qr_btn.pack(pady=5)
        self.load_qr_button = load_qr_btn
        
        self.qr_path_label = tk.Label(load_frame, text="No QR code loaded", fg="gray", font=("Arial", 9))
        self.qr_path_label.pack()
        
        pwd_frame = ttk.LabelFrame(decrypt_frame, text="Decryption Password", padding=10)
        pwd_frame.pack(fill=tk.X, padx=10, pady=5)
        self.decrypt_password_entry = ttk.Entry(pwd_frame, show="*", width=50, font=("Arial", 10))
        self.decrypt_password_entry.pack(pady=5)
        
        self.decrypt_attempts_label = tk.Label(decrypt_frame, text="", font=("Arial", 9), fg="orange")
        self.decrypt_attempts_label.pack(pady=2)
        
        decrypt_btn = ttk.Button(decrypt_frame, text="Decrypt Message", style="Accent.TButton")
        decrypt_btn.pack(pady=10)
        self.decrypt_button = decrypt_btn
        
        result_frame = ttk.LabelFrame(decrypt_frame, text="Decrypted Message", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.decrypted_text = scrolledtext.ScrolledText(result_frame, height=15, width=60, wrap=tk.WORD, font=("Arial", 10), state=tk.DISABLED)
        self.decrypted_text.pack(fill=tk.BOTH, expand=True)
    
    def update_auth_status(self, username):
        if username:
            self.notebook.tab(2, state='normal')
            self.notebook.tab(3, state='normal')
            self.login_status_label.config(text=f"Logged in as: {username}", fg="green")
            self.decrypt_attempts_label.config(text="")
        else:
            self.notebook.tab(2, state='disabled')
            self.notebook.tab(3, state='disabled')
            self.login_status_label.config(text="Not logged in", fg="red")
            self.decrypt_attempts_label.config(text="")
    
    def display_qr_image(self, qr_image):
        display_size = 300
        qr_image_copy = qr_image.copy()
        qr_image_copy.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(qr_image_copy)
        self.qr_label.config(image=photo, text="")
        self.qr_label.image = photo


class QRSecretMessagesApp:
    def __init__(self, root):
        self.gui = GUI(root)
        self.auth = AuthSystem()
        self.current_user = None
        self.current_qr_image = None
        self.encrypted_payload = None
        self.loaded_qr_data = None
        
        self._setup_event_handlers()
        self.gui.update_auth_status(None)
    
    def _setup_event_handlers(self):
        self.gui.register_password_entry.bind('<KeyRelease>', self._on_password_change)
        self.gui.register_button.config(command=self._register_user)
        self.gui.login_button.config(command=self._login_user)
        self.gui.logout_button.config(command=self._logout_user)
        self.gui.load_file_button.config(command=self._load_text_file)
        self.gui.generate_button.config(command=self._generate_qr)
        self.gui.save_qr_button.config(command=self._save_qr_image)
        self.gui.save_bin_button.config(command=self._save_encrypted_data)
        self.gui.load_qr_button.config(command=self._load_qr_image)
        self.gui.decrypt_button.config(command=self._decrypt_qr)
    
    def _on_password_change(self, event=None):
        password = self.gui.register_password_entry.get()
        if password:
            result = check_password_strength(password)
            strength = result['strength']
            score = result['score']
            
            if strength == 'strong':
                self.gui.register_strength_label.config(text=f"Password Strength: STRONG ({score}/100)", fg="green")
            else:
                self.gui.register_strength_label.config(text=f"Password Strength: WEAK ({score}/100)", fg="red")
            
            self.gui.register_feedback_text.config(state=tk.NORMAL)
            self.gui.register_feedback_text.delete(1.0, tk.END)
            for feedback in result['feedback']:
                self.gui.register_feedback_text.insert(tk.END, feedback + "\n")
            self.gui.register_feedback_text.config(state=tk.DISABLED)
        else:
            self.gui.register_strength_label.config(text="")
            self.gui.register_feedback_text.config(state=tk.NORMAL)
            self.gui.register_feedback_text.delete(1.0, tk.END)
            self.gui.register_feedback_text.config(state=tk.DISABLED)
    
    def _register_user(self):
        username = self.gui.register_username_entry.get().strip()
        password = self.gui.register_password_entry.get()
        
        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        if not is_password_strong(password):
            result = messagebox.askyesno("Weak Password", "Your password is weak. Do you want to register anyway?\n\nStrong passwords should have:\n- At least 8 characters (12+ recommended)\n- Uppercase and lowercase letters\n- Numbers\n- Special characters")
            if not result:
                return
        
        success, message = self.auth.register_user(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.gui.register_username_entry.delete(0, tk.END)
            self.gui.register_password_entry.delete(0, tk.END)
            self.gui.register_strength_label.config(text="")
            self.gui.register_feedback_text.config(state=tk.NORMAL)
            self.gui.register_feedback_text.delete(1.0, tk.END)
            self.gui.register_feedback_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Registration Failed", message)
    
    def _login_user(self):
        username = self.gui.login_username_entry.get().strip()
        password = self.gui.login_password_entry.get()
        
        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        success, message = self.auth.login(username, password)
        
        if success:
            self.current_user = username
            self.gui.update_auth_status(username)
            messagebox.showinfo("Success", message)
            self.gui.login_username_entry.delete(0, tk.END)
            self.gui.login_password_entry.delete(0, tk.END)
            self.gui.failed_attempts_label.config(text="")
        else:
            messagebox.showerror("Login Failed", message)
            attempts = self.auth.get_failed_attempts(username)
            if attempts > 0:
                remaining = self.auth.max_attempts - attempts
                if remaining > 0:
                    self.gui.failed_attempts_label.config(text=f"Failed attempts: {attempts}/{self.auth.max_attempts} ({remaining} remaining)", fg="orange")
                else:
                    remaining_time = self.auth.get_lockout_remaining(username)
                    minutes = remaining_time // 60
                    seconds = remaining_time % 60
                    self.gui.failed_attempts_label.config(text=f"Account locked. Try again in {minutes}m {seconds}s", fg="red")
    
    def _logout_user(self):
        if self.current_user:
            self.current_user = None
            self.gui.update_auth_status(None)
            messagebox.showinfo("Success", "Logged out successfully.")
        else:
            messagebox.showinfo("Info", "You are not logged in.")
    
    def _load_text_file(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        
        filepath = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.gui.message_text.delete(1.0, tk.END)
                self.gui.message_text.insert(1.0, content)
                messagebox.showinfo("Success", f"Loaded text from {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def _generate_qr(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        
        message = self.gui.message_text.get(1.0, tk.END).strip()
        password = self.gui.password_entry.get()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encrypt.")
            return
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        try:
            encrypted_payload = encrypt_message(message, password)
            self.encrypted_payload = encrypted_payload
            qr_image = generate_qr_code(encrypted_payload)
            self.current_qr_image = qr_image
            self.gui.display_qr_image(qr_image)
            messagebox.showinfo("Success", "QR code generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def _save_qr_image(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        if self.current_qr_image is None:
            messagebox.showwarning("Warning", "No QR code to save. Generate one first.")
            return
        
        filepath = filedialog.asksaveasfilename(title="Save QR Code", defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        
        if filepath:
            try:
                save_qr_code(self.current_qr_image, filepath)
                messagebox.showinfo("Success", f"QR code saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
    
    def _save_encrypted_data(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        if self.encrypted_payload is None:
            messagebox.showwarning("Warning", "No encrypted data to save. Generate QR code first.")
            return
        
        filepath = filedialog.asksaveasfilename(title="Save Encrypted Data", defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        
        if filepath:
            try:
                with open(filepath, 'wb') as f:
                    f.write(self.encrypted_payload)
                messagebox.showinfo("Success", f"Encrypted data saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save encrypted data: {str(e)}")
    
    def _load_qr_image(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        
        filepath = filedialog.askopenfilename(title="Select QR Code Image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")])
        
        if filepath:
            try:
                qr_data = read_qr_code(filepath)
                self.loaded_qr_data = qr_data
                self.auth.reset_decryption_attempts(self.current_user)
                self.gui.decrypt_attempts_label.config(text="")
                self.gui.qr_path_label.config(text=f"Loaded: {os.path.basename(filepath)}", fg="green")
                messagebox.showinfo("Success", "QR code loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load QR code: {str(e)}")
                self.gui.qr_path_label.config(text="Failed to load QR code", fg="red")
    
    def _decrypt_qr(self):
        if not self.current_user:
            messagebox.showwarning("Warning", "Please login first.")
            return
        if self.loaded_qr_data is None:
            messagebox.showwarning("Warning", "Please load a QR code image first.")
            return
        
        if self.auth.is_decryption_locked(self.current_user):
            messagebox.showerror("Decryption Locked", f"You have exceeded the maximum number of decryption attempts ({self.auth.max_attempts}).\nPlease load a new QR code to reset attempts.")
            return
        
        password = self.gui.decrypt_password_entry.get()
        
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        try:
            decrypted_message = decrypt_message(self.loaded_qr_data, password)
            self.auth.reset_decryption_attempts(self.current_user)
            self.gui.decrypt_attempts_label.config(text="")
            self.gui.decrypted_text.config(state=tk.NORMAL)
            self.gui.decrypted_text.delete(1.0, tk.END)
            self.gui.decrypted_text.insert(1.0, decrypted_message)
            self.gui.decrypted_text.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Message decrypted successfully!")
        except ValueError as e:
            attempts = self.auth.increment_decryption_attempts(self.current_user)
            remaining = self.auth.max_attempts - attempts
            
            if remaining > 0:
                self.gui.decrypt_attempts_label.config(text=f"Failed attempts: {attempts}/{self.auth.max_attempts} ({remaining} remaining)", fg="orange")
                messagebox.showerror("Decryption Failed", f"Invalid password. {remaining} attempt(s) remaining.")
            else:
                self.gui.decrypt_attempts_label.config(text=f"Decryption locked! Maximum attempts ({self.auth.max_attempts}) exceeded.", fg="red")
                messagebox.showerror("Decryption Locked", f"You have exceeded the maximum number of decryption attempts ({self.auth.max_attempts}).\nPlease load a new QR code to reset attempts.")
            
            self.gui.decrypted_text.config(state=tk.NORMAL)
            self.gui.decrypted_text.delete(1.0, tk.END)
            self.gui.decrypted_text.insert(1.0, "Decryption failed. Please check your password.")
            self.gui.decrypted_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = QRSecretMessagesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
