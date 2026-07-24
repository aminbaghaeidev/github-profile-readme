import os
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.github_profile import generate_profile
from src.gpt import chatbot
from src.sections import (
    add_description,
    add_extensions,
    add_personal_info,
    add_skills,
    add_social_accounts,
    add_tech_stack,
)

# Add project root to sys.path, so that we can import modules from src
# This is needed because streamllit cloud is running streamlit_app.py
# from the root directory.
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Github Profile Readme Generator",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Report a bug": "https://github.com/hejazizo/github-profile-readme/issues",
        "About": "Built by [Pytopia](pytopia.ai) team.",
    },
)


st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 420px !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.02);
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.7rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.dialog(":warning: API Key")
def show_api_warning():
    st.write("Please enter your API key to continue.")
    if st.button("Okay"):
        st.rerun()


st.title(":zap: Github Profile Readme Generator")
st.image("src/assets/profile-with-readme.png")


"""
This app generates a Github profile readme file. To learn how to add a readme file to your Github profile, check out
[this](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).
You can customize it and use it in your Github profile.
- First, fill out the forms below.
- Then, go to **Code** tab to copy the code and paste it in your `README.md` file.

You can also change the theme of the readme file by selecting a theme from the dropdown below.
Themes are added by the community. If you want to add a theme, check out the [Github repo](https://github.com/hejazizo/github-profile-readme).
"""

st.header("Personalize your Readme")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        ":bust_in_silhouette: Profile Info",
        ":globe_with_meridians: Social Accounts",
        ":memo: Description",
        ":computer: Skills",
        ":gear: Tech Stack",
        ":heavy_plus_sign: Extensions",
    ]
)

kwargs = {}
kwargs = add_personal_info(tab1, **kwargs)
kwargs = add_social_accounts(tab2, **kwargs)
kwargs = add_description(tab3, **kwargs)
kwargs = add_skills(tab4, **kwargs)
kwargs = add_tech_stack(tab5, **kwargs)
kwargs = add_extensions(tab6, **kwargs)

# -- Sidebar --
with st.sidebar:
    with st.expander(":key: API Key"):
        ai_api_key = st.text_input(
            "OpenAI API Key", type="password", key="chatbot_api_key"
        )
        st.markdown("[Get OpenAI API Key](https://platform.openai.com/api-keys)")

    st.divider()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "What’s on your mind?"}
        ]

    chat_container = st.container(height=350, border=False)

    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    st.caption(":zap: Quick Actions")

    selected_prompt = None

    readme_desc_prompt = f"""I am writing a GitHub README profile. Here is my current description:
        ["{kwargs["description"]}"]
        Please fix any grammatical errors, make it sound more professional and engaging for developers,
        also you can add emojies to make it more friendly and nice.
        keep it in the same language as the description."""

    bio_ideas_prompt = f"""Based on my skills: ["{kwargs["skills"]}"]
        Please suggest 3 catchy, cool, and professional one-liner bios/headlines
        that I can use at the top of my GitHub profile README."""

    projects_idea_prompt = f"""Based on my Tech Stack (just read inside the ![]): ["{kwargs["tech_stacks"]}"]
        Suggest some impressive open-source project ideas that I can build to showcase on my GitHub profile,
        along with a short template for the 'Featured Projects' section of my README."""

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(":sparkles: Improve Description", use_container_width=True):
            selected_prompt = readme_desc_prompt

    with col2:
        if st.button(":bulb: Suggest Github Bio", use_container_width=True):
            selected_prompt = bio_ideas_prompt

    with col3:
        if st.button(":zap: Project Ideas", use_container_width=True):
            selected_prompt = projects_idea_prompt

    prompt_input = st.chat_input("Ask anything...")

    final_prompt = selected_prompt or prompt_input

    if final_prompt:
        if os.getenv("OPENAI_API_KEY"):
            API_KEY = os.getenv("OPENAI_API_KEY")
        if ai_api_key:
            API_KEY = ai_api_key

        if ai_api_key or API_KEY:
            st.session_state.messages.append({"role": "user", "content": final_prompt})
            with chat_container:
                st.chat_message("user").write(final_prompt)

            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Generating Response..."):
                        msg = chatbot(user_message=final_prompt, api=API_KEY)
                        st.write(msg)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": msg}
                        )
                        st.rerun()
        else:
            show_api_warning()


st.header("README.md Preview")
"""
- Select a theme from the dropdown below.
- Go to **Code** tab to copy the code and paste it in your `README.md` file.
- **Github extensions will not work in the preview.** You can only see them in the code and in your Github profile.
"""

# Select Theme
themes = Path("src/themes").iterdir()
themes = [theme.name for theme in themes]
theme = st.selectbox("Theme:", themes)

# Generate Profile
profile = generate_profile(theme, **kwargs)
tab1, tab2 = st.tabs(["Preview", "Code"])
tab1.markdown(profile)

with tab2:
    "Copy the code below and paste it in your README.md file"
    st.code(profile)

st.write(
    '<h4>&#128161; Built by <a href="https://pytopia.ai" target="_blank">Pytopia</a> team.</h4>',
    unsafe_allow_html=True,
)
st.write("---")
