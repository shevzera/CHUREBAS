import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import time

st.set_page_config(page_title="TikTok Script Generator", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .stCodeBlock {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 TikTok Script Generator")
st.markdown("**Gere roteiros virais em inglês + Image Prompts + Descrição + Hashtags + Imagens com IA**")

with st.sidebar:
    st.header("⚙️ Configuração")
    
    st.markdown("### 📏 Especificações")
    st.info("✅ Script: 1300-1500 caracteres\n\n✅ Estilo: Viral\n\n✅ Público: Americano\n\n✅ Duração: ~60 segundos")
    
    st.markdown("---")
    st.markdown("### 🎨 Geração de Imagens")
    gerar_imagens = st.checkbox("Gerar imagens automaticamente", value=True)
    if gerar_imagens:
        st.info("🎨 Imagens com **Flux 1.1 Pro** (qualidade profissional)")

col1, col2 = st.columns([1, 1])

with col1:
    tema = st.text_area("📝 Tema (em português)", placeholder="Ex: A história sombria por trás do McDonald's", height=100)

with col2:
    roteiro_exemplo = st.text_area("📄 Roteiro Pronto (opcional)", placeholder="Se já tem um roteiro em português, cole aqui.", height=100)

if st.button("🚀 Gerar Conteúdo Completo", type="primary", use_container_width=True):
    
    if not tema and not roteiro_exemplo:
        st.error("⚠️ Insira um tema OU um roteiro pronto!")
        st.stop()
    
    try:
        api_key = "AIzaSyDdhBQhmX_IXPH1vrIQA0hu4pyXhw9eSR4"
        genai.configure(api_key=api_key)
        model_text = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        base_content = roteiro_exemplo if roteiro_exemplo else tema
        content_type = "ROTEIRO ORIGINAL (português)" if roteiro_exemplo else "TEMA (português)"
        
        prompt = f"""Você é um especialista em criar conteúdo VIRAL para TikTok voltado para o público AMERICANO.

{content_type}: {base_content}

REGRAS IMPORTANTES:
- O SCRIPT deve ter entre 1300-1500 caracteres
- NO SCRIPT: NÃO incluir marcações de segundos, APENAS [PAUSE], [EMPHASIS], [BREATH]
- Seja criativo e detalhado para atingir o tamanho ideal

ENTREGUE EXATAMENTE NO FORMATO (com os delimitadores |||):

SCRIPT|||
[Script completo em inglês formatado para ElevenLabs APENAS com [PAUSE], [EMPHASIS], [BREATH]. SEM [0-3s]. 1300-1500 caracteres. Estilo viral com gancho forte nos primeiros 3 segundos. Linguagem simples para público americano.]

PROMPTS|||
0-3s: [descrição ULTRA detalhada para geração de imagem: composição específica, lighting detalhado, camera angle preciso, mood, cores, texturas, movimento]. Cinematic, hyper-realistic, 4K quality, professional color grading.
3-7s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
7-12s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
12-17s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
17-22s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
22-27s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
27-32s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
32-37s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
37-42s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
42-47s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.
47-52s: [descrição ultra detalhada completa]. Cinematic, hyper-realistic, 4K quality.

DESCRIPTION|||
[Descrição engajante de 150-200 caracteres com call-to-action americano forte]

[8-10 hashtags trending nos EUA incluindo #fyp #viral e específicos do tema]
"""
        
        with st.spinner("🤖 Gerando roteiro e prompts..."):
            response = model_text.generate_content(prompt)
            resultado = response.text
        
        partes = resultado.split("|||")
        
        if len(partes) < 4:
            st.error(f"❌ Erro no formato. Tentando novamente...")
            st.rerun()
        
        script_text = partes[1].strip()
        prompts_text = partes[2].strip()
        description_text = partes[3].strip()
        
        script_text = script_text.replace("PROMPTS", "").replace("PROMPT", "").strip()
        
        char_count = len(script_text)
        
        if char_count < 1200:
            st.warning(f"⚠️ Script muito curto ({char_count} caracteres). Gerando novamente...")
            st.rerun()
        elif char_count > 1600:
            script_text = script_text[:1550].rsplit('.', 1)[0] + '.'
            char_count = len(script_text)
        
        st.success("✅ Conteúdo gerado com sucesso!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Caracteres", f"{char_count}")
        with col2:
            st.metric("⏱️ Duração", "~60s")
        with col3:
            if 1300 <= char_count <= 1500:
                st.metric("Status", "✅ Perfeito")
            elif 1200 <= char_count < 1300:
                st.metric("Status", "✅ Bom")
            else:
                st.metric("Status", "✅ Ok")
        
        st.markdown("---")
        
        st.markdown("### 🎙️ Roteiro (ElevenLabs Ready)")
        st.code(script_text, language="text")
        
        st.markdown("### 🎨 Prompts das Imagens")
        
        prompts_lines = [line.strip() for line in prompts_text.split('\n') if line.strip()]
        prompts_list = []
        
        for prompt_line in prompts_lines:
            if ':' in prompt_line:
                parts = prompt_line.split(':', 1)
                timestamp = parts[0].strip()
                content = parts[1].strip()
                
                prompts_list.append({"timestamp": timestamp, "prompt": content})
                
                st.markdown(f"**⏱️ {timestamp}**")
                st.code(content, language="text")
        
        st.markdown("### 📝 Descrição + Hashtags")
        st.code(description_text, language="text")
        
        texto_completo = f"""ROTEIRO:
{script_text}

PROMPTS DAS IMAGENS:
{prompts_text}

DESCRIÇÃO + HASHTAGS:
{description_text}
"""
        
        st.markdown("---")
        st.download_button("📥 Download Completo", data=texto_completo, file_name=f"tiktok_{char_count}chars.txt", mime="text/plain", use_container_width=True)
        
        if gerar_imagens and prompts_list:
            st.markdown("---")
            st.markdown("### 🖼️ Imagens Geradas com IA")
            st.info(f"🎨 Gerando {len(prompts_list)} imagens com **Flux 1.1 Pro** (qualidade profissional)... Aguarde.")
            
            fal_key = "99587ba2-f99b-4cc3-a505-fd4f581ba722:c0e36bbb2a82285ede5a9f98720d463f"
            
            headers = {
                "Authorization": f"Key {fal_key}",
                "Content-Type": "application/json"
            }
            
            for idx, prompt_data in enumerate(prompts_list):
                timestamp = prompt_data["timestamp"]
                prompt_img = prompt_data["prompt"]
                
                st.markdown(f"#### 📸 {timestamp}")
                
                with st.spinner(f"🎨 Gerando imagem profissional {idx+1}/{len(prompts_list)}..."):
                    try:
                        payload = {
                            "prompt": prompt_img,
                            "image_size": "landscape_16_9",
                            "num_inference_steps": 28,
                            "guidance_scale": 3.5,
                            "num_images": 1
                        }
                        
                        response_img = requests.post(
                            "https://fal.run/fal-ai/flux-pro/v1.1",
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        if response_img.status_code == 200:
                            result = response_img.json()
                            image_url = result.get("images", [{}])[0].get("url")
                            
                            if image_url:
                                img_response = requests.get(image_url)
                                image = Image.open(BytesIO(img_response.content))
                                st.image(image, caption=f"Imagem Flux Pro para {timestamp}", use_container_width=True)
                                
                                buf = BytesIO()
                                image.save(buf, format="PNG")
                                st.download_button(
                                    label=f"📥 Download {timestamp}",
                                    data=buf.getvalue(),
                                    file_name=f"tiktok_flux_pro_{timestamp.replace(':', '-')}.png",
                                    mime="image/png",
                                    key=f"download_{idx}"
                                )
                            else:
                                st.warning("⚠️ Erro ao obter URL da imagem")
                                st.code(prompt_img, language="text")
                        else:
                            st.error(f"❌ Erro {response_img.status_code}: {response_img.text[:200]}")
                            st.code(prompt_img, language="text")
                        
                        time.sleep(2)
                        
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
                        st.code(prompt_img, language="text")
            
            st.success(f"✅ Todas as {len(prompts_list)} imagens foram geradas com Flux Pro!")
    
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

st.markdown("---")
st.markdown("Made with ❤️ | Powered by Google Gemini 2.0 Flash + Flux 1.1 Pro")
