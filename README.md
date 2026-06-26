# BookMyDoctor

## Doctor Appointment Booking Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1+-purple.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive hospital appointment management system supporting Admin, Doctor, and Patient workflows with strict Online/Offline mode separation.

## 📋 Features

### Admin Role

- **Dashboard Overview**: Total appointments, revenue statistics, doctor/patient counts
- **Doctor Management**: Add/update/deactivate doctors with specialities and consultation modes
- **Shift Management**: Create and manage doctor shifts (Morning/Evening/Night)
- **Slot & Token Management**: Generate time-based slots with token numbers
- **Speciality Management**: Add and manage medical specializations
- **System Monitoring**: Track appointment lifecycle and generate reports

### Doctor Role

- **Schedule Access**: View assigned duty schedules (read-only)
- **Appointment Handling**: Update appointment status (confirmed/completed/cancelled/no-show)
- **Prescription Management**: Add diagnosis, medicines, and follow-up instructions
- **Online Consultation**: Join video consultations with patients
- **Offline Consultation**: Display clinic address automatically

### Patient Role

- **Dashboard**: Toggle between Online/Offline mode, view appointments
- **Doctor Filtering**: Filter by speciality, availability, and consultation mode
- **Appointment Booking**: Select available shifts and slots, receive token numbers
- **Medical History**: View past prescriptions and consultation notes
- **Prescription Details**: Access detailed prescription records with medicines
- **Online/Offline Appointments**: Join video consultations or view clinic information

## 🛠️ Tech Stack

### Backend

- **Python 3.8+** - Programming language
- **Flask 2.3.3** - Web framework
- **Flask-SQLAlchemy 3.0.5** - ORM for database management
- **SQLAlchemy 1.4.23** - SQL toolkit and ORM
- **Flask-Login 0.6.3** - User session & authentication management
- **Flask-Migrate 4.0.5** - Database schema migrations (Alembic)
- **Flask-WTF 1.1.1** - Form handling & CSRF protection
- **Flask-Bcrypt 1.0.1** - Password hashing
- **Flask-SocketIO 5.3.6** - Real-time WebSocket support
- **PyMySQL 1.1.0** - MySQL database driver
- **python-dotenv 1.0.0** - Environment variable management
- **email-validator 2.0.0** - Email validation
- **Werkzeug 2.3.7** - WSGI utility library
- **cryptography 41.0.0+** - Cryptographic operations

### Database

- **MySQL 8.0+** - Relational database (Development, Testing & Production)
  - `doctor_appointment_dev` — Development database
  - `doctor_appointment_test` — Testing database
  - `doctor_appointment_prod` — Production database

### Frontend

- **HTML5** - Markup structure
- **CSS3** - Custom styling (`style.css`)
- **Bootstrap 5.1** - Responsive UI framework
- **JavaScript** - Client-side logic (`main.js`, `fixes.js`)
- **Jinja2** - Server-side template engine
- **Font Awesome 6** - Icon library
- **Chart.js** - Included in frontend templates for dashboards/analytics

### Video Consultation

- **Room-based consultation system** with time-gated access control
- **Flask-SocketIO** for real-time communication support

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL Server 8.0+
- pip and virtualenv

### Quick Start

1. **Clone and setup**

   ```bash
   git clone https://github.com/madhanmohanreddyperam06/BookMyDoctor.git
   cd Doctor-Appointment-System
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Copy `.env.example` to `.env` and update with your configuration:

   ```bash
   cp .env.example .env
   ```

   Update the `.env` file with your MySQL credentials and secret key:

   ```env
   SECRET_KEY=your-secret-key-here-generate-a-random-string
   DATABASE_URL=mysql+pymysql://username:password@localhost/doctor_appointment
   FLASK_ENV=development
   ```

   **Important:** Generate a secure SECRET_KEY for production. You can generate one using:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Initialize the database**

   ```bash
   # Create MySQL databases
   python init_mysql.py

   # Seed with sample data
   python init_mysql_data.py
   ```

5. **Start the application**

   ```bash
   python run.py
   ```

6. **Access the application**

   - Open browser: `http://localhost:5000`
   - Admin: `admin@hospital.com` / `admin123`
   - Patient: `patient1@email.com` / `patient123`

## 🌐 Deployment

### Production Deployment

1. **Set environment variables**

   Create a `.env` file with production values:

   ```env
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=mysql+pymysql://user:password@production-host/doctor_appointment
   FLASK_ENV=production
   ```

2. **Use production configuration**

   Set the `FLASK_ENV` environment variable to `production`:

   ```bash
   export FLASK_ENV=production  # Linux/macOS
   set FLASK_ENV=production     # Windows
   ```

3. **Database setup**

   Ensure MySQL is configured and the database exists on the production server.

4. **Run with production server**

   For production, use a WSGI server like Gunicorn:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Security Notes

- Never commit `.env` file to version control
- Use strong, randomly generated SECRET_KEY
- Use HTTPS in production
- Configure firewall rules to restrict database access
- Keep dependencies updated regularly

### Database Setup

#### MySQL (Default)

- Driver: **PyMySQL** via `mysql+pymysql://` connection string
- Configuration: `config.py` and `.env`
- Separate databases for Development, Testing, and Production environments

#### Database Management

```bash
# Check database status
python check_database.py

# Create MySQL databases
python init_mysql.py

# Initialize with sample data
python init_mysql_data.py

# Test MySQL connection
python test_mysql.py

# View database contents
python view_database.py
```

#### Database Migrations

```bash
# Initialize migration
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Project Structure

```text
Doctor-Appointment-System/
├── 📄 .env                        # Environment variables (MySQL config)
├── 📄 .gitignore                  # Git ignore rules
├── 📄 LICENSE                     # MIT License
├── 📄 README.md                   # Project documentation
├── 📄 requirements.txt            # Python dependencies
├── 📄 config.py                   # App configuration (Dev/Test/Prod)
├── 📄 run.py                      # Main application entry point
├── 📄 init_mysql.py               # MySQL database creator
├── 📄 init_mysql_data.py          # Database seeder with sample data
├── 📁 app/                        # Main application package
│   ├── 📄 __init__.py             # App factory & extension init
│   ├── 📁 models/                 # SQLAlchemy database models
│   │   ├── 📄 user.py             # User authentication model
│   │   ├── 📄 admin.py            # Admin model
│   │   ├── 📄 doctor.py           # Doctor model
│   │   ├── 📄 patient.py          # Patient model
│   │   ├── 📄 speciality.py       # Medical speciality model
│   │   ├── 📄 shift.py            # Doctor shift model
│   │   ├── 📄 slot.py             # Appointment slot model
│   │   ├── 📄 appointment.py      # Appointment model
│   │   ├── 📄 prescription.py     # Prescription model
│   │   └── 📄 medicine.py         # Medicine model
│   ├── 📁 routes/                 # Flask blueprints & route handlers
│   │   ├── 📄 auth.py             # Authentication routes
│   │   ├── 📄 admin.py            # Admin dashboard routes
│   │   ├── 📄 doctor.py           # Doctor dashboard routes
│   │   ├── 📄 patient.py          # Patient dashboard routes
│   │   ├── 📄 main.py             # Landing page & general routes
│   │   └── 📄 video.py            # Video consultation routes
│   ├── 📁 static/                 # Static assets
│   │   ├── 📁 css/                # Stylesheets
│   │   │   └── 📄 style.css       # Custom application styles
│   │   ├── 📁 js/                 # JavaScript files
│   │   │   ├── 📄 main.js         # Core client-side logic
│   │   │   └── 📄 fixes.js        # UI fixes & enhancements
│   │   └── 📁 images/             # Image assets & icons
│   └── 📁 templates/              # Jinja2 HTML templates
│       ├── 📄 base.html           # Base layout template
│       ├── 📄 video_consultation.html  # Video consultation page
│       ├── 📁 auth/               # Authentication templates
│       │   ├── 📄 landing.html    # Landing page
│       │   ├── 📄 login.html      # Login page
│       │   ├── 📄 register_patient.html  # Patient registration
│       │   └── 📄 profile.html    # User profile page
│       ├── 📁 admin/              # Admin dashboard templates
│       │   ├── 📄 dashboard.html  # Admin overview
│       │   ├── 📄 doctors.html    # Doctor management
│       │   ├── 📄 add_doctor.html # Add new doctor
│       │   ├── 📄 specialities.html  # Speciality management
│       │   ├── 📄 add_speciality.html  # Add speciality
│       │   ├── 📄 shifts.html     # Shift management
│       │   └── 📄 add_shift.html  # Add new shift
│       ├── 📁 doctor/             # Doctor dashboard templates
│       │   ├── 📄 dashboard.html  # Doctor overview
│       │   ├── 📄 schedule.html   # Duty schedule
│       │   ├── 📄 appointments.html  # Appointment list
│       │   ├── 📄 appointment_detail.html  # Appointment detail
│       │   └── 📄 prescription.html  # Prescription form
│       └── 📁 patient/            # Patient dashboard templates
│           ├── 📄 dashboard.html  # Patient overview
│           ├── 📄 doctors.html    # Browse doctors
│           ├── 📄 doctor_detail.html  # Doctor profile
│           ├── 📄 book_appointment.html  # Book appointment
│           ├── 📄 appointments.html  # Appointment list
│           ├── 📄 appointment_detail.html  # Appointment detail
│           ├── 📄 medical_history.html  # Medical history
│           └── 📄 prescription_detail.html  # Prescription view
└── 📁 venv/                       # Virtual environment (not tracked)
```

## 🗄️ Database Schema

The system uses the following main entities:

- **Users** — Base user authentication with role-based access (admin/doctor/patient)
- **Admins** — Hospital administrators
- **Doctors** — Medical practitioners with specialities and consultation modes
- **Patients** — Individuals seeking medical consultations
- **Specialities** — Medical specializations (e.g., Cardiology, Dermatology)
- **Shifts** — Doctor duty schedules (Morning/Evening/Night)
- **Slots** — Time-based appointment slots with token numbers
- **Appointments** — Patient-doctor consultations with status tracking
- **Prescriptions** — Medical prescriptions with diagnosis and follow-up details
- **Medicines** — Medications linked to prescriptions

## 🔐 Default Login Credentials

### Admin

- Email: `admin@hospital.com`
- Password: `admin123`

### Doctors

- Dr. John Smith: `dr.smith@hospital.com` / `smith123`
- Dr. Sarah Johnson: `dr.johnson@hospital.com` / `johnson123`
- Dr. Michael Wilson: `dr.wilson@hospital.com` / `wilson123`
- Dr. Emily Brown: `dr.brown@hospital.com` / `brown123`
- Dr. Robert Davis: `dr.davis@hospital.com` / `davis123`

### Patients

- Alice Johnson: `patient1@email.com` / `patient123`
- Bob Smith: `patient2@email.com` / `patient123`
- Carol Williams: `patient3@email.com` / `patient123`

## 🎯 Key Features

- **Role-based Access Control**: Separate Admin, Doctor, and Patient workflows
- **Online/Offline Consultation Modes**: Distinct consultation pathways
- **Token-based Booking**: Unique appointment tokens per slot
- **Shift Management**: Morning/Evening/Night shift scheduling
- **Prescription System**: Complete medical prescriptions with medicines
- **Video Consultation**: Time-gated room-based video consultation system
- **Interactive Dashboards**: Chart.js powered analytics and statistics
- **Responsive Design**: Bootstrap 5 mobile-first responsive layout
- **Enhanced UI/UX**: Modern login/register pages with Font Awesome icons
- **MySQL Database**: Production-ready relational database with sample data

## 🛠️ Technical Features

- **Flask Application Factory**: Modular app creation pattern
- **Blueprint Architecture**: Route separation by role (auth, admin, doctor, patient, video)
- **SQLAlchemy ORM**: Type-safe database models and relationships
- **Flask-Login**: Session-based authentication with user loader
- **Flask-Bcrypt**: Secure password hashing
- **Flask-Migrate**: Alembic-based database schema migrations
- **Flask-WTF**: CSRF protection and form validation
- **Flask-SocketIO**: WebSocket support for real-time features
- **Environment Configuration**: Separate Dev/Test/Prod configs via `config.py`
- **Jinja2 Templating**: Server-side rendering with template inheritance

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
FLASK_CONFIG=development

# Database Configuration - MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=doctor_appointment

DATABASE_URL=mysql+pymysql://root:your_password@localhost/doctor_appointment
DEV_DATABASE_URL=mysql+pymysql://root:your_password@localhost/doctor_appointment_dev
TEST_DATABASE_URL=mysql+pymysql://root:your_password@localhost/doctor_appointment_test

# Security
SECRET_KEY=your-secret-key-here

# Email Configuration (Optional)
MAIL_SERVER=
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=
MAIL_PASSWORD=
```

### Application Configuration

Database and application settings are managed in `config.py` with separate classes:

| Config Class        | Purpose                | Database                        |
| ------------------- | ---------------------- | ------------------------------- |
| `DevelopmentConfig` | Local development      | `doctor_appointment_dev`        |
| `TestingConfig`     | Automated testing      | `doctor_appointment_test`       |
| `ProductionConfig`  | Production deployment  | `doctor_appointment_prod`       |

## 🧪 Testing

```bash
# Test MySQL connection
python test_mysql.py

# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=app
```

## 🤝 Development

### Adding New Features

1. Create models in `app/models/`
2. Add routes in `app/routes/`
3. Create templates in `app/templates/`
4. Update static files in `app/static/`
5. Register new blueprints in `app/__init__.py`

### Database Changes

```bash
# Create a new migration after model changes
flask db migrate -m "Description of changes"

# Apply the migration
flask db upgrade

# Or reinitialize with fresh data
python init_mysql.py
python init_mysql_data.py
```

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue in the repository or contact:

### Madhan Mohan Reddy Peram

- 📧 Email: [madhanmohanreddyperam06@gmail.com](mailto:madhanmohanreddyperam06@gmail.com)
- 📱 Mobile: +91 9110395993
- 🔗 LinkedIn: [Madhan Mohan Reddy Peram](https://www.linkedin.com/in/madhan-mohan-reddy-peram-63181b253)
- 🐦 Twitter: [@MadhanM16616334](https://x.com/MadhanM16616334)
