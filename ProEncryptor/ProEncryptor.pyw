from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import os.path
from chardet import detect
import source.decryptor as decryptor
import source.encryptor as encryptor


class Encryptor(Frame):
	def __init__(self, parent):
		self.encoding='windows-1251'
		self.frame = Frame.__init__(self, parent)
		self.input_frame = Frame(self, height=50)
		self.input_frame.pack(side=TOP, fill=X, padx=10, pady=10)
		self.input_kind= IntVar()
		self.input_kind.set(1)
		fr =Frame(self.input_frame)
		fr.pack(side=TOP)
		Radiobutton(fr, text="Ввести самому", variable=self.input_kind, value=1, command=self.change_input).pack(side=LEFT)
		Radiobutton(fr, text="Взять из файла", variable=self.input_kind, value=2, command=self.change_input).pack(side=LEFT)

		self.input_kind_lbl = Label(self.input_frame, text='Введите исходный текст тут:')
		self.input_kind_lbl.pack(anchor=W)
		self.input_text_frame = Frame(self.input_frame)
		self.input_text_frame.pack(fill=X)
		self.input_text = Text(self.input_text_frame, height=7)
		self.scroll_input_text = Scrollbar(self.input_text_frame, command=self.input_text.yview)
		self.input_text['yscrollcommand'] = self.scroll_input_text.set
		self.scroll_input_text.pack(fill = Y, side=RIGHT)
		self.input_text.pack(fill=X, side=LEFT, expand=True)

		self.input_file_dialog_btn = Button(self.input_frame, text="Выбрать", command=self.get_input_file_name)
		self.input_file = ''

		self.frame_way = Frame(self)
		self.way=IntVar()
		self.way.set(1)
		Radiobutton(self.frame_way, text="Зашифровать", variable=self.way, value=1, command=self.check_additional_field).pack(side=LEFT)
		Radiobutton(self.frame_way, text="Дешифровать", variable=self.way, value=2, command=self.check_additional_field).pack(side=LEFT)
		self.frame_way.pack(side=TOP, fill=X, padx=10, pady=10)

		self.method = IntVar()
		self.method.set(1)
		self.radio_frame = Frame(self)
		self.radio_frame.pack(side=TOP, fill=X, padx = 10, pady= 10)
		Label(self.radio_frame, text='Выберите метод шифования:').pack(anchor=W)
		Radiobutton(self.radio_frame, text='Обратная горизнотальная перестановка', variable=self.method, value=1, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Возрастающая альтернативная перестановка', variable=self.method, value=2, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Возрастающая обратная альтернативная перестановка', variable=self.method, value=3, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Убывающая альтернативная горизонтальная перестановка', variable=self.method, value=4, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Убывающая обратная альтернаятивная горизонтальная перестановка', variable=self.method, value=5, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Рассановка букв сначала с четными индексами, потом с нечетными', variable=self.method, value=6, command=self.check_additional_field).pack(anchor=W)
		Radiobutton(self.radio_frame, text='Вымышленные буквы', variable=self.method, value=7, command=self.check_additional_field).pack(anchor=W)
		self.bad_decrypt_radio = Radiobutton(self.radio_frame, text='Исключение одной или нескольких букв', variable=self.method, value=8, command=self.check_additional_field)
		self.bad_decrypt_radio.pack(anchor=W)
		self.additional_entry_label = Label(self.radio_frame)
		self.additional_entry = Entry(self.radio_frame)
		self.frame_what_to_do = Frame(self.radio_frame)
		self.frame_what_to_do.pack(anchor=E)
		self.btnfile = Button(self.frame_what_to_do, text='Зашифровать в файл', command=self.encrypt_into_file)
		self.btnfile.pack(side=LEFT)
		self.btnfield = Button(self.frame_what_to_do, text='Зашифровать в текстовое поле', command=self.encrypt_into_field)
		self.btnfield.pack(side=LEFT)

		self.output_frame = Frame(self)
		self.output_frame.pack(side=BOTTOM, fill=X, padx = 10, pady=10)
		Label(self.output_frame, text = 'Зашифрованный текст:').pack(anchor=W)
		self.output_text_frame = Frame(self.output_frame)
		self.output_text_frame.pack(fill=X)
		self.output_text = Text(self.output_text_frame, height=7)
		self.scroll_output_text = Scrollbar(self.output_text_frame, command=self.output_text.yview)
		self.output_text['yscrollcommand'] = self.scroll_output_text.set
		self.scroll_output_text.pack(fill=Y, side=RIGHT)
		self.output_text.pack(fill= X, expand=True, side=LEFT)
		self.output_text.config(state='disabled')

	def check_additional_field(self):
		if self.way.get() == 2:
			self.btnfield.configure(text="Дешифровать в текстовое поле", command=self.decrypt_into_field)
			self.btnfile.configure(text="Дешифровать в файл", command=self.decrypt_into_file)
			self.additional_entry.pack_forget()
			self.additional_entry_label.pack_forget()
			self.bad_decrypt_radio.pack_forget()
			if self.method.get() == 8:
				self.method.set(1)
			return
		else:
			self.btnfield.configure(text="Зашифровать в текстовое поле", command=self.encrypt_into_field)
			self.btnfile.configure(text="Зашифровать в файл", command=self.encrypt_into_file)
			self.bad_decrypt_radio.pack(anchor=W)
			self.frame_what_to_do.pack_forget()
			self.frame_what_to_do.pack(anchor=E)
		if self.method.get() == 7:
			self.additional_entry_label['text'] = 'Введите вымышленные буквы'
			self.additional_entry_label.pack(anchor=W)
			self.additional_entry.pack(anchor=W)
			self.frame_what_to_do.pack_forget()
			self.frame_what_to_do.pack(anchor=E)
		elif self.method.get() == 8:
			self.additional_entry_label['text'] = 'Введите удаляемые буквы'
			self.additional_entry_label.pack(anchor=W)
			self.additional_entry.pack(anchor=W)
			self.frame_what_to_do.pack_forget()
			self.frame_what_to_do.pack(anchor=E)
		else:
			self.additional_entry_label.pack_forget()
			self.additional_entry.pack_forget()

	def change_input(self):
		if self.input_kind.get() == 1:
			self.encoding='windows-1251'
			self.input_kind_lbl['text'] = 'Введите исходный текст тут:'
			self.input_file_dialog_btn.pack_forget()
			self.input_text_frame.pack(fill=X)
		else:
			if self.input_file:
				self.input_kind_lbl["text"] = "Выбран файл с текстом: " + self.input_file
			else:
				self.input_kind_lbl['text'] = 'Выберите путь к файлу с текстом'
			self.input_text_frame.pack_forget()
			self.input_file_dialog_btn.pack()

	def get_input_file_name(self):
		self.input_file = askopenfilename()
		if self.input_file:
			self.input_kind_lbl["text"] = "Выбран файл с текстом: "+self.input_file

	def encrypt_into_file(self):
		if self.input_kind.get() == 1:
			text = self.input_text.get(1.0, END)
		else:
			if not self.input_file:
				messagebox.showerror('Ошибка', 'Не указан путь к файлу с исходным текстом!')
				return
			else:
				text = b''.join(open(self.input_file, 'rb').readlines())

				self.encoding = detect(text[:128])['encoding']
				if not self.encoding:
					text = text.decode(encoding='windows-1251')
				else:
					text = text.decode(encoding=self.encoding)
		if self.input_file:
			ext = os.path.splitext(self.input_file)[-1]
			if not ext:
				ext = '.txt'
		else:
			ext = '.txt'
		if ext!='.txt':
			file = asksaveasfilename(defaultextension=ext, filetypes=(('', '*'+ext), ('text', '*.txt'), ('all files', '*.*')))
		else:
			file = asksaveasfilename(defaultextension=ext, filetypes=(('text', '*.txt'), ('all files', '*.*')))
		if file:
			open(file, 'w', encoding='utf-8').write(self.encrypt(text))

	def encrypt_into_field(self):
		if self.input_kind.get() == 1:
			text = self.input_text.get(1.0, END)
		else:
			if not self.input_file:
				messagebox.showerror('Ошибка', 'Не указан путь к файлу с исходным текстом!')
				return
			else:
				text = b''.join(open(self.input_file, 'rb').readlines())
				encoding = detect(text[:128])['encoding']
				if not encoding:
					text = text.decode(encoding='latin-1')
				else:
					text = text.decode(encoding=encoding)
		self.output_text.config(state='normal')
		self.output_text.delete(1.0, END)
		self.output_text.insert(END, self.encrypt(text))
		self.output_text.config(state='disabled')

	def decrypt_into_field(self):
		if self.input_kind.get() == 1:
			text = self.input_text.get(1.0, END)
		else:
			if not self.input_file:
				messagebox.showerror('Ошибка', 'Не указан путь к файлу с исходным текстом!')
				return
			else:
				text = b''.join(open(self.input_file, 'rb').readlines())
				encoding = detect(text[:128])['encoding']
				if not encoding:
					text = text.decode(encoding='latin-1')
				else:
					text = text.decode(encoding=encoding)
		self.output_text.config(state='normal')
		self.output_text.delete(1.0, END)
		self.output_text.insert(END, self.decrypt(text))
		self.output_text.config(state='disabled')

	def decrypt_into_file(self):
		if self.input_kind.get() == 1:
			text = self.input_text.get(1.0, END)
		else:
			if not self.input_file:
				messagebox.showerror('Ошибка', 'Не указан путь к файлу с исходным текстом!')
				return
			else:
				text = b''.join(open(self.input_file, 'rb').readlines())
				self.encoding = detect(text[:128])['encoding']
				if not self.encoding:
					text = text.decode(encoding='windows-1251')
				else:
					text = text.decode(encoding=self.encoding)
		if self.input_file:
			ext = os.path.splitext(self.input_file)[-1]
			if not ext:
				ext = '.txt'
		else:
			ext = '.txt'
		if ext!='.txt':
			file = asksaveasfilename(defaultextension=ext, filetypes=(('', '*'+ext), ('text', '*.txt'), ('all files', '*.*')))
		else:
			file = asksaveasfilename(defaultextension=ext, filetypes=(('text', '*.txt'), ('all files', '*.*')))
		if file:
			open(file, 'w', encoding='utf-8').write(self.decrypt(text))

	def encrypt(self, text):
		if self.method.get() == 1:
			return encryptor.reverse_horizontal_permutation(text)
		if self.method.get() == 2:
			return encryptor.increasing_alternative_horizontal_permutation(text)
		if self.method.get() == 3:
			return encryptor.increasing_reverse_horizontal_permutation(text)
		if self.method.get() == 4:
			return encryptor.decreasing_alternative_horizontal_permutation(text)
		if self.method.get() == 5:
			return encryptor.decreasing_reverse_alternative_horizontal_permutation(text)
		if self.method.get() == 6:
			return encryptor.sequential_permutation(text)
		if self.method.get() == 7:
			additional_arg = self.additional_entry.get()
			additional_arg =additional_arg.replace(',', '')
			additional_arg = additional_arg.replace(' ', '')
			if not additional_arg.isalpha() or set('aeiouyуеоаяиёэюыAEIOUYУЕЭОАЫЯИЮЁ').intersection(additional_arg):
				messagebox.showerror('Ошибка', 'Лишние символы должны быть не гласными буквами!')
				self.output_text.config(state='disabled')
				return ""
			return encryptor.encrypting_with_odd_symbols(text, list(additional_arg))
		if self.method.get() == 8:
			additional_arg = self.additional_entry.get()
			additional_arg =additional_arg.replace(',', '')
			additional_arg =additional_arg.replace(' ', '')
			if not additional_arg.isalpha():
				messagebox.showerror('Ошибка', 'Удаляемые символы должны быть буквами!')
				self.output_text.config(state='disabled')
				return ""
			return encryptor.encrypting_with_deleting_symbols(text, list(additional_arg))

	def decrypt(self, text):
		if self.input_kind.get() == 1:
			text= self.input_text.get(1.0, END)
		else:
			pass
		self.output_text.config(state='normal')
		self.output_text.delete(1.0, END)
		if self.method.get() == 1:
			return decryptor.reverse_horizontal_permutation(text)
		if self.method.get() == 2:
			return decryptor.increasing_alternative_horizontal_permutation(text)
		if self.method.get() == 3:
			return decryptor.increasing_reverse_horizontal_permutation(text)
		if self.method.get() == 4:
			return decryptor.decreasing_alternative_horizontal_permutation(text)
		if self.method.get() == 5:
			return decryptor.decreasing_reverse_alternative_horizontal_permutation(text)
		if self.method.get() == 6:
			return decryptor.sequential_permutation(text)
		if self.method.get() == 7:
			return decryptor.encrypting_with_odd_symbols(text)
		self.output_text.config(state='disabled')


root = Tk()
root.title('Encryptor Pro')
#root.iconbitmap(default="ProEncryptor.ico")
Encryptor(root).pack(expand=True, fill=BOTH)
root.resizable(width=False, height=False)
root.mainloop()
