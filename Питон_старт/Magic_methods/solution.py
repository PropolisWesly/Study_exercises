import os.path
import random
import tempfile
class File:

     def __init__(self, path):

        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('')

        self.path = path
        self.current = 0
        self.content()


     def content(self):
        with open(self.path, 'r') as f:
            self.content_list = f.readlines()
        self.end = len(self.content_list)


     def read(self):
        with open(self.path, 'r') as f:
            content = f.read()
        return content


     def write(self, new_content):
        with open(self.path, 'w') as f:
            f.write(new_content)

        self.content()


     def generation(self):
         bukvi = ['a', 'b', 'c', 'd', 'e', 'f', 'g', '1', '2', '3', '4', '5', '6']
         tail = random.choices(bukvi, k=20)
         tail = ''.join(tail)
         return tail

     def __add__(self, obj):
        tempfile.gettempdir()
        with open(self.path, 'r') as f:
            content1 = f.read()

        with open(obj.path, 'r') as f:
            content2 = f.read()

        path_head = tempfile.gettempdir()

  #      path_tail = '71b9e7b695f64d85a7488f07f2bc051c'
        path_tail = self.generation()
        new_path = os.path.join(path_head, path_tail)

        while True:
            if os.path.exists(new_path):
                path_tail = self.generation()
                new_path = os.path.join(path_head, path_tail)
            else:
                break

        new_obj = File(new_path)
        new_content = content1 + content2
        new_obj.write(new_content)
        return new_obj


     def __str__(self):
        return self.path


     def __iter__(self):
        return self


     def __next__(self):
        if self.current >= self.end:
            self.current = 0
            raise StopIteration

        result = self.content_list[self.current]
        self.current += 1
        return result
