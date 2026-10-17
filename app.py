import streamlit as st
from zxcvbn import zxcvbn


# Page configuration
st.set_page_config(
    page_title="AI Password Strength Analyzer",
    page_icon="🔐",
    layout="centered"
)


# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f4f7fb;
    }

    .title {
        text-align: center;
        color: #172554;
        font-size: 34px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
    }

    .result {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# Application heading
st.markdown(
    '<div class="title">🔐 Password Strength Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze password strength and improve your security.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# Password input
password = st.text_input(
    "Enter your password",
    type="password",
    placeholder="Type a password to analyze"
)


# Analyze password
if password:

    result = zxcvbn(password)

    # zxcvbn score ranges from 0 to 4
    score = result["score"]

    # Convert score to percentage
    percentage = score * 25

    # Strength classification
    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }

    strength = strength_levels[score]

    # Display results
    st.subheader("Analysis Results")

    st.metric("Strength Score", f"{percentage}/100")

    st.progress(percentage / 100)

    st.markdown(
        f"### Password Strength: {strength}"
    )

    # Display estimated crack time
    crack_time = result["crack_times_display"][
        "offline_slow_hashing_1e4_per_second"
    ]

    st.write("**Estimated guessing time:**", crack_time)

    # Feedback section
    st.subheader("Security Recommendations")

    feedback = result.get("feedback", {})
    warning = feedback.get("warning", "")
    suggestions = feedback.get("suggestions", [])

    if warning:
        st.warning(warning)

    if suggestions:
        for suggestion in suggestions:
            st.write("💡", suggestion)
    elif score >= 3:
        st.success("No additional recommendations from the estimator.")

    # Additional checks
    st.subheader("Password Characteristics")

    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains uppercase letters": any(
            char.isupper() for char in password
        ),
        "Contains lowercase letters": any(
            char.islower() for char in password
        ),
        "Contains numbers": any(
            char.isdigit() for char in password
        ),
        "Contains special characters": any(
            not char.isalnum() for char in password
        )
    }

    for description, passed in checks.items():
        symbol = "✅" if passed else "❌"
        st.write(f"{symbol} {description}")


else:
    st.info("Enter a password above to begin the analysis.")


# Privacy notice
st.divider()

st.caption(
    "Privacy: This application does not intentionally store passwords. "
    "Use a test password rather than a real account password."
)