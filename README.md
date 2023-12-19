# Yoga Class Enrollment Application

This application manages enrollments for yoga classes, allowing users to enroll, update their batch preferences, and providing admin access to view enrollments.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Flask-WTF
- SQLite3

### Setup

1. Clone the repository.
2. Install the required packages: `pip install -r requirements.txt`.
3. Run the application: `python app.py`.

## Usage

### Routes

- `/`: Home page
- `/enroll`: Enroll in a yoga class
- `/update`: Update batch preferences
- `/admin/enrollments`: Admin panel to view enrollments

### Database

The application uses an SQLite database (`yogaa.db`) to store enrollment details. 

### File Structure

- `app.py`: Main application file
- `templates/`: Contains HTML templates
- `static/`: Static files (CSS, JS)

## Development

- The application uses Flask for the backend and Jinja2 templating for the frontend.
- Bootstrap is used for styling.
- SQLite3 is used as the database.

## Troubleshooting

If encountering issues:

- Check database connections.
- Ensure Flask routes are correctly defined.
- Inspect console logs for errors.

## Contributing

Feel free to fork and contribute to the project!
