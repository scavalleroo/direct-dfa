class DFANode:
    def __init__(self, data):
        self.left: DFANode = None
        self.right: DFANode = None
        self.data = data
        self.id_n = 0

    def count_leaf(self) -> int:
        return 1 if self.is_leaf() \
            else (self.left.count_leaf() if self.left else 0) + (
            self.right.count_leaf() if self.right else 0)

    def get_characters(self) -> set:
        return set(tuple([self.data]) if self.is_leaf()
                   else (tuple(self.left.get_characters())
                         if self.left else tuple()) +
                        (tuple(self.right.get_characters())
                         if self.right else tuple())
                   )

    def set_id(self, id_n: int):
        if self.is_leaf():
            self.id_n = id_n
            return self.id_n - 1
        return self.left.set_id(self.right.set_id(id_n)
                                if self.right else id_n) \
            if self.left else id_n

    def set_all_id(self):
        self.set_id(id_n=self.count_leaf())

    # Print the dfa_structure
    def print_tree(self, level: int = 0):
        print(f'L{level}, ID{self.id_n}: {self.data}, '
              f'First:{self.first()}\tLast:{self.last()}')
        if self.left:
            self.left.print_tree(level=level + 1)
        if self.right:
            self.right.print_tree(level=level + 1)

    def is_leaf(self) -> bool:
        return not self.left and not self.right

    def nullable(self) -> bool:
        if self.is_leaf():
            return False

        if self.data == '*':
            return True

        nullable_left = self.left.nullable() if self.left else True
        nullable_right = self.right.nullable() if self.right else True

        if self.data == '|':
            return nullable_left or nullable_right

        if self.data == '.':
            return nullable_left and nullable_right

    def first(self) -> set:
        if self.is_leaf():
            return set(tuple([self.id_n]))

        first_left = tuple(self.left.first()) if self.left else tuple()
        first_right = tuple(self.right.first()) if self.right else tuple()

        if self.data == '*':
            return set(first_left)

        nullable_left = self.left.nullable() if self.left else True

        if self.data == '|':
            return set(first_left + first_right)

        if self.data == '.':
            return set(
                first_left + first_right if nullable_left else first_left)

    def last(self) -> set:
        if self.is_leaf():
            return set(tuple([self.id_n]))

        last_left = tuple(self.left.last()) if self.left else tuple()
        last_right = tuple(self.right.last()) if self.right else tuple()

        if self.data == '*':
            return set(last_left)

        nullable_right = self.right.nullable() if self.right else True

        if self.data == '|':
            return set(last_left + last_right)

        if self.data == '.':
            return set(last_left + last_right if nullable_right else last_right)

    def follow(self, table: dict) -> dict:
        if self.left:
            table = self.left.follow(table=table)

        if self.right:
            table = self.right.follow(table=table)

        if self.data == '.' and self.left and self.right:
            for i in self.left.last():
                t_table = tuple(table[i]) + tuple(self.right.first())
                table[i] = set(t_table)

        if self.data == '*' and self.left:
            for i in self.last():
                t_table = tuple(table[i]) + tuple(self.first())
                table[i] = set(t_table)

        return table

    def find_leaves_by_data_and_ids(self, data, ids: list) -> set:
        if self.is_leaf() and self.data == data and self.id_n in ids:
            return set(tuple([self]))
        return set(
            (tuple(self.left.find_leaves_by_data_and_ids(data=data, ids=ids))
             if self.left else tuple()) +
            (tuple(self.right.find_leaves_by_data_and_ids(data=data, ids=ids))
             if self.right else tuple()))
