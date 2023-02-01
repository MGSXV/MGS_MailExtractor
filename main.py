import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import os

print("""
      		___  ________  _____ 
		|  \/  |  __ \/  ___|
		| .  . | |  \/\ `--. 
		| |\/| | | __  `--. \
		| |  | | |_\ \/\__/ /
Developed by:	\_|  |_/\____/\____/ 

Telegram	:	https://t.me/ZodiacMGS
Email		:	selkhamlichi97@gmail.com

""")

INPUT_FOLDER = ''
OUTPUT_FOLDER = ''
DOMAIN = ''

def worker(input_dir: str, output_dir: str, domain: str):
	MAX_PER_FILE = 1000000
	files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
	file_lines = []
	for input_file in files:
		try:
			with open(os.path.join(input_dir, input_file), "r", encoding='utf8') as f:
				file_lines.extend(f.readlines())
		except:
			pass
	deduplicated_lines = list(set(file_lines))
	file_number = 1
	line_count = 0
	output_file = os.path.join(output_dir, domain + "_" + str(file_number) + ".txt")
	with open(output_file, "w", encoding='utf-8') as f:
		for line in deduplicated_lines:
			output = line.split(f'@{domain}')
			if len(output) > 1:
				f.write(f'{output[0]}@{domain}\n')
				line_count += 1
			if line_count == MAX_PER_FILE:
				file_number += 1
				line_count = 0
				output_file = os.path.join(output_dir, domain + "_" + str(file_number) + ".txt")
				f.close()
				f = open(output_file, "w")
	f.close()
	messagebox.showinfo("Done", "All file were successfully processed")
	

def route(input_dir: str, output_dir: str, domain: str):
	thread = Thread(target=worker, args=(input_dir, output_dir, domain))
	thread.start()

def start_application(domain: str):
	global INPUT_FOLDER, OUTPUT_FOLDER, DOMAIN
	DOMAIN = domain
	if INPUT_FOLDER == '' or OUTPUT_FOLDER == '' or DOMAIN == '':
		messagebox.showerror('Error', 'Error: All fields are required!')
		return
	route(INPUT_FOLDER, OUTPUT_FOLDER, DOMAIN)


def ask_directory(root, row, io: bool):
	filepath=filedialog.askdirectory()
	label_path = tk.Label(root, text=filepath)
	label_path.grid(row=row, column=1, padx=5, pady=5)
	if io:
		global INPUT_FOLDER
		INPUT_FOLDER = filepath
	else:
		global OUTPUT_FOLDER
		OUTPUT_FOLDER = filepath


def init():
	root = tk.Tk()
	root.title("ADN Mail Exporter")
	label = tk.Label(root, text="Domain:")
	label.grid(row=0, column=0, padx=5, pady=5)
	domain_input = tk.Entry(root)
	domain_input.grid(row=0, column=1, padx=5, pady=5)
	input_folder = tk.Button(root, text='Select input folder', command=lambda: ask_directory(root, 1, True))
	input_folder.grid(row=1, column=0, padx=5, pady=5)
	output_folder = tk.Button(root, text='Select output folder', command=lambda: ask_directory(root, 2, False))
	output_folder.grid(row=2, column=0, padx=5, pady=5)
	quit_button = tk.Button(root, text="Quit", command=root.destroy)
	quit_button.grid(row=3, column=1, sticky="E", padx=5, pady=5)
	start_button = tk.Button(root, text="Start", command=lambda: start_application(domain_input.get()))
	start_button.grid(row=3, column=0, sticky="W", padx=5, pady=5)
	root.mainloop()


def main():
	init()

if __name__ == '__main__':
	main()
