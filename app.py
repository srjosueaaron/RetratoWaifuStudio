import gradio as gr
from model import get_device, load_model
from utils import build_prompt, generate_image
from translations import TRANSLATIONS

device = get_device()
pipe = load_model(device)

def create_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 2.5em; color: #4F46E5; font-weight: bold;">🎨Retrato WaifuStudio</h1>
            <h3 style="color: #6B7280;">Genera fotos de perfil estilo anime totalmente personalizables</h3>
            <p style="font-size: 0.9em; color: #9CA3AF; margin-top: 20px;">Si disfrutas de esta herramienta y deseas apoyar su desarrollo continuo, considera realizar una donación sin restricciones para contribuir a futuras mejoras, incluyendo la posibilidad de generar contenido sin limitaciones, tanto creativo como explícito.</p>
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

        gr.HTML("""
        <footer style="text-align: center; margin-top: 50px; padding: 20px; background-color: #f9fafb; border-top: 1px solid #e5e7eb; font-size: 0.9em; color: #6b7280;">
            <p>© 2024 WaifuCreator. Usando el modelo Waifu Diffusion de <a href="https://huggingface.co/hakurei/waifu-diffusion" style="font-size: 1em; color: #4F46E5; text-decoration: underline;">Hakurei</a></p>
            <p>Desarrollado con ❤️ por <a href="https://www.linkedin.com/in/srjosueaaron" style="font-size: 1em; color: #4F46E5; text-decoration: underline;">@srjosueaaron</a></p>
        </footer>
        """)
    return demo

# Lanzar la interfaz
demo = create_interface()
demo.launch(debug=True)