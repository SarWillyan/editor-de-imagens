import customtkinter as ctk
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import matplotlib.pyplot as plt

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.filtros_frame = None
        self.transforma_frame = None
        # Variáveis para armazenar a imagem original e a imagem modificada
        self.imagem_original = None
        self.imagem_modificada = None
        self.img_com_brilho = None
        self.img_com_contraste = None
        self.img_com_gama = None
        self.img_com_equalizacao = None
        self.img_com_especificacao = None
        self.img_com_box = None
        self.img_com_laplaciano = None
        self.img_com_gaussiano = None
        self.img_com_mediana = None
        self.img_com_sobel = None
        
        self.zoom = 1.0
        
        # Configurações da janela =================================================
        ctk.set_default_color_theme("dark-blue")
        
        self.title("EDITOR DE IMAGENS")
        self.minsize(width=800, height=600)
        self.grid_columnconfigure(1, weight=1) # Configuração para o frame da imagem
        self.grid_rowconfigure(0, weight=1) # Configuração para o frame do menu
        # =========================================================================
        
        # Cria o frame do menu e o posiciona na janela principal inicio ================================
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw", rowspan=2)
        
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
        
        # zoom
        self.amplia_img = Image.open("icons/ampliar.png")
        self.reduz_img = Image.open("icons/reduzir.png")
        self.amplia_img = ctk.CTkImage(light_image=self.amplia_img, dark_image=self.amplia_img, size=(20, 20))
        self.reduz_img = ctk.CTkImage(light_image=self.reduz_img, dark_image=self.reduz_img, size=(20, 20))
        self.opcoes_button_ampliar = ctk.CTkButton(self.menu_frame, text=None,image=self.amplia_img, command=self.amplia, anchor="e", width=20, height=20, fg_color='transparent')
        self.opcoes_button_ampliar.grid(row=2, column=0, padx=10, pady=2, sticky="e")
        self.opcoes_button_reduzir = ctk.CTkButton(self.menu_frame, text=None, image=self.reduz_img, command=self.reduz, anchor="w", width=20, height=20, fg_color='transparent')
        self.opcoes_button_reduzir.grid(row=2, column=1, padx=10, pady=2, sticky="w")
        
        # abre imagem
        self.menu_button_abrir = ctk.CTkButton(self.menu_frame, text="Abrir Imagem", command=self.abrir_imagem)
        self.menu_button_abrir.grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        # salva imagem
        self.menu_button_salvar = ctk.CTkButton(self.menu_frame, text="Salvar Imagem", command=self.salvar_imagem)
        self.menu_button_salvar.grid(row=4, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        # transformações
        self.menu_button_transformacoes = ctk.CTkButton(self.menu_frame, text="Transformações", command=self.transforma)
        self.menu_button_transformacoes.grid(row=5, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        # filtros
        self.menu_button_filtros = ctk.CTkButton(self.menu_frame, text="Filtros", command=self.filtros)
        self.menu_button_filtros.grid(row=6, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        
        
        # Fim da criação do frame do menu ================================================================
        
        # Cria o frame da imagem e o posiciona na janela principal inicio ================================
        self.image_frame = ctk.CTkScrollableFrame(self, orientation="vertical")
        self.image_frame.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
        
        # Configurações do frame da imagem
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        
        # Cria o subframe para a imagem 
        self.image_sub_frame = ctk.CTkScrollableFrame(self.image_frame, orientation="horizontal", height=550)
        self.image_sub_frame.grid(row=0, column=0, sticky="ew")
        
        # Configurações do subframe
        self.image_sub_frame.grid_columnconfigure(0, weight=1)   
        self.image_sub_frame.grid_rowconfigure(0, weight=1)
        
        # Fim da criação do frame da imagem ================================================================
    def is_numbers(self, char):
        return char.isdigit()
        
    def abrir_imagem(self):
        caminho = ctk.filedialog.askopenfilename(title="Selecione uma imagem", filetypes=[("Imagens", ".jpg .jpeg .png .bmp .tif")])
        if caminho:
            # Limpa as variáveis de imagem
            self.imagem_original = None
            self.imagem_modificada = None
            self.img_com_brilho = None
            self.img_com_contraste = None
            self.img_com_gama = None
            self.img_com_equalizacao = None
            self.img_com_especificacao = None
            self.img_com_box = None
            self.img_com_laplaciano = None
            self.img_com_gaussiano = None
            self.img_com_mediana = None
            self.img_com_sobel = None
            self.zoom = 1.0
            
            # Abre a imagem e a mostra no frame da imagem
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
                if self.imagem_original[-4:] == 'jpeg':
                    self.imagem_modificada.save(caminho+self.imagem_original[-5:])
                else: 
                    self.imagem_modificada.save(caminho+self.imagem_original[-4:])
            else:
                pass
        else:
            pass
        
    def negativo(self):
        if self.imagem_modificada:
            self.imagem_modificada = Image.fromarray(255 - np.array(self.imagem_modificada))
            self.atualiza_imagem(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            self.imagem_modificada = Image.fromarray(255 - np.array(img))
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
        self.transforma_label_equalizacao = ctk.CTkLabel(self.transforma_frame_histogramas, text="Equalização")
        self.transforma_label_equalizacao.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_equalizado = ctk.CTkButton(self.transforma_frame_histogramas, text="Equaliza", command=self.histograma_equalizado)
        self.transforma_button_hist_equalizado.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_salva_equalizado = ctk.CTkButton(self.transforma_frame_histogramas, text="Salvar Equalização", command=self.acao_salva_equalização)
        self.transforma_button_hist_salva_equalizado.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_label_especifacao = ctk.CTkLabel(self.transforma_frame_histogramas, text="Especificação")
        self.transforma_label_especifacao.grid(row=3, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_especifica = ctk.CTkButton(self.transforma_frame_histogramas, text="Especifica", command=self.histograma_especificado)
        self.transforma_button_hist_especifica.grid(row=4, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_hist_salva_especifica = ctk.CTkButton(self.transforma_frame_histogramas, text="Salvar Especificação", command=self.acao_salva_especificacao)
        self.transforma_button_hist_salva_especifica.grid(row=5, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        # ---------------------------------------------------------------------------
        
        self.transforma_button_voltar = ctk.CTkButton(self.transforma_frame, text="Voltar", command=self.acao_voltar_menu)
        self.transforma_button_voltar.grid(row=8, column=0, padx=10, pady=5, sticky="sew") # Posição 8 em transforma_frame
        # Fim da criação do frame das transformações ================================================================
    
    def acao_voltar_menu(self):

        if self.filtros_frame and self.filtros_frame.winfo_ismapped():
            self.filtros_frame.grid_forget()
            self.menu_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        elif self.transforma_frame and self.transforma_frame.winfo_ismapped():
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
            self.gama(self.imagem_modificada, event)
        if self.imagem_original:
            img = Image.open(self.imagem_original)
            self.gama(img, event)
    
    def gama(self, imagem, event):
        img = np.array(imagem)
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
        R, G, B = cv2.split(img)
        output_R = cv2.equalizeHist(R)
        output_G = cv2.equalizeHist(G)
        output_B = cv2.equalizeHist(B)
        img = cv2.merge((output_R, output_G, output_B))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.plot(img[0])
        plt.show()
        return Image.fromarray(img)
            
    def acao_salva_especificacao(self):
        if self.img_com_especificacao:
            self.imagem_modificada = self.img_com_especificacao
    
    def histograma_especificado(self):
        img = None
        if self.imagem_modificada:
            img = self.gerar_histograma_especificado(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.gerar_histograma_especificado(img)
            
        if img:
            self.img_com_especificacao = img
            self.atualiza_imagem(img)
    
    def gerar_histograma_especificado(self, imagem):
        path = ctk.filedialog.askopenfilename(title="Selecione uma imagem", 
                                              filetypes=[("Imagens", ".jpg .jpeg .png .bmp .tif")])
        if path:
            # conversões para o opemCV
            img_entrada = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
            img_ref = np.array(Image.open(path))
            img_ref = cv2.cvtColor(img_ref, cv2.COLOR_RGB2BGR)
            # calcula os histogramas normalizados
            pr = [cv2.calcHist([chan], [0], None, [256], [0, 256]).ravel() for chan in cv2.split(img_entrada)]
            pz = [cv2.calcHist([chan], [0], None, [256], [0, 256]).ravel() for chan in cv2.split(img_ref)]
            # calcula os histogramas acumulados
            cdf_input = [np.cumsum(hist) for hist in pr]
            cdf_ref = [np.cumsum(hist) for hist in pz]

            img_out = np.zeros(img_entrada.shape, dtype=np.uint8)

            for c in range(3):
                for i in range(256):
                    diff = np.absolute(cdf_ref[c] - cdf_input[c][i])
                    indice = diff.argmin()
                    img_out[img_entrada[:, :, c] == i, c] = indice
            
            img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
            
            return Image.fromarray(img_out)

    def amplia(self):
        self.acao_zoom(0.1)
        
    def reduz(self):
        self.acao_zoom(-0.1)

    def acao_zoom(self, event):
        if self.imagem_original:
            self.zoom += float(event)
            img = Image.open(self.imagem_original)
            self.aplica_zoom(img)
            
    def aplica_zoom(self, imagem):
        print(imagem.width, imagem.height)
        print(int(imagem.width*self.zoom), int(imagem.height*self.zoom))
        img = imagem.resize((int(imagem.width*self.zoom), int(imagem.height*self.zoom)))
        self.imagem_modificada = img
        self.atualiza_imagem(img)
        
    def filtros(self):
        # esconde o frame do menu e mostra o frame dos filtros
        self.menu_frame.grid_forget()
        
        # Cria o frame dos filtros e o posiciona na janela principal inicio ================================
        self.filtros_frame = ctk.CTkFrame(self) 
        self.filtros_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        validacao = self.filtros_frame.register(self.is_numbers)
        # Configurações do frame dos filtros
        self.filtros_frame.grid_columnconfigure(0, weight=1)
        self.filtros_frame.grid_rowconfigure(12, weight=1)
        
        # titulo do frame dos filtros
        self.filtros_title = ctk.CTkLabel(self.filtros_frame, text='FILTROS', fg_color="gray30", corner_radius=6)
        self.filtros_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        # botões do frame dos filtros
        self.salve_img = Image.open("icons/salve.png")
        self.salve_img = ctk.CTkImage(light_image=self.salve_img, dark_image=self.salve_img, size=(20, 20))
        
        # filtro box
        self.filtros_frame_input_box = ctk.CTkEntry(self.filtros_frame, validate="key", validatecommand=(validacao, '%S'))
        self.filtros_frame_input_box.grid(row=1, column=0, padx=(10,5), pady=(5,0), sticky="ew")
        self.filtros_frame_button_box = ctk.CTkButton(self.filtros_frame, text="Box", command=self.filtro_box)
        self.filtros_frame_button_box.grid(row=2, column=0, padx=(10,5), pady=5, sticky="ew")
        self.filtros_frame_button_salvar_box = ctk.CTkButton(self.filtros_frame, text=None, image=self.salve_img, command=self.salvar_box,
                                                             anchor="w", width=20, height=20, fg_color='transparent')
        self.filtros_frame_button_salvar_box.grid(row=2, column=1, padx=(5,10), pady=5, sticky="e")
        
        # filtro gaussiano
        self.filtros_frame_input_gaussiano = ctk.CTkEntry(self.filtros_frame, validate="key", validatecommand=(validacao, '%S'))
        self.filtros_frame_input_gaussiano.grid(row=3, column=0, padx=(10,5), pady=(5,0), sticky="ew")
        self.filtros_frame_button_gaussiano = ctk.CTkButton(self.filtros_frame, text="Gaussiano", command=self.filtro_gaussiano)
        self.filtros_frame_button_gaussiano.grid(row=4, column=0, padx=(10,5), pady=5, sticky="ew")
        self.filtros_frame_button_salvar_gaussiano = ctk.CTkButton(self.filtros_frame, text=None, image=self.salve_img, command=self.salvar_gaussiano,
                                                             anchor="w", width=20, height=20, fg_color='transparent')
        self.filtros_frame_button_salvar_gaussiano.grid(row=4, column=1, padx=(5,10), pady=5, sticky="e")
       
        # filtro mediana
        self.filtros_frame_input_mediana = ctk.CTkEntry(self.filtros_frame, validate="key", validatecommand=(validacao, '%S'))
        self.filtros_frame_input_mediana.grid(row=5, column=0, padx=(10,5), pady=(5,0), sticky="ew")
        self.filtros_frame_button_mediana = ctk.CTkButton(self.filtros_frame, text="Mediana", command=self.filtro_mediana)
        self.filtros_frame_button_mediana.grid(row=6, column=0, padx=(10,5), pady=5, sticky="ew")
        self.filtros_frame_button_salvar_mediana = ctk.CTkButton(self.filtros_frame, text=None, image=self.salve_img, command=self.salvar_mediana,
                                                             anchor="w", width=20, height=20, fg_color='transparent')
        self.filtros_frame_button_salvar_mediana.grid(row=6, column=1, padx=(5,10), pady=5, sticky="e")
        
        # filtro laplaciano
        self.filtros_frame_input_laplaciano = ctk.CTkEntry(self.filtros_frame, validate="key", validatecommand=(validacao, '%S'))
        self.filtros_frame_input_laplaciano.grid(row=7, column=0, padx=(10,5), pady=(5,0), sticky="ew")
        self.filtros_frame_button_laplaciano = ctk.CTkButton(self.filtros_frame, text="Laplaciano", command=self.filtro_laplaciano)
        self.filtros_frame_button_laplaciano.grid(row=8, column=0, padx=(10,5), pady=5, sticky="ew")
        self.filtros_frame_button_salvar_laplaciano = ctk.CTkButton(self.filtros_frame, text=None, image=self.salve_img, command=self.salvar_laplaciano,
                                                             anchor="w", width=20, height=20, fg_color='transparent')
        self.filtros_frame_button_salvar_laplaciano.grid(row=8, column=1, padx=(5,10), pady=5, sticky="e")
        # filtro sobel
        self.filtros_frame_input_sobel = ctk.CTkEntry(self.filtros_frame, validate="key", validatecommand=(validacao, '%S'))
        self.filtros_frame_input_sobel.grid(row=9, column=0, padx=(10,5), pady=(5,0), sticky="ew")
        self.filtros_frame_button_sobel = ctk.CTkButton(self.filtros_frame, text="Sobel", command=self.filtro_sobel)
        self.filtros_frame_button_sobel.grid(row=10, column=0, padx=(10,5), pady=5, sticky="ew")
        self.filtros_frame_button_salvar_sobel = ctk.CTkButton(self.filtros_frame, text=None, image=self.salve_img, command=self.salvar_sobel,
                                                             anchor="w", width=20, height=20, fg_color='transparent')
        self.filtros_frame_button_salvar_sobel.grid(row=10, column=1, padx=(5,10), pady=5, sticky="e")
        
        
        # voltar
        self.filtros_frame_button_voltar = ctk.CTkButton(self.filtros_frame, text="Voltar", command=self.acao_voltar_menu)
        self.filtros_frame_button_voltar.grid(row=12, column=0, padx=10, pady=5, sticky="sew", columnspan=2)
      
    def filtro_box(self):
        if self.imagem_modificada:
            img = self.box(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.box(img)
        
        if img:
            self.img_com_box = img
            self.atualiza_imagem(img)
            
    def box(self, imagem):
        img = np.array(imagem)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        kernel = int(self.filtros_frame_input_box.get())
        img = cv2.boxFilter(img, -1, (kernel,kernel))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)
    
    def salvar_box(self):
        if self.img_com_box:
            self.imagem_modificada = self.img_com_box
            
    def filtro_gaussiano(self):
        if self.imagem_modificada:
            img = self.gaussiano(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.gaussiano(img)
        
        if img:
            self.img_com_gaussiano = img
            self.atualiza_imagem(img)
            
    def gaussiano(self, imagem):
        img = np.array(imagem)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        kernel = int(self.filtros_frame_input_gaussiano.get())
        img = cv2.GaussianBlur(img, (kernel,kernel), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)

    def salvar_gaussiano(self):
        if self.img_com_gaussiano:
            self.imagem_modificada = self.img_com_gaussiano
    
    def filtro_mediana(self):
        if self.imagem_modificada:
            img = self.mediana(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.mediana(img)
        
        if img:
            self.img_com_mediana = img
            self.atualiza_imagem(img)
    
    def mediana(self, imagem):
        img = np.array(imagem)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        kernel = int(self.filtros_frame_input_mediana.get())
        img = cv2.medianBlur(img, kernel)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)
    
    def salvar_mediana(self):
        if self.img_com_mediana:
            self.imagem_modificada = self.img_com_mediana
            
    def filtro_laplaciano(self):
        if self.imagem_modificada:
            img = self.laplaciano(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.laplaciano(img)
        
        if img:
            self.img_com_laplaciano = img
            self.atualiza_imagem(img)
    
    def laplaciano(self, imagem):
        img = np.array(imagem)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        kernel = int(self.filtros_frame_input_laplaciano.get())
        img = cv2.Laplacian(img, cv2.CV_64F, ksize=kernel)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return Image.fromarray(img)
    
    def salvar_laplaciano(self):
        if self.img_com_laplaciano:
            self.imagem_modificada = self.img_com_laplaciano
    
    def filtro_sobel(self):
        if self.imagem_modificada:
            img = self.sobel(self.imagem_modificada)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = self.sobel(img)
        
        if img:
            self.img_com_sobel = img
            self.atualiza_imagem(img)
            
    def sobel(self, imagem):
        img = np.array(imagem)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # x e y são os gradientes horizontais e verticais
        kernel = int(self.filtros_frame_input_sobel.get())
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=kernel)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=kernel)
        # Calcula a magnitude do gradiente
        maginitude = np.sqrt(sobelx**2.0 + sobely**2.0)
        # Normaliza a magnitude do gradiente para o intervalo 0.0-255.0
        maginitude = cv2.normalize(maginitude, None, 0.0, 255.0, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        
        img = cv2.cvtColor(maginitude, cv2.COLOR_BGR2GRAY)
        return Image.fromarray(img)
    
    def salvar_sobel(self):
        if self.img_com_sobel:
            self.imagem_modificada = self.img_com_sobel
            
if __name__ == "__main__":
    
    app = App()
    app.mainloop()