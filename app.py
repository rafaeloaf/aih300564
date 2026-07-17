import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Configuração da Interface Gráfica (Streamlit)
st.title("Gerador de Relatórios (PDF Estático)")
st.subheader("Preencha os dados abaixo:")

nome = st.text_input("Nome Completo:")
# Usamos uma string para evitar problemas de formatação de data
data = st.date_input("Data do Relatório:")
observacoes = st.text_area("Observações:")

if st.button("Gerar Relatório PDF"):
    
    # Validação simples para garantir que o nome foi preenchido antes de gerar
    if not nome:
        st.warning("Por favor, preencha o campo 'Nome Completo' antes de gerar.")
    else:
        # 2. Criar um "PDF temporário" na memória apenas com os textos digitados
        packet = io.BytesIO()
        canva_texto = canvas.Canvas(packet, pagesize=letter)
        
        # Definindo a fonte e o tamanho do texto
        canva_texto.setFont("Helvetica", 9)
        
        # "Carimbando" os textos nas coordenadas X e Y da página (em pontos)
        canva_texto.drawString(38, 679, f"{nome}")
        canva_texto.drawString(38, 530, f"Data: {data}")
        canva_texto.drawString(100, 550, f"Data: {observacoes}")
        canva_texto.drawString(100, 100, f"o 100-100")
        canva_texto.drawString(100, 200, f"o 100-200")
        canva_texto.drawString(200, 200, f"o 200-200")
        canva_texto.drawString(300, 300, f"o 300-300")
        canva_texto.drawString(300, 400, f"o 300-400")
        canva_texto.drawString(400, 400, f"o 400-400")
        canva_texto.drawString(500, 500, f"o 500-500")
        canva_texto.drawString(550, 550, f"o 550-550")
        canva_texto.drawString(550, 600, f"o 550-600")
        canva_texto.drawString(550, 700, f"o 550-700")
        
        canva_texto.save()
        packet.seek(0)
        
        # 3. Ler o texto criado e o seu PDF Modelo original
        pdf_texto = PdfReader(packet)
        pdf_modelo = PdfReader("AIH_base.pdf") # Substitua pelo nome do seu arquivo
        
        pdf_final = PdfWriter()
        
        # Pega a primeira página do seu modelo
        pagina_modelo = pdf_modelo.pages[0]
        
        # Mescla (carimba) a página de texto por cima da página do modelo
        pagina_modelo.merge_page(pdf_texto.pages[0])
        
        # Adiciona a página mesclada ao arquivo final
        pdf_final.add_page(pagina_modelo)
        
        # 4. Preparar o PDF final na memória para o download
        pdf_em_memoria = io.BytesIO()
        pdf_final.write(pdf_em_memoria)
        pdf_em_memoria.seek(0)
        
        st.success("🎉 PDF gerado com sucesso!")
        
        # 5. Botão oficial de Download do Streamlit
        nome_saida = f"Relatorio_{nome.replace(' ', '_')}.pdf"
        st.download_button(
            label="⬇️ Clique aqui para baixar o PDF",
            data=pdf_em_memoria,
            file_name=nome_saida,
            mime="application/pdf"
        )
