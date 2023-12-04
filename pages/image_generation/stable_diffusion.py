import streamlit as st

import utils
from src.generative_ai.image_generation import stable_diffusion_image

loader = utils.PageConfigLoader(__file__)
loader.set_page_config(globals())

logger = utils.CustomLogger(__file__)


def main():
    st.caption(
        body="Using Stability AI's Stable Diffusion model, this app performs image creation based on a user prompt.",
        help="[Stable Diffusion](https://stability.ai/stable-diffusion)",
        unsafe_allow_html=True,
    )

    utils.show_source_code(path="src/generative_ai/image_generation/dall_e.py")

    submitted = False
    with st.form(key="stable_diffusion_form"):
        prompt = st.text_input(label="Input prompt: ")
        centered = st.columns(3)[1]
        with centered:
            submitted = st.form_submit_button(
                label="Generate with Stable Diffusion", use_container_width=True
            )
    st.subheader(body="Output", anchor=False)
    if submitted:
        image = stable_diffusion_image(prompt=prompt)
        st.image(image=image, caption="{prompt} - Generated by Stable Diffusion")
