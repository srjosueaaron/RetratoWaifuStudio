import gradio as gr
from data_image_guide import hair, texture, eyes_styles, helmets, hats, COLUMNS

def render_list(lst, title):
    gr.Markdown(
        f"""
        <h1 style="text-align: center; color: #4F46E5;">🔶 {title}</h1>
        """
    )
    for i in range(0, len(lst), COLUMNS):
        with gr.Row(equal_height=True):
            for item in lst[i:i+COLUMNS]:
                with gr.Column(scale=1, min_width=150):
                    gr.Image(item['image'], height=200, width=200)
                    gr.Markdown(
                        f"""
                        <h3 style="text-align: center;">{item['name']}</h3>
                        """
                    )

def create_guide_tab():
    with gr.Blocks(theme=gr.themes.Soft()) as guide_tab:
        render_list(hair, "CORTES DE CABELLO 👩")

        render_list(texture, "TEXTURA DEL CABELLO 🧒")

        render_list(eyes_styles, "ESTILOS DE LOS OJOS 👀")
    
        render_list(helmets, "CASCOS VARIADOS 🎩")
        
        render_list(hats, "SOMBREROS VARIADOS 👒")
        
    return guide_tab