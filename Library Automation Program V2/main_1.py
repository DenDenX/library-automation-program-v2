"""
2.7.4

Last Updated: 19 May 2023
Last Test: 02.03.2024

"""

from tkinter import StringVar, Label, messagebox, filedialog as fd, PhotoImage, NSEW, END, CENTER
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Style, Treeview
from customtkinter import *
from modules_1 import *
from locale import setlocale, LC_ALL
from time import time, sleep



# Yerel ay gun ve sorgu kutulari
setlocale(category=LC_ALL, locale='')

# Gorunum modunu karanlik olarak ayarlama
set_appearance_mode("Dark")
set_default_color_theme('dark-blue')
 
class Program(): # Pogramin yapisi
    l = Log()
    l.log(f"Program konumu: {resource_path('')}")     
     
    def __init__(self, admin: bool = False):
        Program.l.log('1')
        Program.l.log(f'Program baslatildi:' + 'Admin' if admin == True else 'Program baslatildi:' +  "Nobetci")
        
        if admin == True:
            self.state = 'normal' 
            self.state2 = 'normal'           
        else:
            self.state = 'disabled'
            self.state2 = 'disabled'
        
        self.main = CTk() 
        Program.l.log('2    ')
        style = Style(self.main) 
        self.main.call("source", resource_path("forest-dark.tcl"))
        style.theme_use("forest-dark")  
        self.main.geometry("1366x748")
        self.main.title("FETGEM Kütüphane Otomasyon")
        self.main.minsize(1300, 650)
        
        def on_closing():
            result = messagebox.askyesno("Emin misiniz?", "Çıkmak istediğinizden emin misiniz?")
            if result:
                self.main.destroy()
                

        # Kapatma düğmesine bir fonksiyon atama
        self.main.protocol("WM_DELETE_WINDOW", on_closing)
        
        
        self.tabs = CTkTabview(self.main, corner_radius=12)

        self.tabs.insert(index= 0, name="        Alınacak Kitaplar       ")
        self.tabs.insert(index= 1, name="               Kitap Ver              ")
        self.tabs.insert(index= 2, name="       Öğrenci ve Kitap Listesi     ")
        if admin == True:
            self.tabs.insert(index= 3, name="    Öğrenci/ Kitap İşlemleri    ")
        self.tabs.insert(index= 4 if admin == True else 3, name="        Kullanım Kılavuzu       ")
        if admin == True:
            self.tabs.insert(index= 5 if admin == True else 4, name="                Ayarlar               ")
        
        self.tabs.place(x=0, y=0, relheight=0.956076135, relwidth=1)
        
        
        def oturumu_kapat():
            if messagebox.askyesno('Emin misiniz?', 'Oturumu kapatmak istediğinizden emin misiniz?'):
                self.main.destroy()
                start = BProgram()
                Program.l.log('Oturum Kapatildi')
        
        def _exit():
            if messagebox.askyesno('Emin misiniz?', 'Çıkmak istediğinizden emin misiniz?'):
                self.main.destroy()
                con.close()
                Program.l.log('Program Kapatildi')
                    
        user = CTkButton(self.main, text="Oturumu Kapat", command=oturumu_kapat, fg_color='#a34410', hover_color='#bd490b',corner_radius=15)
        user.place(relx=0.790, rely=0.960076135, relheight=0.033923865, relwidth=0.099)

        exit = CTkButton(self.main, width=40,text="Çıkış", command= _exit, fg_color='#a30f0f', hover_color='#ba0909',corner_radius=15)
        exit.place(relx=0.891, rely=0.960076135, relheight=0.033923865, relwidth=.099)
        
        c.execute("SELECT * FROM ogrenciler")
        con.commit()
        self.tOS = len(c.fetchall())
        
        c.execute("SELECT * FROM kitaplar")
        con.commit()
        self.tKS = len(c.fetchall())
            
        
        self.toplamKitapSayisiLabel = CTkLabel(self.main, text=f"Toplam Kitap Sayısı: {self.tKS}", corner_radius=30)
        self.toplamOgrenciSayisiLabel = CTkLabel(self.main, text=f"Toplam Öğrenci Sayısı: {self.tOS}", corner_radius=30 )
        self.saatLabel               = CTkLabel(self.main, text="Yükleniyor...", anchor='w', corner_radius=10)
        
        self.toplamKitapSayisiLabel.place(relx=0.490, rely=0.960046135, relheight=0.033923865, relwidth=0.280)
        self.toplamOgrenciSayisiLabel.place(relx=0.210, rely=0.960046135, relheight=0.033923865, relwidth=0.290)
        self.saatLabel              .place(relx=0.010, rely=0.960046135, relheight=0.033923865, relwidth=0.200)
        

        def saatGuncelle():
            
            self.saatLabel.configure(text=strftime('%T \t %' + 'd %B %A'))
            self.saatLabel.after(1000, saatGuncelle)
        
        self.saatLabel.after(1000, saatGuncelle)
        
        
        # |||||||||||||||||||||||||||||||\\
            
        Program.alinacakKitaplarOlustur(self)
        Program.kitapVerOlustur(self)
        Program.ogrKtpListeOlustur(self)
        if admin == True:

            Program.ogrKtpIslemleriOlustur(self)
        Program.kullanimKilavuzuOlustur(self)
        if admin == True:
            Program.ayarlarOlustur(self)
            
        # |||||||||||||||||||||||||||||||\\
    
        

        self.main.mainloop()     
        
##### Program ##################################################################################################333
    def kitapGuncelle(self, deger, set = False):
        if set == False:
            self.tKS += deger
            self.toplamKitapSayisiLabel.configure(text=f"Toplam Kitap Sayısı: {self.tKS}")
        else:
            self.tKS = deger
            self.toplamKitapSayisiLabel.configure(text=f"Toplam Kitap Sayısı: {self.tOS}")
            
            
    def ogrenciGuncelle(self, deger, set = False):
        if set == False:
            self.tOS += deger
            self.toplamOgrenciSayisiLabel.configure(text=f"Toplam Öğrenci Sayısı: {self.tOS}")
        else:
            self.tOS = deger
            self.toplamOgrenciSayisiLabel.configure(text=f"Toplam Öğrenci Sayısı: {self.tOS}")
        



    def alinacakKitaplarOlustur(self):
        
        
        self.anahtar1 = True
        

        columns = ["ogrenci", "kitap", "kalan_gun"]
        self.agac = Treeview(self.tabs.tab('        Alınacak Kitaplar       '), columns=columns, show="headings", height=32)
        self.alinacakKtpScroll = CTkScrollbar(self.tabs.tab('        Alınacak Kitaplar       '), command=self.agac.yview)
        self.alinacakKtpScroll.place(relx=0.985, relheight=1, relwidth=0.015)
        self.agac.configure(selectmode='browse')
        self.agac.heading("ogrenci",     text="Öğrenci")
        self.agac.heading("kitap",       text="Kitap")
        self.agac.heading("kalan_gun",   text="Kalan Gün")

        self.agac.column("ogrenci")
        self.agac.column("kitap")
        self.agac.column("kalan_gun")
        
        self.agac.place(relheight=1, relwidth=.985)
        self.tabs.tab('        Alınacak Kitaplar       ').columnconfigure(0, weight=1)
        self.tabs.tab('        Alınacak Kitaplar       ').rowconfigure(0, weight=1)

        c.execute("""SELECT * FROM kitaplarverildi ORDER BY tarih2""")
        veriler = c.fetchall()

        for veri in veriler:
            iid = str(veri[0]) + " " + str(veri[1])
            veri = veri_ver(veri[0], veri[1], veri[2])

            if int(veri[2]) < 0:
                self.agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("az"))
            elif int(veri[2]) < 1:
                self.agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("orta"))

            elif int(veri[2]) < 8:
                self.agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("normal"))

            else:
                self.agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=('uzak'))

        def soru():
            
            if self.anahtar1:
                return messagebox.askyesno(title="Kitabı al?", message="Kitabın teslim edildiğini onaylıyor musunuz?")
            else:
                self.anahtar1 = True
                
        def kitap_al_ttk(bos):
            
            if soru():
                iid = self.agac.selection()[0]
                self.agac.delete(iid)
                iid_bol = iid.split(" ")
                kitap_al(iid_bol[0], iid_bol[1])
                Program.l.ktp_al(iid_bol[0], iid_bol[1])
                self.agac.focus()
                self.anahtar1 = False
                

        self.agac.tag_configure("az",     background="red")
        self.agac.tag_configure("orta",   background="orange")
        self.agac.tag_configure("normal", background="blue")
        self.agac.configure(yscrollcommand=self.alinacakKtpScroll.set)
        self.agac.bind("<<TreeviewSelect>>", kitap_al_ttk)
        
    def kitapVerOlustur(self):
        
        bilgilendirme = CTkFrame(self.tabs.tab('               Kitap Ver              '), corner_radius=10)
        giris         = CTkFrame(self.tabs.tab('               Kitap Ver              '), corner_radius=10)

        bilgilendirme.place(relx=0.066 + .066 + .301, rely=0.1, relwidth=0.501, relheight=0.8)
        giris        .place(relx=0.066, rely=0.1, relwidth=0.301, relheight=0.8)

        self.tarih_se_var = IntVar()
        self.tarih_se_var.set(8)

        self.ktp_veri_var = StringVar()
        self.no_veri_var = StringVar()
        self.tarih_veri_var = StringVar()
        
        self.ktp_veri_var.set('Sorgu bekleniyor...')
        self.no_veri_var.set('Sorgu bekleniyor...')
        self.tarih_veri_var.set('Sorgu bekleniyor...')

        def kitap_ver_tk():
            
            if messagebox.askyesno(title="Onayla?", message="Kitabın ödünç verildiğini onaylıyor musunuz?"):
                
                sonuc = kitap_ver(self.barkod_e.get(), self.no_e.get(), int(self.tarih_se_var.get()))
                if  sonuc == 1:

                    self.agac.grid_forget()
                    Program.alinacakKitaplarOlustur(self)
                    Program.l.ktp_ver(self.barkod_e.get(), self.no_e.get(), int(self.tarih_se_var.get()))
                    
                else:
                    if sonuc == 0:
                        messagebox.showerror(title="Hata", message="İşlem Tamamlanamadı! Kitap veya öğrenci bulunamadı. Kitap önceden verilmiş olabilir.")
                    if sonuc == 3:
                        messagebox.showerror(title="Hata", message="İşlem Tamamlanamadı! Kitap öğrenciye daha önce verilmiş. Tekrar almak için önce Alınacak Kitaplar sekmesinden kitabı alınız.")
              
                self.ktp_veri_var.set('Sorgu bekleniyor...')
                self.no_veri_var.set('Sorgu bekleniyor...')
                self.tarih_veri_var.set('Sorgu bekleniyor...')
                self.onay_b.configure(state="disabled")

                self.barkod_e.delete(0, END)
                self.no_e.delete(0, END)

        def ktp_ver_sorgu():
            
                       
            
            if not (len(self.barkod_e.get()) == 0 or len(self.no_e.get()) == 0 or int(self.tarih_se_var.get()) == 0):
                
                int_bool = True
                ogr_bool = True
                ktp_bool = True
                
                try:
                    ogr_bool = kitap_ver_sorgu_ogr(self.no_e.get())
                    ktp_bool = kitap_ver_sorgu_barkod(self.barkod_e.get())
                except:
                    int_bool = False
                    
                if  ogr_bool and ktp_bool and int_bool:
                    
                    
                    c.execute("""SElECT ogrenci FROM ogrenciler WHERE no = (?)""", (self.no_e.get(),))
                    con.commit()

                    ogr_veri = c.fetchall()[0][0]

                    c.execute("""SElECT kitap FROM kitaplar WHERE barkod = (?)""", (self.barkod_e.get(),))
                    con.commit()

                    ktp_veri = c.fetchall()[0][0]                    
                    tarih = datetime.today() + timedelta(int(self.tarih_se_var.get()))
                    
                    
                    if len(ktp_veri) > 49:
                        ktp_adi_kisa = ''
                        for i in range(43):
                            ktp_adi_kisa = ktp_adi_kisa + ktp_veri[i]
                        ktp_adi_kisa = ktp_adi_kisa + '...'

                    else:
                        ktp_adi_kisa = ktp_veri


                    if len(ogr_veri) > 49:
                        ogr_adi_kisa = ''
                        for i in range(43):
                            ogr_adi_kisa = ogr_adi_kisa + ogr_veri[i]
                        ogr_adi_kisa = ogr_adi_kisa + '...'

                    else:
                        ogr_adi_kisa = ogr_veri

                    tarih_veri = str(tarih.strftime("%" + "d %B, %Y"))
                    
                    self.no_veri_var.set(ogr_adi_kisa)
                    self.ktp_veri_var.set(ktp_adi_kisa)
                    self.tarih_veri_var.set(tarih_veri)
                    
                    self.onay_b.configure(state="normal")


                else:
                    if int_bool:
                        if (ogr_bool or ktp_bool) == False:
                            
                            messagebox.showerror('Hata', 'Kitap ve öğrenci kaydı bulunamadı.')
                            
                        elif ogr_bool == False:
                            
                            messagebox.showerror('Hata', 'Öğrenci kaydı bulunamadı.')
                            
                        elif ktp_bool == False:
                            
                            messagebox.showerror('Hata', 'Kitap kaydı bulunamadı. Daha önceden verilmiş olabilir.')
                    else:
                        messagebox.showerror('Hata', 'Öğrenci no ve barkod tamsayı olmalıdır.')     
                                           
                    self.ktp_veri_var.set('Sorgu Bekleniyor...')
                    self.no_veri_var.set('Sorgu Bekleniyor...')
                    self.tarih_veri_var.set('Sorgu Bekleniyor...')
                    self.onay_b.configure(state='disabled')

            else:
                messagebox.showerror('Hata', 'Tüm alanları doldurunuz.')
   
        self.barkod_e       =   CTkEntry (giris, corner_radius=14,  placeholder_text="Barkod")
        self.no_e           =   CTkEntry (giris, corner_radius=14,  placeholder_text="Öğrenci No")
        self.tarih_se_lab   =   CTkLabel (giris, textvariable=self.tarih_se_var, width=50, height=40, corner_radius=10)
        self.tarih_se_lab2  =   CTkLabel (giris, text='Gün' ,width=50, height=40, corner_radius=10)
        self.tarih_se2      =   CTkSlider(giris, corner_radius=14, height=20, variable=self.tarih_se_var, from_= 1, to= 28)
        self.sorgu_b        =   CTkButton(giris, text='      Sorgu       ', command=ktp_ver_sorgu)

        self.onay_b         = CTkButton(bilgilendirme, text="   Kitabı Ver   ", command=kitap_ver_tk, state='disabled')

        self.ogr_bilg_label = CTkLabel(bilgilendirme, textvariable=self.no_veri_var)
        self.ktp_bilg_label = CTkLabel(bilgilendirme, textvariable=self.ktp_veri_var)
        self.trh_bilg_label = CTkLabel(bilgilendirme,  textvariable=self.tarih_veri_var)

        self.barkod_e      .place(relx=0.0625,  rely=0.118, relheight=0.094, relwidth=0.875)
        self.no_e          .place(relx=0.0625,  rely=0.308, relheight=0.094, relwidth=0.875)
        self.tarih_se2     .place(relx=0.0625,  rely=0.497, relheight=0.094, relwidth=0.710)
        self.tarih_se_lab  .place(relx=0.7555,  rely=0.497, relheight=0.094, relwidth=0.118)
        self.tarih_se_lab2 .place(relx=0.8335,  rely=0.497, relheight=0.094, relwidth=0.118)

        self.ogr_bilg_label.place(relx=0.125, rely=0.125)
        self.ktp_bilg_label.place(relx=0.125, rely=0.3)
        self.trh_bilg_label.place(relx=0.125, rely=0.475)

        self.sorgu_b       .place(relx=0.25, rely=0.822, relwidth=0.5, relheight=0.118)
        self.onay_b        .place(relx=0.25, rely=0.822, relwidth=0.5, relheight=0.118)

    def ogrKtpListeOlustur(self):     
        # self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(0, weight=50)
        # self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(1, weight=1)
        # self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(2, weight=50)
        # self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(3, weight=1)

        self.agac_o = Treeview(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), columns=["ogr", "no"], show="headings")
        
        self.agac_o.heading("ogr", text="Öğrenci")
        self.agac_o.heading("no", text="No")
        
        self.agac_o.column('no', width=5)
        self.agac_o.place(x=0, y=0, relwidth=.485, relheight=.94)
        


        self.agac_k = Treeview(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), columns=["ktp", "barkod"], show="headings")
        
        self.agac_k.heading("ktp", text="Kitap")
        self.agac_k.heading("barkod", text="Barkod")
        
        self.agac_k.column('barkod', width=5)        
        self.agac_k.place(relx=.5, y=0, relwidth=.485, relheight=.94)
        
        
        self.agacOScroll = CTkScrollbar(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), command=self.agac_o.yview)
        self.agacKScroll = CTkScrollbar(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), command=self.agac_k.yview)
        
        self.agacOScroll.place(relx=.485, y=0, relwidth=.015, relheight=1)
        self.agacKScroll.place(relx=.985, y=0, relwidth=.015, relheight=1)
        self.agac_o.configure(yscrollcommand=self.agacOScroll.set)
        self.agac_k.configure(yscrollcommand=self.agacKScroll.set)
 
        
        def ogrenci_yerlestir():
            c.execute("SELECT * FROM ogrenciler ORDER BY ogrenci")
            con.commit()
            ogr_liste = c.fetchall()
            for ogr in ogr_liste:
                self.agac_o.insert("", END, values=ogr)
                

        def kitap_yerlestir():
            c.execute("SELECT * FROM kitaplar ORDER BY kitap")
            con.commit()
            ktp_liste = c.fetchall()
            for ktp in ktp_liste:
                self.agac_k.insert("", END, values=ktp)
       

        def komut_k_xl():
            
            dosya_k_xl = fd.askopenfile(title="XLS dosyası", filetypes=[(".xls", "*.xls")])
            try:
                if excelden_aktar(ktp_excel_dosya=dosya_k_xl.name) == False:
                    messagebox.showerror('Hata', 'Beklenmeyen bir hata oluştu. Dosyanın .xls formatında ve erişilebilir oldugundan emin olun.')
                else:
                    Program.l.log(f'Kitaplar, {dosya_k_xl.name}, dosyasindan iceri aktarildi.')
                    self.agac_o.grid_forget()
                    self.agac_k.grid_forget()
                    Program.ogrKtpListeOlustur(self)
                    c.execute("SELECT * FROM kitaplar")
                    con.commit()
                    self.tKS = len(c.fetchall())
                    Program.kitapGuncelle(self, self.tKS, set=True)
            finally:
                pass           
            
                      
            
        def komut_o_xl():

            dosya_o_xl = fd.askopenfile(title="XLS dosyası", filetypes=[(".xls", "*.xls")])
            
            if dosya_o_xl != None:
                try:
                    if excelden_aktar(ogr_excel_dosya=dosya_o_xl.name) == False:
                        messagebox.showerror('Hata', 'Beklenmeyen bir hata oluştu. Dosyanın .xls formatında ve erişilebilir oldugundan emin olun.')
                    
                    else:
                        self.agac_o.destroy()
                        self.agac_k.destroy()
                        Program.ogrKtpListeOlustur(self)
                        Program.l.log('Ogrenciler, {dosya_o_xl.name} dosyasindan iceri aktarildi.')
                        c.execute("SELECT * FROM ogrenciler")
                        con.commit()
                        self.tOS = len(c.fetchall())
                        Program.ogrenciGuncelle(self, self.tOS, set=True)
                finally:
                    pass
                
                    self.agac_o.destroy()
                    self.agac_k.destroy()
                    Program.ogrKtpListeOlustur(self)

            
        buton_o_xl = CTkButton(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), text="İçeri Aktar", command=komut_o_xl, state=self.state2)
        buton_k_xl = CTkButton(self.tabs.tab('       Öğrenci ve Kitap Listesi     '), text="İçeri Aktar", command=komut_k_xl, state=self.state2)
        
        buton_o_xl.place(x=0, rely=.94, relwidth=.4857, relheight=.06)
        buton_k_xl.place(relx=.5, rely=.94, relwidth=.4857, relheight=.06)

        self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(0, weight=1)
        self.tabs.tab('       Öğrenci ve Kitap Listesi     ').columnconfigure(1, weight=1)
        self.tabs.tab('       Öğrenci ve Kitap Listesi     ').rowconfigure   (0, weight=30)
        self.tabs.tab('       Öğrenci ve Kitap Listesi     ').rowconfigure   (1, weight=1)



        kitap_yerlestir()
        ogrenci_yerlestir()

    def ogrKtpIslemleriOlustur(self):
        
        def komut_ogr_1():
            
            ogrAdi = self.ogr_adi_e.get()
            ogrNo = self.ogr_no_e.get()
            
            ogrAdiGirildi = False if ogrAdi == '' else True
            ogrNoGirildi = False if ogrNo == '' else True
            
            if ogrAdiGirildi and ogrNoGirildi:
                
                devam = False
                
                try:                   
                    ogrNo = int(ogrNo)
                    devam = True
                    
                except:
                    messagebox.showerror('Hata','Öğrenci no tamsayı olmalıdır.')
                    devam = False
                    
                if devam:
                    
                    if ogr_ekle(ogrAdi, ogrNo):
                        Program.l.ogr_ekle(ogrAdi, ogrNo)
                        
                        self.ogr_adi_e.delete(0, END)
                        self.ogr_no_e.delete(0, END)
                        self.agac_o.grid_forget()
                        self.agac_k.grid_forget()
                        Program.ogrKtpListeOlustur(self)
                        messagebox.showinfo('işlem tamamlandı', 'Öğrenci başarıyla kaydedildi.')
                        Program.ogrenciGuncelle(self, 1)
                        
                    else:
                        messagebox.showerror('Hata', 'Öğrenci no daha önce kaydedilmiş.')

            
            else:
                messagebox.showerror('Hata', 'Tüm alanları doldurunuz.')
                          
        
        def komut_ogr_2():
            
            ogrNoSil = self.ogr_no_sil_e.get()
            
            if ogrNoSil != '':
                
                devam = False
                
                try:
                    ogrNoSil = int(ogrNoSil)
                    devam = True
                    
                except:
                    messagebox.showerror('Hata','Öğrenci no tamsayı olmalıdır.')
                    
                    
                if devam:
                    ogr_sil(ogrNoSil)
                    Program.l.ogr_sil(ogrNoSil)
                    self.ogr_no_sil_e.delete(0, END)
                    
                    self.agac_o.grid_forget()
                    self.agac_k.grid_forget()
                    Program.ogrKtpListeOlustur(self)
                    messagebox.showinfo('işlem tamamlandı', 'Öğrenci kaydı başarıyla silindi.')
                    Program.ogrenciGuncelle(self, -1)    
        
            else:
                messagebox.showerror('Hata', 'Tüm alanları doldurunuz.')
    
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        
        def komut_ktp_1():
            ktpAdi = self.ktp_adi_e.get()
            ktpBarkod = self.ktp_no_e.get()
            
            ktpAdiGirildi = False if ktpAdi == '' else True
            ktpBarkodGirildi = False if ktpBarkod == '' else True
            
            if ktpAdiGirildi and ktpBarkodGirildi:
                devam = False
                
                try:
                    ktpBarkod = int(ktpBarkod)
                    devam = True
                    
                except:
                    devam = False
                    messagebox.showerror('Hata','Barkod tamsayı olmalıdır.')
                    
                if devam:
                    
                    kitap_ekle(ktpAdi, ktpBarkod)
                    Program.l.ktp_ekle(ktpAdi, ktpBarkod)
                    self.ktp_adi_e.delete(0, END)
                    self.ktp_no_e.delete(0, END)
                    self.agac_o.grid_forget()
                    self.agac_k.grid_forget()
                    Program.ogrKtpListeOlustur(self)
                    messagebox.showinfo('işlem tamamlandı', 'Kitap başarıyla kaydedildi.')
                    Program.kitapGuncelle(self, 1)    
                    
                                    
            
            else:
                messagebox.showerror('Hata', 'Tüm alanları doldurunuz.')
                
        
        def komut_ktp_2():
            
            ktpBarkodSil = self.ktp_no_sil_e.get()
            
            if ktpBarkodSil != '':
                
                devam = False
                
                try:
                    ktpBarkodSil = int(ktpBarkodSil)
                    devam = True
                    
                except:
                    messagebox.showerror('Hata','Barkod tamsayı olmalıdır.')
                    
                    
                if devam:
                    kitap_sil(ktpBarkodSil)
                    Program.l.ktp_sil(ktpBarkodSil)
                    
                    self.ktp_no_sil_e.delete(0, END)
                    
                    self.agac_o.grid_forget()
                    self.agac_k.grid_forget()
                    Program.ogrKtpListeOlustur(self)
                    messagebox.showinfo('işlem tamamlandı', 'Kitap kaydı başarıyla silindi.')
                    Program.kitapGuncelle(self, -1)    
        
            else:
                messagebox.showerror('Hata', 'Tüm alanları doldurunuz.')                             
        
        ogr_frame = CTkFrame(self.tabs.tab('    Öğrenci/ Kitap İşlemleri    '), corner_radius=10)
        ktp_frame = CTkFrame(self.tabs.tab('    Öğrenci/ Kitap İşlemleri    '), corner_radius=10)

        label_ogr = Label(self.tabs.tab('    Öğrenci/ Kitap İşlemleri    '), anchor="center", text="Öğrenci", font='ubuntu 15')
        label_ktp = Label(self.tabs.tab('    Öğrenci/ Kitap İşlemleri    '), anchor="center", text="Kitap"  , font='ubuntu 15')
        
        label_ogr.place(relx=0.1376, rely=0.18911, relwidth=0.292, relheight=0.09358)
        label_ktp.place(relx=0.5680, rely=0.18911, relwidth=0.292, relheight=0.09358)


        self.ogr_adi_e =     CTkEntry(ogr_frame, width=21, corner_radius=14, placeholder_text="Öğrenci adı")
        self.ogr_no_e =      CTkEntry(ogr_frame, width=21, corner_radius=14, placeholder_text="Öğrenci no")
        
        self.ogr_no_sil_e =  CTkEntry(ogr_frame, width=21, corner_radius=14, placeholder_text="Öğrenci no")
        
        ogr_onay =      CTkButton(ogr_frame, text="Ekle", command=komut_ogr_1, state=self.state)
        ogr_sil_onay =  CTkButton(ogr_frame, text="Sil", command=komut_ogr_2, state=self.state)


        self.ogr_adi_e     .place(relx=0.0625, rely=0.108, relheight=0.092, relwidth=0.875)
        self.ogr_no_e      .place(relx=0.0625, rely=0.258, relheight=0.092, relwidth=0.875)
        ogr_onay      .place(relx=0.25, rely=0.401, relwidth=0.5, relheight=0.092)
        
        self.ogr_no_sil_e  .place(relx=0.0625, rely=0.664, relheight=0.092, relwidth=0.875)
        ogr_sil_onay  .place(relx=0.25, rely=0.815, relwidth=0.5, relheight=0.092)



        self.ktp_adi_e =     CTkEntry(ktp_frame, width=21, corner_radius=14, placeholder_text="Kitap adı")
        self.ktp_no_e =      CTkEntry(ktp_frame, width=21, corner_radius=14, placeholder_text="Barkod")

        self.ktp_no_sil_e =  CTkEntry(ktp_frame, width=21, corner_radius=14, placeholder_text="Barkod")
        
        ktp_onay =           CTkButton(ktp_frame, text="Ekle", command=komut_ktp_1, state=self.state)
        ktp_sil_onay =       CTkButton(ktp_frame, text="Sil",command=komut_ktp_2, state=self.state)
        

        self.ktp_adi_e       .place(relx=0.0625, rely=0.108, relheight=0.092, relwidth=0.875)
        self.ktp_no_e        .place(relx=0.0625, rely=0.258, relheight=0.092, relwidth=0.875)
        ktp_onay             .place(relx=0.25, rely=0.401, relwidth=0.5, relheight=0.092)

        self.ktp_no_sil_e    .place(relx=0.0625, rely=0.664, relheight=0.092, relwidth=0.875)
        ktp_sil_onay         .place(relx=0.25, rely=0.815, relwidth=0.5, relheight=0.092)
        
        ogr_frame.place(relx=0.1376, rely=0.25869, relwidth=0.2928, relheight=0.5762) #188 146
        ktp_frame.place(relx=0.5680, rely=0.25869, relwidth=0.2928, relheight=0.5762) #776 146

    def kullanimKilavuzuOlustur(self):
        
        kk_text="""
        Kitap Verme
- Kitap Ver sekmesine gidiniz. 
- Üstteki giriş kutusuna kıtabın barkodunu ve alttaki giriş kutusuna kitabı alacak öğrencinin okul numarasını yazınız.
- Sorgula butonuna basınız.

Eğer kitap bulunamadı hatası verirse Öğrenciler Kitaplar sekmesinden kitabın kayıtlı olup olmadığını teyit ediniz.
Aynı şekilde öğrenci bulunamadı hatası verirse Öğrenciler Kitaplar sekmesinden öğrencinin kayıtlı olup olmadığını teyit ediniz.

- Hata yoksa sağdaki doğrulama kutusundan bilgileri kontrol ediniz.
- Bilgiler doğruysa Kitabı Ver butonuna basınız.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        Kitap Alma
- Alınacak Kitaplar sekmesine gidiniz. 
- Alınması istenen kitap kaydının üzerine bir kez tıklayınız ve ardından onay veriniz.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Öğrenci Ekleme
- Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci/Kitap İşlemleri sekmesine gidiniz.
- Öğrenci kutusunundaki Ekle butonunun üstündeki kutulara sırasıyla Öğrenci Adı ve Ögrenci No'sunu yazınız.
- Ekle butonuna basınız.

Uyarı
Öğrenci numarasının başında sıfır olmamalıdır.
Ögrenci adı giriş kutusuna sırasıyla "Sınıf", "/ işareti", "Şube (Büyük Harf)" ve "Öğrenci Adı" şeklinde yazılmalıdır.

Örnek: 10/C Yasin Karagöz
Örnek: 188

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Öğrenci Silme
- Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci/ Kitap işlemleri sekmesine gidilir.
- Öğrenci başlığı altındaki "Sil" butonunun üstündeki giriş kutusuna Öğrenci No'sunu yazınız ve ardından Sil butonuna basınız.

Dikkat!
Bu işlem geri alınamaz!

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Kitap Ekleme
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci/Kitap İşlemleri sekmesine gidiniz.
- Kitap kutusunundaki Ekle butonunun üstündeki kutulara sırasıyla Kitap Adı ve Kitap Barkodu'nu yazınız.
- Ekle butonuna basınız.

Uyarı!
Barkodun başında sıfır olmamalıdır.

Örnek: Don Kişot - Cermantes
Örnek: 1111111111111

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Kitap Silme
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci/ Kitap işlemleri sekmesine gidiniz.
- Kitap başlığı altındaki "Sil" butonunun üstündeki giriş kutusuna Kitap Barkodu'nu yazınız.
- Sil butonuna basınız.

Dikkat!
Bu işlem geri alınamaz!

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Dosyadan Öğrenci Aktarma
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci ve Kitap Listesi sekmesine gidiniz. 
- Öğrenci listesininin altındakı aktar butonuna basınız.
- Aktarmak istediğiniz XLS dosyasını seçiniz.
- Tamam butonuna basınız.

Dikkat!
Dosya aktarma işlemi sırasında tüm öğrenci kayıtları silinecektir. Bu işlem geri alınamaz!

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Dosyadan Kitap Aktarma
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Öğrenci ve Kitap Listesi sekmesine gidiniz.
- Kitap listesininin altındakı aktar butonuna basınız. Aktarmak istediğiniz XLS dosyasını seçiniz.
- Tamam butonuna basınız.

Dikkat!
Dosya aktarma işlemi sırasında tüm kitap kayıtları silinecektir. Bu işlem geri alınamaz!

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Şifre Değiştirme
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- yarlar sekmesine gidiniz. 
- Şifre Değiştirme kutusuna geliniz.
- Giriş kutularına sırasıyla şifesini değiştirmek istediğiniz kullanıcı adı ve ardından yeni şifrenizi giriniz.
- Şifre değiştir butonuna basınız.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Kilit Süresi Ayarlama
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Ayarlar sekmesine gidiniz.
- Kilit süresi kutusuna geliniz.
- Ayar kaydırağından kilit süresini ayarlayınız.
- Uygula butonuna basınız.

        Kilit Deneme Sayısı Ayarlama
Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Ayarlar sekmesine gidiniz.
- Kilit Deneme Sayısı kutusuna geliniz.
- Ayar kaydırağından Kilit Deneme Sayısını ayarlayınız.
- Uygula butonuna basınız.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        Kurtarma Şifresi Ayarlama
Kurtarma şifresi, şifrenizi unuttuğunuzda kullanabileceğiniz yedek şifrenizdir.
Maksimum hatalı giriş sayısına ulaştığınızda karşınıza çıkan kilit penceresi içerisindeki Kurtarma Şifresi Kullan butonuna basarak şifrelerinizi tekrar oluşturabilirsiniz.

Uyarı!
Yeni şifrelerinizi oluştururken uygulamayı kapatmak hatalara neden olabilir.

Bu işlem için yönetici hesabı ile giriş yapılmalıdır.

- Ayarlar sekmesine gidiniz.
- Kurtarma Şifresi Ayarla butonuna basınız.
- Gelen diyalog ekranına yeni kurtarma şifrenizi yazınız.
- Tamam butonuna basınız.
"""
        
        
        kk = CTkTextbox(self.tabs.tab('        Kullanım Kılavuzu       '), corner_radius=10)
        kk.insert(END, text=kk_text)
        kk.configure(state="disabled")
        
        kk.place(x=0, y=0, relwidth=1, relheight=1)     
        
    def ayarlarOlustur(self):
        
        c.execute('SELECT * FROM ayarlar')
        con.commit()
        
        tum_ayarlar = c.fetchall()
        
        kilit_suresi = tum_ayarlar[0][1]
        deneme_sayisi = tum_ayarlar[1][1]
        kurtarma_sifresi = tum_ayarlar[2][1]
        log_yazdir = tum_ayarlar[3][1]
       
                
        sifre_degistir_frame =      CTkFrame(self.tabs.tab('                Ayarlar               '))
        
        
        sifre_degistirme_baslik_label = Label(sifre_degistir_frame, text="Şifre Değiştirme", font='Ubuntu 15')
        
        self.kadi_e =   CTkEntry(sifre_degistir_frame, placeholder_text='Kullanıcı Adı')
        self.ysifre_e = CTkEntry(sifre_degistir_frame, placeholder_text='Yeni şifre')
        
        def sifre_degistir_main():
            kadi = self.kadi_e.get()
            ysifre = self.ysifre_e.get()
            
            if sifre_degistir(kadi, ysifre):
                Program.l.sifre_degistir(kadi, ysifre)
                messagebox.showinfo('İşlem Tamamlandı', 'Kullanıcı şifresi başarıyla değiştirildi.')
                Program.l.sifre_degistir(kadi, ysifre)
                self.kadi_e.delete(0, END)
                self.ysifre_e.delete(0, END)
                
            else:
                messagebox.showerror('Hata', 'Kullanıcı adı hatalı. Kontrol edip tekrar deneyin.')
                
        
        
        sifre_degistirme_onay_b = CTkButton(sifre_degistir_frame, text='Şifre Değiştir', command=sifre_degistir_main)
        
        sifre_degistirme_baslik_label.place(relx=.25, rely=.05, relwidth=.5, relheight=.2)
        self.kadi_e.place(relx=.25, rely=.35, relwidth=.5, relheight=.1)
        self.ysifre_e.place(relx=.25, rely=.50, relwidth=.5, relheight=.1)
        sifre_degistirme_onay_b.place(relx=.375, rely=.75, relwidth=.25, relheight=.1)
        
        sifre_degistir_frame.place(x = 0, y=0, relwidth=.4, relheight=.6)
        
        
        ##### KILIT SURESI ################################################################################
        
        
        kilit_suresi_frame =        CTkFrame(self.tabs.tab('                Ayarlar               '))
        kilit_suresi_baslik_label = Label(kilit_suresi_frame, text="Kilit Süresi", font='Ubuntu 15').place(relx=.25, rely=.05, relwidth=.5, relheight=.2)
        
        
        def kilitSuresiSliderEvent(x):
            self.kilit_suresi_slider_label.configure(text=f'Yanlış giriş yapıldığında {int(x)} dakika boyunca kilitle.')                
            kilit_suresi_onay_b.configure(state='normal')
            
            
        self.kilit_suresi_slider = CTkSlider(kilit_suresi_frame, from_=3, to=60, command=lambda x: kilitSuresiSliderEvent(x))
        self.kilit_suresi_slider_label = CTkLabel(kilit_suresi_frame, text=f'Maksimum yanlış giriş sayısına ulaşıldığında {kilit_suresi} dakika boyunca kilitle.')
        self.kilit_suresi_slider.set(int(kilit_suresi))
        
        def kilit_suresini_yenile():
            yeni_sure = int(self.kilit_suresi_slider.get())
            c.execute('''UPDATE ayarlar SET deger = ? WHERE ayar = 'kilit_suresi' ''', (yeni_sure,))
            con.commit()
            kilit_suresi = yeni_sure
            
            messagebox.showinfo(title="Tamamlandı", message="İşlem Tamamlandı")
            Program.l.log(f'Kilit suresi, {yeni_sure} e ayarlandi')
            kilit_suresi_onay_b.configure(state='disabled')
        
        
        kilit_suresi_onay_b = CTkButton(kilit_suresi_frame, text='Uygula', command=kilit_suresini_yenile, state='disabled')
        
        
        self.kilit_suresi_slider.place(relx=.25, rely=.35, relwidth=.5, relheight=.1)
        self.kilit_suresi_slider_label.place(relx=0, rely=.50, relwidth=1, relheight=.1)
        kilit_suresi_onay_b.place(relx=.375, rely=.75, relwidth=.25, relheight=.2)
        
        kilit_suresi_frame.place(relx =.4, y=0, relwidth=.6, relheight=.30)
                
        
        ### KILIT DENEME SAYISI ##########################################################################
        
        
        kilit_deneme_sayisi_frame =        CTkFrame(self.tabs.tab('                Ayarlar               '))
        kilit_deneme_sayisi_label = Label(kilit_deneme_sayisi_frame, text="Kilit Deneme Sayısı", font='Ubuntu 15').place(relx=.25, rely=.05, relwidth=.5, relheight=.2)
        
        def kilit_deneme_sayisi_yenile():
            deneme_sayisi = int(self.kilit_deneme_sayisi_slider.get())
            c.execute('UPDATE ayarlar SET deger = ? WHERE ayar = "deneme_sayisi"', (deneme_sayisi,))
            con.commit()
            messagebox.showinfo(title="Tamamlandı", message="İşlem Tamamlandı")
            Program.l.log(f'Maksimum kilit deneme sayisi {deneme_sayisi} e ayarlandi')
            kilit_deneme_sayisi_onay_b.configure(state='disabled')
            
            
        def kilitDenemeSayisiSliderEvent(x):
            self.kilit_deneme_sayisi_slider_label.configure(text=f'Kilit ekranında en fazla {int(x)} kez hatalı giriş yapılabilsin.')
            kilit_deneme_sayisi_onay_b.configure(state='normal')
            
        
        
        self.kilit_deneme_sayisi_slider = CTkSlider(kilit_deneme_sayisi_frame, from_=2 ,to=10, command=lambda x: kilitDenemeSayisiSliderEvent(x))
        self.kilit_deneme_sayisi_slider_label = CTkLabel(kilit_deneme_sayisi_frame, text=f'Kilit ekranında en fazla {deneme_sayisi} kez hatalı giriş yapılabilsin.')
        kilit_deneme_sayisi_onay_b = CTkButton(kilit_deneme_sayisi_frame, text='Uygula', command=kilit_deneme_sayisi_yenile, state='disabled')
        self.kilit_deneme_sayisi_slider.set(int(deneme_sayisi))
        
        self.kilit_deneme_sayisi_slider.place(relx=.25, rely=.35, relwidth=.5, relheight=.1)
        self.kilit_deneme_sayisi_slider_label.place(relx=0, rely=.50, relwidth=1, relheight=.1)
        kilit_deneme_sayisi_onay_b.place(relx=.375, rely=.75, relwidth=.25, relheight=.2)
        
        kilit_deneme_sayisi_frame.place(relx =.4, rely=.3, relwidth=.6, relheight=.3)
        
        ##### KURTARMA SIFRESI ##############################################################################     
       
        kurtarma_sifresi_frame =    CTkFrame(self.tabs.tab('                Ayarlar               '))
        
        def kurtarmaSifresiBelirle():
            self.kurtarmaSifresiDialog = CTkInputDialog(title='Kurtarma Şifresi Belirle', text="Yeni kurtarma şifresini giriniz.")
            kurtarmaSifresi = self.kurtarmaSifresiDialog.get_input()
            
            if kurtarmaSifresi != 'None' and kurtarmaSifresi != '' and kurtarmaSifresi != None:
            
                c.execute('''UPDATE ayarlar SET deger = ? WHERE ayar = "kurtarma_sifresi"''', (kurtarmaSifresi,))
                con.commit()
                messagebox.showinfo('İşlem Tamamlandı', 'Kurtarma şifreniz başarıyla oluşturuldu.')
                Program.l.log(f'Kurtarma Sifresi {kurtarmaSifresi} e ayarlandi')
        
        kurtarma_sifresi_frame_button = CTkButton(kurtarma_sifresi_frame, text="Kurtarma Şifresi Ayarla", font=('roboto', 15), command=kurtarmaSifresiBelirle)
        kurtarma_sifresi_frame_button.place(relx=.25, rely=.4, relwidth=.5, relheight=.2)
        
        
        kurtarma_sifresi_frame.place(x=0, rely=.6, relwidth=1, relheight=.4)
        
    
    
    
    
class BProgram(): # Kilit yapisi
    

    def __init__(self):
        
        c.execute("SELECT deger FROM ayarlar WHERE ayar = 'deneme_sayisi'")
        con.commit()
        
        self.maxYanlisGiris = int(c.fetchall()[0][0])
        
        c.execute("SELECT deger FROM ayarlar WHERE ayar = 'kilit_suresi'")
        con.commit()
        
        self.kilitSuresi = c.fetchall()[0][0]
        
        
        qfl = query_for_lock()
        if qfl == False:    
        
            c.execute("SELECT * FROM sifre")
            con.commit()
            sifreler = c.fetchall()

            
            if len(sifreler) < 2:
                BProgram.slayt(self)

            else:
                BProgram.sifreKontrol(self)

        else:
            BProgram.kilit(self, qfl)
                      
    def slayt(self, sifremi_unuttum = True):
        self.sayac = 2

        self.main = CTk()
        # self.main.iconify()
        # self.main.deiconify()

        
        style = Style(self.main)
        self.main.call("source", resource_path("forest-dark.tcl"))
        style.theme_use("forest-dark")
        self.main.resizable(False, False)
        self.main.title("Hoşgeldiniz")
        
        pht1 = PhotoImage(file=resource_path("1.png"))
        pht2 = PhotoImage(file=resource_path("2.png"))
        pht3 = PhotoImage(file=resource_path("3.png"))
        pht4 = PhotoImage(file=resource_path("4.png"))
        
        showImg = Label(self.main, image=pht2)
        showImg.pack(fill="both", anchor=CENTER)
        if sifremi_unuttum:

            def degistir(event):

                self.sayac += 1

                if self.sayac == 2:
                    showImg.configure(image=pht2)

                elif self.sayac == 3:
                    showImg.configure(image=pht3)

                elif self.sayac == 4:
                    showImg.configure(image=pht4)

                elif self.sayac == 5:
                    showImg.configure(image=pht1)
                    BProgram.sifreler_olustur(self)
                    
                else:
                    pass
            self.main.bind("<Button-1>", degistir)
        else:
            showImg.configure(image=pht1)        
            BProgram.sifreler_olustur(self)
        self.main.focus()
        
        self.main.mainloop()

    def sifreler_olustur(self):
        

        def y_n_onay_b_command(event=None):
            y_kadi = self.y_kadi_e  .get()
            y_sifre = self.y_sifre_e.get()
            n_kadi = self.n_kadi_e  .get()
            n_sifre = self.n_sifre_e.get()

            if y_kadi == "" or y_sifre == "" or  n_kadi == "" or n_sifre == "" :
                messagebox.showerror("Hata", "Tüm alanları doldurunuz!")

            elif y_kadi == n_kadi:
                messagebox.showerror("Hata", "Yönetici ve Nöbetçi kullanıcı adları aynı olamaz!")
                self.y_kadi_e.delete(0, END)
                self.n_kadi_e.delete(0, END)

            else:
                baslangic_sifre_olustur(y_kadi, y_sifre, n_kadi, n_sifre)
                messagebox.showinfo("İşlem Tamamlandı", 'Kullanıcılar başarıyla kaydedildi.')

                self.main.destroy()
                unlock()
                BProgram.sifreKontrol(self)
                

        self.y_kadi_e = CTkEntry(self.main, placeholder_text="Yönetici kullanıcı adı", corner_radius=20, bg_color='#454545')
        self.y_sifre_e = CTkEntry(self.main, placeholder_text="Yönetici şifre", corner_radius=20, bg_color='#454545')
        self.n_kadi_e = CTkEntry(self.main, placeholder_text="Nöbetçi kullanıcı adı", corner_radius=20, bg_color='#454545')
        self.n_sifre_e = CTkEntry(self.main, placeholder_text="Nöbetçi şifre", corner_radius=20, bg_color='#454545')

        self.y_n_onay_b = CTkButton(self.main, text="Kaydet", corner_radius=20, command= y_n_onay_b_command, bg_color='#303030')
        
        self.y_kadi_e.place(x=42, y=115, height=32, width=258)
        self.y_sifre_e.place(x=42, y=174, height=32, width=258)
        self.n_kadi_e.place(x=369, y=115, height=32, width=258)
        self.n_sifre_e.place(x=369, y=174, height=32, width=258)

        self.y_n_onay_b.place(x=248, y=275, height=32, width=172)

        self.main.bind("<Return>", y_n_onay_b_command)   

    ######################### Sifre Kontrol ##################################################################################

    def sifreKontrol(self):
        
        
        
        self.yanlis_giris_sayaci = 0

        self.main = CTk()
  
        style = Style(self.main)
        
        
        
        self.main.call("source", resource_path("forest-dark.tcl"))
        style.theme_use("forest-dark")
        self.main.title("FETGEM Kütüphane Otomasyon")
        self.main.geometry("668x352")
        self.main.resizable(False, False)
        
        def giris(event=None):

            kadi = self.giris_kadi_e.get()
            sifre = self.giris_sifre_e.get()

            if kadi == '' or sifre == '':
                
                messagebox.showerror("Hatalı Giriş", "Tüm alanları doldurunuz!")

            else:
                

                tf, ad_nb = sifre_kontrol(kadi, sifre)

        
                if tf is False:
                    
                    c.execute("""INSERT INTO programi_kilitle_2 VALUES ('.')""")
                    con.commit()
                    c.execute('SELECT * FROM programi_kilitle_2')
                    con.commit()
                    anlikYanlisGiris = len(c.fetchall())
                    self.yanlis_giris_sayaci = self.maxYanlisGiris - anlikYanlisGiris
                    messagebox.showerror("Hatalı Giriş", f"Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin!")
                    Program.l.yanlis_giris(kadi, sifre, anlikYanlisGiris)
                    self.kalan_sifre.configure(text=f'*{self.yanlis_giris_sayaci} deneme hakkınız kaldı.')
                    
                    if self.yanlis_giris_sayaci == 0:
                        messagebox.showwarning("Program Kilitlendi", f'Kullanıcı adı ve şifreyi {self.maxYanlisGiris} defa hatalı girdiniz. {self.kilitSuresi} dakika sonra tekrar deneyiniz.')
                        self.main.destroy()
                        lock()
                        c.execute('DELETE FROM programi_kilitle_2')
                        con.commit
                        Program.l.kilit(query_for_lock())
                        BProgram.kilit(self, query_for_lock())
                else:
                    c.execute('DELETE FROM programi_kilitle_2')
                    con.commit
                    self.main.destroy()
                    
                    if ad_nb == 1:

                        baslat = Program(admin=True)
                    else:
                        baslat = Program()

        self.main.bind("<Return>", giris)

        pht  = PhotoImage(file=resource_path('giris.png'))
        showImg = Label(self.main, text='', image=pht)
        showImg.place(x=0, y=0, relwidth=1, relheight=1)
        self.giris_kadi_e = CTkEntry(self.main, placeholder_text="Kullanıcı adı",corner_radius=20, bg_color="#444444")
        self.giris_sifre_e = CTkEntry(self.main, show="*", placeholder_text="Şifre",corner_radius=20, bg_color="#444444")

        onay_button = CTkButton(self.main, text="Giriş",corner_radius=20, bg_color="#444444", command=giris)

        self.giris_kadi_e.place(x=372, y=96, width=263, height=37)
        self.giris_sifre_e.place(x=372, y=155, width=263, height=37)

        onay_button.place(x=440, y=214, width=128, height=37)
        
        self.kalan_sifre = CTkLabel(self.main,text='', anchor='center', bg_color='#424242')
        self.kalan_sifre.place(x=372, y=260, width=263, height=15)
        self.main.focus()
        self.main.mainloop()
        
    ############################# Kilit ######################################################################################

    def kilit(self, acilacak_zaman):
        
        self.main = CTk()
        #self.main.iconify()
        #self.main.deiconify()
        
        def giris():
            self.main.destroy()
            unlock()
            BProgram.sifreKontrol(self)
            
            
        def kurtarmaSifresiniKullan():
            c.execute('SELECT deger FROM ayarlar WHERE ayar = "kurtarma_sifresi"')
            con.commit()
            deger = c.fetchall()[0][0]
            if deger == '':
                messagebox.showerror('Hata', 'Kurtarma şifresi belirtilmemiş.')
            else:
                kurtarmaSifresiKullanDialog = CTkInputDialog(title='Kurtarma Şifresi Kullan', text='Lütfen daha önceden belirlediğiniz kurtarma şifresini giriniz.')
                kurtarmaSifresi = kurtarmaSifresiKullanDialog.get_input()
                if kurtarmaSifresi != 'None' and kurtarmaSifresi != '' and kurtarmaSifresi != None:
                    
                    if kurtarmaSifresi == deger:
                    
                        self.main.destroy()
                        
                        BProgram.slayt(self, sifremi_unuttum=False)
                        
                    else:
                        messagebox.showerror('Hata', 'Girdiğiniz kurtarma şifresi hatalıdır. Lütfen tekrar deneyin')
        
        self.kilitLabel = CTkLabel(self.main, text='Yükleniyor...' , font=('Roboto', 20))
        
        self.girisButon = CTkButton(self.main, text='Giriş', state='disabled', command=giris)
        self.cikisButon = CTkButton(self.main, text='Kapat', command= lambda:self.main.destroy(), hover_color='#ba0909')
        self.kurtarmaSifresiButon = CTkButton(self.main, text='Kurtarma Şifresini Kullan', command= kurtarmaSifresiniKullan, hover_color='#176A07')
        
        def dongu():
            kalanZaman = acilacak_zaman - int(time())
            
            if kalanZaman > 0:
                
                kalanDk = kalanZaman // 60
                kalanSaniye = kalanZaman % 60
                self.kilitLabel.after(1000, dongu)
                self.kilitLabel.configure(text=f"{self.maxYanlisGiris} defa hatalı giriş yaptığınız için program geçici olarak kilitlendi.\n{kalanDk} dakika {kalanSaniye} saniye sonra giriş yapabilirsiniz." if kalanDk != 0 else f"5 defa hatalı giriş yaptığınız için program geçici olarak kilitlendi.\n{kalanSaniye} saniye sonra tekrar deneyebilirsiniz.")
                
            else:
                self.kilitLabel.configure(text='Kilit sona erdi "Giriş" butonuna basarak giriş yapabilirsiniz.')
                self.girisButon.configure(state='Enabled')
                self.kurtarmaSifresiButon.configure(state='disabled')
                unlock()
            
        
        
        self.kilitLabel.place(x = 0, rely=.3, relwidth = 1)
        self.kilitLabel.after(1000, dongu)
        
        self.girisButon.place(relx =.52, rely=.5, relwidth=.21)
        self.cikisButon.place(relx = .27, rely=.5, relwidth=.21)
        self.kurtarmaSifresiButon.place(relx = .30, rely=.65, relwidth=.40)
        

        
        self.main.geometry("668x352")
        self.main.resizable(False, False)
        self.main.title('Kilit')
        self.main.mainloop()
              
              

    
start = BProgram() if __name__ == '__main__' else None
