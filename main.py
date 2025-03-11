import re
import streamlit as st
import string
import random
import plotly.graph_objects as go
import streamlit.components.v1 as com

# Set Page Configuration
st.set_page_config(
    page_title="Password Generator | Strength Checker",
    page_icon="🔒",
    layout="centered",
    menu_items={
        'About': """
        ## Password Generator
        This app is made by Osama bin Adnan.
        Source code is available on [GitHub](https://github.com/OsamabinAdnan/).
        """
    }
)

com.iframe("https://lottie.host/embed/7bde058d-2083-4425-ad14-834874a56d27/sYgGdw2kmg.lottie")

# 🎯 Title Section
st.title("🔒 Password Generator & Strength Checker")

# 🔹 Creating Tabs
tab1, tab2 = st.tabs(["🔑 Password Generator", "🛡️ Password Strength Checker"])

# --- 🔹 PASSWORD GENERATOR --- #
with tab1:
    st.header("🔑 Generate a Secure Password")
    length = st.slider("Password Length:", min_value=6, max_value=20, value=13)
    use_digit = st.checkbox("Include Digits")
    use_special = st.checkbox("Include Special Characters")

    # Function to generate random passwords
    def generate_random_password(length, use_digit, use_special):
        characters = string.ascii_letters
        if use_digit:
            characters += string.digits
        if use_special:
            characters += string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    if st.button("🔄 Generate Password"):
        password = generate_random_password(length, use_digit, use_special)

        # Styled password display
        st.markdown(
            f"<p style='font-size:22px; font-weight:bold;'>🔐 Generated Password:</p>"
            f"<p style='font-size:22px; font-weight:bold; color:green; background-color:#f0f0f0; padding:5px; border-radius:5px; display:inline-block;'>{password}</p>",
            unsafe_allow_html=True
        )

# --- 🔹 PASSWORD STRENGTH CHECKER --- #
with tab2:
    st.header("🛡️ Check Your Password Strength")

    password = st.text_input("Enter your password:", placeholder="At least 8 characters", type="password")
    # Check if the password field is empty
    if  len(password) == 0:
        st.warning("Please enter a password to check its strength.")
        st.stop()

    # Blacklisted Weak Passwords
    BLACKLISTED_PASSWORDS = {"password", "123456", "qwerty", "password123", "admin", "letmein", "welcome"}

    # Function to check password strength
    def check_password_strength(password):
        score = 0
        feedback = []

        # Check if password is in the blacklist
        if password.lower() in BLACKLISTED_PASSWORDS:
            return 0, "❌ Very Weak", ["This password is too common and easily guessed. Use a unique one."]

        # Check password length
        if len(password) >= 8:
            score += 2
        else:
            feedback.append("Increase password length to at least 8 characters.")

        # Check upper and lowercase characters
        if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
            score += 1
        else:
            feedback.append("Include both uppercase and lowercase letters.")

        # Check digits
        if re.search(r"\d", password):
            score += 1
        else:
            feedback.append("Add at least one number (0-9).")

        # Check special characters
        if re.search(r"[!@#$%^&*()]", password):
            score += 1
        else:
            feedback.append("Use at least one special character (!@#$%^&*()).")

        # Determine password strength
        if score <= 3:
            return score, "❌ Weak", feedback
        elif score <= 4:
            return score, "⚠️ Moderate", feedback
        else:
            return score, "✅ Strong", []

    # Function to suggest a stronger password
    def generate_suggest_password(password):
        suggested_password = list(password)

        # Ensure at least 8 characters
        while len(suggested_password) < 8:
            suggested_password.append(random.choice(string.ascii_letters))
        
        # Ensure password contains required character types
        if not re.search(r"[A-Z]", password):
            suggested_password.append(random.choice(string.ascii_uppercase))
        if not re.search(r"[a-z]", password):
            suggested_password.append(random.choice(string.ascii_lowercase))
        if not re.search(r"[0-9]", password):
            suggested_password.append(random.choice(string.digits))
        if not re.search(r"[!@#$%^&*()]", password):
            suggested_password.append(random.choice("!@#$%^&*()"))

        random.shuffle(suggested_password)
        return "".join(suggested_password)

    # Function to create gauge chart
    def create_gauge(score):
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': 'gold'},
                'bgcolor': 'white',
                'bordercolor': 'gray',
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 2], 'color': 'red'},
                    {'range': [2, 4], 'color': 'yellow'},
                    {'range': [4, 5], 'color': 'green'}
                ]
            }
        ))
        return fig

    # --- Checking Password Strength --- #
    if password:
        score, strength, feedback = check_password_strength(password)

        # Display strength level
        st.write(f"### Strength: {strength} (Score: {score}/5)")

        # Display gauge meter
        st.plotly_chart(create_gauge(score))

        # Provide feedback based on strength
        if strength == "❌ Weak":
            st.error("⚠️ Your password is weak! Improve it with the suggestions below:")
            for tip in feedback:
                st.write(f"- {tip}")
            suggested_password = generate_suggest_password(password)
            st.info(f"🔑 Suggested Strong Password: **{suggested_password}**")

        elif strength == "⚠️ Moderate":
            st.warning("⚠️ Your password is moderate. Consider strengthening it!")
            for tip in feedback:
                st.write(f"- {tip}")
            suggested_password = generate_suggest_password(password)
            st.info(f"🔑 Suggested Stronger Password: **{suggested_password}**")

        elif strength == "✅ Strong":
            st.success("✅ Great job! Your password is strong and secure. 🎉")

    # --- Generate a Strong Random Password --- #
    if st.button("🔄 Generate Strong Password"):
        strong_password = generate_suggest_password("random")
        st.markdown(
            f"<p style='font-size:22px; font-weight:bold;'>🔐 Generated Strong Password:</p>"
            f"<p style='font-size:22px; font-weight:bold; color:green; background-color:#f0f0f0; padding:5px; border-radius:5px; display:inline-block;'>{strong_password}</p>",
            unsafe_allow_html=True
        )

# 🔹 Footer
st.markdown("---")
st.markdown("👨‍💻 Built with ❤️ by [Osama bin Adnan](https://github.com/OsamabinAdnan)")
