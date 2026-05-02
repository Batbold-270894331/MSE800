from database import create_tables
##from user_manager import add_user, view_users, search_user, delete_user

def main():
    create_tables()
    print("All tables created.")

if __name__ == "__main__":
    main()
