import gradio as gr
import requests

def ask_api(question:str):
    if not question or not question.strip():
        return "输入不能为空，请先输入问题。",""
    try:
        response = requests.post("http://127.0.0.1:8000/ask",json={"q":question})
        data = response.json()
        return data["a"],"\n".join(data["retrieved"])
    except Exception:
        return "后端服务未处于运行状态，请先运行。",""

with gr.Blocks(title="d2l知识库问答") as demo:
    gr.Markdown("<h1 style='text-align: center;'>d2l 知识库问答</h1>")
    gr.Markdown("每次请只输入一个与《Dive into Deep Learning（动手学深度学习）》相关的问题")
    with gr.Row():
        answer = gr.Textbox(label="回答",lines=12,scale=2)
        retrieved = gr.Textbox(label="检索候选",lines=12,scale=1)
    with gr.Row():
        question = gr.Textbox(label="输入框",scale=4)
        ask = gr.Button("提问",scale=1).click(fn=ask_api,inputs=question,outputs=[answer,retrieved])
        question.submit(fn=ask_api,inputs=question,outputs=[answer,retrieved])

demo.launch()