#!/usr/bin/env python3
# Saulo S. Ortiz
# 20260722
# desc: for DeedRAT (SnappyBee/BloodAlchemy) payload
# note: make sure this script and SBAMRES.DLL.CC are in the same location

# line to edit all the way at the bottom of the script!

import os
import struct
import zlib
import lzma


# clears the screen
def clear_screen():
	os.system('clear')
clear_screen()

print("**************************")
print("    Naked_DeedRAT v1.0"    )
print("      (deobfuscator)"      )
print("**************************")

def deobfuscate_cc_payload(input_path, output_path):
	decrypted_bytes = bytearray()
	decompressed_payload = None
	output_type = "Decrypted VZ Container"

	if not os.path.exists(input_path):
		print(f"[-] Error: {input_path} not found.")
		return

	with open(input_path, "rb") as f:
		file_data = f.read()

	if len(file_data) < 16:
		print(f"[-] Error: File is too small to be a valid payload.")
		return

	magic = struct.unpack("<I", file_data[0:4])[0]
	if magic != 0x97d57f7a: # change this hex to your MZ header finding
		print(f"[!] Warning: Magic mismatch (Got {hex(magic)}). Proceeding anyway...")

	header_size = 16
	encrypted_payload = file_data[header_size:]
	key = 0x5A

	for i, b in enumerate(encrypted_payload):
		decrypted_byte = b ^ ((key + i) & 0xFF)
		decrypted_bytes.append(decrypted_byte)

#new ------------------------------------
	if len(decrypted_bytes) >= 2 and decrypted_bytes[0:2] == b'VZ':
		print(f"[+] Success! Found 'VZ' compressed magic bytes container!")
	else:
		print(f"[!] Warning: 'VZ' header not found at start of decrypted bytes.")
	compressed_data = bytes(decrypted_bytes[4:])
	print(f"[+] Attempting to expand decompression layers...")
	
	try:
		decompressed_payload = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
		output_type = "Fully Decompressed Payload!"
		print(f"[+] Successfully decompressed via Zlib wrapper!")
	except Exception:
		try: 
			decompressed_payload = zlib.decompress(compressed_data)
			output_type = "Fully Decompressed Payload!"
			print(f"[+] Successfully decompressed via standard Zlib!")
		except Exception:
			try:
				decompressed_payload = lzma.decompress(compressed_data)
				output_type = "Fully Decompressed Payload!"
				print(f"[+] Successfully decompressed via standard LZMA!")
			except Exception:
				print(f"[-] Standard Python decompression routines skipped.")
				print(f"[-] Note: This sample likely uses a native Windows LZNT1/LZO structure.")

	final_output = decompressed_payload if decompressed_payload else decrypted_bytes
#new ------------------------------------
	try:
		with open(output_path, "wb") as out_f:
			out_f.write(final_output)		
		print(f"[+] Success! Output saved to: {output_path} ({output_type})")

		if final_output.startswith(b'MZ'):
			print(f"[***] SUCCESS! Found a valid MZ header in the final file!")
		else:
			print(f"[i] No MZ header found in output! It may be a fileless raw shellcode.")
			
	except Exception as e:
		print(f"[-] Decompression error: {e}")

# change the file here to yours...i'll change this line soon to make it a user input one
deobfuscate_cc_payload("SBAMRES.DLL.CC", "unpacked_deedrat_stage.bin")










