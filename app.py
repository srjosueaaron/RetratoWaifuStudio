import gradio as gr
from model import get_device, load_model
from utils import build_prompt, generate_image
from translations import TRANSLATIONS
from image_guide import create_guide_tab

device = get_device()
pipe = load_model(device)

def create_main_tab():
    with gr.Blocks(theme=gr.themes.Soft()) as main_tab:
        gr.Markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 2.5em; color: #4F46E5; font-weight: bold;">🎨Retrato WaifuStudio</h1>
            <h3 style="color: #6B7280;">Genera fotos de perfil estilo anime totalmente personalizables</h3>
            <p style="font-size: 0.9em; color: #9CA3AF; margin-top: 20px;">Si disfrutas de esta herramienta y deseas apoyar su desarrollo continuo, considera realizar una donación para contribuir a futuras mejoras, incluyendo la posibilidad de generar contenido sin limitaciones, tanto creativo como explícito.</p>
            <a href="https://paypal.me/srjosuearon?country.x=MX&locale.x=es_XC" style="font-size: 1em; color: #4F46E5; text-decoration: underline;">Apoya con una donación</a>            
        </div>
        """)
        
        user_inputs = {}

        with gr.Row():
            with gr.Column():
                for category, options in TRANSLATIONS.items():
                    with gr.Accordion(category, open=False):
                        user_inputs[category] = gr.CheckboxGroup(
                            options, label=category
                        )

            with gr.Column():
                with gr.Row():
                    clear_button = gr.Button("🧹 Limpiar texto")
                    generate_button = gr.Button("🚀 Generar Imagen")

                prompt_output = gr.Textbox(label="📝 Características de la imagen", interactive=True)
                image_output = gr.Image(label="📥 Imagen generada")
                
                gr.Markdown("""
                ```bash
                Proximamente ejemplos completos 😎
                """)
        def update_prompt(*args):
            kwargs = {key: value for key, value in zip(TRANSLATIONS.keys(), args)}
            return build_prompt(**kwargs)

        def on_generate_image(*args):
            kwargs = {key: value for key, value in zip(TRANSLATIONS.keys(), args)}
            prompt = build_prompt(**kwargs)
            image = generate_image(prompt, pipe, device)
            return prompt, image

        def clear_fields():
            return ([],) * len(TRANSLATIONS) + ("",)

        for input_component in user_inputs.values():
            input_component.change(
                fn=update_prompt,
                inputs=list(user_inputs.values()),
                outputs=prompt_output
            )

        clear_button.click(
            fn=clear_fields,
            inputs=[],
            outputs=list(user_inputs.values()) + [prompt_output]
        )

        generate_button.click(
            fn=on_generate_image,
            inputs=list(user_inputs.values()),
            outputs=[prompt_output, image_output]
        )

        gr.HTML("""
            <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
                <button onclick="window.scrollTo({ top: 0, behavior: 'smooth' });"
                style="background-color: #4CAF50; color: white; border: none; padding: 10px 20px;
                border-radius: 5px; cursor: pointer; font-size: 14px;">
                    ⬆ Volver al Inicio
                </button>
            </div>
        """)
        
        gr.Markdown(""" 
        ---
        
        © 2024 Retrato WaifuStudio. Usando el modelo Waifu Diffusion de [Hakurei](https://huggingface.co/hakurei/waifu-diffusion).
        
        Desarrollado con ❤️ por [@srjosueaaron](https://www.instagram.com/srjosueaaron/).
        """)

    return main_tab

def create_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        with gr.Tabs():
            with gr.Tab("Retrato WaifuStudio"):
                create_main_tab()

            with gr.Tab("Guía para generar"):
                create_guide_tab()
    return demo

demo = create_interface()
demo.launch(debug=True, share=True)