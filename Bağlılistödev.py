import tkinter as tk
from tkinter import messagebox, ttk

# ==========================
#  BAĞLI LİSTE SINIFLARI
# ==========================

class DersNode:
    def __init__(self, ders_kodu, harf_notu):
        self.ders_kodu = ders_kodu
        self.harf_notu = harf_notu
        self.next_ders = None


class OgrenciNode:
    def __init__(self, numara):
        self.numara = numara
        self.dersler_head = None  # her öğrencinin bağlı ders listesi bu öğrencinin ilk dersine bağlantılı
        self.next_ogrenci = None  # listedeki sonraki öğrenciye bağlantı 

        # yani her öğrenci kendi içinde ayrı bir bağlı ders listesi taşır


class OgrenciListesi:  # bu sınıf tüm sistemi yönetiyor bütün öğrenciler buradan ekleniyor siliniyor listeleniyor
    def __init__(self):
        self.head = None

    # --- 1. Derse yeni öğrenci ekleme ---
    def ogrenci_ekle(self, numara):
        yeni = OgrenciNode(numara)
        if not self.head:
            self.head = yeni
        else:
            current = self.head  # CURRENT : şuanda üzerinde durduğumuz düğüm
            while current.next_ogrenci:
                current = current.next_ogrenci
            current.next_ogrenci = yeni
        print(f"Öğrenci eklendi: {numara}")

    # --- 2. Öğrenciye ders ekleme ---
    def derse_ekle(self, numara, ders_kodu, harf_notu):
        ogr = self.ogrenci_bul(numara)
        if not ogr:
            messagebox.showerror("Hata", f"{numara} numaralı öğrenci bulunamadı.")
            return
        yeni_ders = DersNode(ders_kodu, harf_notu)
        if not ogr.dersler_head:
            ogr.dersler_head = yeni_ders
        else:
            current = ogr.dersler_head
            while current.next_ders:
                current = current.next_ders
            current.next_ders = yeni_ders
        print(f"{numara} numaralı öğrenciye {ders_kodu} dersi eklendi ({harf_notu})")

    # --- 3. Öğrenciden ders silme ---
    def ders_sil(self, numara, ders_kodu):
        ogr = self.ogrenci_bul(numara)
        if not ogr:
            messagebox.showerror("Hata", "Öğrenci bulunamadı.")
            return
        prev = None
        current = ogr.dersler_head
        while current:
            if current.ders_kodu == ders_kodu:
                if prev:
                    prev.next_ders = current.next_ders
                else:
                    ogr.dersler_head = current.next_ders
                print(f"{numara} numaralı öğrenciden {ders_kodu} dersi silindi.")
                return
            prev = current
            current = current.next_ders
        messagebox.showinfo("Bilgi", "Bu öğrenci bu dersi almıyor.")

    # --- 4. Bir öğrenciyi silme ---
    def ogrenci_sil(self, numara):
        prev = None
        current = self.head
        while current:
            if current.numara == numara:
                if prev:
                    prev.next_ogrenci = current.next_ogrenci
                else:
                    self.head = current.next_ogrenci
                print(f"{numara} numaralı öğrenci silindi.")
                return
            prev = current
            current = current.next_ogrenci
        messagebox.showinfo("Bilgi", "Öğrenci bulunamadı.")

    # --- 5. Tüm öğrencileri numaraya göre listele ---
    def ogrencileri_listele(self):
        liste = []
        current = self.head
        while current:
            liste.append(current.numara)
            current = current.next_ogrenci
        liste.sort()
        return liste

    # --- 6. Bir öğrencinin aldığı dersleri listele ---
    def ogrencinin_derslerini_listele(self, numara):
        ogr = self.ogrenci_bul(numara)
        if not ogr:
            return []
        dersler = []
        current = ogr.dersler_head
        while current:
            dersler.append((current.ders_kodu, current.harf_notu))
            current = current.next_ders
        dersler.sort(key=lambda x: x[0])
        return dersler

    def ogrenci_bul(self, numara):
        current = self.head
        while current:
            if current.numara == numara:
                return current
            current = current.next_ogrenci
        return None


# ==========================
#  TKINTER ARAYÜZÜ
# ==========================

class BagliListeApp:
    def __init__(self, root):
        self.liste = OgrenciListesi()
        self.root = root
        self.root.title("Bağlı Liste - Öğrenci ve Ders Sistemi")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        # Girdi alanları
        tk.Label(frame, text="Öğrenci No:").grid(row=0, column=0)
        self.numara_entry = tk.Entry(frame)
        self.numara_entry.grid(row=0, column=1)

        tk.Label(frame, text="Ders Kodu:").grid(row=1, column=0)
        self.ders_entry = tk.Entry(frame)
        self.ders_entry.grid(row=1, column=1)

        tk.Label(frame, text="Harf Notu:").grid(row=2, column=0)
        self.not_entry = tk.Entry(frame)
        self.not_entry.grid(row=2, column=1)

        # Butonlar
        tk.Button(frame, text="Öğrenci Ekle", command=self.ogrenci_ekle).grid(row=3, column=0, pady=5)
        tk.Button(frame, text="Ders Ekle", command=self.ders_ekle).grid(row=3, column=1)
        tk.Button(frame, text="Ders Sil", command=self.ders_sil).grid(row=4, column=0)
        tk.Button(frame, text="Öğrenci Sil", command=self.ogrenci_sil).grid(row=4, column=1)
        tk.Button(frame, text="Tüm Öğrencileri Listele", command=self.ogrencileri_listele).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Öğrencinin Derslerini Listele", command=self.dersleri_listele).grid(row=6, column=0, columnspan=2, pady=5)

        # Listeleme alanı
        self.text_area = tk.Text(frame, width=50, height=10)
        self.text_area.grid(row=7, column=0, columnspan=2, pady=10)

    # ==== ARAYÜZ FONKSİYONLARI ====

    def ogrenci_ekle(self):
        numara = self.numara_entry.get()
        if numara:
            self.liste.ogrenci_ekle(numara)
            messagebox.showinfo("Bilgi", f"{numara} numaralı öğrenci eklendi.")
        else:
            messagebox.showerror("Hata", "Öğrenci numarası giriniz.")

    def ders_ekle(self):
        numara = self.numara_entry.get()
        ders = self.ders_entry.get()
        notu = self.not_entry.get()
        if numara and ders and notu:
            self.liste.derse_ekle(numara, ders, notu)
            messagebox.showinfo("Bilgi", f"{numara} öğrencisine {ders} dersi eklendi.")
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurun.")

    def ders_sil(self):
        numara = self.numara_entry.get()
        ders = self.ders_entry.get()
        if numara and ders:
            self.liste.ders_sil(numara, ders)
        else:
            messagebox.showerror("Hata", "Numara ve ders kodu giriniz.")

    def ogrenci_sil(self):
        numara = self.numara_entry.get()
        if numara:
            self.liste.ogrenci_sil(numara)
        else:
            messagebox.showerror("Hata", "Öğrenci numarası giriniz.")

    def ogrencileri_listele(self):
        self.text_area.delete(1.0, tk.END)
        ogr_listesi = self.liste.ogrencileri_listele()
        if ogr_listesi:
            self.text_area.insert(tk.END, "Öğrenci Listesi (Sıralı):\n")
            for o in ogr_listesi:
                self.text_area.insert(tk.END, f"- {o}\n")
        else:
            self.text_area.insert(tk.END, "Hiç öğrenci yok.\n")

    def dersleri_listele(self):
        self.text_area.delete(1.0, tk.END)
        numara = self.numara_entry.get()
        if not numara:
            messagebox.showerror("Hata", "Öğrenci numarası giriniz.")
            return
        dersler = self.liste.ogrencinin_derslerini_listele(numara)
        if dersler:
            self.text_area.insert(tk.END, f"{numara} numaralı öğrencinin dersleri:\n")
            for d, n in dersler:
                self.text_area.insert(tk.END, f"- {d}: {n}\n")
        else:
            self.text_area.insert(tk.END, "Bu öğrencinin dersi yok.\n")


# ==========================
#  PROGRAMI ÇALIŞTIR
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = BagliListeApp(root)
    root.mainloop()
