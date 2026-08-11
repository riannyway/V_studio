
import base64
import os
from pathlib import Path

# ---------------------------------------------------------
# Local proxy
# ---------------------------------------------------------
LOCAL_NO_PROXY = "localhost,127.0.0.1,0.0.0.0"
os.environ["NO_PROXY"] = ",".join(
    x for x in (os.environ.get("NO_PROXY", ""), LOCAL_NO_PROXY) if x
)
os.environ["no_proxy"] = ",".join(
    x for x in (os.environ.get("no_proxy", ""), LOCAL_NO_PROXY) if x
)

# ---------------------------------------------------------
# HEIC / HEIF
# ---------------------------------------------------------
from pillow_heif import register_heif_opener
register_heif_opener(thumbnails=False)

import gradio as gr

# 保留你当前已经跑通的业务逻辑
from agent import VStudioAgent
from config import get_settings, SIZE_OPTIONS


BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
SETTINGS = get_settings()
agent = VStudioAgent()


def image_data_uri(path: Path) -> str:
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "image/png")

    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


LOGO_URI = image_data_uri(ASSET_DIR / "vstudio_logo.png")
WORDMARK_URI = image_data_uri(ASSET_DIR / "vstudio_wordmark.png")


CSS = r"""
:root {
    --page: #f3f5f8;
    --surface: rgba(255, 255, 255, 0.96);
    --surface-2: #f8fafc;
    --border: #e3e7ee;
    --border-strong: #d5dbe5;
    --text: #0b132b;
    --muted: #8490a3;
    --navy: #071f52;
    --blue: #3378f6;
    --cyan: #37c9e9;
    --mint: #42e0bd;
    --black: #111318;
    --shadow: 0 28px 80px rgba(20, 35, 65, 0.10);
    --shadow-soft: 0 12px 36px rgba(20, 35, 65, 0.065);
}

/* ---------- global ---------- */
html, body {
    background: var(--page) !important;
}

.gradio-container {
    min-height: 100vh !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background:
        radial-gradient(circle at 12% 10%, rgba(55, 201, 233, .08), transparent 28%),
        radial-gradient(circle at 89% 14%, rgba(51, 120, 246, .07), transparent 30%),
        var(--page) !important;
    font-family:
        Inter, -apple-system, BlinkMacSystemFont, "SF Pro Display",
        "PingFang SC", "Microsoft YaHei", sans-serif !important;
    color: var(--text) !important;
}

footer {
    display: none !important;
}

button, input, textarea {
    font-family: inherit !important;
}

/* ---------- page wrapper ---------- */
#app-shell {
    width: 100%;
    max-width: 1580px;
    margin: 0 auto;
    padding: 28px 34px 34px;
}

/* ==================== HOME ==================== */

#home-page {
    min-height: calc(100vh - 62px);
    justify-content: center !important;
}

#home-card {
    position: relative;
    min-height: 760px;
    padding: 84px 58px 46px !important;
    box-sizing: border-box;
    align-items: center !important;
    border: 1px solid rgba(255,255,255,.85) !important;
    border-radius: 38px !important;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% -8%, rgba(50, 119, 246, .075), transparent 42%),
        radial-gradient(circle at 50% 110%, rgba(66, 224, 189, .055), transparent 38%),
        var(--surface) !important;
    box-shadow: var(--shadow) !important;
}

#home-card::before {
    content: "";
    position: absolute;
    width: 480px;
    height: 480px;
    border-radius: 999px;
    top: -330px;
    left: -120px;
    background: rgba(66, 224, 189, .07);
    filter: blur(2px);
    pointer-events: none;
}

#home-card::after {
    content: "";
    position: absolute;
    width: 540px;
    height: 540px;
    border-radius: 999px;
    right: -350px;
    bottom: -350px;
    background: rgba(51, 120, 246, .075);
    pointer-events: none;
}


.wordmark {
    width: min(680px, 72vw);
    height: auto;
    object-fit: contain;
    display: block;
    margin: 2px auto 50px;
}

.home-hero {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.home-copy {
    text-align: center;
}

.home-cn {
    margin: 0;
    font-size: clamp(34px, 3.3vw, 56px);
    line-height: 1.14;
    letter-spacing: -.03em;
    font-weight: 650;
    background: linear-gradient(
        90deg,
        #39dcb7 0%,
        #33cbd4 31%,
        #35a7ed 61%,
        #356bf3 100%
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.home-en {
    margin: 17px 0 0;
    font-size: clamp(20px, 2vw, 32px);
    color: #3269e9;
    letter-spacing: -.02em;
    font-weight: 480;
}

#design-btn {
    width: 150px;
    margin: 30px auto 0 !important;
}

#design-btn button {
    min-height: 52px !important;
    width: 100% !important;
    padding: 0 25px !important;
    border: 1px solid #0d0f13 !important;
    border-radius: 14px !important;
    background: var(--black) !important;
    color: #fff !important;
    font-size: 16px !important;
    font-weight: 650 !important;
    letter-spacing: .02em;
    box-shadow: 0 12px 25px rgba(10, 13, 18, .16) !important;
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease !important;
}

#design-btn button:hover {
    transform: translateY(-2px);
    background: #1b1e24 !important;
    box-shadow: 0 16px 32px rgba(10, 13, 18, .21) !important;
}

.home-footer {
    margin-top: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 7px;
}

.home-footer-logo {
    width: 122px;
    height: 96px;
    object-fit: contain;
}

.home-footer-copy {
    margin: 0;
    color: #9aa5b7;
    font-size: 13px;
    letter-spacing: .035em;
}

/* ==================== STUDIO ==================== */

#studio-page {
    min-height: calc(100vh - 62px);
}

#studio-header {
    margin-bottom: 17px !important;
    align-items: center !important;
}

#back-btn {
    width: 106px !important;
    min-width: 106px !important;
}

#back-btn button {
    min-height: 44px !important;
    width: 100% !important;
    border-radius: 12px !important;
    border: 1px solid var(--black) !important;
    background: var(--black) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 630 !important;
    box-shadow: 0 8px 20px rgba(10, 13, 18, .12) !important;
    transition: all .18s ease !important;
}

#back-btn button:hover {
    transform: translateY(-1px);
    background: #1b1e24 !important;
}

.studio-brand {
    margin-left: auto;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-height: 44px;
}

.studio-brand img {
    height: 33px;
    width: auto;
    display: block;
}

#workspace {
    gap: 20px !important;
    align-items: stretch !important;
}

/* panels */
.workspace-panel {
    border: 1px solid rgba(226, 231, 239, .94) !important;
    border-radius: 26px !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow-soft) !important;
    padding: 22px !important;
}

#editor-panel {
    gap: 15px !important;
}

#preview-panel {
    position: relative;
    min-height: 742px;
}

/* micro header */
.panel-kicker {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 25px;
    margin-bottom: 4px;
}

.panel-title {
    color: var(--text);
    font-size: 13px;
    font-weight: 720;
    letter-spacing: .075em;
    text-transform: uppercase;
}

.panel-meta {
    color: var(--muted);
    font-size: 12px;
}

/* upload */
#upload-box {
    border-radius: 20px !important;
    overflow: hidden !important;
}

#upload-box > .wrap,
#upload-box .image-container,
#upload-box .image-frame,
#upload-box .upload-box {
    border-radius: 20px !important;
}

#upload-box .upload-box {
    min-height: 286px !important;
    border: 1.5px dashed #cfd6e2 !important;
    background:
        linear-gradient(180deg, #fbfcfe 0%, #f7f9fc 100%) !important;
}

#upload-box .upload-box:hover {
    border-color: #9fb6df !important;
    background: #f8fbff !important;
}

/* prompt */
#prompt-box {
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    overflow: hidden;
    background: #fbfcfe !important;
}

#prompt-box .wrap {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

#prompt-box textarea {
    min-height: 112px !important;
    padding: 17px 18px !important;
    border: none !important;
    background: transparent !important;
    color: var(--text) !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
    box-shadow: none !important;
}

#prompt-box textarea::placeholder {
    color: #a2abba !important;
}

/* controls */
.control-row {
    gap: 12px !important;
}

.control-field {
    gap: 7px !important;
}

.control-name {
    margin: 0 0 0 2px;
    color: #687386;
    font-size: 12px;
    font-weight: 670;
    letter-spacing: .025em;
}

.control-field .wrap {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #fff !important;
    min-height: 49px !important;
    box-shadow: none !important;
}

.control-field input {
    color: var(--text) !important;
}

/* generate */
#generate-btn {
    margin-top: 4px !important;
}

#generate-btn button {
    min-height: 56px !important;
    width: 100% !important;
    border: 1px solid var(--black) !important;
    border-radius: 15px !important;
    background: var(--black) !important;
    color: #fff !important;
    font-size: 16px !important;
    font-weight: 680 !important;
    letter-spacing: .02em;
    box-shadow: 0 13px 28px rgba(10, 13, 18, .14) !important;
    transition: all .18s ease !important;
}

#generate-btn button:hover {
    transform: translateY(-1px);
    background: #1b1e24 !important;
    box-shadow: 0 17px 32px rgba(10, 13, 18, .19) !important;
}

/* preview */
.preview-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 2px 15px;
}

.preview-title {
    font-size: 13px;
    font-weight: 720;
    letter-spacing: .075em;
    text-transform: uppercase;
    color: var(--text);
}

.preview-status {
    display: flex;
    gap: 7px;
    align-items: center;
    color: #8b96a8;
    font-size: 12px;
}

.preview-status::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 99px;
    background: #58d8bc;
    box-shadow: 0 0 0 4px rgba(88, 216, 188, .11);
}

#result-box {
    flex: 1;
    border-radius: 20px !important;
    overflow: hidden !important;
}

#result-box > .wrap,
#result-box .image-container,
#result-box .image-frame,
#result-box .upload-box {
    border-radius: 20px !important;
}

#result-box .image-frame,
#result-box .upload-box {
    min-height: 625px !important;
    border: 1px solid var(--border) !important;
    background:
        radial-gradient(circle at 50% 42%, #f8fafc 0%, #eff2f6 100%) !important;
}

/* download */
#download-file {
    margin-top: 15px !important;
}

#download-file .wrap {
    min-height: 50px !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #fafbfd !important;
    box-shadow: none !important;
}

#download-file label {
    color: #566276 !important;
    font-size: 13px !important;
    font-weight: 620 !important;
}

#error-box {
    margin: 4px 2px 0 !important;
}

#error-box p,
#error-box .prose {
    color: #bd3346 !important;
    font-size: 13px !important;
}

/* ---------- responsive ---------- */
@media (max-width: 980px) {
    #app-shell {
        padding: 18px;
    }

    #home-card {
        min-height: calc(100vh - 36px);
        padding: 70px 24px 30px !important;
    }

    .wordmark {
        width: min(620px, 87vw);
        margin-bottom: 38px;
    }

    #workspace {
        flex-direction: column !important;
    }

    #preview-panel {
        min-height: auto;
    }

    #result-box .image-frame,
    #result-box .upload-box {
        min-height: 520px !important;
    }
}

@media (max-width: 640px) {
    #app-shell {
        padding: 11px;
    }

    #home-card {
        border-radius: 24px !important;
    }

    #home-card {
        padding-top: 74px !important;
    }

    .home-cn {
        font-size: 31px;
    }

    .home-en {
        font-size: 18px;
    }

    .home-footer-logo {
        width: 96px;
    }

    .workspace-panel {
        padding: 15px !important;
        border-radius: 20px !important;
    }

    .studio-brand img {
        height: 26px;
    }
}
"""


HOME_HERO_HTML = f"""
<div class="home-hero">
    <img class="wordmark" src="{WORDMARK_URI}" alt="V Studio">
    <div class="home-copy">
        <h1 class="home-cn">当你有想法时，我们早已在路上</h1>
        <p class="home-en">When you have an idea, we have already been on way.</p>
    </div>
</div>
"""

HOME_FOOTER_HTML = f"""
<div class="home-footer">
    <img class="home-footer-logo" src="{LOGO_URI}" alt="v-studio">
    <p class="home-footer-copy">copyright @v studio</p>
</div>
"""


STUDIO_BRAND_HTML = f"""
<div class="studio-brand">
    <img src="{WORDMARK_URI}" alt="V Studio">
</div>
"""


def show_studio():
    return gr.update(visible=False), gr.update(visible=True)


def show_home():
    return gr.update(visible=True), gr.update(visible=False)


def update_file_count(image):
    return "1 / 1" if image is not None else "0 / 1"


def run_generate(reference_image, prompt, style, temperature, size):
    try:
        result_image, file_path = agent.generate(
            prompt=prompt,
            reference_image=reference_image,
            style=style,
            size=size,
            temperature=temperature,
        )

        return result_image, file_path, ""

    except Exception as exc:
        return None, None, f"生成失败：{exc}"


with gr.Blocks(
    css=CSS,
    title="V Studio",
    theme=gr.themes.Base(),
) as demo:

    with gr.Column(elem_id="app-shell"):

        # =====================================================
        # HOME
        # =====================================================
        with gr.Column(visible=True, elem_id="home-page") as home_page:
            with gr.Column(elem_id="home-card"):
                gr.HTML(HOME_HERO_HTML)

                design_btn = gr.Button(
                    "Design  →",
                    elem_id="design-btn",
                )

                gr.HTML(HOME_FOOTER_HTML)

        # =====================================================
        # STUDIO
        # =====================================================
        with gr.Column(visible=False, elem_id="studio-page") as studio_page:

            with gr.Row(elem_id="studio-header"):
                back_btn = gr.Button(
                    "←  返回",
                    elem_id="back-btn",
                )

                gr.HTML(
                    STUDIO_BRAND_HTML,
                    min_width=180,
                )

            with gr.Row(elem_id="workspace"):

                # ----------------- LEFT -----------------
                with gr.Column(
                    scale=9,
                    elem_classes=["workspace-panel"],
                    elem_id="editor-panel",
                ):

                    gr.HTML(
                        """
                        <div class="panel-kicker">
                            <span class="panel-title">Reference</span>
                            <span class="panel-meta">Image input</span>
                        </div>
                        """
                    )

                    reference_image = gr.Image(
                        type="pil",
                        sources=["upload"],
                        show_label=False,
                        height=286,
                        elem_id="upload-box",
                    )

                    with gr.Row():
                        gr.HTML(
                            '<div class="control-name">文件数量</div>'
                        )
                        file_count = gr.Markdown(
                            "0 / 1",
                            container=False,
                        )

                    gr.HTML(
                        """
                        <div class="panel-kicker" style="margin-top:4px">
                            <span class="panel-title">Prompt</span>
                            <span class="panel-meta">0 / 100</span>
                        </div>
                        """
                    )

                    prompt = gr.Textbox(
                        show_label=False,
                        placeholder="每当你有想法，我们早已在路上~",
                        lines=4,
                        max_lines=6,
                        elem_id="prompt-box",
                    )

                    with gr.Row(elem_classes=["control-row"]):

                        with gr.Column(
                            scale=1,
                            elem_classes=["control-field"],
                        ):
                            gr.HTML(
                                '<p class="control-name">Size</p>'
                                )
                            style = gr.Dropdown(
                                choices=[
                                    "默认",
                                    "电影感",
                                    "清新",
                                    "科技感",
                                    "海报感",
                                ],
                                value="默认",
                                show_label=False,
                            )

                        with gr.Column(
                            scale=1,
                            elem_classes=["control-field"],
                        ):
                            gr.HTML(
                                '<p class="control-name">Temperature</p>'
                            )
                            temperature = gr.Number(
                                value=5,
                                minimum=0,
                                maximum=10,
                                precision=0,
                                show_label=False,
                            )

                    with gr.Row(elem_classes=["control-row"]):

                        with gr.Column(
                            scale=1,
                            elem_classes=["control-field"],
                        ):
                            gr.HTML(
                                '<p class="control-name">Aspect Ratio</p>'
                            )
                            size = gr.Dropdown(
                                choices=SIZE_OPTIONS,
                                value="1:1",
                                show_label=False,
                            )

                        with gr.Column(scale=1):
                            # 仅用于保持视觉平衡
                            gr.HTML("")

                    generate_btn = gr.Button(
                        "生成",
                        elem_id="generate-btn",
                    )

                    error_box = gr.Markdown(
                        "",
                        elem_id="error-box",
                    )

                # ----------------- RIGHT -----------------
                with gr.Column(
                    scale=11,
                    elem_classes=["workspace-panel"],
                    elem_id="preview-panel",
                ):

                    gr.HTML(
                        """
                        <div class="preview-head">
                            <span class="preview-title">Preview</span>
                            <span class="preview-status">Ready</span>
                        </div>
                        """
                    )

                    result_image = gr.Image(
                        type="pil",
                        show_label=False,
                        interactive=False,
                        height=625,
                        elem_id="result-box",
                    )

                    download_file = gr.File(
                        label="Download",
                        interactive=False,
                        elem_id="download-file",
                    )

    # =========================================================
    # EVENTS
    # =========================================================
    design_btn.click(
        fn=show_studio,
        inputs=None,
        outputs=[home_page, studio_page],
    )

    back_btn.click(
        fn=show_home,
        inputs=None,
        outputs=[home_page, studio_page],
    )

    reference_image.change(
        fn=update_file_count,
        inputs=[reference_image],
        outputs=[file_count],
    )

    generate_btn.click(
        fn=run_generate,
        inputs=[
            reference_image,
            prompt,
            style,
            temperature,
            size,
        ],
        outputs=[
            result_image,
            download_file,
            error_box,
        ],
    )


if __name__ == "__main__":
    demo.launch(
        server_name=SETTINGS["app_host"],
        server_port=SETTINGS["app_port"],
        share=False,
    )
