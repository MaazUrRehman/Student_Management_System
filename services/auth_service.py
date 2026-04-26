from models.auth_model import AuthModel
from services.account_service import AccountService
from utils.helpers import hash_password


class AuthService:
    VALID_ROLES = {"admin", "accountant", "student", "staff"}

    @staticmethod
    def login(username, password):
        hashed = hash_password(password)
        user = AuthModel.verify_user(username, hashed)
        if user:
            return {"success": True, "user": user}
        return {"success": False, "message": "Invalid credentials"}

    @staticmethod
    def get_allowed_registration_roles(current_user):
        if not current_user:
            return []

        role = current_user.get("role")
        if role == "admin":
            return ["admin", "accountant", "student", "staff"]
        return []

    @staticmethod
    def create_user(current_user, username, password, role, student_data=None, staff_data=None):
        if not current_user:
            raise PermissionError("You must be logged in to register users.")

        creator_role = current_user.get("role")
        if creator_role == "student":
            raise PermissionError("Students are not allowed to register users.")

        if creator_role != "admin":
            raise PermissionError("This account is not allowed to register users.")

        if role not in AuthService.VALID_ROLES:
            raise ValueError("Invalid role selected.")

        if not username or not password:
            raise ValueError("Username and password are required.")

        if role == "student":
            student_data = student_data or {}
            if not student_data.get("name") or not student_data.get("class_name"):
                raise ValueError("Student name and class are required.")

        if role == "staff":
            staff_data = staff_data or {}
            if not staff_data.get("name"):
                raise ValueError("Staff name is required.")
            if staff_data.get("salary") in (None, ""):
                raise ValueError("Staff salary is required.")

        try:
            user_id = AuthModel.add_user(username, hash_password(password), role)
        except Exception as exc:
            error_text = str(exc).lower()
            if "unique" in error_text or "username" in error_text:
                raise ValueError("Username already exists.") from exc
            raise

        if role == "student":
            AccountService.add_student(
                student_data["name"],
                student_data["class_name"],
                student_data.get("parent_name", ""),
                student_data.get("phone", ""),
                user_id
            )
            
            # Get the student record to generate invoices
            # We need to find the student by user_id
            from models.student_model import StudentModel
            students = StudentModel.search_students(student_data["name"])
            for student in students:
                if student.get("user_id") == user_id:
                    # Check if invoices already exist before generating
                    if not AccountService.check_invoices_exist_for_student(student["id"]):
                        # Generate 12 monthly invoices automatically
                        AccountService.generate_student_invoices(
                            student["id"], 
                            student_data["class_name"]
                        )
                    break
        
        # Handle staff registration
        if role == "staff":
            staff_data = staff_data or {}
            AccountService.add_staff(
                staff_data.get("name", ""),
                staff_data.get("father_name", ""),
                staff_data.get("qualification", ""),
                staff_data.get("department", ""),
                staff_data.get("designation", ""),
                float(staff_data.get("salary", 0)),
                user_id
            )

        return {
            "id": user_id,
            "username": username,
            "role": role
        }

    @staticmethod
    def get_user(user_id):
        return AuthModel.get_user_by_id(user_id)

    @staticmethod
    def get_all_users():
        return AuthModel.get_all_users()
