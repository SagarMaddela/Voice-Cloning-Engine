"""

Gradio User Interface for Voice Cloning Engine.



This module creates the Gradio web interface for the voice cloning application,

including tabs for speech generation and voice cloning.

"""

import gradio as gr

from config import (

    SPEED_MIN,

    SPEED_MAX,

    SPEED_DEFAULT,

    SPEED_STEP

)




def create_header():
    """
    Create a clean, product-style hero header.
    """
    return """
    <div style="
        width: 100%;
        max-width: 1200px;
        margin: 0 auto 2rem auto;
        padding: 2.5rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        flex-wrap: wrap;
    ">
        <div style="flex: 1; min-width: 260px;">
            <h1 style="
                font-size: 2.8rem;
                margin: 0;
                font-weight: 700;
                letter-spacing: -0.02em;
            ">
                NeuTTS Voice Engine
            </h1>
            <p style="
                margin-top: 0.75rem;
                font-size: 1.1rem;
                color: #cbd5f5;
                max-width: 520px;
                line-height: 1.6;
            ">
                High-fidelity speech synthesis and instant voice cloning.
                Generate natural voices or create your own in seconds.
            </p>
        </div>

        <div style="
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            align-items: flex-end;
            min-width: 220px;
        ">


            <a href="https://github.com/SagarMaddela/Voice-Cloning-Engine.git" target="_blank"
               style="
                    text-decoration: none;
                    color: #0f172a;
                    background: #e2e8f0;
                    padding: 0.7rem 1.2rem;
                    border-radius: 10px;
                    font-weight: 600;
                    font-size: 0.95rem;
                    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
               ">
                View Project
            </a>
        </div>
    </div>
    """


def create_generation_tab(voice_manager, speech_generator):

    """

    Create the speech generation tab.

   

    Args:

        voice_manager: VoiceManager instance

        speech_generator: SpeechGenerator instance

       

    Returns:

        tuple: Gradio components for the generation tab

    """

    with gr.Row():

        with gr.Column():

            text_input = gr.Textbox(label="Input Text", lines=4)

            with gr.Row():

                voice_select = gr.Dropdown(

                    label="Select Voice",

                    choices=voice_manager.get_voice_list(),

                    value=voice_manager.get_voice_list()[0] if voice_manager.get_voice_list() else None

                )

                delete_btn = gr.Button("🗑️ Delete Voice", variant="secondary", size="sm")

            speed_slider = gr.Slider(

                label="Speed",

                minimum=SPEED_MIN,

                maximum=SPEED_MAX,

                value=SPEED_DEFAULT,

                step=SPEED_STEP

            )

            generate_btn = gr.Button("🎙️ Generate Speech", variant="primary")

       

        with gr.Column():

            progress_bar = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)

            status_box = gr.Textbox(label="Generation Status", value="", lines=3, interactive=False)

            delete_status = gr.Textbox(label="Status", visible=False)

            audio_output = gr.Audio(label="Output", autoplay=True)

   

    # Event handlers

    generate_btn.click(

        fn=speech_generator.generate_speech,

        inputs=[text_input, voice_select, speed_slider],

        outputs=[progress_bar, audio_output, status_box, delete_status]

    )

   

    delete_btn.click(

        fn=voice_manager.delete_voice,

        inputs=[voice_select],

        outputs=[delete_status, voice_select]

    )

   

    return voice_select





def create_cloning_tab(voice_manager, voice_select):

    """

    Create the voice cloning tab.

   

    Args:

        voice_manager: VoiceManager instance

        voice_select: Voice dropdown component from generation tab

       

    Returns:

        None

    """

    with gr.Row():

        with gr.Column():

            new_voice_name = gr.Textbox(label="New Voice Name")

            ref_text_input = gr.Textbox(label="Reference Text (same text spoken in sample)", lines=3)

            ref_audio_input = gr.Audio(label="Reference Audio (.wav)", type="filepath")

            clone_btn = gr.Button("🧬 Clone Voice", variant="primary")

       

        with gr.Column():

            clone_status = gr.Textbox(label="Status")

   

    # Event handler

    clone_btn.click(

        fn=voice_manager.clone_voice,

        inputs=[new_voice_name, ref_text_input, ref_audio_input],

        outputs=[clone_status, voice_select]

    )





def create_interface(voice_manager, speech_generator):

    """

    Create the complete Gradio interface.

   

    Args:

        voice_manager: VoiceManager instance

        speech_generator: SpeechGenerator instance

       

    Returns:

        gr.Blocks: Gradio Blocks interface

    """

    with gr.Blocks(title="NeuTTS Voice Cloning", theme=gr.themes.Soft()) as app:

        gr.HTML(create_header())

       

        with gr.Tab("Generate Speech"):

            voice_select = create_generation_tab(voice_manager, speech_generator)

       

        with gr.Tab("Instantly Clone New Voice"):

            create_cloning_tab(voice_manager, voice_select)

   

    return app

