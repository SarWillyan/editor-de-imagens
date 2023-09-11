import customtkinter as ctk
from PIL import Image, ImageEnhance
import numpy as np

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Variáveis para armazenar a imagem original e a imagem modificada
        self.imagem_original = None
        self.imagem_modificada = None
        self.img_com_brilho = None
        self.img_com_contraste = None
        
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
            self.imagem_original = caminho # Armazena o caminho da imagem original
            img = Image.open(caminho)
            self.image_sub_frame.configure(width=img.width)
            self.image_sub_frame.configure(height=img.height)
            img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.image_frame_label = ctk.CTkLabel(self.image_sub_frame, text=None, image=img)
            self.image_frame_label.grid(row=0, column=0, sticky="nsew")
        else:
            ctk.messagebox.showerror("Erro", "Nenhuma imagem selecionada!")
    
    def acao_desfazer(self):
        if self.imagem_original:
            img = Image.open(self.imagem_original)
            self.image_sub_frame.configure(width=img.width)
            self.image_sub_frame.configure(height=img.height)
            img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.image_frame_label.configure(image=img)
        else:
            ctk.messagebox.showerror("Erro", "Nenhuma imagem modificada!")
            
    def acao_refazer(self):
        if self.imagem_modificada:
            self.image_sub_frame.configure(width=self.imagem_modificada.width)
            self.image_sub_frame.configure(height=self.imagem_modificada.height)
            img = ctk.CTkImage(light_image=self.imagem_modificada, 
                               dark_image=self.imagem_modificada, 
                               size=(self.imagem_modificada.width, self.imagem_modificada.height))
            self.image_frame_label.configure(image=img)
        else:
            ctk.messagebox.showerror("Erro", "Nenhuma imagem modificada!")
        
    def salvar_imagem(self):
        if self.imagem_modificada:
            caminho = ctk.filedialog.asksaveasfilename(title="Salvar imagem", filetypes=[("Imagens", ".jpg .jpeg .png .bmp .tif")])
            if caminho:
                self.imagem_modificada.save(caminho+self.imagem_original[-4:])
            else:
                ctk.messagebox.showerror("Erro", "Nenhum caminho selecionado!")
        else:
            ctk.messagebox.showerror("Erro", "Nenhuma imagem modificada!")
        
    def verificar_imagem(self):
        print('Verificando imagem...')
        print(f'Imagem original: {self.imagem_original}')
        print(f'Imagem modificada: {self.imagem_modificada}')
        
    def negativo(self):
        if self.imagem_modificada:
            self.imagem_modificada = Image.fromarray(255 - np.array(self.imagem_modificada))
            self.image_sub_frame.configure(width=self.imagem_modificada.width)
            self.image_sub_frame.configure(height=self.imagem_modificada.height)
            img = ctk.CTkImage(light_image=self.imagem_modificada, 
                               dark_image=self.imagem_modificada, 
                               size=(self.imagem_modificada.width, self.imagem_modificada.height))
            self.image_frame_label.configure(image=img)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = np.array(img)
            img = 255 - img
            img = Image.fromarray(img)
            self.imagem_modificada = img
            self.image_sub_frame.configure(width=self.imagem_modificada.width)
            self.image_sub_frame.configure(height=self.imagem_modificada.height)
            img = ctk.CTkImage(light_image=self.imagem_modificada, 
                               dark_image=self.imagem_modificada, 
                               size=(self.imagem_modificada.width, self.imagem_modificada.height))
            self.image_frame_label.configure(image=img)
    
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
        self.transforma_button_negativo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        # brilho
        self.transforma_frame_brilho = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_brilho.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.transforma_label_brilho = ctk.CTkLabel(self.transforma_frame_brilho, text="Brilho")
        self.transforma_label_brilho.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_brilho = ctk.CTkSlider(self.transforma_frame_brilho, from_= 0.1, to = 1.9,command=self.acao_brilho)
        self.transforma_button_brilho.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_brilho.set(1.0)
        self.transforma_button_salvar_brilho = ctk.CTkButton(self.transforma_frame_brilho, text="Salvar Brilho", command=self.acao_salvar_brilho)
        self.transforma_button_salvar_brilho.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        # contraste
        self.transforma_frame_contraste = ctk.CTkFrame(self.transforma_frame)
        self.transforma_frame_contraste.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.transforma_label_contraste = ctk.CTkLabel(self.transforma_frame_contraste, text="Contraste")
        self.transforma_label_contraste.grid(row=0, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_contraste = ctk.CTkSlider(self.transforma_frame_contraste, from_= 0.1, to = 1.9, command=self.acao_contraste)
        self.transforma_button_contraste.grid(row=1, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        self.transforma_button_salvar_contraste = ctk.CTkButton(self.transforma_frame_contraste, text="Salvar Contraste", command=self.acao_salvar_constraste)
        self.transforma_button_salvar_contraste.grid(row=2, column=0, padx=(0,10), pady=(0,10), sticky="ew")
        
        self.transforma_button_voltar = ctk.CTkButton(self.transforma_frame, text="Voltar", command=self.acao_voltar_menu)
        self.transforma_button_voltar.grid(row=8, column=0, padx=10, pady=5, sticky="sew")
    
    def acao_voltar_menu(self):
        self.transforma_frame.grid_forget()
        self.menu_frame.grid(row=0, column=0, padx=(3,3), pady=1, sticky="nsw")
        
        if self.imagem_modificada:
            self.acao_refazer()
        else:
            self.acao_desfazer()
        
    def acao_salvar_brilho(self):
            self.imagem_modificada = self.img_com_brilho
            self.transforma_button_brilho.set(1.0)
        
    def acao_brilho(self, event):
        if self.imagem_modificada:
            img = ImageEnhance.Brightness(self.imagem_modificada).enhance(float(event))
            self.img_com_brilho = img
            self.image_sub_frame.configure(width=self.img_com_brilho.width)
            self.image_sub_frame.configure(height=self.img_com_brilho.height)
            img = ctk.CTkImage(light_image=self.img_com_brilho, 
                               dark_image=self.img_com_brilho, 
                               size=(self.img_com_brilho.width, self.img_com_brilho.height))
            self.image_frame_label.configure(image=img)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = ImageEnhance.Brightness(img).enhance(float(event))
            self.img_com_brilho = img
            self.image_sub_frame.configure(width=self.img_com_brilho.width)
            self.image_sub_frame.configure(height=self.img_com_brilho.height)
            img = ctk.CTkImage(light_image=self.img_com_brilho, 
                               dark_image=self.img_com_brilho, 
                               size=(self.img_com_brilho.width, self.img_com_brilho.height))
            self.image_frame_label.configure(image=img)
    
    def acao_salvar_constraste(self):
        self.imagem_modificada = self.img_com_contraste
        self.transforma_button_contraste.set(1.0)
    
    def acao_contraste(self, event):
        if self.imagem_modificada:
            img = ImageEnhance.Contrast(self.imagem_modificada).enhance(float(event))
            self.img_com_contraste = img
            self.image_sub_frame.configure(width=img.width)
            self.image_sub_frame.configure(height=img.height)
            img = ctk.CTkImage(light_image=img, 
                               dark_image=img, 
                               size=(img.width, img.height))
            self.image_frame_label.configure(image=img)
        elif self.imagem_original:
            img = Image.open(self.imagem_original)
            img = ImageEnhance.Contrast(img).enhance(float(event))
            self.img_com_contraste = img
            self.image_sub_frame.configure(width=img.width)
            self.image_sub_frame.configure(height=img.height)
            img = ctk.CTkImage(light_image=img, 
                               dark_image=img, 
                               size=(img.width, img.height))
            self.image_frame_label.configure(image=img)

if __name__ == "__main__":
    
    app = App()
    app.mainloop()