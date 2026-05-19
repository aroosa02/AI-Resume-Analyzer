import streamlit.components.v1 as components


def speak_text(text: str, button_label: str = "🔊 Read Aloud") -> None:
    safe_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("\n", " ")
        .replace('"', '\\"')
    )

    components.html(
        f"""
        <button
            onclick="speakText()"
            style="
                background: linear-gradient(135deg, #2563eb, #7c3aed);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 10px;
                font-size: 14px;
                cursor: pointer;
                font-weight: 600;
                margin-top: 8px;
            "
        >
            {button_label}
        </button>

        <script>
        function speakText() {{
            const text = `{safe_text}`;

            if (!window.speechSynthesis) {{
                alert("Voice is not supported in this browser.");
                return;
            }}

            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-US";
            utterance.rate = 0.95;
            utterance.pitch = 1;

            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=70,
    )