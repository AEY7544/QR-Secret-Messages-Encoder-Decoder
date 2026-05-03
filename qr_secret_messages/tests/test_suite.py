

import os
import sys
import tempfile
import base64
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_utils import encrypt_message, decrypt_message, derive_key
from qr_utils import generate_qr_code, read_qr_code, save_qr_code
from password_strength import check_password_strength, is_password_strong
from auth_system import AuthSystem

class TestResults:
    
    def __init__(self):
        self.passed = []
        self.failed = []
        self.total = 0
    
    def add_result(self, test_name, passed, explanation, output=None, security_note=None, suggestion=None):
        self.total += 1
        result = {
            'name': test_name,
            'passed': passed,
            'explanation': explanation,
            'output': output,
            'security_note': security_note,
            'suggestion': suggestion
        }
        if passed:
            self.passed.append(result)
        else:
            self.failed.append(result)
    
    def print_summary(self):
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.total}")
        print(f"Passed: {len(self.passed)}")
        print(f"Failed: {len(self.failed)}")
        print(f"Success Rate: {len(self.passed)/self.total*100:.1f}%")
        print("="*80)

def test_key_derivation():
    
    print("\n" + "="*80)
    print("TEST A: Key Derivation (SHA-256)")
    print("="*80)
    
    results = TestResults()

    password = "test_password_123"
    key = derive_key(password)
    
    passed = len(key) == 32
    results.add_result(
        "A1: SHA-256 produces 32-byte key",
        passed,
        f"Password '{password}' -> Key length: {len(key)} bytes",
        output=f"Key (hex): {key.hex()[:32]}...",
        security_note="SHA-256 produces deterministic 32-byte keys suitable for AES-256",
        suggestion="Consider adding salt and PBKDF2 for stronger key derivation"
    )

    key1 = derive_key("same_password")
    key2 = derive_key("same_password")
    passed = key1 == key2
    results.add_result(
        "A2: Deterministic key derivation",
        passed,
        "Same password produces same key",
        output=f"Keys match: {passed}",
        security_note="Deterministic keys allow decryption with same password"
    )

    key1 = derive_key("password1")
    key2 = derive_key("password2")
    passed = key1 != key2
    results.add_result(
        "A3: Different passwords produce different keys",
        passed,
        "Different passwords produce different keys",
        output=f"Keys differ: {passed}",
        security_note="Key uniqueness ensures password security"
    )
    
    return results

def test_aes_gcm_encryption():
    
    print("\n" + "="*80)
    print("TEST B: AES-GCM Encryption/Decryption")
    print("="*80)
    
    results = TestResults()

    message = "Hello, this is a secret message!"
    password = "mySecurePassword123"
    
    try:
        encrypted_payload = encrypt_message(message, password)
        passed = isinstance(encrypted_payload, bytes) and len(encrypted_payload) > 0

        payload = base64.b64decode(encrypted_payload)
        nonce = payload[:16]
        tag = payload[16:32]
        ciphertext = payload[32:]
        
        results.add_result(
            "B1: Basic encryption produces valid payload",
            passed,
            f"Message encrypted successfully",
            output=f"Payload length: {len(encrypted_payload)} bytes (base64), "
                   f"Raw: {len(payload)} bytes (nonce: 16, tag: 16, ciphertext: {len(ciphertext)})",
            security_note="Payload format: [16-byte nonce][16-byte tag][variable ciphertext]"
        )

        structure_correct = len(nonce) == 16 and len(tag) == 16 and len(ciphertext) > 0
        results.add_result(
            "B2: Payload structure (nonce + tag + ciphertext)",
            structure_correct,
            "Payload contains nonce (16B) + tag (16B) + ciphertext",
            output=f"Nonce: {len(nonce)}B, Tag: {len(tag)}B, Ciphertext: {len(ciphertext)}B",
            security_note="GCM mode provides authenticated encryption with integrity verification"
        )

        decrypted = decrypt_message(encrypted_payload, password)
        passed = decrypted == message
        results.add_result(
            "B3: Decryption with correct password",
            passed,
            "Decrypted message matches original",
            output=f"Original: '{message[:30]}...', Decrypted: '{decrypted[:30]}...'",
            security_note="AES-GCM ensures message integrity and authenticity"
        )

        try:
            decrypt_message(encrypted_payload, "wrong_password")
            passed = False
            error_msg = "Should have raised ValueError"
        except ValueError as e:
            passed = True
            error_msg = str(e)
        
        results.add_result(
            "B4: Decryption with wrong password fails",
            passed,
            "Wrong password correctly rejected",
            output=error_msg,
            security_note="GCM tag verification prevents decryption with wrong key"
        )

        msg1 = "Message 1"
        msg2 = "Message 2"
        enc1 = encrypt_message(msg1, password)
        enc2 = encrypt_message(msg2, password)
        passed = enc1 != enc2
        results.add_result(
            "B5: Different messages produce different ciphertexts",
            passed,
            "Unique nonces ensure different ciphertexts",
            output=f"Ciphertexts differ: {passed}",
            security_note="Random nonces ensure semantic security"
        )

        enc1 = encrypt_message(message, password)
        enc2 = encrypt_message(message, password)
        passed = enc1 != enc2
        results.add_result(
            "B6: Same message encrypted twice produces different ciphertexts",
            passed,
            "Random nonces ensure unique ciphertexts",
            output=f"Ciphertexts differ: {passed}",
            security_note="Nonce uniqueness prevents pattern analysis"
        )
        
    except Exception as e:
        results.add_result(
            "B1: Basic encryption",
            False,
            f"Encryption failed: {str(e)}",
            output=str(e)
        )
    
    return results

def test_qr_code_generation():
    
    print("\n" + "="*80)
    print("TEST G: QR Code Generation")
    print("="*80)
    
    results = TestResults()
    
    try:
        
        message = "Test message for QR code"
        password = "test123"
        encrypted = encrypt_message(message, password)
        
        qr_image = generate_qr_code(encrypted)
        passed = qr_image is not None
        
        results.add_result(
            "G1: QR code generation",
            passed,
            "QR code image generated successfully",
            output=f"Image size: {qr_image.size if qr_image else 'N/A'}",
            security_note="QR codes encode base64-encoded encrypted payload"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            qr_image.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            decoded_data = read_qr_code(tmp_path)
            passed = decoded_data == encrypted
            results.add_result(
                "G2: QR code readability",
                passed,
                "QR code can be read back correctly",
                output=f"Decoded length: {len(decoded_data)} bytes, Match: {passed}",
                security_note="QR code preserves encrypted payload integrity"
            )
        except Exception as e:
            results.add_result(
                "G2: QR code readability",
                False,
                f"Failed to read QR code: {str(e)}",
                output=str(e)
            )
        finally:
            os.unlink(tmp_path)

        width, height = qr_image.size
        passed = width > 0 and height > 0 and width == height
        results.add_result(
            "G3: QR code dimensions",
            passed,
            "QR code has valid square dimensions",
            output=f"Size: {width}x{height}",
            suggestion="Consider adjusting QR code version for larger payloads"
        )
        
    except Exception as e:
        results.add_result(
            "G1: QR code generation",
            False,
            f"QR generation failed: {str(e)}",
            output=str(e)
        )
    
    return results

def test_qr_code_decryption():
    
    print("\n" + "="*80)
    print("TEST H: QR Code Decryption")
    print("="*80)
    
    results = TestResults()
    
    try:
        
        original_message = "This is a secret message that will be encrypted!"
        password = "secure_password_456"
        
        encrypted = encrypt_message(original_message, password)
        qr_image = generate_qr_code(encrypted)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            qr_image.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            qr_data = read_qr_code(tmp_path)
            decrypted = decrypt_message(qr_data, password)
            passed = decrypted == original_message
            
            results.add_result(
                "H1: Full encryption -> QR -> decryption cycle",
                passed,
                "Complete cycle works correctly",
                output=f"Original: '{original_message[:40]}...', "
                       f"Decrypted: '{decrypted[:40]}...', Match: {passed}",
                security_note="End-to-end encryption preserves message integrity"
            )
        finally:
            os.unlink(tmp_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            qr_image.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            qr_data = read_qr_code(tmp_path)
            try:
                decrypt_message(qr_data, "wrong_password")
                passed = False
                error_msg = "Should have raised ValueError"
            except ValueError:
                passed = True
                error_msg = "Correctly rejected wrong password"
            
            results.add_result(
                "H2: Wrong password on QR decryption",
                passed,
                "Wrong password correctly rejected",
                output=error_msg,
                security_note="Password verification prevents unauthorized access"
            )
        finally:
            os.unlink(tmp_path)
        
    except Exception as e:
        results.add_result(
            "H1: QR code decryption",
            False,
            f"Decryption test failed: {str(e)}",
            output=str(e)
        )
    
    return results

def test_text_file_encryption():
    
    print("\n" + "="*80)
    print("TEST F: Text File Encryption")
    print("="*80)
    
    results = TestResults()
    
    try:
        
        test_content = "This is a test file.\nIt has multiple lines.\nAnd some special characters: !@
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
            tmp.write(test_content)
            tmp_path = tmp.name
        
        try:
            
            password = "file_password_789"
            encrypted = encrypt_message(test_content, password)
            passed = len(encrypted) > 0
            
            results.add_result(
                "F1: Text file content encryption",
                passed,
                "File content encrypted successfully",
                output=f"Original size: {len(test_content)} chars, "
                       f"Encrypted: {len(encrypted)} bytes (base64)",
                security_note="File encryption preserves all content including special characters"
            )

            decrypted = decrypt_message(encrypted, password)
            passed = decrypted == test_content
            
            results.add_result(
                "F2: Text file content decryption",
                passed,
                "Decrypted content matches original file",
                output=f"Match: {passed}, Lines preserved: {decrypted.count(chr(10)) == test_content.count(chr(10))}",
                security_note="Decryption restores exact file content"
            )
            
        finally:
            os.unlink(tmp_path)
        
    except Exception as e:
        results.add_result(
            "F1: Text file encryption",
            False,
            f"File encryption test failed: {str(e)}",
            output=str(e)
        )
    
    return results

def test_password_strength():
    
    print("\n" + "="*80)
    print("TEST C: Password Strength Checker")
    print("="*80)
    
    results = TestResults()

    weak_password = "12345"
    result = check_password_strength(weak_password)
    passed = result['strength'] == 'weak' and result['score'] < 70
    
    results.add_result(
        "C1: Weak password detection",
        passed,
        f"Password '{weak_password}' correctly classified as weak",
        output=f"Strength: {result['strength']}, Score: {result['score']}/100",
        security_note="Weak passwords are vulnerable to brute-force attacks"
    )

    strong_password = "A9m$kp1Y"
    result = check_password_strength(strong_password)
    passed = result['strength'] == 'strong' and result['score'] >= 70
    
    results.add_result(
        "C2: Strong password detection",
        passed,
        f"Password '{strong_password}' correctly classified as strong",
        output=f"Strength: {result['strength']}, Score: {result['score']}/100",
        security_note="Strong passwords resist brute-force attacks"
    )

    test_password = "Test123!"
    result = check_password_strength(test_password)
    reqs = result['requirements']
    passed = (reqs['length_8'] and reqs['has_uppercase'] and 
              reqs['has_lowercase'] and reqs['has_digit'] and reqs['has_special'])
    
    results.add_result(
        "C3: Password requirements validation",
        passed,
        "Password meets all basic requirements",
        output=f"Requirements met: {passed}",
        security_note="Multiple character types increase password entropy"
    )

    common_password = "password123"
    result = check_password_strength(common_password)
    passed = not result['requirements']['not_common'] or result['score'] < 70
    
    results.add_result(
        "C4: Common password detection",
        passed,
        "Common passwords are flagged",
        output=f"Common password detected: {not result['requirements']['not_common']}",
        security_note="Common passwords are easily guessed"
    )

    passed = not is_password_strong("12345") and is_password_strong("A9m$kp1Y")
    
    results.add_result(
        "C5: is_password_strong helper function",
        passed,
        "Helper function correctly identifies strong passwords",
        output=f"Weak: {not is_password_strong('12345')}, Strong: {is_password_strong('A9m$kp1Y')}",
        security_note="Quick password validation for registration"
    )
    
    return results

def test_authentication():
    
    print("\n" + "="*80)
    print("TEST E: Authentication System")
    print("="*80)
    
    results = TestResults()

    users_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    users_file.close()
    lockout_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    lockout_file.close()
    
    try:
        auth = AuthSystem(users_file.name, lockout_file.name)

        success, message = auth.register_user("testuser", "TestPass123!")
        passed = success and "successfully" in message.lower()
        
        results.add_result(
            "E1: User registration",
            passed,
            "New user can be registered",
            output=f"Result: {message}",
            security_note="User credentials stored securely with hashed passwords"
        )

        success, message = auth.register_user("testuser", "AnotherPass123!")
        passed = not success and "already exists" in message.lower()
        
        results.add_result(
            "E2: Duplicate user registration prevention",
            passed,
            "Duplicate usernames are rejected",
            output=f"Result: {message}",
            security_note="Prevents username conflicts"
        )

        success, message = auth.login("testuser", "TestPass123!")
        passed = success and "successful" in message.lower()
        
        results.add_result(
            "E3: Login with correct password",
            passed,
            "Correct password allows login",
            output=f"Result: {message}",
            security_note="Password verification enables secure access"
        )

        success, message = auth.login("testuser", "WrongPassword123!")
        passed = not success and "invalid" in message.lower()
        
        results.add_result(
            "E4: Login with wrong password",
            passed,
            "Wrong password is rejected",
            output=f"Result: {message}",
            security_note="Failed attempts are tracked for brute-force protection"
        )

        attempts_before = auth.get_failed_attempts("testuser")
        auth.login("testuser", "wrong1")
        attempts_after = auth.get_failed_attempts("testuser")
        passed = attempts_after > attempts_before
        
        results.add_result(
            "E5: Failed attempts counter",
            passed,
            "Failed login attempts are tracked",
            output=f"Attempts: {attempts_before} -> {attempts_after}",
            security_note="Counter enables brute-force protection"
        )
        
    finally:
        
        if os.path.exists(users_file.name):
            os.unlink(users_file.name)
        if os.path.exists(lockout_file.name):
            os.unlink(lockout_file.name)
    
    return results

def test_brute_force_protection():
    
    print("\n" + "="*80)
    print("TEST D: Brute Force Protection")
    print("="*80)
    
    results = TestResults()

    users_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    users_file.close()
    lockout_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    lockout_file.close()
    
    try:
        auth = AuthSystem(users_file.name, lockout_file.name)

        auth.register_user("brutetest", "CorrectPass123!")

        attempts_list = []
        for i in range(4):
            auth.login("brutetest", "wrong" + str(i))
            attempts_list.append(auth.get_failed_attempts("brutetest"))
        
        passed = all(attempts_list[i] < attempts_list[i+1] for i in range(len(attempts_list)-1))
        
        results.add_result(
            "D1: Failed attempts counter increments",
            passed,
            "Counter increments with each failed attempt",
            output=f"Attempts progression: {attempts_list}",
            security_note="Tracking attempts enables lockout mechanism"
        )

        success, message = auth.login("brutetest", "wrong5")
        passed = not success and "locked" in message.lower()
        
        results.add_result(
            "D2: Account lockout after max attempts",
            passed,
            "Account locks after 5 failed attempts",
            output=f"Result: {message}",
            security_note="Lockout prevents brute-force attacks"
        )

        success, message = auth.login("brutetest", "CorrectPass123!")
        passed = not success and "locked" in message.lower()
        
        results.add_result(
            "D3: Locked account prevents login",
            passed,
            "Even correct password is rejected when locked",
            output=f"Result: {message}",
            security_note="Lockout applies regardless of password correctness"
        )

        is_locked = auth.is_user_locked("brutetest")
        passed = is_locked
        
        results.add_result(
            "D4: Lockout status check",
            passed,
            "System correctly identifies locked accounts",
            output=f"Locked: {is_locked}",
            security_note="Status check enables UI feedback"
        )

        remaining = auth.get_lockout_remaining("brutetest")
        passed = remaining > 0 and remaining <= auth.lockout_duration
        
        results.add_result(
            "D5: Lockout remaining time",
            passed,
            "System tracks remaining lockout time",
            output=f"Remaining: {remaining} seconds (max: {auth.lockout_duration})",
            security_note="Time-based lockout provides temporary protection"
        )

    finally:
        
        if os.path.exists(users_file.name):
            os.unlink(users_file.name)
        if os.path.exists(lockout_file.name):
            os.unlink(lockout_file.name)
    
    return results

def run_all_tests():
    
    print("\n" + "="*80)
    print("QR CODE SECRET MESSAGES - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    all_results = TestResults()

    test_suites = [
        ("A", test_key_derivation),
        ("B", test_aes_gcm_encryption),
        ("C", test_password_strength),
        ("D", test_brute_force_protection),
        ("E", test_authentication),
        ("F", test_text_file_encryption),
        ("G", test_qr_code_generation),
        ("H", test_qr_code_decryption),
    ]
    
    for suite_name, test_func in test_suites:
        try:
            suite_results = test_func()
            
            for result in suite_results.passed:
                all_results.passed.append(result)
            for result in suite_results.failed:
                all_results.failed.append(result)
            all_results.total += suite_results.total
        except Exception as e:
            print(f"\nERROR in {suite_name} test suite: {str(e)}")

    print("\n" + "="*80)
    print("DETAILED TEST RESULTS")
    print("="*80)
    
    for result in all_results.passed + all_results.failed:
        status = "[PASS]" if result['passed'] else "[FAIL]"
        print(f"\n{status}: {result['name']}")
        print(f"  Explanation: {result['explanation']}")
        if result['output']:
            print(f"  Output: {result['output']}")
        if result['security_note']:
            print(f"  Security Note: {result['security_note']}")
        if result['suggestion']:
            print(f"  Suggestion: {result['suggestion']}")

    all_results.print_summary()
    
    return all_results

if __name__ == "__main__":
    results = run_all_tests()

