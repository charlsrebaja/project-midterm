"""
Script to create the MySQL database for the security system
Run this before running migrations
"""
import MySQLdb

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password is empty
}

try:
    # Connect to MySQL server
    connection = MySQLdb.connect(**db_config)
    cursor = connection.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS security_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    print("✅ Database 'security_system_db' created successfully!")
    
    # Show existing databases to confirm
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\n📊 Available databases:")
    for db in databases:
        if db[0] == 'security_system_db':
            print(f"  ✓ {db[0]} (ready to use)")
        else:
            print(f"    {db[0]}")
    
    cursor.close()
    connection.close()
    
except MySQLdb.Error as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Make sure:")
    print("  1. XAMPP is running")
    print("  2. MySQL service is started")
    print("  3. Your MySQL credentials are correct")
