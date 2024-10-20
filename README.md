
# Find a Campsite App

## Overview
The Find a Campsite App is a Kivy-based graphical user interface application that allows users to manage their campsite bookings through a secure account system. The app provides features such as account creation, secure login, password recovery, and a help screen for user guidance. It uses Redis as the backend for storing user data, with passwords encrypted for security.

This repository contains the complete Python code required to run the app, including Kivy screen definitions, Redis connection management, and logic for handling user interactions.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Execution](#execution)
- [Directory Structure](#directory-structure)
- [File Descriptions](#file-descriptions)
- [Testing](#testing)
- [License](#license)

## Features
- **Account Management:** Allows users to create accounts with encrypted passwords and custom security questions for password recovery.
- **Secure Login:** Utilises bcrypt for secure password verification against stored encrypted hashes.
- **Password Recovery:** Provides a password reset feature using custom security questions.
- **Interactive GUI:** Built with Kivy for a responsive, user-friendly interface.
- **Data Encryption:** Ensures all sensitive user data is securely encrypted before storage in Redis.
- **Error Handling:** Robust error handling for database operations and user inputs.

## Installation

1. **Clone the repository:**

   - git clone https://github.com/Harrison-Shepherd/Find-a-Campsite-App
   - cd find-a-campsite-app
    


## Usage

**The application can be used to manage campsite accounts securely through a simple and interactive interface.**

- Create an Account: Register by providing an email, password, first name, and a security question.
- Login: Use your credentials to access your account.
- Forgot Password: Reset your password by answering your security question correctly.
- Help: Access guidance on how to use the app from the information screen.

## Execution
**To run the Application: Run the main application file:**

- python gui_main.py

This will launch the Kivy app window with the main menu, allowing you to navigate between different features.

**To clean the Redis Database (Optional):**

- python clean_database.py

Allows you to clear the redis environment. The data is permanently lost.

## Directory Structure

Find-a-Campsite-App/
│
├── gui_main.py
|── clean_database.py
├── Logic/
│   ├── app_logic.py
│   ├── ...
├── Models/
│   ├── redis_client.py
│   ├── account.py
│   ├── ...
├── Screens/
│   ├── main_menu_screen.py
│   ├── create_account_screen.py
│   ├── login_screen.py
│   ├── forgot_password_screen.py
│   ├── info_screen.py
│   ├── ...
├── Utils/
│   ├── data_loader.py
│   ├── error_handler.py
│   ├── ...
├── GUI/
│   ├── gui_helpers.py
│   ├── gui_kivy.py
│   ├── ...
├── Tests/
│   ├── test_account_setup.py
│   ├── test_data_loader.py
│   ├── test_login.py
│   ├── test_security.py


## File Descriptions

- **`gui_main.py`**  
  **Purpose:** Main entry point for the application. Initializes the Kivy application and sets up the screen manager with various screens.

- **`app_logic.py`**  
  **Purpose:** Contains the main logic for handling account operations, including account creation, login, password reset, and data validation with Redis.

- **`redis_client.py`**  
  **Purpose:** Manages Redis database connections and provides methods for common Redis operations like fetching, setting, and deleting keys.

- **`account.py`**  
  **Purpose:** Manages individual account operations, including creating new accounts, validating logins, and handling password recovery using bcrypt encryption.

- **`data_loader.py`**  
  **Purpose:** Loads initial data from a CSV file into Redis for testing purposes. Handles encryption of passwords on load and skips setting the security question if not present.

- **`clean_database.py`**  
  **Purpose:** Provides a utility to clean the Redis database by deleting all keys. Useful for resetting the database during testing.

- **`gui_helpers.py`**  
  **Purpose:** Provides reusable helper functions for creating GUI components like buttons, popups, and labels used across various Kivy screens.

- **`Screens/ - Screen Files`**  
  **Contains individual Kivy screen files such as:**
  - **`main_menu_screen.py`** - Main entry screen with navigation options.
  - **`create_account_screen.py`** - Screen for user registration.
  - **`login_screen.py`** - Screen for logging in.
  - **`forgot_password_screen.py`** - Screen for resetting passwords.
  - **`info_screen.py`** - Screen providing help and usage information.




## Testing 
**Run Tests: Run the tests to ensure the functionality works as expected:**
- python -m unittest discover Tests

Tests cover account creation, login, error handling, and data validation within the redis environment.
