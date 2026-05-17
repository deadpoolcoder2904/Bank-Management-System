import json
import random
import string
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class Bank:
    """Backend used by the Streamlit UI in app.py.

    Provides pure methods (no input()) matching the signatures used in app.py.
    Data is stored in data.json in the same folder.
    """

    database = "data.json"
    data = []  # type: list[Dict[str, Any]]

    # ---- persistence helpers ----
    @classmethod
    def _load(cls) -> None:
        try:
            p = Path(cls.database)
            if p.exists() and p.stat().st_size > 0:
                cls.data = json.loads(p.read_text(encoding="utf-8"))
            else:
                cls.data = []
        except Exception:
            cls.data = []

    @classmethod
    def _save(cls) -> None:
        Path(cls.database).write_text(json.dumps(cls.data, indent=2), encoding="utf-8")

    @classmethod
    def __accountgenerate(cls) -> str:
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        _id = alpha + num + spchar
        random.shuffle(_id)
        return "".join(_id)

    # ---- API used by app.py ----
    @classmethod
    def create_account(
        cls, name: str, age: int, email: str, pin: int
    ) -> Tuple[Optional[Dict[str, Any]], str]:
        cls._load()

        if not (name and email):
            return None, "Name and email are required"
        if age < 18:
            return None, "Sorry you cannot create your account (age must be 18+)"
        if len(str(pin)) != 4:
            return None, "PIN must be a 4-digit number"

        # prevent duplicate email (optional but helpful)
        for u in cls.data:
            if u.get("email") == email:
                return None, "An account with this email already exists"

        user = {
            "name": name,
            "age": int(age),
            "email": email,
            "pin": int(pin),
            "accountNo.": cls.__accountgenerate(),
            "balance": 0,
        }

        cls.data.append(user)
        cls._save()
        return user, "Account has been created successfully"

    @classmethod
    def find_user(cls, acc_no: str, pin: int) -> Optional[Dict[str, Any]]:
        cls._load()
        for u in cls.data:
            if u.get("accountNo.") == acc_no and int(u.get("pin")) == int(pin):
                return u
        return None

    @classmethod
    def deposit(cls, acc_no: str, pin: int, amount: int) -> Tuple[bool, str]:
        cls._load()

        if amount <= 0:
            return False, "Amount must be greater than 0"
        if amount > 10000:
            return False, "Sorry the amount is too much. Max deposit is 10000"

        for u in cls.data:
            if u.get("accountNo.") == acc_no and int(u.get("pin")) == int(pin):
                u["balance"] = int(u.get("balance", 0)) + int(amount)
                cls._save()
                return True, "Amount deposited successfully"

        return False, "No account found (wrong account number or PIN)"

    @classmethod
    def withdraw(cls, acc_no: str, pin: int, amount: int) -> Tuple[bool, str]:
        cls._load()

        if amount <= 0:
            return False, "Amount must be greater than 0"

        for u in cls.data:
            if u.get("accountNo.") == acc_no and int(u.get("pin")) == int(pin):
                if int(u.get("balance", 0)) < int(amount):
                    return False, "Sorry you don't have that much money"
                u["balance"] = int(u.get("balance", 0)) - int(amount)
                cls._save()
                return True, "Amount withdrew successfully"

        return False, "No account found (wrong account number or PIN)"

    @classmethod
    def update_user(
        cls,
        acc_no: str,
        pin: int,
        name: str,
        email: str,
        new_pin: Any,
    ) -> Tuple[bool, str]:
        cls._load()

        user = None
        for u in cls.data:
            if u.get("accountNo.") == acc_no and int(u.get("pin")) == int(pin):
                user = u
                break

        if not user:
            return False, "No such user found"

        updates_made = False

        if name:
            user["name"] = name
            updates_made = True
        if email:
            # prevent duplicate email with other users
            for u in cls.data:
                if u is not user and u.get("email") == email:
                    return False, "Another account already uses this email"
            user["email"] = email
            updates_made = True

        if new_pin not in (None, ""):
            try:
                new_pin_int = int(new_pin)
            except Exception:
                return False, "New PIN must be a 4-digit number"
            if len(str(new_pin_int)) != 4:
                return False, "PIN must be a 4-digit number"
            user["pin"] = new_pin_int
            updates_made = True

        if not updates_made:
            return True, "No changes provided"

        cls._save()
        return True, "details updated successfully"

    @classmethod
    def delete_user(cls, acc_no: str, pin: int) -> Tuple[bool, str]:
        cls._load()

        for i, u in enumerate(list(cls.data)):
            if u.get("accountNo.") == acc_no and int(u.get("pin")) == int(pin):
                cls.data.pop(i)
                cls._save()
                return True, "Account deleted successfully"

        return False, "No such data exist (wrong account number or PIN)"

