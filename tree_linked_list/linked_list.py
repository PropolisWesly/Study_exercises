class Paper:
	def __init__(self, value):
		self.value = value
		self.next = None
		self.previous = None

class ListedLink:
	def __init__(self):
		self.head = None

	def add_item(self, paper):
		if self.head is None:
			self.head = paper
			paper.previous = self
			return

		last_paper = self.head
		while last_paper.next:
			last_paper = last_paper.next

		last_paper.next = paper
		paper.previous = last_paper

	def value_search(self, value):
		index = 0
		paper = self.head
		while paper.next:
			if paper.value == value:
				return print(f'Значение {value} найдено на индексе {index}')
			index += 1
			paper = paper.next
		if paper.value == value:
			return print(f'Значение {value} найдено на индексе {index}')
		else:
			return print('Нет такого значения в списке')

	def delete_item(self, value):
		if self.head is None:
			return print('Пустой лист')
		last_paper = self.head

		if last_paper.value == value:
			if last_paper.next is not None:
				last_paper.next.previous = self
				self.head = last_paper.next
				return
			else:
				self.head = None
				return

		last_paper = last_paper.next

		while last_paper.next:
			if last_paper.value == value:
				last_paper.previous.next = last_paper.next
				last_paper.next.previous = last_paper.previous
				return
			last_paper = last_paper.next
		if last_paper.value == value:
			last_paper.previous.next = last_paper.next
			last_paper.next.previous = last_paper.previous
			return
		else:
			print('Нет такого значения')


integer = ListedLink()
for i in range(10):
	integer.add_item(Paper(i))

integer.value_search(6)
integer.delete_item(4)
integer.value_search(3)
integer.delete_item(3)
integer.value_search(6)

listik = ListedLink()
trop = ['а', 'б', 'в', 'г', 'д' ,'е']
for letter in trop:
	listik.add_item(Paper(letter))
listik.value_search('г')
listik.delete_item('г')
listik.value_search('г')
listik.value_search('д')





