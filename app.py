import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Configuração da Interface Gráfica (Streamlit)
st.title("Gerador de Relatórios (PDF Estático)")
st.subheader("Preencha os dados abaixo:")

nome = st.text_input("Nome Completo:")
data = st.date_input("Data do Relatório:")
observacoes = st.text_area("Observações:")

if st.button("Gerar Relatório PDF"):
    
    # 2. Criar um "PDF temporário" na memória apenas com os textos digitados
    packet = io.BytesIO()
    canva_texto = canvas.Canvas(packet, pagesize=letter)
    
    # Definindo a fonte e o tamanho do texto
    canva_texto.setFont("Helvetica", 12)
    
    # "Carimbando" os textos nas coordenadas X e Y da página (em pontos)
    # Você precisará ajustar esses números (Ex: 100, 500) para encaixar no seu modelo
    canva_texto.drawString(100, 600, f"{nome}")
    canva_texto.drawString(100, 550, f"Data: {data}")
    canva_texto.drawString(100, 500, f"Obs: {observacoes}")
    
    canva_texto.save()
    packet.seek(0)
    
    # 3. Ler o texto criado e o seu PDF Modelo original
    pdf_texto = PdfReader(packet)
    pdf_modelo = PdfReader("seu_modelo.pdf") # Substitua pelo nome do seu arquivo
    
    pdf_final = PdfWriter()
    
    # Pega a primeira página do seu modelo
    pagina_modelo = pdf_modelo.pages[0]
    
    # Mescla (carimba) a página de texto por cima da página do modelo
    pagina_modelo.merge_page(pdf_texto.pages[0])
    
    # Adiciona a página mesclada ao arquivo final
    pdf_final.add_page(pagina_modelo)
    
    # 4. Salvar o arquivo final
    nome_saida = f"Relatorio_{nome}.pdf"
    with open(nome_saida, "wb") as saida:
        pdf_final.write(saida)
        
    st.success(f"🎉 PDF gerado com sucesso: {nome_saida}")