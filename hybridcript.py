import os
import sys
import json
import base64
import secrets
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any

try:
    from Crypto.Cipher import AES, PKCS1_OAEP
    from Crypto.PublicKey import RSA, DSA
    from Crypto.Signature import DSS, pkcs1_15
    from Crypto.Random import get_random_bytes
    from Crypto.Protocol.KDF import HKDF
    from Crypto.Hash import SHA256
except ImportError:
    print("=" * 80)
    print("ERROR: Library pycryptodome belum terpasang!")
    print("=" * 80)
    print("\nInstall dengan perintah:")
    print("  pip install pycryptodome")
    sys.exit(1)

BANNER = '''
+==============================================================================+
|                SISTEM PENGAMANAN HIBRIDA KRIPTOGRAFI                         |
|          AES-GCM | RSA | DSA | SHA-256 | DH-RSA | LSB Terintegrasi           |
|                       HAVIDZ ANDRIAN - 2311118999                            |                                                                  
+==============================================================================+
'''

PESAN = {
    "terima_kasih": "Terima Kasih Telah Menggunakan Program Ini :)",
    "menu_awal": "Pilih untuk melanjutkan:",
    "mulai": "1. Mulai",
    "selesai_awal": "2. Selesai",
    "pilih_awal": "Pilih opsi (1-2)",
    "pilihan_tidak_valid": "Pilihan tidak valid!",
    "status_sistem": "STATUS SISTEM SAAT INI:",
    "komponen": "Komponen",
    "status": "Status",
    "aktif": "AKTIF",
    "nonaktif": "NONAKTIF",
    "menu_utama": "MENU UTAMA:",
    "manajemen_kunci": "MANAJEMEN KUNCI",
    "enkripsi_dekripsi": "ENKRIPSI & DEKRIPSI",
    "tanda_tangan": "TANDA TANGAN DIGITAL",
    "steganografi": "STEGANOGRAFI",
    "sistem": "SISTEM",
    "menu_1": "1. Generate Kunci RSA + DSA",
    "menu_2": "2. Pertukaran Kunci Diffie-Hellman + RSA Signature",
    "menu_3": "3. Hash Teks (SHA-256)",
    "menu_4": "4. Enkripsi Hibrida (AES-GCM + RSA)",
    "menu_5": "5. Dekripsi Hibrida (AES-GCM + RSA)",
    "menu_6": "6. Tanda Tangani Pesan (DSA + SHA-256)",
    "menu_7": "7. Verifikasi Tanda Tangan",
    "menu_8": "8. Sembunyikan Pesan Aman ke Gambar (Crypto + Stego)",
    "menu_9": "9. Ekstrak Pesan Aman dari Gambar",
    "menu_10": "10. Tampilkan Riwayat Eksperimen",
    "menu_0": "0. Keluar Program",
    "pilih_menu": "Pilih menu (0-10)",
    "menu_tidak_valid": "Menu tidak valid!",
    "opsi_selanjutnya": "OPSI SELANJUTNYA:",
    "lanjutkan": "1. Lanjutkan eksperimen",
    "simpan_lanjut": "2. Simpan hasil & lanjutkan",
    "selesai": "0. Selesai (keluar program)",
    "pilih_opsi": "Pilih opsi (0-2)",
    "program_selesai": "Terima Kasih Telah Menggunakan Program Ini :)",
    "judul_generate": "GENERATE KUNCI RSA + DSA",
    "ukuran_rsa": "Ukuran kunci RSA (2048/4096)",
    "ukuran_dsa": "Ukuran kunci DSA (2048/3072)",
    "buat_rsa": "Sedang membuat kunci RSA...",
    "buat_dsa": "Sedang membuat kunci DSA...",
    "kunci_berhasil": "Kunci berhasil dibuat!",
    "judul_dh": "PERTUKARAN KUNCI DIFFIE-HELLMAN + RSA SIGNATURE",
    "proses_dh": "Melakukan pertukaran kunci terautentikasi...",
    "dh_berhasil": "Pertukaran kunci berhasil!",
    "publik_alice": "Kunci Publik DH Alice",
    "publik_bob": "Kunci Publik DH Bob",
    "shared_cocok": "Shared Secret Cocok",
    "kunci_aes": "Kunci AES-256 (Base64)",
    "judul_hash": "HASH TEKS - SHA-256",
    "masukkan_teks_hash": "Masukkan teks yang akan di-hash",
    "input": "Input",
    "judul_encrypt": "ENKRIPSI HIBRIDA - AES-GCM + RSA",
    "rsa_belum": "ERROR: RSA public key belum tersedia. Generate keys terlebih dahulu!",
    "masukkan_plaintext": "Masukkan plaintext",
    "sumber_aes": "Sumber kunci AES:",
    "pakai_dh": "1. Gunakan session key dari Diffie-Hellman",
    "kunci_baru": "2. Generate kunci baru",
    "pilih_1_2": "Pilih (1/2)",
    "gunakan_dh": "Menggunakan session key dari DH",
    "aes_baru": "Generate kunci AES baru",
    "sedang_enkripsi": "Melakukan enkripsi...",
    "enkripsi_berhasil": "Enkripsi berhasil!",
    "paket_enkripsi": "Paket terenkripsi:",
    "judul_decrypt": "DEKRIPSI HIBRIDA - AES-GCM + RSA",
    "decrypt_belum": "ERROR: RSA private key atau ciphertext tidak tersedia!",
    "sedang_dekripsi": "Melakukan dekripsi...",
    "plaintext": "Plaintext",
    "cocok_asli": "Cocok dengan data asli",
    "ya": "YA",
    "tidak": "TIDAK",
    "judul_sign": "TANDA TANGAN DIGITAL - DSA + SHA-256",
    "dsa_belum": "ERROR: DSA private key belum tersedia. Generate keys terlebih dahulu!",
    "masukkan_pesan_ttd": "Masukkan pesan untuk ditandatangani",
    "sedang_ttd": "Membuat tanda tangan digital...",
    "ttd_berhasil": "Tanda tangan digital berhasil dibuat!",
    "signature": "Signature (Base64)",
    "verifikasi": "Verifikasi",
    "valid": "VALID",
    "tidak_valid": "TIDAK VALID",
    "judul_verify": "VERIFIKASI TANDA TANGAN DIGITAL",
    "verify_belum": "ERROR: DSA public key atau signature tidak tersedia!",
    "mode_verify": "Mode verifikasi:",
    "verify_asli": "1. Verifikasi dengan pesan asli yang tersimpan",
    "verify_baru": "2. Verifikasi dengan pesan baru",
    "masukkan_pesan_verify": "Masukkan pesan untuk diverifikasi",
    "integritas": "Integritas",
    "autentik": "Autentik dan utuh",
    "tidak_autentik": "Tidak autentik atau telah diubah",
    "judul_stego_hide": "STEGANOGRAFI TERINTEGRASI - SEMBUNYIKAN PESAN AMAN",
    "pilih_cover": "Pilih cover image:",
    "generate_demo": "1. Generate demo BMP",
    "pakai_bmp": "2. Gunakan file BMP yang sudah ada",
    "lebar": "Lebar gambar (pixel)",
    "tinggi": "Tinggi gambar (pixel)",
    "demo_dibuat": "Demo BMP dibuat",
    "path_cover": "Path file BMP cover",
    "file_tidak_ditemukan": "ERROR: File tidak ditemukan",
    "masukkan_pesan_rahasia": "Masukkan pesan rahasia",
    "nama_output": "Nama file output",
    "sembunyikan": "Menyembunyikan paket terenkripsi ke dalam gambar...",
    "stego_berhasil": "Pesan berhasil disembunyikan!",
    "cover": "Cover",
    "output": "Output",
    "bit_disisipkan": "Bits disisipkan",
    "ukuran_pesan": "Ukuran pesan",
    "judul_stego_extract": "STEGANOGRAFI TERINTEGRASI - EKSTRAK PESAN AMAN",
    "path_stego": "Path file stego BMP",
    "ekstrak": "Mengekstrak paket terenkripsi dari gambar...",
    "ekstrak_berhasil": "Pesan berhasil diekstrak!",
    "file": "File",
    "pesan": "Pesan",
    "panjang": "Panjang",
    "judul_history": "RIWAYAT EKSPERIMEN",
    "history_kosong": "Belum ada eksperimen yang dilakukan.",
    "total_eksperimen": "Total eksperimen",
    "waktu": "Waktu",
    "aksi": "Aksi",
    "detail": "Detail",
    "error": "ERROR",
    "eksperimen_ke": "EKSPERIMEN",
    "pemisah": "=" * 80,
    "pemisah_kecil": "-" * 80,
}

class CryptoSession:
    def __init__(self):
        self.data = {
            "dh_params": None,
            "aes_key": None,
            "last_cipher": None,
            "last_signature": None,
            "last_plaintext": None,
            "rsa_private": None,
            "rsa_public": None,
            "dsa_private": None,
            "dsa_public": None,
            "last_stego_file": None,
            "last_extracted_message": None,
            "last_integrated_packet": None
        }
        self.experiment_history = []
        self.experiment_count = 0
        self.load_log()

    def load_log(self):
        try:
            if Path("experiment_log.json").exists():
                with open("experiment_log.json", "r", encoding="utf-8") as f:
                    self.experiment_history = json.load(f)
                if self.experiment_history:
                    self.experiment_count = self.experiment_history[-1]["id"]
        except Exception:
            self.experiment_history = []

    def save_log(self):
        with open("experiment_log.json", "w", encoding="utf-8") as f:
            json.dump(self.experiment_history, f, indent=2, default=str)

    def add_experiment(self, action: str, details: Dict[str, Any]):
        self.experiment_count += 1
        entry = {
            "id": self.experiment_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details
        }
        self.experiment_history.append(entry)
        self.save_log()

    def get_status(self) -> Dict[str, bool]:
        return {
            "Diffie-Hellman + RSA Auth": bool(self.data["dh_params"]),
            "AES Session Key": bool(self.data["aes_key"]),
            "RSA Keys": bool(self.data["rsa_private"]),
            "DSA Keys": bool(self.data["dsa_private"]),
            "Last Ciphertext": bool(self.data["last_cipher"]),
            "Last Signature": bool(self.data["last_signature"]),
            "Last Stego File": bool(self.data["last_stego_file"])
        }

class CryptoCore:
    @staticmethod
    def bytes_to_b64(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def b64_to_bytes(data: str) -> bytes:
        return base64.b64decode(data.encode("utf-8"))

    @staticmethod
    def sha256_hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_rsa_keys(bits: int = 2048) -> Tuple:
        private_key = RSA.generate(bits)
        public_key = private_key.publickey()
        return private_key, public_key

    @staticmethod
    def generate_dsa_keys(bits: int = 2048) -> Tuple:
        private_key = DSA.generate(bits)
        public_key = private_key.publickey()
        return private_key, public_key

    @staticmethod
    def aes_encrypt(plaintext: str, key: bytes) -> Tuple[bytes, bytes, bytes]:
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
        return cipher.nonce, ciphertext, tag

    @staticmethod
    def aes_decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes) -> str:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")

    @staticmethod
    def rsa_encrypt_key(aes_key: bytes, public_key) -> bytes:
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(aes_key)

    @staticmethod
    def rsa_decrypt_key(encrypted_key: bytes, private_key) -> bytes:
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(encrypted_key)

    @staticmethod
    def sign_message(message: str, private_key) -> bytes:
        h = SHA256.new(message.encode("utf-8"))
        signer = DSS.new(private_key, "fips-186-3")
        return signer.sign(h)

    @staticmethod
    def verify_signature(message: str, signature: bytes, public_key) -> bool:
        h = SHA256.new(message.encode("utf-8"))
        verifier = DSS.new(public_key, "fips-186-3")
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def rsa_sign_bytes(data: bytes, private_key) -> bytes:
        h = SHA256.new(data)
        return pkcs1_15.new(private_key).sign(h)

    @staticmethod
    def rsa_verify_bytes(data: bytes, signature: bytes, public_key) -> bool:
        h = SHA256.new(data)
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def diffie_hellman_key_exchange_authenticated() -> Tuple[Dict[str, Any], bytes]:
        p = int(
            "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
            "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
            "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
            "E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF",
            16
        )
        g = 2

        alice_private = secrets.randbelow(p - 2) + 2
        bob_private = secrets.randbelow(p - 2) + 2

        alice_public = pow(g, alice_private, p)
        bob_public = pow(g, bob_private, p)

        alice_rsa_private, alice_rsa_public = CryptoCore.generate_rsa_keys(2048)
        bob_rsa_private, bob_rsa_public = CryptoCore.generate_rsa_keys(2048)

        alice_public_bytes = str(alice_public).encode("utf-8")
        bob_public_bytes = str(bob_public).encode("utf-8")

        alice_signature = CryptoCore.rsa_sign_bytes(alice_public_bytes, alice_rsa_private)
        bob_signature = CryptoCore.rsa_sign_bytes(bob_public_bytes, bob_rsa_private)

        alice_verified = CryptoCore.rsa_verify_bytes(alice_public_bytes, alice_signature, alice_rsa_public)
        bob_verified = CryptoCore.rsa_verify_bytes(bob_public_bytes, bob_signature, bob_rsa_public)

        if not (alice_verified and bob_verified):
            raise ValueError("Autentikasi RSA pada public key DH gagal")

        alice_shared = pow(bob_public, alice_private, p)
        bob_shared = pow(alice_public, bob_private, p)

        if alice_shared != bob_shared:
            raise ValueError("Shared secret DH tidak cocok")

        shared_bytes = alice_shared.to_bytes((alice_shared.bit_length() + 7) // 8, "big")
        aes_key = HKDF(shared_bytes, 32, b"SALT-AES-KEY", SHA256)

        dh_params = {
            "p": p,
            "g": g,
            "alice_public": alice_public,
            "bob_public": bob_public,
            "alice_signature": CryptoCore.bytes_to_b64(alice_signature),
            "bob_signature": CryptoCore.bytes_to_b64(bob_signature),
            "alice_rsa_public_pem": alice_rsa_public.export_key().decode("utf-8"),
            "bob_rsa_public_pem": bob_rsa_public.export_key().decode("utf-8"),
            "alice_verified": alice_verified,
            "bob_verified": bob_verified,
            "shared_secret": alice_shared,
            "shared_match": alice_shared == bob_shared,
            "authenticated": alice_verified and bob_verified
        }
        return dh_params, aes_key

    @staticmethod
    def build_integrated_secure_packet(message: str, dsa_private, rsa_public) -> Dict[str, Any]:
        message_hash = CryptoCore.sha256_hash(message)
        signature = CryptoCore.sign_message(message, dsa_private)

        signed_payload = {
            "message": message,
            "hash": message_hash,
            "signature": CryptoCore.bytes_to_b64(signature),
            "signature_algorithm": "DSA-SHA256"
        }

        aes_key = get_random_bytes(32)
        payload_json = json.dumps(signed_payload, ensure_ascii=False)
        nonce, ciphertext, tag = CryptoCore.aes_encrypt(payload_json, aes_key)
        encrypted_key = CryptoCore.rsa_encrypt_key(aes_key, rsa_public)

        packet = {
            "scheme": "HYBRID-STEGO-INTEGRATED-V2",
            "aes_mode": "AES-GCM",
            "rsa_mode": "RSA-OAEP",
            "payload_format": "JSON",
            "nonce": CryptoCore.bytes_to_b64(nonce),
            "ciphertext": CryptoCore.bytes_to_b64(ciphertext),
            "tag": CryptoCore.bytes_to_b64(tag),
            "encrypted_key": CryptoCore.bytes_to_b64(encrypted_key),
            "timestamp": datetime.now().isoformat()
        }
        return packet

    @staticmethod
    def extract_integrated_secure_packet(packet: Dict[str, Any], rsa_private, dsa_public) -> Dict[str, Any]:
        encrypted_key = CryptoCore.b64_to_bytes(packet["encrypted_key"])
        nonce = CryptoCore.b64_to_bytes(packet["nonce"])
        ciphertext = CryptoCore.b64_to_bytes(packet["ciphertext"])
        tag = CryptoCore.b64_to_bytes(packet["tag"])

        aes_key = CryptoCore.rsa_decrypt_key(encrypted_key, rsa_private)
        payload_json = CryptoCore.aes_decrypt(nonce, ciphertext, tag, aes_key)
        signed_payload = json.loads(payload_json)

        message = signed_payload["message"]
        stored_hash = signed_payload["hash"]
        signature = CryptoCore.b64_to_bytes(signed_payload["signature"])

        recomputed_hash = CryptoCore.sha256_hash(message)
        hash_valid = stored_hash == recomputed_hash
        signature_valid = CryptoCore.verify_signature(message, signature, dsa_public)

        return {
            "message": message,
            "stored_hash": stored_hash,
            "recomputed_hash": recomputed_hash,
            "hash_valid": hash_valid,
            "signature_valid": signature_valid,
            "integrity_valid": hash_valid and signature_valid,
            "signature_algorithm": signed_payload.get("signature_algorithm", "DSA-SHA256")
        }

class SteganographyLSB:
    @staticmethod
    def generate_demo_bmp(path: str = "demo_cover.bmp", width: int = 256, height: int = 256):
        row_size = (width * 3 + 3) & ~3
        pixel_data_size = row_size * height
        file_size = 54 + pixel_data_size

        header = bytearray()
        header.extend(b"BM")
        header.extend(file_size.to_bytes(4, "little"))
        header.extend((0).to_bytes(4, "little"))
        header.extend((54).to_bytes(4, "little"))

        dib = bytearray()
        dib.extend((40).to_bytes(4, "little"))
        dib.extend(width.to_bytes(4, "little"))
        dib.extend(height.to_bytes(4, "little"))
        dib.extend((1).to_bytes(2, "little"))
        dib.extend((24).to_bytes(2, "little"))
        dib.extend((0).to_bytes(4, "little"))
        dib.extend(pixel_data_size.to_bytes(4, "little"))
        dib.extend((2835).to_bytes(4, "little"))
        dib.extend((2835).to_bytes(4, "little"))
        dib.extend((0).to_bytes(4, "little"))
        dib.extend((0).to_bytes(4, "little"))

        pixels = bytearray()
        for y in range(height):
            row = bytearray()
            for x in range(width):
                b = (x * 3) % 256
                g = (y * 2) % 256
                r = ((x + y) * 2) % 256
                row.extend(bytes([b, g, r]))
            while len(row) < row_size:
                row.append(0)
            pixels.extend(row)

        with open(path, "wb") as f:
            f.write(bytes(header))
            f.write(bytes(dib))
            f.write(bytes(pixels))

        return path

    @staticmethod
    def embed_message(cover_path: str, message: str, output_path: str) -> int:
        with open(cover_path, "rb") as f:
            data = bytearray(f.read())

        if len(data) < 54 or data[:2] != b"BM":
            raise ValueError("File harus BMP 24-bit yang valid")

        header = data[:54]
        body = data[54:]

        message_bytes = message.encode("utf-8")
        length_prefix = len(message_bytes).to_bytes(4, "big")
        payload = length_prefix + message_bytes
        bits = "".join(f"{byte:08b}" for byte in payload)

        if len(bits) > len(body):
            raise ValueError(
                f"Kapasitas tidak cukup. Tersedia: {len(body)} bits, Dibutuhkan: {len(bits)} bits"
            )

        bit_index = 0
        for i in range(0, len(body) - 1, 2):
            if bit_index >= len(bits):
                break

            target_bit = int(bits[bit_index])
            pair_lsb = ((body[i] & 1) << 1) | (body[i + 1] & 1)

            if target_bit == 0:
                if pair_lsb in (2, 3):
                    body[i] ^= 1
            else:
                if pair_lsb in (0, 1):
                    body[i] ^= 1
            bit_index += 1

        with open(output_path, "wb") as f:
            f.write(bytes(header))
            f.write(bytes(body))
        return bit_index

    @staticmethod
    def extract_message(stego_path: str) -> str:
        with open(stego_path, "rb") as f:
            data = bytearray(f.read())

        if len(data) < 54 or data[:2] != b"BM":
            raise ValueError("File harus BMP 24-bit yang valid")

        body = data[54:]
        bits = []

        for i in range(0, len(body) - 1, 2):
            pair_lsb = ((body[i] & 1) << 1) | (body[i + 1] & 1)
            bits.append("0" if pair_lsb in (0, 1) else "1")

        bitstream = "".join(bits)

        if len(bitstream) < 32:
            raise ValueError("Data tidak cukup untuk ekstraksi")

        length_bits = bitstream[:32]
        message_length = int(length_bits, 2)

        if message_length <= 0 or message_length > len(bitstream) // 8:
            raise ValueError("Format data tidak valid")

        message_bits = bitstream[32:32 + (message_length * 8)]
        message_bytes = bytearray()

        for i in range(0, len(message_bits), 8):
            byte_bits = message_bits[i:i + 8]
            if len(byte_bits) == 8:
                message_bytes.append(int(byte_bits, 2))

        return bytes(message_bytes).decode("utf-8", errors="ignore")

class TerminalUI:
    @staticmethod
    def print_big_separator():
        print(PESAN["pemisah"])

    @staticmethod
    def print_small_separator():
        print(PESAN["pemisah_kecil"])

    @staticmethod
    def print_header(experiment_num: int):
        print(f"\n{PESAN['pemisah']}")
        print(f" {PESAN['eksperimen_ke']} #{experiment_num}")
        print(f"{PESAN['pemisah']}")

    @staticmethod
    def print_status(status: Dict[str, bool]):
        print(f"\n{PESAN['status_sistem']}")
        print("+-----------------------------------+------------+")
        print(f"| {PESAN['komponen']:<33} | {PESAN['status']:<10} |")
        print("+-----------------------------------+------------+")
        for component, active in status.items():
            status_text = PESAN["aktif"] if active else PESAN["nonaktif"]
            print(f"| {component:<33} | {status_text:<10} |")
        print("+-----------------------------------+------------+")

    @staticmethod
    def print_menu():
        print(f"\n{PESAN['menu_utama']}")
        print("+----------------------------------------------------------+")
        print(f"| {PESAN['manajemen_kunci']:<56} |")
        print(f"| {PESAN['menu_1']:<56} |")
        print(f"| {PESAN['menu_2']:<56} |")
        print("|                                                          |")
        print(f"| {PESAN['enkripsi_dekripsi']:<56} |")
        print(f"| {PESAN['menu_3']:<56} |")
        print(f"| {PESAN['menu_4']:<56} |")
        print(f"| {PESAN['menu_5']:<56} |")
        print("|                                                          |")
        print(f"| {PESAN['tanda_tangan']:<56} |")
        print(f"| {PESAN['menu_6']:<56} |")
        print(f"| {PESAN['menu_7']:<56} |")
        print("|                                                          |")
        print(f"| {PESAN['steganografi']:<56} |")
        print(f"| {PESAN['menu_8']:<56} |")
        print(f"| {PESAN['menu_9']:<56} |")
        print("|                                                          |")
        print(f"| {PESAN['sistem']:<56} |")
        print(f"| {PESAN['menu_10']:<56} |")
        print(f"| {PESAN['menu_0']:<56} |")
        print("+----------------------------------------------------------+")

    @staticmethod
    def get_input(prompt: str, default: str = None) -> str:
        if default is not None:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        return input(f"{prompt}: ").strip()

    @staticmethod
    def continue_experiment() -> bool:
        print(f"\n{PESAN['pemisah_kecil']}")
        print(PESAN["opsi_selanjutnya"])
        print(f" {PESAN['lanjutkan']}")
        print(f" {PESAN['simpan_lanjut']}")
        print(f" {PESAN['selesai']}")
        print(f"{PESAN['pemisah_kecil']}")
        choice = input(f"{PESAN['pilih_opsi']}: ").strip()
        if choice in ("1", "2"):
            return True
        print(f"\n{PESAN['program_selesai']}")
        return False

session = CryptoSession()
crypto = CryptoCore()
stego = SteganographyLSB()
ui = TerminalUI()

def operation_generate_keys():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_generate']}")
    ui.print_small_separator()

    rsa_bits = int(ui.get_input(PESAN["ukuran_rsa"], "2048"))
    print(PESAN["buat_rsa"])
    rsa_priv, rsa_pub = crypto.generate_rsa_keys(rsa_bits)
    session.data["rsa_private"] = rsa_priv
    session.data["rsa_public"] = rsa_pub

    dsa_bits = int(ui.get_input(PESAN["ukuran_dsa"], "2048"))
    print(PESAN["buat_dsa"])
    dsa_priv, dsa_pub = crypto.generate_dsa_keys(dsa_bits)
    session.data["dsa_private"] = dsa_priv
    session.data["dsa_public"] = dsa_pub

    print(f"\n{PESAN['kunci_berhasil']}")
    print(f" RSA: {rsa_bits}-bit key pair")
    print(f" DSA: {dsa_bits}-bit key pair")

    session.add_experiment("Generate Keys", {
        "rsa_bits": rsa_bits,
        "dsa_bits": dsa_bits
    })

def operation_dh_exchange():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_dh']}")
    ui.print_small_separator()
    print(PESAN["proses_dh"])

    dh_params, aes_key = crypto.diffie_hellman_key_exchange_authenticated()
    session.data["dh_params"] = dh_params
    session.data["aes_key"] = aes_key

    print(f"\n{PESAN['dh_berhasil']}")
    print(f" {PESAN['publik_alice']}: {str(dh_params['alice_public'])[:60]}...")
    print(f" {PESAN['publik_bob']}: {str(dh_params['bob_public'])[:60]}...")
    print(f" Verifikasi RSA Signature Alice: {PESAN['ya'] if dh_params['alice_verified'] else PESAN['tidak']}")
    print(f" Verifikasi RSA Signature Bob  : {PESAN['ya'] if dh_params['bob_verified'] else PESAN['tidak']}")
    print(f" {PESAN['shared_cocok']}: {PESAN['ya'] if dh_params['shared_match'] else PESAN['tidak']}")
    print(f" Kunci publik DH terautentikasi: {PESAN['ya'] if dh_params['authenticated'] else PESAN['tidak']}")
    print(f" {PESAN['kunci_aes']}: {crypto.bytes_to_b64(aes_key)}")

    session.add_experiment("DH Key Exchange + RSA Signature", {
        "authenticated": dh_params["authenticated"],
        "shared_match": dh_params["shared_match"]
    })

def operation_hash_text():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_hash']}")
    ui.print_small_separator()

    text = ui.get_input(PESAN["masukkan_teks_hash"])
    sha256_hash = crypto.sha256_hash(text)

    print(f"\n{PESAN['input']}: {text}")
    print(f"SHA-256: {sha256_hash}")

    session.add_experiment("Hash Text", {
        "input_length": len(text)
    })

def operation_hybrid_encrypt():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_encrypt']}")
    ui.print_small_separator()

    if not session.data["rsa_public"]:
        print(PESAN["rsa_belum"])
        return

    plaintext = ui.get_input(PESAN["masukkan_plaintext"])

    print(f"\n{PESAN['sumber_aes']}")
    print(f" {PESAN['pakai_dh']}")
    print(f" {PESAN['kunci_baru']}")
    key_choice = ui.get_input(PESAN["pilih_1_2"], "2")

    if key_choice == "1" and session.data["aes_key"]:
        aes_key = session.data["aes_key"]
        print(PESAN["gunakan_dh"])
    else:
        aes_key = get_random_bytes(32)
        session.data["aes_key"] = aes_key
        print(PESAN["aes_baru"])

    print(PESAN["sedang_enkripsi"])

    nonce, ciphertext, tag = crypto.aes_encrypt(plaintext, aes_key)
    encrypted_key = crypto.rsa_encrypt_key(aes_key, session.data["rsa_public"])

    packet = {
        "aes_mode": "AES-GCM",
        "nonce": crypto.bytes_to_b64(nonce),
        "ciphertext": crypto.bytes_to_b64(ciphertext),
        "tag": crypto.bytes_to_b64(tag),
        "encrypted_key": crypto.bytes_to_b64(encrypted_key),
        "timestamp": datetime.now().isoformat()
    }

    session.data["last_cipher"] = packet
    session.data["last_plaintext"] = plaintext

    print(f"\n{PESAN['enkripsi_berhasil']}")
    print(PESAN["paket_enkripsi"])
    print(json.dumps(packet, indent=2))

    session.add_experiment("Hybrid Encrypt AES-GCM + RSA", {
        "plaintext_length": len(plaintext)
    })

def operation_hybrid_decrypt():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_decrypt']}")
    ui.print_small_separator()

    if not session.data["rsa_private"] or not session.data["last_cipher"]:
        print(PESAN["decrypt_belum"])
        return
    print(PESAN["sedang_dekripsi"])

    packet = session.data["last_cipher"]
    encrypted_key = crypto.b64_to_bytes(packet["encrypted_key"])
    nonce = crypto.b64_to_bytes(packet["nonce"])
    ciphertext = crypto.b64_to_bytes(packet["ciphertext"])
    tag = crypto.b64_to_bytes(packet["tag"])

    aes_key = crypto.rsa_decrypt_key(encrypted_key, session.data["rsa_private"])
    plaintext = crypto.aes_decrypt(nonce, ciphertext, tag, aes_key)
    print(f"\n{PESAN['plaintext']}: {plaintext}")

    if session.data["last_plaintext"]:
        match = plaintext == session.data["last_plaintext"]
        print(f"{PESAN['cocok_asli']}: {PESAN['ya'] if match else PESAN['tidak']}")

    session.add_experiment("Hybrid Decrypt AES-GCM + RSA", {
        "success": True
    })

def operation_sign_message():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_sign']}")
    ui.print_small_separator()

    if not session.data["dsa_private"]:
        print(PESAN["dsa_belum"])
        return

    message = ui.get_input(PESAN["masukkan_pesan_ttd"])
    print(PESAN["sedang_ttd"])

    signature = crypto.sign_message(message, session.data["dsa_private"])
    is_valid = crypto.verify_signature(message, signature, session.data["dsa_public"])

    session.data["last_signature"] = {
        "message": message,
        "signature": crypto.bytes_to_b64(signature),
        "algorithm": "DSA-SHA256",
        "timestamp": datetime.now().isoformat()
    }

    print(f"\n{PESAN['ttd_berhasil']}")
    print(f" {PESAN['signature']}: {crypto.bytes_to_b64(signature)[:100]}...")
    print(f" {PESAN['verifikasi']}: {PESAN['valid'] if is_valid else PESAN['tidak_valid']}")

    session.add_experiment("Sign Message", {
        "is_valid": is_valid
    })

def operation_verify_signature():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_verify']}")
    ui.print_small_separator()

    if not session.data["dsa_public"] or not session.data["last_signature"]:
        print(PESAN["verify_belum"])
        return

    print(PESAN["mode_verify"])
    print(f" {PESAN['verify_asli']}")
    print(f" {PESAN['verify_baru']}")

    mode = ui.get_input(PESAN["pilih_1_2"], "1")
    if mode == "1":
        message = session.data["last_signature"]["message"]
        print(f"{PESAN['pesan']}: {message}")
    else:
        message = ui.get_input(PESAN["masukkan_pesan_verify"])

    signature = crypto.b64_to_bytes(session.data["last_signature"]["signature"])
    is_valid = crypto.verify_signature(message, signature, session.data["dsa_public"])

    print(f"\nStatus: {'TANDA TANGAN VALID' if is_valid else 'TANDA TANGAN TIDAK VALID'}")
    print(f"{PESAN['pesan']}: {message}")
    print(f"{PESAN['integritas']}: {PESAN['autentik'] if is_valid else PESAN['tidak_autentik']}")

    session.add_experiment("Verify Signature", {
        "is_valid": is_valid
    })

def operation_stego_hide():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_stego_hide']}")
    ui.print_small_separator()

    if not session.data["rsa_public"]:
        print("ERROR: RSA public key belum tersedia. Generate keys terlebih dahulu!")
        return

    if not session.data["dsa_private"]:
        print("ERROR: DSA private key belum tersedia. Generate keys terlebih dahulu!")
        return

    print(PESAN["pilih_cover"])
    print(f" {PESAN['generate_demo']}")
    print(f" {PESAN['pakai_bmp']}")

    cover_choice = ui.get_input(PESAN["pilih_1_2"], "1")
    if cover_choice == "1":
        width = int(ui.get_input(PESAN["lebar"], "256"))
        height = int(ui.get_input(PESAN["tinggi"], "256"))
        cover_path = stego.generate_demo_bmp("demo_cover.bmp", width, height)
        print(f"{PESAN['demo_dibuat']}: {cover_path} ({width}x{height})")
    else:
        cover_path = ui.get_input(PESAN["path_cover"])
        if not Path(cover_path).exists():
            print(f"{PESAN['file_tidak_ditemukan']}: {cover_path}")
            return

    message = ui.get_input(PESAN["masukkan_pesan_rahasia"])
    output_path = ui.get_input(PESAN["nama_output"], "stego_output.bmp")

    try:
        print(PESAN["sembunyikan"])

        packet = crypto.build_integrated_secure_packet(
            message,
            session.data["dsa_private"],
            session.data["rsa_public"]
        )
        packet_json = json.dumps(packet, ensure_ascii=False)

        bits_embedded = stego.embed_message(cover_path, packet_json, output_path)

        session.data["last_stego_file"] = output_path
        session.data["last_integrated_packet"] = packet
        session.data["last_plaintext"] = message
        session.data["last_cipher"] = packet

        print(f"\n{PESAN['stego_berhasil']}")
        print(f" {PESAN['cover']}: {cover_path}")
        print(f" {PESAN['output']}: {output_path}")
        print(f" {PESAN['bit_disisipkan']}: {bits_embedded}")
        print(f" {PESAN['ukuran_pesan']}: {len(message)} bytes")
        print(" Pipeline: SHA256 -> DSA Sign -> AES-GCM Encrypt -> RSA Encrypt AES Key -> LSB Stego")
        print(f" Scheme : {packet['scheme']}")

        session.add_experiment("Integrated Secure Stego Hide", {
            "bits_embedded": bits_embedded,
            "message_length": len(message),
            "scheme": packet["scheme"]
        })

    except ValueError as e:
        print(f"{PESAN['error']}: {e}")
    except Exception as e:
        print(f"{PESAN['error']}: {e}")


def operation_stego_extract():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_stego_extract']}")
    ui.print_small_separator()

    if not session.data["rsa_private"]:
        print("ERROR: RSA private key belum tersedia. Generate keys terlebih dahulu!")
        return

    if not session.data["dsa_public"]:
        print("ERROR: DSA public key belum tersedia. Generate keys terlebih dahulu!")
        return

    if session.data["last_stego_file"]:
        stego_path = ui.get_input(PESAN["path_stego"], session.data["last_stego_file"])
    else:
        stego_path = ui.get_input(PESAN["path_stego"])

    if not Path(stego_path).exists():
        print(f"{PESAN['file_tidak_ditemukan']}: {stego_path}")
        return

    try:
        print(PESAN["ekstrak"])

        packet_json = stego.extract_message(stego_path)
        packet = json.loads(packet_json)

        result = crypto.extract_integrated_secure_packet(
            packet,
            session.data["rsa_private"],
            session.data["dsa_public"]
        )

        session.data["last_extracted_message"] = result["message"]
        session.data["last_signature"] = {
            "message": result["message"],
            "algorithm": result["signature_algorithm"],
            "timestamp": datetime.now().isoformat()
        }

        print(f"\n{PESAN['ekstrak_berhasil']}")
        print(f" {PESAN['file']}: {stego_path}")
        print(f" {PESAN['pesan']}: {result['message']}")
        print(f" {PESAN['panjang']}: {len(result['message'])} karakter")
        print(f" Hash valid      : {PESAN['ya'] if result['hash_valid'] else PESAN['tidak']}")
        print(f" Signature valid : {PESAN['ya'] if result['signature_valid'] else PESAN['tidak']}")
        print(f" Integritas akhir: {PESAN['autentik'] if result['integrity_valid'] else PESAN['tidak_autentik']}")

        session.add_experiment("Integrated Secure Stego Extract", {
            "message_length": len(result["message"]),
            "hash_valid": result["hash_valid"],
            "signature_valid": result["signature_valid"],
            "integrity_valid": result["integrity_valid"]
        })

    except ValueError as e:
        print(f"{PESAN['error']}: {e}")
    except json.JSONDecodeError:
        print(f"{PESAN['error']}: Data hasil ekstraksi bukan paket JSON yang valid")
    except Exception as e:
        print(f"{PESAN['error']}: {e}")

def operation_show_history():
    ui.print_header(session.experiment_count + 1)
    print(f"\n{PESAN['judul_history']}")
    ui.print_small_separator()

    if not session.experiment_history:
        print(PESAN["history_kosong"])
        return

    print(f"{PESAN['total_eksperimen']}: {len(session.experiment_history)}\n")

    for exp in session.experiment_history:
        print(f" ID: {exp['id']}")
        print(f" {PESAN['waktu']}: {exp['timestamp']}")
        print(f" {PESAN['aksi']}: {exp['action']}")
        print(f" {PESAN['detail']}: {json.dumps(exp['details'], indent=4)}")
        ui.print_small_separator()

def menu_awal() -> bool:
    print(BANNER)
    print(PESAN["menu_awal"])
    print(PESAN["mulai"])
    print(PESAN["selesai_awal"])

    choice = input(f"{PESAN['pilih_awal']}: ").strip()
    if choice == "1":
        return True
    if choice == "2":
        print(f"\n{PESAN['terima_kasih']}")
        return False
    print(PESAN["pilihan_tidak_valid"])
    return menu_awal()

def main():
    if not menu_awal():
        return

    menu_actions = {
        "1": operation_generate_keys,
        "2": operation_dh_exchange,
        "3": operation_hash_text,
        "4": operation_hybrid_encrypt,
        "5": operation_hybrid_decrypt,
        "6": operation_sign_message,
        "7": operation_verify_signature,
        "8": operation_stego_hide,
        "9": operation_stego_extract,
        "10": operation_show_history
    }

    while True:
        ui.print_big_separator()
        ui.print_status(session.get_status())
        ui.print_menu()
        ui.print_big_separator()

        choice = input(f"{PESAN['pilih_menu']}: ").strip()

        if choice == "0":
            print(f"\n{PESAN['program_selesai']}")
            print(PESAN["pemisah"])
            break
        elif choice in menu_actions:
            try:
                menu_actions[choice]()
            except Exception as e:
                print(f"{PESAN['error']}: {e}")

            if not ui.continue_experiment():
                print(PESAN["pemisah"])
                break
        else:
            print(PESAN["menu_tidak_valid"])

if __name__ == "__main__":
    main()