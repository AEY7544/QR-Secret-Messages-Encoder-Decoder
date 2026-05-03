import re
import string


def check_password_strength(password: str) -> dict:
    if not password:
        return {
            'strength': 'weak',
            'score': 0,
            'feedback': ['Password is empty'],
            'requirements': {}
        }
    feedback = []
    requirements = {
        'length_8': len(password) >= 8,
        'length_12': len(password) >= 12,
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_digit': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password)),
        'not_common': password.lower() not in ['password', '123456', 'qwerty', 'abc123', 'password123'],
    }
    score = 0
    if requirements['length_12']:
        score += 25
        feedback.append(" Good length (12+ characters)")
    elif requirements['length_8']:
        score += 15
        feedback.append(" Minimum length (8+ characters)")
    else:
        feedback.append(" Too short (minimum 8 characters)")
    if requirements['has_uppercase']:
        score += 15
        feedback.append(" Contains uppercase letters")
    else:
        feedback.append(" Missing uppercase letters")
    if requirements['has_lowercase']:
        score += 15
        feedback.append(" Contains lowercase letters")
    else:
        feedback.append("✗ Missing lowercase letters")
    if requirements['has_digit']:
        score += 15
        feedback.append(" Contains numbers")
    else:
        feedback.append(" Missing numbers")
    if requirements['has_special']:
        score += 20
        feedback.append(" Contains special characters")
    else:
        feedback.append(" Missing special characters")
    if requirements['not_common']:
        score += 10
        feedback.append(" Not a common password")
    else:
        score -= 20
        feedback.append(" Common password detected")
    if len(password) >= 16:
        score += 10
        feedback.append(" Very long password (16+ characters)")
    score = max(0, min(100, score))
    if score >= 70:
        strength = 'strong'
    else:
        strength = 'weak'
    return {
        'strength': strength,
        'score': score,
        'feedback': feedback,
        'requirements': requirements
    }


def is_password_strong(password: str) -> bool:
    result = check_password_strength(password)
    return result['strength'] == 'strong'
