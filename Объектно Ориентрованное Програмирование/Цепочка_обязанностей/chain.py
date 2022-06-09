class NullHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
            self.successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'event_set':
            self.__set_handler(obj, event)
        elif event.kind == 'event_get':
            return self.__get_handler(obj, event)
        else:
            raise ValueError(f'This kind of event doesn\'t exist {event.kind}')

    def __set_handler(self, obj, event):
        if isinstance(event.value, int):
            obj.integer_field = event.value
        else:
            self.successor.handle(obj, event)

    def __get_handler(self, obj, event):
        if issubclass(event.typer, int):
            return obj.integer_field
        else:
            return self.successor.handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'event_set':
            self.__set_handler(obj, event)
        elif event.kind == 'event_get':
            return self.__get_handler(obj, event)
        else:
            raise ValueError(f'This kind of event doesn\'t exist {event.kind}')

    def __set_handler(self, obj, event):
        if isinstance(event.value, float):
            obj.float_field = event.value
        else:
            self.successor.handle(obj, event)

    def __get_handler(self, obj, event):
        if issubclass(event.typer, float):
            return obj.float_field
        else:
            return self.successor.handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == 'event_set':
            self.__set_handler(obj, event)
        elif event.kind == 'event_get':
            return self.__get_handler(obj, event)
        else:
            raise ValueError(f'This kind of event doesn\'t exist {event.kind}')

    def __set_handler(self, obj, event):
        if isinstance(event.value, str):
            obj.string_field = event.value
        else:
            self.successor.handle(obj, event)

    def __get_handler(self, obj, event):
        if issubclass(event.typer, str):
            return obj.string_field
        else:
            return self.successor.handle(obj, event)


class EventGet:
    def __init__(self, typer):
        self.typer = typer
        self.kind = 'event_get'


class EventSet:
    def __init__(self, value):
        self.value = value
        self.kind = 'event_set'