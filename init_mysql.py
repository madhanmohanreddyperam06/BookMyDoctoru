#!/usr/bin/env python3
"""
MySQL Database Setup for Doctor Appointment System
Creates MySQL database and initializes it with sample data
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_mysql_database():
    """Create MySQL database and user if they don't exist"""
    
    # MySQL connection parameters
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Madhanreddy@123',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    databases = ['doctor_appointment', 'doctor_appointment_dev', 'doctor_appointment_test']
    
    try:
        print("🔧 Connecting to MySQL server...")
        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()
        
        print("✅ Connected to MySQL server successfully!")
        
        # Create databases
        for db_name in databases:
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ Database '{db_name}' created or already exists")
            except pymysql.Error as e:
                print(f"❌ Error creating database '{db_name}': {e}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 MySQL databases setup completed!")
        print("\n📋 Next steps:")
        print("1. Make sure MySQL server is running")
        print("2. Update the password in .env file if needed")
        print("3. Run: python init_mysql.py to initialize the database")
        print("4. Run: python start.py to start the application")
        
    except pymysql.Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL server is installed and running")
        print("2. Check if MySQL root password is correct")
        print("3. Verify MySQL service is running on localhost:3306")
        print("4. Update password in this script if needed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_mysql_database()
