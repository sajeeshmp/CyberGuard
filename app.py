import streamlit as st
from ml.ml_service import analyze_scam


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CyberGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛡️ CyberGuard")
st.subheader("Cyber Security Awareness Platform")

st.write(
    "Protect yourself from phishing messages, suspicious links, "
    "and digital arrest scams."
)

st.divider()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🛡️ CyberGuard")
st.sidebar.write("Navigate through the platform.")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Home",
        "Message Analysis",
        "URL Analysis",
        "Cyber Awareness Center",
        "Cyber Safety Quiz",
    ],
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.header("Welcome to CyberGuard 👋")

    st.write(
        """
        CyberGuard helps users understand potential online scams
        and recognize common warning signs in suspicious messages.

        ### What can you do here?

        - 🔍 **Message Analysis:** Check suspicious messages for scam indicators.
        - 🔗 **URL Analysis:** Access the URL analysis section.
        - 📚 **Cyber Awareness Center:** Learn how to stay safe online.
        - 🧠 **Cyber Safety Quiz:** Test your cybersecurity knowledge.
        """
    )

    st.info(
        "CyberGuard provides educational guidance. "
        "Its predictions are experimental and cannot guarantee "
        "whether a message is safe or fraudulent."
    )

    st.subheader("Stay safe online")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Platform", "CyberGuard")

    with col2:
        st.metric("Focus", "Scam Awareness")

    with col3:
        st.metric("Purpose", "Online Safety")


# --------------------------------------------------
# MESSAGE ANALYSIS
# --------------------------------------------------

elif page == "Message Analysis":

    st.header("🔍 Suspicious Message Analysis")

    st.write(
        "Paste a suspicious SMS, email, or chat message below "
        "to examine possible scam indicators."
    )

    message = st.text_area(
        "Enter the message",
        placeholder=(
            "Example: URGENT! Your bank account will be blocked. "
            "Verify your KYC immediately using this link."
        ),
        height=180,
        key="message_input",
    )

    if st.button("Analyze Message", type="primary"):

        if not message.strip():

            st.warning("Please enter a message before analyzing.")

        else:

            with st.spinner("Analyzing the message..."):

                try:
                    result = analyze_scam(message.strip())

                    if not isinstance(result, dict):
                        st.error(
                            "The analysis service returned an unexpected result."
                        )
                    else:
                        st.subheader("Analysis Results")

                        # Display the prediction.
                        prediction = result.get(
                            "prediction",
                            result.get("label", "Unknown"),
                        )

                        prediction_text = str(prediction)
                        prediction_lower = prediction_text.lower()

                        if (
                            "scam" in prediction_lower
                            or "spam" in prediction_lower
                        ):
                            st.error(
                                f"⚠️ Potential Scam Detected: "
                                f"{prediction_text}"
                            )

                        elif (
                            "legitimate" in prediction_lower
                            or "ham" in prediction_lower
                            or "safe" in prediction_lower
                        ):
                            st.success(
                                f"Prediction: {prediction_text}"
                            )

                        else:
                            st.info(
                                f"Prediction: {prediction_text}"
                            )

                        # Display probability, if available.
                        probability = result.get(
                            "probability",
                            result.get(
                                "scam_probability",
                                None,
                            ),
                        )

                        if probability is not None:

                            try:
                                probability_value = float(probability)

                                # Support both 0-1 and 0-100 formats.
                                if 0 <= probability_value <= 1:
                                    probability_percent = (
                                        probability_value * 100
                                    )
                                else:
                                    probability_percent = probability_value

                                probability_percent = max(
                                    0,
                                    min(100, probability_percent),
                                )

                                st.metric(
                                    "Estimated Scam Probability",
                                    f"{probability_percent:.2f}%",
                                )

                                st.progress(
                                    probability_percent / 100
                                )

                            except (TypeError, ValueError):
                                st.write(
                                    "Probability:",
                                    probability,
                                )

                        # Display explanation, if available.
                        explanation = result.get(
                            "explanation",
                            result.get("reason", None),
                        )

                        if explanation:
                            st.subheader("Why was it flagged?")
                            st.write(explanation)

                        # Display warning, if available.
                        warning = result.get("warning", None)

                        if warning:
                            st.warning(warning)

                        st.info(
                            "Important: This result is an experimental "
                            "machine-learning prediction, not proof that "
                            "a message is genuine or fraudulent. "
                            "Do not click suspicious links or share "
                            "passwords, OTPs, or banking details."
                        )

                except Exception as error:

                    st.error(
                        "Message analysis could not be completed."
                    )

                    st.caption(
                        f"Technical details: {error}"
                    )


# --------------------------------------------------
# URL ANALYSIS
# --------------------------------------------------

elif page == "URL Analysis":

    st.header("🔗 Suspicious URL Analysis")

    st.write(
        "Use this section to learn about suspicious links "
        "and identify common URL warning signs."
    )

    url = st.text_input(
        "Enter a suspicious URL",
        placeholder="https://example.com",
    )

    st.warning(
        "URL analysis has not yet been connected to the URL "
        "risk engine. This section does not currently verify "
        "or classify the URL."
    )

    if st.button("Check URL"):

        if not url.strip():

            st.warning("Please enter a URL.")

        else:

            st.info(
                "The URL analysis module will be connected "
                "when the URL Analysis & Risk Engine is ready."
            )

            st.write("Entered URL:", url.strip())

            st.caption(
                "Do not open a suspicious link just to test it."
            )


# --------------------------------------------------
# CYBER AWARENESS CENTER
# --------------------------------------------------

elif page == "Cyber Awareness Center":

    st.header("📚 Cyber Awareness Center")

    st.write(
        "Learn to recognize common cyber scams and protect "
        "your personal information."
    )

    with st.expander("🎣 1. Phishing Scams"):

        st.write(
            """
            Phishing messages try to trick people into revealing
            passwords, OTPs, banking details, or other sensitive data.

            **Warning signs:**
            - Urgent demands for immediate action.
            - Unexpected links or attachments.
            - Requests for passwords or OTPs.
            - Suspicious sender addresses.
            - Offers that seem too good to be true.

            **Stay safe:** Verify requests using the organization's
            official website or a trusted contact method.
            """
        )

    with st.expander("🚨 2. Digital Arrest Scams"):

        st.write(
            """
            In a digital arrest scam, criminals may impersonate
            police officers, government officials, or investigators
            through phone or video calls.

            They may threaten arrest or claim that your identity
            or bank account is connected to a crime.

            **Warning signs:**
            - Threats of immediate arrest over a video call.
            - Demands for money to avoid legal action.
            - Instructions to keep the conversation secret.
            - Requests to transfer money for supposed verification.

            **Stay safe:** Do not transfer money because of threats.
            Verify the claims independently and report suspected
            cybercrime through official channels.
            """
        )

    with st.expander("🏦 3. Banking and KYC Scams"):

        st.write(
            """
            Fraudsters may claim that your bank account, debit card,
            or KYC registration will be blocked unless you act quickly.

            **Warning signs:**
            - Unexpected account-blocking messages.
            - Links requesting banking credentials.
            - Requests for OTPs, PINs, or passwords.

            **Stay safe:** Contact your bank through its official
            app, website, or verified customer-care number.
            Never share your OTP or PIN.
            """
        )

    with st.expander("🎁 4. Prize and Lottery Scams"):

        st.write(
            """
            These scams claim that you have won a prize or lottery
            you do not remember entering.

            You may be asked to pay a fee or provide personal
            information to receive the supposed reward.

            **Stay safe:** Do not pay unexpected fees to claim
            suspicious prizes or share sensitive information.
            """
        )

    with st.expander("🛡️ 5. Essential Cyber Safety Tips"):

        st.write(
            """
            - Use strong, unique passwords.
            - Enable two-factor authentication.
            - Never share OTPs, PINs, or passwords.
            - Verify suspicious messages independently.
            - Avoid clicking unexpected links.
            - Keep your devices and applications updated.
            - Report suspected cybercrime through official channels.
            """
        )


# --------------------------------------------------
# CYBER SAFETY QUIZ
# --------------------------------------------------

elif page == "Cyber Safety Quiz":

    st.header("🧠 Cyber Safety Quiz")

    st.write(
        "Answer these questions to test your cybersecurity knowledge."
    )

    questions = [
        {
            "question": (
                "1. A message says your bank account will be blocked "
                "unless you click an unfamiliar link. What should you do?"
            ),
            "options": [
                "Click the link immediately",
                "Share your OTP",
                "Verify through the bank's official channel",
                "Forward the message to everyone",
            ],
            "answer": "Verify through the bank's official channel",
        },
        {
            "question": (
                "2. Someone claiming to be a police officer demands "
                "money during a video call to avoid arrest. What is "
                "the safest response?"
            ),
            "options": [
                "Transfer the money immediately",
                "Share your banking password",
                "Follow every instruction",
                "Do not pay and verify the claim independently",
            ],
            "answer": "Do not pay and verify the claim independently",
        },
        {
            "question": "3. Should you share an OTP with a caller?",
            "options": [
                "Yes, if they sound official",
                "Yes, if they know your name",
                "No, never share your OTP with a caller",
                "Only share it with unknown callers",
            ],
            "answer": "No, never share your OTP with a caller",
        },
        {
            "question": (
                "4. What is a common sign of a phishing message?"
            ),
            "options": [
                "An unexpected urgent request for sensitive information",
                "A message from a trusted contact that you verified",
                "A normal offline conversation",
                "A reminder you expected from an official app",
            ],
            "answer": (
                "An unexpected urgent request for sensitive information"
            ),
        },
        {
            "question": (
                "5. What should you do if you suspect an online scam?"
            ),
            "options": [
                "Send the scammer more information",
                "Ignore every warning sign",
                "Verify the claim and report suspected fraud",
                "Share the message with your passwords",
            ],
            "answer": "Verify the claim and report suspected fraud",
        },
    ]

    with st.form("cyber_safety_quiz"):

        answers = []

        for index, question in enumerate(questions):

            selected = st.radio(
                question["question"],
                question["options"],
                index=None,
                key=f"quiz_question_{index}",
            )

            answers.append(selected)

        submitted = st.form_submit_button(
            "Submit Answers",
            type="primary",
        )

    if submitted:

        unanswered = sum(
            answer is None for answer in answers
        )

        if unanswered > 0:

            st.warning(
                "Please answer all the questions before submitting."
            )

        else:

            score = sum(
                answer == question["answer"]
                for answer, question in zip(answers, questions)
            )

            st.subheader(
                f"Your Score: {score} / {len(questions)}"
            )

            if score == len(questions):

                st.success(
                    "Excellent! You answered every question correctly."
                )

            elif score >= 3:

                st.info(
                    "Good work! Review the explanations and keep learning."
                )

            else:

                st.warning(
                    "Keep practising. Review the Cyber Awareness Center "
                    "to improve your cyber safety knowledge."
                )

            st.write("### Correct Answers")

            for question in questions:

                st.write(
                    f"**{question['question']}**"
                )

                st.write(
                    f"Correct answer: {question['answer']}"
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CyberGuard | Cyber Security Awareness Platform | "
    "Educational prototype — predictions may be inaccurate."
)