# Listings from chapter 5

# Note: Links are often referred to as nodes
#
# using lower_case instead of mixedCase for functions and variables
# __str__using __iter__

class Link:
    __slots__ = ('__data', '__next')

    def __init__(self, data, next=None):
        self.__data = data
        self.__next = next

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_next(self):
        return self.__next

    def set_next(self, link):
        self.__next = link

    def is_last(self):
        return self.__next is None

    def __str__(self):
        return str(self.get_data())


def identity(x):
    return x


class LinkedList:
    def __init__(self):
        self.__first = None

    def get_first(self):
        return self.__first

    def set_first(self, link):
        if link is None or isinstance(link, Link):
            self.__first = link
        else:
            raise RuntimeError("First link must be Link or None")

    def get_next(self):
        return self.get_first()

    def set_next(self, link):
        self.set_first(link)

    def is_empty(self):
        return self.__first is None

    def first(self):
        if self.is_empty():
            raise RuntimeError("No first item in empty list")
        return self.get_first().get_data()

    def __iter__(self):
        def _iter(link):
            if link:
                yield link.get_data()
                yield from _iter(link.get_next())
        return _iter(self.get_first())

    def __len__(self):
        def _len(link):
            if not link:
                return 0
            return 1 + _len(link.get_next())
        return _len(self.get_first())

    def __str__(self):
        result = "["
        for elem in self:  # using __iter__
            if len(result) > 1:
                result += " > "
            result += str(elem)
        return result + "]"

    def insert(self, data):
        # create a new Link with next referencing the list's current first
        link = Link(data, self.get_first())
        self.set_first(link)

    def find(self, goal, key=identity):
        def _find(link):
            if not link:
                return None
            if key(link.get_data()) == goal:
                return link
            return _find(link.get_next())

        return _find(self.get_first())

    def search(self, goal, key=identity):
        link = self.find(goal, key)
        if link is None:
            return False
        return link.get_data()

    def insert_after(self, goal, new_data, key=identity):
        link = self.find(goal, key)
        if link is None:
            return False
        # create a new Link with next referencing link's next
        new_link = Link(new_data, link.get_next())
        # update link's next to reference the new link
        link.set_next(new_link)
        return True

    def delete_first(self):
        if self.is_empty():
            raise RuntimeError("Cannot delete first of empty list")
        first = self.get_first()
        self.set_first(first.get_next())
        return first.get_data()  # Return data of deleted link

    def delete(self, goal, key=identity):
        def _delete(previous, current):
            if not current:
                raise RuntimeError("No item with matching key found in list")
            if goal == key(current.get_data()):  # Found the link to delete
                previous.set_next(current.get_next())
                return current.get_data()  # Return data of deleted link
            return _delete(current, current.get_next())

        if self.is_empty():
            raise RuntimeError("Cannot delete from empty list")
        # special case if the first link is to be deleted
        if key(self.get_first().get_data()) == goal:
            return self.delete_first()
        return _delete(self, self.get_next())


if __name__ == '__main__':
    # test link
    link = Link(3)
    print("link, get_data()==3", link.get_data() == 3)
    print("link, get_next() is None", link.get_next() is None)
    linked_list = LinkedList()
    print("linked_list is_empty()", linked_list.is_empty())
    print("linked_list get_first is None", linked_list.get_first() is None)
    print("len(linked_list) == 0", len(linked_list) == 0)
    linked_list.set_first(link)
    print("linked_list get_first().get_data() == 3", linked_list.get_first().get_data() == 3)
    print("len(linked_list) == 1", len(linked_list) == 1)
    for i in range(5, 10):
        linked_list.insert(i)
    print("linked_list after insertions: ", str(linked_list))
    print("len(linked_list) == 6", len(linked_list) == 6)

    for i in range(0, 3):
        print("search returned False:", linked_list.search(i) == False)
    for i in range(5, 10):
        print("search returned data", linked_list.search(i) == i)

    linked_list.insert_after(5, 4)
    linked_list.insert_after(3, 2)
    print("linked_list after insert_after calls: ", str(linked_list))

    linked_list.delete_first()
    print("len(linked_list)==7", len(linked_list) == 7)

    linked_list.delete(5)
    linked_list.delete(2)
    # test removing the first
    linked_list.delete(8)
    try:
        linked_list.delete(2)
        print("No exception raised.")
    except:
        print("Exception raised as expected.")
    print("len(linked_list)==4", len(linked_list) == 4)
    print("linked_list after deletions: ", str(linked_list))
    for i in [2, 5, 8, 9]:
        print("search returned False:", linked_list.search(i) == False)
