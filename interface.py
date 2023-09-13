import customtkinter as ctk
from PIL import Image, ImageEnhance
import numpy as np
import cv2

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Variáveis para armazenar a imagem original e a imagem modificada
        self.imagem_original = None
        self.imagem_modificada = None
        self.img_com_brilho = None
        self.img_com_contraste = None
        self.img_com_gama = None
        self.img_com_equalizacao = None
        
        # Configurações da janela =================================================
        ctk.set_default_color_theme("dark-blue")
        
        self.title("EDITOR DE IMAGENS")
        self.minsize(width=800, height=600)
        self.grid_columnconfigure(1, weight=1) # Configuração para o frame da imagem
        self.grid_rowconfigure(0, weight=1) # Configuração para o frame do menu
        # =========================================================================
        
        # Cria o frame do menu e o posiciona na janela principal inicio ================================
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        
        self.desfazer_img = Image.open("icons/desfazer.png")
        self.refazer_img = Image.open("icons/refazer.png")
        
        self.desfazer_img = ctk.CTkImage(light_image=self.desfazer_img, dark_image=self.desfazer_img, size=(20, 20))
        self.refazer_img = ctk.CTkImage(light_image=self.refazer_img, dark_image=self.refazer_img, size=(20, 20))
        
        # botões do menu incio
        self.menu_title = ctk.CTkLabel(self.menu_frame, text='MENU', fg_color="gray30", corner_radius=6)
        self.menu_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        self.menu_button_desfazer = ctk.CTkButton(self.menu_frame, text=None,image=self.desfazer_img, command=self.acao_desfazer, anchor="e", width=20, height=20, fg_color='transparent')
        self.menu_button_desfazer.grid(row=1, column=0, padx=10, pady=2, sticky="e")
        self.menu_button_refazer = ctk.CTkButton(self.menu_frame, text=None,image=self.refazer_img, command=self.acao_refazer, anchor="w", width=20, height=20, fg_color='transparent')
        self.menu_button_refazer.grid(row=1, column=1, padx=10, pady=2, sticky="w")
        
        self.menu_button_abrir = ctk.CTkButton(self.menu_frame, text="Abrir Imagem", command=self.abrir_imagem)
        self.menu_button_abrir.grid(row=2, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        self.menu_button_salvar = ctk.CTkButton(self.menu_frame, text="Salvar Imagem", command=self.salvar_imagem)
        self.menu_button_salvar.grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)   
        self.menu_button_verificar = ctk.CTkButton(self.menu_frame, text="Verificar Imagem", command=self.verificar_imagem)
        self.menu_button_verificar.grid(row=4, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        self.menu_button_transformacoes = ctk.CTkButton(self.menu_frame, text="Transformações", command=self.transforma)
        self.menu_button_transformacoes.grid(row=5, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        
        # Fim da criação do frame do menu ================================================================
        
        # Cria o frame da imagem e o posiciona na janela principal inicio ================================
        self.image_frame = ctk.CTkScrollableFrame(self, orientation="vertical")
        self.image_frame.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
        
        # Configurações do frame da imagem
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        
        # Cria o subframe para a imagem 
        self.image_sub_frame = ctk.CTkScrollableFrame(self.image_frame, orientation="horizontal")
        self.image_sub_frame.grid(row=0, column=0, sticky="ew")
        
        # Configurações do subframe
        self.image_sub_frame.grid_columnconfigure(0, weight=1)   
        self.image_sub_frame.grid_rowconfigure(0, weight=1)
        
        # Fim da criação do frame da imagem ================================================================
        
    def abrir_imagem(self):
        caminho = ctk.filedialog.askopenfilename(title="Selecione uma imagem", filetypes=[("Imagens", ".jpg .jpeg .png .bmp .tif")])
        if caminho:
            # Limpa as variáveis de imagem
            self.imagem_modificada = None
            self.img_com_brilho = None
            self.img_com_contraste = None
            self.img_com_gama = None
            
            self.imagem_original = caminho # Armazena o caminho da imagem original
            img = Image.open(caminho)
            self.image_sub_frame.configure(width=img.width)
            self.image_sub_frame.configure(height=img.height)
            img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.image_frame_label = ctk.CTkLabel(self.image_sub_frame, text=None, image=img)
            self.image_frame_label.grid(row=0, column=0, sticky="nsew")
        else:
            pass
            
    def atualiza_imagem(self, imagem):
        self.image_sub_frame.configure(width=imagem.width)
        self.image_sub_frame.configure(height=imagem.height)
        img = ctk.CTkImage(light_image=imagem, 
                           dark_image=imagem, 
                           size=(imagem.width, imagem.height))
        self.image_frame_label.configure(image=img)
    
    def acao_desfazer(self):
        if self.imagem_original:
            img = Image.open(self.imagem_original)
            self.atualiza_imagem(img)
        else:
            pass
            
    def acao_refazer(self):
        if self.imagem_modificada:
            self.atualiza_imagem(self.imagem_modificada)
        else:
            pass
        
    def salvar_imagem(self):
        if self.imagem_modificada:
            caminho = ctk.filedialog.asksaveasfilename(title="Salvar imagem", filetypes=[("Imagens", ".jpg .jpeg .png .bmp .tif")])
            if caminho:
                self.imagem_modificada.save(caminho+self.imagem_original[-4:])
            else:
                pass
        else:
            pass
        
    def verificar_imagem(self):
        print('Verificando imagem...')
        print(f'Imagem original: {self.imagem_original}')
        print(f'Imagem modificada: {self.imagem_modificada}')
        
    def negativo(self):
        if self.imagem_modificada:
            self.imagem_modificada = Image.fromarray(255 - np.array(self.imagem_modificada))
            self.atualiza_imagem(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = np.array(img)
            img = 255 - img
            img = Image.fromarray(img)
            self.imagem_modificada = img
            self.atualiza_imagem(self.imagem_modificada)
    
    def transforma(self):
        # Esconde o frame do menu e mostra o frame das transformações
        self.menu_frame.grid_forget()
        
        # Cria o frame das transformações e o posiciona na janela principal inicio ================================
        self.transforma_frame = ctk.CTkFrame(self)
        self.transforma_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        # Configurações do frame das transformações
        self.transforma_frame.grid_columnconfigure(0, weight=1)
        self.transforma_frame.grid_rowconfigure(8, weight=1)
        
        # titulo do frame das transformações
        self.transforma_title = ctk.CTkLabel(self.transforma_frame, text='TRASNFORMAÇÕES', fg_color="gray30", corner_radius=6)
        self.transforma_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # botões do frame das transformações
        # negativo
        self.transforma_button_negativo = ctk.CTkButton(self.transforma_frame, text="Negativo", command=self.negativo)
        self.transforma_button_negativo.grid(row=1, column=0, padx=10, pady=5, sticky="ew") # Posição 1 em transforma_frame
        # brilho
        self.transforma_frame_brilho = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_brilho.grid(row=2, column=0, padx=10, pady=5, sticky="ew") # Posição 2 em transforma_frame
        self.transforma_label_brilho = ctk.CTkLabel(self.transforma_frame_brilho, text="Brilho")
        self.transforma_label_brilho.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_brilho = ctk.CTkSlider(self.transforma_frame_brilho, from_= 0.1, to = 1.9,command=self.acao_brilho)
        self.transforma_button_brilho.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_brilho.set(1.0)
        self.transforma_button_salvar_brilho = ctk.CTkButton(self.transforma_frame_brilho, text="Salvar Brilho", command=self.acao_salvar_brilho)
        self.transforma_button_salvar_brilho.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        # contraste
        self.transforma_frame_contraste = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_contraste.grid(row=3, column=0, padx=10, pady=5, sticky="ew") # Posição 3 em transforma_frame
        self.transforma_label_contraste = ctk.CTkLabel(self.transforma_frame_contraste, text="Contraste")
        self.transforma_label_contraste.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_contraste = ctk.CTkSlider(self.transforma_frame_contraste, from_= 0.1, to = 1.9, command=self.acao_contraste)
        self.transforma_button_contraste.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_contraste.set(1.0)
        self.transforma_button_salvar_contraste = ctk.CTkButton(self.transforma_frame_contraste, text="Salvar Contraste", command=self.acao_salvar_constraste)
        self.transforma_button_salvar_contraste.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        # gama 
        self.transforma_frame_gama = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_gama.grid(row=4, column=0, padx=10, pady=5, sticky="ew") # Posição 4 em transforma_frame
        self.transforma_label_gama = ctk.CTkLabel(self.transforma_frame_gama, text="Gama")
        self.transforma_label_gama.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_gama = ctk.CTkSlider(self.transforma_frame_gama, from_= 0.1, to = 4.0, command=self.acao_gama)
        self.transforma_button_gama.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_gama.set(1.0)
        self.transforma_button_salvar_gama = ctk.CTkButton(self.transforma_frame_gama, text="Salvar Gama", command=self.acao_salvar_gama)
        self.transforma_button_salvar_gama.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        # histogramas ---------------------------------------------------------------
        
        self.transforma_frame_histogramas = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_histogramas.grid(row=5, column=0, padx=10, pady=5, sticky="ew") # Posição 5 em transforma_frame
        self.transforma_frame_histogramas.grid_columnconfigure(0, weight=1)
        self.transforma_label_histogramas = ctk.CTkLabel(self.transforma_frame_histogramas, text="Histogramas",)
        self.transforma_label_histogramas.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_equalizado = ctk.CTkButton(self.transforma_frame_histogramas, text="Equalizado", command=self.histograma_equalizado)
        self.transforma_button_hist_equalizado.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_salva_equalizado = ctk.CTkButton(self.transforma_frame_histogramas, text="Salvar Equalização", command=self.acao_salva_equalização)
        self.transforma_button_hist_salva_equalizado.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        
        # ---------------------------------------------------------------------------
        
        self.transforma_button_voltar = ctk.CTkButton(self.transforma_frame, text="Voltar", command=self.acao_voltar_menu)
        self.transforma_button_voltar.grid(row=8, column=0, padx=10, pady=5, sticky="sew") # Posição 8 em transforma_frame
        # Fim da criação do frame das transformações ================================================================
    
    def acao_voltar_menu(self):
        self.transforma_frame.grid_forget()
        self.menu_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        
        if self.imagem_modificada:
            self.atualiza_imagem(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            print(img.mode)
            self.atualiza_imagem(img)
        
    def acao_salvar_brilho(self):
            self.imagem_modificada = self.img_com_brilho
            self.transforma_button_brilho.set(1.0)
        
    def acao_brilho(self, event):
        if self.imagem_modificada:
            img = ImageEnhance.Brightness(self.imagem_modificada).enhance(float(event))
            self.img_com_brilho = img
            self.atualiza_imagem(self.img_com_brilho)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = ImageEnhance.Brightness(img).enhance(float(event))
            self.img_com_brilho = img
            self.atualiza_imagem(self.img_com_brilho)
    
    def acao_salvar_constraste(self):
        self.imagem_modificada = self.img_com_contraste
        self.transforma_button_contraste.set(1.0)
    
    def acao_contraste(self, event):
        if self.imagem_modificada:
            img = ImageEnhance.Contrast(self.imagem_modificada).enhance(float(event))
            self.img_com_contraste = img
            self.atualiza_imagem(self.img_com_contraste)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = ImageEnhance.Contrast(img).enhance(float(event))
            self.img_com_contraste = img
            self.atualiza_imagem(self.img_com_contraste)
    
    def acao_salvar_gama(self):
        self.imagem_modificada = self.img_com_gama
        self.transforma_button_gama.set(1.0)
    
    def acao_gama(self, event):
        if self.imagem_modificada:
            img = np.array(self.imagem_modificada)
            c = 255.0 / (255.0 ** float(event))
            img_gamma = c * (img.astype(np.float64)) ** float(event)
            # Converta a matriz NumPy resultante de volta para uma imagem Pillow
            img_gamma = img_gamma.round().clip(0, 255).astype(np.uint8)
            self.img_com_gama = Image.fromarray(img_gamma)
            self.atualiza_imagem(self.img_com_gama)
        if self.imagem_original:
            img = Image.open(self.imagem_original)
            img = np.array(img)
            c = 255.0 / (255.0 ** float(event))
            img_gamma = c * (img.astype(np.float64)) ** float(event)
            # Converta a matriz NumPy resultante de volta para uma imagem Pillow
            img_gamma = img_gamma.round().clip(0, 255).astype(np.uint8)
            self.img_com_gama = Image.fromarray(img_gamma)
            self.atualiza_imagem(self.img_com_gama)
   
    def acao_salva_equalização(self):
        if self.img_com_equalizacao:
            self.imagem_modificada = self.img_com_equalizacao
    
    def histograma_equalizado(self):
        img = None
        if self.imagem_modificada:
            img = self.gerar_histograma_equalizado(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.gerar_histograma_equalizado(img)
            
        if img:
            self.img_com_equalizacao = img
            self.atualiza_imagem(img)
    
    def gerar_histograma_equalizado(self, imagem):
        img = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
        R = img.shape[0]
        C = img.shape[1]
        #calculo do histograma normalizado (pr)
        hist = cv2.calcHist([img], [0], None, [256], [0, 256]) 
        pr = hist/(R*C)
        # cummulative distribution function (CDF)
        cdf = pr.cumsum()
        sk = 255 * cdf
        sk = np.round(sk)
        
        # criando a imagem de saída
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_out = np.zeros(img.shape, dtype=np.uint8)
        for i in range(256):
            img_out[img == i] = sk[i]
        
        return Image.fromarray(img_out)
            
            
            

if __name__ == "__main__":
    
    app = App()
    app.mainloop()