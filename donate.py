import streamlit as st
import mysql.connector


st.header("Donation Page")

def init_db():
    conn = mysql.connector.connect(
        host="Toukeer-pc",       
        user="root",             
        password="Toukeer@125",  
        database="donar"         
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            viral_disease VARCHAR(255),
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_user(name, email, age, gender, viral_disease, password):
    try:
        conn = mysql.connector.connect(
            host="Toukeer-pc",
            user="root",
            password="Toukeer@125",
            database="donar"
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, age, gender, viral_disease, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email, age, gender, viral_disease, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False


def fetch_users():
    conn = mysql.connector.connect(
        host="Toukeer-pc",
        user="root",
        password="Toukeer@125",
        database="donar"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, age, gender, viral_disease FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


init_db()

st.title("User Registration System")


st.header("Register as a Donor")
with st.form("user_form"):
    name = st.text_input("Name")  
    email = st.text_input("Email")  
    age = st.number_input("Age", min_value=1, max_value=120, step=1)  
    gender = st.radio("Gender", options=["Male", "Female", "Other"])  
    viral_disease = st.text_input("Do you have any viral disease?")  
    password = st.text_input("Password", type="password")  
    submit = st.form_submit_button("Register")  

    if submit:  
        if name and email and age and gender and password: 
            success = insert_user(name, email, age, gender, viral_disease, password)
            if success:
                st.success("User registered successfully!")  
            else:
                st.error("Error: Email already exists!")
        else:
            st.error("Please fill in all fields.") 


st.header("Registered Users")
users = fetch_users()
if users:
    st.write("Here are all the registered users:")
    st.table(users) 
else:
    st.write("No users registered yet.")  
