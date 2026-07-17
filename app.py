import io
import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Configuração da Interface Gráfica (Streamlit)
st.subheader("Preencha os dados abaixo:")

nomePaciente = st.text_input("Nome Completo:")
municipioUF = st.text_input("Município - UF:")
sintomasClin = st.text_input("Principais sintomas clínicos:")
justificativa = st.text_area("Condições que justificam a internação:")
exames = st.text_area("Resultados de exames realizados:")
diagInicial = st.text_area("Diagnóstico inicial:")
cid = st.text_area("CID:")
cidSecundario = st.text_area("CID secundário (se existir):")
procedimento = st.text_area("Descrição do procedimento:")
cpfMedico = st.text_area("CPF Médico:")
nomeMedico = st.text_area("Nome do Médico solicitante:")

# Usamos uma string para evitar problemas de formatação de data
data = st.date_input("Data da Solicitação:")
CRM_Medico = st.text_input("CRM:")

if st.button("Gerar Relatório PDF"):
    
    # Validação simples para garantir que o nome foi preenchido antes de gerar
    if not nomePaciente:
        st.warning("Por favor, preencha o campo 'Nome Completo' antes de gerar.")
    else:
        # 2. Criar um "PDF temporário" na memória apenas com os textos digitados
        packet = io.BytesIO()
        canva_texto = canvas.Canvas(packet, pagesize=letter)
        
        # Definindo a fonte e o tamanho do texto
        canva_texto.setFont("Helvetica", 9)
        
        # "Carimbando" os textos nas coordenadas X e Y da página (em pontos)
        canva_texto.drawString(38, 679, f"{nomePaciente}")
        canva_texto.drawString(38, 562, f"{municipioUF}")
        canva_texto.drawString(38, 530, f"{sintomasClin}")
        canva_texto.drawString(38, 420, f"{justificativa}")
        canva_texto.drawString(38, 370, f"{exames}")
        canva_texto.drawString(38, 318, f"{diagInicial}")
        canva_texto.drawString(270, 318, f"{cid}")
        canva_texto.drawString(330, 318, f"{cidSecundario}")
        canva_texto.drawString(38, 282, f"{procedimento}")
        canva_texto.drawString(38, 227, f"{nomeMedico}")
        canva_texto.drawString(300, 227, f"{data}")
        canva_texto.drawString(302, 250, f"{cpfMedico}")        
        canva_texto.drawString(300, 325, f"{CRMMedico}")
        
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
        nome_saida = f"Relatorio_{nomePaciente.replace(' ', '_')}.pdf"
        st.download_button(
            label="⬇️ Clique aqui para baixar o PDF",
            data=pdf_em_memoria,
            file_name=nome_saida,
            mime="application/pdf"
        )
