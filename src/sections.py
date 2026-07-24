import urllib.parse

import streamlit as st
from streamlit_tags import st_tags

from src.constants import POPULAR_TECH_STACKS, default_description, skills, tech_stacks


def add_personal_info(tab, **kwargs):
    """
    Add personal info to tab.

    :param tab: Streamlit tab
    """
    with tab:
        col1, col2 = st.columns(2)
        kwargs['name'] = col1.text_input('Name', 'Ali Hejazizo')
        kwargs['email'] = col2.text_input('Email', 'hejazizo@ualberta.ca')

    return kwargs


def add_social_accounts(tab, **kwargs):
    """
    Add social accounts to tab.

    :param tab: Streamlit tab
    """
    with tab:
        col1, col2 = st.columns(2)
        kwargs['homepage'] = col1.text_input('Homepage', 'https://pytopia.ai')
        kwargs['linkedin'] = col2.text_input('Linkedin', 'hejazizo')
        kwargs['twitter'] = col1.text_input('Twitter', 'hejazizo')
        kwargs['instagram'] = col2.text_input('Instagram', 'ali.hejazzii')

    return kwargs

def add_description(tab, **kwargs):
    """
    Add description to tab.

    :param tab: Streamlit tab
    """
    with tab:
        st.write('''Write a short description about yourself.''')
        kwargs['description'] = st.text_area('Description', default_description, height=300)

    return kwargs

def add_extensions(tab, **kwargs):
    """
    Add extensions to tab.

    :param tab: Streamlit tab
    """
    with tab:
        st.write('''Add more to your profile. You can add Github stats, Github profile views, and more.''')
        kwargs['github'] = st.text_input('Github', 'hejazizo')
        if not kwargs['github']:
            st.warning('For extensions, you must enter your Github username.')
            kwargs['profile_views'] = None
            kwargs['github_stats'] = None
            return kwargs

        kwargs['github_stats'] = None
        if st.checkbox('Show Github Stats', value=True):
            kwargs['github_stats'] = kwargs['github']

        kwargs['profile_views'] = None
        if st.checkbox('Show Github Profile Views', value=True):
            kwargs['profile_views'] = kwargs['github']

    return kwargs


def add_tech_stack(tab, **kwargs):
    """
    Add tech stacks to tab.

    :param tab: Streamlit tab
    """
    BADGE_TEMPLATE = '![Bootstrap](https://img.shields.io/badge/-{badge}-05122A?style={style}&logo={logo}&color={color})'
    with tab:
        st.write("Add your tech stacks. You can add any tech stack and skills you want.")

        # Badge style and color
        col1, col2 = st.columns(2)
        style = col1.selectbox('Style', ['flat-square', 'flat', 'plastic', 'for-the-badge', 'social'], key='stack_style')
        color = col2.color_picker('Color', '#353535', key='stack_color')
        color = color.lstrip('#')

        st.divider()

        selected_techs = st_tags(
            label='Tech Stacks:',
            text='Write and Press Enter to Apply',
            value=tech_stacks,
            suggestions=POPULAR_TECH_STACKS,
            maxtags=112,
            key='tech_tags'
        )

        # By this chatbot will recieve clean text from tech stacks
        st.session_state['raw_tech_list'] = ", ".join(selected_techs)

        # Logos and badges
        logos = ['-'.join(tech_stack.split()) for tech_stack in selected_techs]
        badges = [urllib.parse.quote(tech_stack) for tech_stack in selected_techs]

        # Format the final url
        badge_pairs = zip(badges, logos)
        kwargs['tech_stacks'] = ' '.join(
            BADGE_TEMPLATE.format(badge=badge, logo=logo, style=style, color=color)
            for badge, logo in badge_pairs
        )

    return kwargs


def add_skills(tab, **kwargs):
    with tab:
        st.write('''Add your skills. You can add any skills you want.
        **Just make sure to separate them with a new line.**
        ''')
        col1, col2 = st.columns(2)
        kwargs['skills'] = col1.text_area('Skills:', skills, height=300, key='skills')
        kwargs['skills'] = kwargs['skills'].split('\n')
        kwargs['skills'] = filter(lambda x: x, kwargs['skills'])
        kwargs['skills'] = [f'- {skill}' for skill in kwargs['skills']]
        kwargs['skills'] = '\n'.join(kwargs['skills'])

    return kwargs
