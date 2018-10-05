import random

def encrypt_text(text, method):
	i = 0
	begword = 0
	result = ''
	while i != len(text):
		if not text[i].isalpha() and not text[i].isdigit():
			result += method(text[begword:i]) + text[i]
			begword = i + 1
		i = i + 1
	else:
		result += text[begword:i][::-1]
	return result


def reverse_horizontal_permutation(text):
	return encrypt_text(text, (lambda word: word[::-1]))


def increasing_alternative_horizontal_permutation_for_word(word):
	wordout_ls = [""]*len(word)
	for i in range(len(word)):
		if i%2 == 0:
			wordout_ls[i//2] = word[i]
		if i%2 == 1:
			wordout_ls[-(i//2+1)] = word[i]
	return ''.join(wordout_ls)


def increasing_alternative_horizontal_permutation(text):
	return encrypt_text(text, increasing_alternative_horizontal_permutation_for_word)


def increasing_reverse_horizontal_permutation(text):
	return encrypt_text(text, (lambda word: increasing_alternative_horizontal_permutation_for_word(word)[::-1]))


def decreasing_alternative_horizontal_permutation_for_word(word):
	wordout_ls = [""]*len(word)
	x = 0
	y = len(word) -1
	for i in range(len(word)-1,-1,-1):
		if i % 2 == 1:
			wordout_ls[x] = word[i]
			x +=1
		else:
			wordout_ls[y] = word[i]
			y -= 1
	return ''.join(wordout_ls)


def decreasing_alternative_horizontal_permutation(text):
	return encrypt_text(text, decreasing_alternative_horizontal_permutation_for_word)


def decreasing_reverse_alternative_horizontal_permutation(text):
	return encrypt_text(text, (lambda word: decreasing_alternative_horizontal_permutation_for_word(word)[::-1]))


def sequential_permutation(text):
	return encrypt_text(text, (lambda word: word[1::2] + word[::2]))


def encrypting_with_odd_symbols_for_word(word, odd_symbols):
	chars = list(word)
	result_word = ''
	for char in chars:
		result_word += char + random.choice(odd_symbols)
	return result_word[:-1]


def encrypting_with_odd_symbols(text, odd_sympols):
	return encrypt_text(text, (lambda word: encrypting_with_odd_symbols_for_word(word, odd_sympols)))


def encrypting_with_deleting_symbols(text, odd_symbols):
	for char in odd_symbols:
		text = text.replace(char.lower(), '')
	for char in odd_symbols:
		text = text.replace(char.upper(), '')
	return text


if __name__ == "__main__":
	print(encrypting_with_odd_symbols('123456789.123456789 123456789,123456789    123456789\n\n12345678.,.', 'ke'))