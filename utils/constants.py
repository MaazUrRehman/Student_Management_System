# COLORS = {
#     "primary": "#1E3A8A",
#     "secondary": "#3B82F6",
#     "background": "#F8FAFC",
#     "card": "#FFFFFF",
#     "text": "#111827",
#     "muted": "#6B7280",
#     "border": "#E5E7EB",
#     "success": "#10B981",
#     "danger": "#EF4444",
#     "white": "#FFFFFF",
#     "light_gray": "#E5E7EB",
#     "row_alt": "#F3F4F6"
# }

# FONTS = {
#     "title": ("Arial", 16, "bold"),
#     "heading": ("Arial", 12, "bold"),
#     "normal": ("Arial", 10),
#     "small": ("Arial", 10)
# }

# DIMENSIONS = {
#     "window_width": 900,
#     "window_height": 600
# }




# constants.py - Fixed version with system fonts
import tkinter.font as tkfont

# Color scheme - Professional Blue Theme
COLORS = {
    # Primary Blue Theme
    "primary": "#1E40AF",      # Deep Blue
    "primary_dark": "#1E3A8A", # Darker Blue
    "primary_light": "#3B82F6", # Light Blue
    "primary_lighter": "#EFF6FF", # Very Light Blue
    
    # Secondary Accent Colors
    "secondary": "#0EA5E9",    # Sky Blue
    "accent": "#F59E0B",        # Amber for highlights
    "success": "#10B981",       # Emerald Green
    "danger": "#EF4444",        # Red
    "warning": "#F59E0B",       # Amber
    
    # Neutrals
    "background": "#F8FAFC",    # Light Gray-Blue Background
    "card": "#FFFFFF",          # White Cards
    "sidebar": "#0F172A",       # Dark Blue Sidebar
    "header": "#1E293B",        # Slate Blue Header
    
    # Text Colors
    "text_primary": "#0F172A",  # Dark Slate for main text
    "text_secondary": "#475569", # Gray for secondary text
    "text_muted": "#94A3B8",    # Light Gray for muted text
    "text_light": "#F8FAFC",    # Light text for dark backgrounds
    
    # Border and Dividers
    "border": "#E2E8F0",        # Light border
    "border_focus": "#3B82F6",  # Focus border
    
    # Table Colors
    "table_header": "#F1F5F9",  # Table header background
    "table_row_even": "#FFFFFF", # Even rows
    "table_row_odd": "#F8FAFC",  # Odd rows
    "table_hover": "#EFF6FF",    # Hover effect
    
    # Status Colors
    "status_paid": "#D1FAE5",    # Light green for paid
    "status_pending": "#FEF3C7", # Light amber for pending
    "status_overdue": "#FEE2E2", # Light red for overdue
    
    # Legacy color names (for backward compatibility)
    "white": "#FFFFFF",
    "light_gray": "#E5E7EB",
    "row_alt": "#F3F4F6",
    "muted": "#6B7280",
    "text": "#111827",
}

# System-compatible fonts (works on Windows, Mac, Linux)
# Try to use Segoe UI on Windows, San Francisco on Mac, fallback to Arial/Helvetica
try:
    # Test if Segoe UI is available (Windows)
    tkfont.Font(family="Segoe UI", size=10)
    FONT_FAMILY = "Segoe UI"
except:
    try:
        # Test if Helvetica is available (Mac)
        tkfont.Font(family="Helvetica", size=10)
        FONT_FAMILY = "Helvetica"
    except:
        # Fallback to Arial (cross-platform)
        FONT_FAMILY = "Arial"

FONTS = {
    "title": (FONT_FAMILY, 20, "bold"),
    "heading": (FONT_FAMILY, 14, "bold"),
    "subheading": (FONT_FAMILY, 12, "bold"),
    "normal": (FONT_FAMILY, 11, "normal"),
    "small": (FONT_FAMILY, 10, "normal"),
    "button": (FONT_FAMILY, 11, "bold"),
    "table_header": (FONT_FAMILY, 11, "bold"),
    "table_cell": (FONT_FAMILY, 10, "normal"),
}

DIMENSIONS = {
    "window_width": 1200,      # Increased for better layout
    "window_height": 700,      # Increased for better layout
    "sidebar_width": 260,      # Width of sidebar
    "header_height": 70,       # Height of header
    "card_padding": 20,        # Default card padding
    "button_height": 36,       # Default button height
    "table_row_height": 35,    # Table row height
}

# UI Element Styling
BUTTON_STYLES = {
    "padding": (15, 8),
    "corner_radius": 8,
    "hover_effect": True,
}

CARD_STYLES = {
    "corner_radius": 12,
    "shadow": True,
    "padding": 20,
}

TABLE_STYLES = {
    "row_height": 35,
    "alternate_rows": True,
    "hover_highlight": True,
    "border_width": 1,
}

# Application Settings
APP_SETTINGS = {
    "app_name": "Student Management System",
    "version": "2.0",
    "company": "Education Management Solutions",
    "date_format": "%Y-%m-%d",
    "datetime_format": "%Y-%m-%d %H:%M:%S",
    "currency_symbol": "$",
    "currency_position": "before",  # 'before' or 'after'
    "items_per_page": 20,          # Pagination setting
}

# Status Messages
STATUS_MESSAGES = {
    "success": {
        "save": "Record saved successfully!",
        "update": "Record updated successfully!",
        "delete": "Record deleted successfully!",
        "login": "Login successful!",
    },
    "error": {
        "save": "Error saving record!",
        "update": "Error updating record!",
        "delete": "Error deleting record!",
        "login": "Invalid username or password!",
        "access": "Access denied!",
    },
    "warning": {
        "delete": "Are you sure you want to delete this record?",
        "logout": "Are you sure you want to logout?",
    }
}

# Validation Patterns
VALIDATION = {
    "email_pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "phone_pattern": r'^[0-9+\-()]{10,15}$',
    "name_pattern": r'^[a-zA-Z\s]{2,50}$',
}

# API Endpoints (if you have any)
API_ENDPOINTS = {
    "students": "/api/students",
    "staff": "/api/staff",
    "fees": "/api/fees",
    "payments": "/api/payments",
    "salaries": "/api/salaries",
    "expenses": "/api/expenses",
}