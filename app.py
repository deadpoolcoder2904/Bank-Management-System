import streamlit as st
from hello import Bank

st.set_page_config(page_title="Simple Bank App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

menu = st.sidebar.selectbox("Choose Action", ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Info", "Delete Account"])

if menu == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=0, step=1)
    email = st.text_input("Your Email")
    pin = st.text_input("4-digit PIN", type="password")
    
    if st.button("Create"):
        if name and email and pin:
            user, msg = Bank.create_account(name, int(age), email, int(pin))
            st.success(msg)
            if user:
                st.info(f"Your Account Number: {user['accountNo.']}")
        else:
            st.warning("Fill all fields")

elif menu == "Deposit":
    st.subheader("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    
    if st.button("Deposit"):
        success, msg = Bank.deposit(acc_no, int(pin), int(amount))
        st.success(msg) if success else st.error(msg)

elif menu == "Withdraw":
    st.subheader("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    
    if st.button("Withdraw"):
        success, msg = Bank.withdraw(acc_no, int(pin), int(amount))
        st.success(msg) if success else st.error(msg)

elif menu == "Show Details":
    st.subheader("Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        user = Bank.find_user(acc_no, int(pin))
        if user:
            st.json(user)
        else:
            st.error("No account found")

elif menu == "Update Info":
    st.subheader("Update Your Info")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password")
    
    name = st.text_input("New Name (Optional)")
    email = st.text_input("New Email (Optional)")
    new_pin = st.text_input("New PIN (Optional)")

    if st.button("Update"):
        success, msg = Bank.update_user(acc_no, int(pin), name, email, new_pin)
        st.success(msg) if success else st.error(msg)

elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        success, msg = Bank.delete_user(acc_no, int(pin))
        st.success(msg) if success else st.error(msg)