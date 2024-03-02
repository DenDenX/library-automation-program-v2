"""

"""


from sqlite3 import Cursor, connect
from datetime import datetime, timedelta
from time import strftime
from time import time 
from xlrd import open_workbook, sys, os

# Database a baglanip isaretleyici belirleniyor.
con = connect("db.db")
c = con.cursor()

# Tablolar olusturuluyor.
c.execute("""CREATE TABLE IF NOT EXISTS ogrenciler(ogrenci text, no integer)""")
c.execute("""CREATE TABLE IF NOT EXISTS kitaplar(kitap text, barkod integer)""")
c.execute("CREATE TABLE IF NOT EXISTS kitaplarvar(barkod integer)")
c.execute("CREATE TABLE IF NOT EXISTS kitaplarverildi(barkod integer, no integer, tarih text, tarih2 integer)")
c.execute("""CREATE TABLE IF NOT EXISTS sifre (kadi text, sifre text)""")
c.execute("""CREATE TABLE IF NOT EXISTS programi_kilitle (zaman text)""")
c.execute("""CREATE TABLE IF NOT EXISTS programi_kilitle_2 (sayac text)""")
c.execute("""CREATE TABLE IF NOT EXISTS programi_kilitle_nobetci (true text)""")
c.execute("""CREATE TABLE IF NOT EXISTS ayarlar (ayar text, deger text)""")

# Ayarlar: Kilit Suresi
# Ayarlar: Deneme sayisi
# Ayarlar: Kurtarma sifresi
# Ayarlar: Sifre degistir
# Ayarlar: Log yazdir

c.execute('SELECT * FROM ayarlar')
con.commit()

if len(c.fetchall()) == 0:
    c.execute('DELETE FROM ayarlar')
    c.execute("INSERT INTO ayarlar VALUES('kilit_suresi', '15')")
    c.execute("INSERT INTO ayarlar VALUES('deneme_sayisi', '5')")
    c.execute("INSERT INTO ayarlar VALUES('kurtarma_sifresi', '')")
    c.execute("INSERT INTO ayarlar VALUES('log_yazdir', '1')")

    con.commit()




con.commit()

#############################################################################################################

def lock():
    '''
    Database de kayitli sure boyuncaprogramin calismasini engeller. Varsayilan olarak 15
    '''
    
    c.execute('SELECT deger FROM ayarlar WHERE ayar = "kilit_suresi"')
    con.commit()
    veri = c.fetchall()
    
    acilacak_zaman = str(int(time()) + int(veri[0][0]) * 60)
    
    c.execute("""INSERT INTO programi_kilitle VALUES (?)""", (acilacak_zaman,))
    con.commit()
    
def unlock():
    
    '''
    Programin kilidini kaldirir.
    '''
    
    c.execute('DELETE FROM programi_kilitle')
    con.commit()
    
    
def query_for_lock():
    
    """
    Database da kilit verisi olup olmadigini sorgular.
    Varsa sureyi yoksa False degerini donderir.
    """    
    c.execute('SELECT * FROM programi_kilitle')
    con.commit()
    veri = c.fetchall()
    
    try:
        return int(veri[0][0])
    except:
        return False
    
#############################################################################################################
    
def baslangic_sifre_olustur(admin, admin_sifre, nobetci, nobetci_sifre):
    
    '''
    Baslangicta yonetici ve nobetci kullanicilarinin sifrelerini olusturur.
    '''
    c.execute('''DELETE FROM sifre''')
    c.execute("""INSERT INTO sifre VALUES(?, ?)""", (admin, admin_sifre))
    c.execute("""INSERT INTO sifre VALUES(?, ?)""", (nobetci, nobetci_sifre))
    con.commit()
    
#############################################################################################################
    
def sifre_degistir(kadi, ksifre):
    '''
    Belirli bir kullanicinin sifresini degistirir.
    '''
        
    c.execute("""SELECT * FROM sifre WHERE kadi = ?""", (kadi,))
    con.commit()
    
    if len(c.fetchall()) != 0:

        c.execute("""UPDATE sifre SET sifre= (?) WHERE kadi= (?)""", (ksifre, kadi))
        con.commit()
        return True
    else:
        return False

#############################################################################################################

def liste_string(s):
    
    s[0] = int(s[0])
    s[1] = int(s[1])
    s[2] = int(s[2])
    str1 = datetime(s[0], s[1], s[2])
    time = str1.strftime('%d %B, %A')
    return time

#############################################################################################################

def sifre_kontrol(kadi, sifre):
    
    '''
    Girilen kullanici adinin sifresini kontrol eder.
    Giris dogru ise gecis anahtarini ve nobetci veya admin sifresi oldugunu dondurur.
    '''
    
    
    sayac = 0
    c.execute("SELECT * FROM sifre")
    con.commit()
    girisler = c.fetchall()
    anahtar = False
    for giris in girisler:
        print(giris[0], giris[1])
        if anahtar == False:
            sayac += 1
        if giris[0] == kadi and giris[1] == sifre:
            anahtar = True
        else:
            pass
    
    return anahtar, sayac

#############################################################################################################

def ogr_ekle(ogrenci, no):
    
    '''
    Ogrenci Adi Soyadi ve Subesini no ile birlikte database kaydeder.
    '''
    
    c.execute('SELECT * FROM ogrenciler WHERE no = ?', (no,))
    con.commit()
        
    if len(c.fetchall()) == 0:
        c.execute("""INSERT INTO ogrenciler VALUES (?, ?)""", (ogrenci, no))
        con.commit()
        return True
    else:
        return False

def ogr_sil(no):
    
    '''Girilen Ogrenci Nosunu siler.'''
    c.execute("""DELETE FROM ogrenciler WHERE no = ?""", (no,))
    con.commit()

#############################################################################################################

def kitap_ekle(kitap, barkod):
    
    '''Girilen Kitap Adi ve Barkodu database e ekler'''
    
    c.execute("""INSERT INTO kitaplar VALUES (?,?)""", (kitap, barkod))
    c.execute("""INSERT INTO kitaplarvar VALUES (?)""", (barkod,))
    con.commit()
    
def kitap_sil(barkod):
    ''''''
    
    c.execute("""DELETE FROM kitaplar WHERE rowid = (SELECT rowid FROM kitaplar WHERE barkod = ? LIMIT 1)""", (barkod,))
    c.execute("""DELETE FROM kitaplarvar WHERE rowid = (SELECT rowid FROM kitaplarvar WHERE barkod = ? LIMIT 1)""", (barkod,))
    con.commit()

#############################################################################################################

def kitap_ver(barkod, no, tarih):
    
    c.execute("""SELECT * FROM kitaplarverildi WHERE barkod = ? AND no = ?""", (barkod, no))
    con.commit()
    
    if len (c.fetchall()) == 0:

        now = datetime.today()
        days = timedelta(tarih)
        a = now + days
        tarih = f"{a.day}-{a.month}-{a.year}"

        tarih2String = f"{a.day}{a.month}{a.year}"
        
        sayac = len(tarih2String)
        tarih2 = ''
        while sayac > 0:
            tarih2 += tarih2String[sayac-1]
            sayac -= 1
            
        print('Tarih 2 : ', tarih2)
                    

        # tarih2 = tarih.split("-")
        # tarih2 = int(tarih2[0] + tarih2[1] + tarih2[2])

        c.execute("SELECT * FROM kitaplarvar WHERE barkod = ?", (barkod,))
        con.commit()
        
        if len(c.fetchall()) != 0:
            
            c.execute("DELETE FROM kitaplarvar WHERE rowid = (SELECT rowid FROM kitaplarvar WHERE barkod = ?)", (barkod,))
            c.execute("INSERT INTO kitaplarverildi VALUES(?, ?, ?, ?)", (barkod, no, tarih, tarih2))
            con.commit()

            return 1
        else:
            return 0
    else:
        return 3
        
def kitap_al(barkod, no):
    c.execute("DELETE FROM kitaplarverildi WHERE rowid = (SELECT rowid FROM kitaplarverildi WHERE barkod = ? AND no = ?)", (barkod, no))
    c.execute("INSERT INTO kitaplarvar VALUES(?)", (barkod,))
    con.commit()

#############################################################################################################

def zaman(tarih):

    bugun = datetime.today()
    t = tarih.split("-")
    t[0] = int(t[0])
    t[1] = int(t[1])
    t[2] = int(t[2])
    print(t)

    tarih = datetime(t[2], t[1], t[0])
    
    kalan_gun = tarih - bugun

    return kalan_gun.days

#############################################################################################################

def veri_ver(barkod, no, tarih):
    c.execute("SELECT ogrenci FROM ogrenciler WHERE no = ?", (no,))
    con.commit()
    try:
        ogrenci = c.fetchall()[0]
    except:
        ogrenci = ['{Veri Yok}']
    c.execute("SELECT kitap FROM kitaplar WHERE barkod = ?", (barkod,))
    con.commit()
    try:
        kitap_adi = c.fetchall()[0]
    except:
        kitap_adi = ['{Veri Yok}']
    kalan_gun = zaman(tarih)
    return ogrenci, kitap_adi, kalan_gun
 
 #############################################################################################################
 
#############################################################################################################
 
def spinbox_tarih():
    liste = []
    for i in range(60):
        b = strftime("%Y %m %d").split(" ")
        b[0] = int(b[0])
        b[1] = int(b[1])
        b[2] = int(b[2])
        bugun = datetime(b[0],b[1],b[2])
        bugun = bugun + timedelta(i)
        bugun = str(bugun).split(" ")[0]
        
        liste.append(bugun)
    return liste

#############################################################################################################

def excelden_aktar(ogr_excel_dosya=None, ktp_excel_dosya=None):
    
    if True:
        if ogr_excel_dosya != None and ogr_excel_dosya != "":
            
            c.execute("DELETE FROM ogrenciler")
            con.commit()
            wb = open_workbook(ogr_excel_dosya)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)
            for i in range(sheet.nrows):
                isim = sheet.cell_value(i, 0)
                no = sheet.cell_value(i, 1)
                c.execute("""INSERT INTO ogrenciler VALUES (?, ?)""", (isim, no))
            con.commit()

                
                
        if ktp_excel_dosya != None and ktp_excel_dosya != "":
            c.execute("DELETE FROM kitaplar")
            c.execute("DELETE FROM kitaplarvar")
            c.execute("DELETE FROM kitaplarverildi")
            con.commit()
    
            wb = open_workbook(ktp_excel_dosya)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)

            for i in range(sheet.nrows):
                isim = sheet.cell_value(i, 0)
                barkod = int(sheet.cell_value(i, 1))
                
                c.execute("""INSERT INTO kitaplar VALUES (?,?)""", (isim, barkod))
                c.execute("""INSERT INTO kitaplarvar VALUES (?)""", (barkod,))
            con.commit()
        return True   

#############################################################################################################

def kitap_ver_sorgu_barkod(barkod):

    
    c.execute("""SELECT * FROM kitaplarvar WHERE barkod = (?)""", (int(barkod),))
    con.commit()

    if len(c.fetchall()) > 0:
        return True
    else:
        return False
   
def kitap_ver_sorgu_ogr(ogr):
    
        
    c.execute("""SELECT * FROM ogrenciler WHERE no = (?)""", (int(ogr),))
    con.commit()
    veri = c.fetchall()
    print(veri)

    if len(veri) > 0:
        return True     
    else:
        return False

#############################################################################################################

def resource_path(relative_path):
    """For pyinstaller add-data"""
    
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
 
    return os.path.join(base_path, relative_path)


class Log():
    
    def __init__(self):
        with open('allLog.txt', 'a+') as log:
            pass
    ayrac = ''' | '''
        
    def log(self, yaz):
        yaz = str(yaz)
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Log                : {yaz}\n''')\
                  
    def kilit(self, zaman):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Kilit              : {zaman} sure boyunca kilitlendi.\n''')\
    
    def yanlis_giris(self, kadi, ksifre, kez):
        
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Yalnis giris       : K: {kadi} S:{ksifre} => {kez} kez yalnis giris yapildi. \n''')
            
    def ogr_ekle(self, ogradi, no):
        
        ogradi = str(ogradi)
        no = str(no)
        
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Ogrenci Ekleme     : {ogradi}, {no}\n''')
            
    def ogr_sil(self, no):
        no = str(no)
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Ogrenci Silme      : {no}\n''')

    def ktp_sil(self, barkod):
        
        barkod = str(barkod)
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Kitap Silme        : {barkod}\n''')
            
    def ktp_ekle(self, ktpadi, barkod):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Kitap Ekleme       : {ktpadi}, {barkod}\n''')
            
    def ktp_ver(self, barkod, no, tarih):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Kitap Verildi      : {barkod}, {no}, {tarih}\n''')
            
    def ktp_al(self, barkod, no):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Kitap Alindi       : {barkod}, {no}\n''')
            
    def sifre_degistir(self, kullanici, ysifre):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Sifre Degistirme   : {kullanici}, {ysifre}\n''')
            
    def ayar_degistir(self, ayaradi, ayardegeri):
        with open('allLog.txt', 'a+') as log:
            time = strftime('%d-%m-%Y | %H:%M:%S |')
            log.write(f'''{time} || Ayar Degistirme    : {ayaradi}, {ayardegeri}\n''')
    
        
    
