class PDA:
    # МП - PushDown Automaton
    BOTTOM = Z0 = 'bottom'  # дно стека
    EPS = 'eps'  # epsilon

    def __init__(self, start_state: str, transitions: dict, end_type: str, finals: list = None,
                 reverse_stack: bool = False):
        """
        start_state - начальное состояние
        transitions - словарь такой что transitions[q][(char, stack_top)] = δ(q,char,stack_top)
            (a, b, c) - неизменяемый массив в Python. Может быть ключом к hash map, т.к. допускает хэширование
        end_type - способ завершения - 'final' - по финальному состоянию, 'empty' - по пустому стеку
            finals - массив финальных состояний
        reverse_stack - добавлять символы в стек так, как записано в `transitions` или наоборот. Надо, т.к. стек - динамический
            массив с добавлением элементов в конец, но изменения стека могут быть описаны добавлением элементов в начало
            (как в автомате в фукции `check_particular`)
        """
        self.start_state = start_state
        self.transitions = transitions
        self.end_type = end_type
        self.reverse_stack = reverse_stack
        if end_type == 'final':
            self.finals = finals

    def step(self, start_state: str, symbol: str, stack_top: str) -> list:
        # возвращает δ(start_state, symbol, stack_top) = [ (q1, stack_change1), (q2, stack_change2), ...]
        # stack_change - список элементов добавляемых в стек
        try:
            return self.transitions[start_state][(symbol, stack_top)]
        except KeyError:
            return []

    def can_stop(self, seq: str, index: int, state: str = None, stack: list = None) -> bool:
        # может ли автомат остановиться
        # конец строки - обязательное условие
        if len(seq) == index:
            if self.end_type == 'final':
                # остановка по финальному состоянию
                return state in self.finals
            else:
                # остановка по пустому стеку
                return len(stack) == 0
        return False

    def new_stack(self, stack: list, extend: list) -> list:
        # создание стека по старому стеку и его изменению
        # создается копия нужная для недетерминированности
        t_stack = stack.copy()
        t_stack.pop()
        t_stack.extend(extend if not self.reverse_stack else extend[::-1])
        return t_stack

    def check(self, sequence: str, index: int = 0, current_state: str = None, stack: list = None) -> bool:
        # рекурсивная функция проверки последовательности на соотвествие МП

        # параметры по умолчанию (первый вызов функции)
        if current_state is None:
            current_state = self.start_state
        if stack is None:
            stack = [PDA.BOTTOM]

        if len(stack):
            # ε-переходы
            eps_tr = self.step(current_state, self.EPS, stack[-1])
            # переходы по следующему символу - только если символы еще есть
            char_tr = self.step(current_state, sequence[index], stack[-1]) if len(sequence) != index else []

            for transitions, new_index in [(eps_tr, index), (char_tr, index + 1)]:
                for new_state, stack_change in transitions:
                    # стек для новой ветви
                    temp_stack = self.new_stack(stack, stack_change)
                    # возвращают - прошла ли цепочка
                    if self.check(sequence, new_index, new_state, temp_stack):
                        return True

        # ни одна ветвь не показала допустимость => проверяем текущую конфигурацию
        return self.can_stop(sequence, index, current_state, stack)


def check_particular_1(seq):
    # по финальному состоянию, нет недетерминированности
    z0 = PDA.BOTTOM
    eps = PDA.EPS
    pda = PDA(
        start_state='q0',
        transitions={
            'q0': {
                ('0', z0): [('q0', [0, 0, z0])],
                ('0', 0): [('q0', [0, 0, 0])],
                ('(', z0): [('q1', [z0])],
                ('(', 0): [('q1', [0])],
            },
            'q1': {
                ('1', 0): [('q1', [])],
                (')', z0): [('q2', [z0])]
            },
            'q2': {
                ('0', z0): [('q3', [z0])]
            },
            'q3': {
                ('0', z0): [('q2', [z0])]
            }
        },
        end_type='final',
        finals=['q2'],
        reverse_stack=True
    )

    return pda.check(seq)


def check_particular_2(seq):
    # по пустому стэку, с недетерминированностью
    z0 = PDA.BOTTOM
    eps = PDA.EPS
    pda = PDA(
        start_state='q0',
        transitions={
            'q0': {
                ('0', z0): [('q0', [0, 0, z0])],
                ('0', 0): [('q0', [0, 0, 0])],
                ('(', z0): [('q1', [z0])],
                ('(', 0): [('q1', [0])],
            },
            'q1': {
                ('1', 0): [('q1', [])],
                (')', z0): [('q2', [z0])]
            },
            'q2': {
                ('0', 0): [('q2', [0, 0])],
                ('0', z0): [('q2', [0, z0])],
                (eps, z0): [('q3', [z0])],
                (eps, 0): [('q3', [0])]
            },
            'q3': {
                ('0', 0): [('q3', [])],
                (eps, z0): [('q3', [])]
            }
        },
        end_type='empty',
        reverse_stack=True
    )
    return pda.check(seq)


def check_and_find_unexpected(seq):
    class MyString(str):
        def __new__(cls, string):
            # метод, создающий строку класса MyString
            # с полем max_used_idx и переопределенным методом __getitem__()
            my_string = str.__new__(cls, string + '\0')
            my_string.max_used_idx = -1
            return my_string

        def __getitem__(self, item):
            # вызов string.__getitem__(item) <=> string[item]
            # item - индекс символа => запоминаем максимальный вызванный индекс
            self.max_used_idx = max(self.max_used_idx, item)
            return super().__getitem__(item)

    for check in [check_particular_1, check_particular_2]:
        accepted = check(seq)
        if accepted:
            print('цепочка принадлежит языку')
        else:
            new_seq = MyString(seq)
            check(new_seq)
            # `+1`, т.к. нужен следующий после последнего использованного
            idx = new_seq.max_used_idx
            print(f'Ошибка: в позиции {idx + 1} - неожидаемый ', end='')
            print(f'символ {seq[idx]}' if idx < len(seq) else 'конец строки')


while True:
    check_and_find_unexpected(input())
    print()
