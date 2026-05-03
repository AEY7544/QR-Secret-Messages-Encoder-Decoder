import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict


class AuthSystem:
    def __init__(self, users_file: str = "users.json", lockout_file: str = "lockouts.json"):
        self.users_file = users_file
        self.lockout_file = lockout_file
        self.max_attempts = 5
        self.lockout_duration = 300
        self.users = self._load_users()
        self.lockouts = self._load_lockouts()
    def _load_users(self) -> Dict:
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    def _load_lockouts(self) -> Dict:
        if os.path.exists(self.lockout_file):
            try:
                with open(self.lockout_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    def _save_lockouts(self):
        with open(self.lockout_file, 'w') as f:
            json.dump(self.lockouts, f, indent=2)
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    def _is_locked_out(self, username: str) -> bool:
        if username not in self.lockouts:
            return False
        lockout_data = self.lockouts[username]
        lockout_time = datetime.fromisoformat(lockout_data['locked_until'])
        if datetime.now() < lockout_time:
            return True
        else:
            del self.lockouts[username]
            self._save_lockouts()
            return False
    def _get_remaining_lockout_time(self, username: str) -> int:
        if username not in self.lockouts:
            return 0
        lockout_data = self.lockouts[username]
        lockout_time = datetime.fromisoformat(lockout_data['locked_until'])
        remaining = (lockout_time - datetime.now()).total_seconds()
        return max(0, int(remaining))
    def register_user(self, username: str, password: str):
        if not username or not password:
            return False, "Username and password are required"
        if username in self.users:
            return False, "Username already exists"
        password_hash = self._hash_password(password)
        self.users[username] = {
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'failed_attempts': 0
        }
        self._save_users()
        return True, "User registered successfully"
    def login(self, username: str, password: str):
        if not username or not password:
            return False, "Username and password are required"
        if username not in self.users:
            return False, "Invalid username or password"
        if self._is_locked_out(username):
            remaining = self._get_remaining_lockout_time(username)
            minutes = remaining // 60
            seconds = remaining % 60
            return False, f"Account locked. Try again in {minutes}m {seconds}s"
        password_hash = self._hash_password(password)
        stored_hash = self.users[username]['password_hash']
        if password_hash == stored_hash:
            self.users[username]['failed_attempts'] = 0
            self._save_users()
            if username in self.lockouts:
                del self.lockouts[username]
                self._save_lockouts()
            return True, "Login successful"
        else:
            self.users[username]['failed_attempts'] = self.users[username].get('failed_attempts', 0) + 1
            attempts = self.users[username]['failed_attempts']
            self._save_users()
            if attempts >= self.max_attempts:
                lockout_until = datetime.now() + timedelta(seconds=self.lockout_duration)
                self.lockouts[username] = {
                    'locked_until': lockout_until.isoformat(),
                    'attempts': attempts
                }
                self._save_lockouts()
                return False, f"Too many failed attempts. Account locked for {self.lockout_duration // 60} minutes."
            remaining = self.max_attempts - attempts
            return False, f"Invalid password. {remaining} attempt(s) remaining."
    def get_failed_attempts(self, username: str) -> int:
        if username not in self.users:
            return 0
        return self.users[username].get('failed_attempts', 0)
    def is_user_locked(self, username: str) -> bool:
        return self._is_locked_out(username)
    def get_lockout_remaining(self, username: str) -> int:
        return self._get_remaining_lockout_time(username)
    def get_decryption_attempts(self, username: str) -> int:
        if username not in self.users:
            return 0
        return self.users[username].get('decryption_attempts', 0)
    def increment_decryption_attempts(self, username: str) -> int:
        if username not in self.users:
            return 0
        self.users[username]['decryption_attempts'] = self.users[username].get('decryption_attempts', 0) + 1
        attempts = self.users[username]['decryption_attempts']
        self._save_users()
        return attempts
    def reset_decryption_attempts(self, username: str):
        if username in self.users:
            self.users[username]['decryption_attempts'] = 0
            self._save_users()
    def is_decryption_locked(self, username: str) -> bool:
        attempts = self.get_decryption_attempts(username)
        return attempts >= self.max_attempts
