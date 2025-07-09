"""
第08章：杯子塔与后悔药的哲学 - 栈的完整实现

栈(Stack)：后进先出(LIFO)的线性数据结构
就像叠盘子一样，最后放上的最先拿掉

作者：DSA Lab 四人组
日期：学习栈的美好一天
"""


class Stack:
    """
    栈的实现类 - 就像管理一摞盘子
    
    核心思想：
    1. 使用Python列表作为底层存储
    2. 列表的末尾作为栈顶，开头作为栈底
    3. 所有操作都在栈顶进行，保证O(1)时间复杂度
    """
    
    def __init__(self):
        """
        初始化一个空栈
        
        self.items: 存储栈元素的列表
        - 索引 0 是栈底（最先进入的元素）
        - 索引 -1 是栈顶（最后进入的元素）
        """
        self.items = []  # 空列表，等待元素的加入
    
    def is_empty(self):
        """
        检查栈是否为空
        
        返回值：
        - True: 栈为空，没有任何元素
        - False: 栈不为空，至少有一个元素
        
        时间复杂度：O(1) - 只需检查列表长度
        """
        return len(self.items) == 0
    
    def push(self, item):
        """
        将元素压入栈顶 - 就像在杯子塔顶部放一个新杯子
        
        参数：
        item: 要压入栈的元素，可以是任何类型
        
        工作原理：
        1. 使用列表的append()方法在末尾添加元素
        2. append()操作时间复杂度是O(1)，非常高效
        3. 新元素成为新的栈顶
        
        为什么不用insert(0, item)？
        - insert(0, item)需要将所有现有元素向后移动一位
        - 时间复杂度是O(n)，效率很低
        - 就像在杯子塔底部插入杯子，需要托起整座塔！
        """
        self.items.append(item)
        print(f"🔵 压入: {item}")
        print(f"📚 当前栈: {self.items}")
        print(f"📏 栈大小: {len(self.items)}")
    
    def pop(self):
        """
        弹出并返回栈顶元素 - 就像拿走杯子塔最顶部的杯子
        
        返回值：
        被弹出的栈顶元素
        
        异常：
        如果栈为空，抛出IndexError异常
        
        工作原理：
        1. 首先检查栈是否为空，空栈无法pop
        2. 使用列表的pop()方法移除并返回最后一个元素
        3. pop()操作时间复杂度是O(1)
        
        为什么不用pop(0)？
        - pop(0)需要将所有剩余元素向前移动一位
        - 时间复杂度是O(n)，效率很低
        """
        if self.is_empty():
            raise IndexError("栈是空的，无法pop！就像空盘子塔无法拿杯子一样 🫗")
        
        # Python的pop()默认移除最后一个元素（索引-1）
        item = self.items.pop()
        print(f"🔴 弹出: {item}")
        print(f"📚 当前栈: {self.items}")
        print(f"📏 栈大小: {len(self.items)}")
        return item
    
    def peek(self):
        """
        查看栈顶元素但不移除 - 就像偷瞄杯子塔最顶部的杯子
        
        返回值：
        栈顶元素（不移除）
        
        异常：
        如果栈为空，抛出IndexError异常
        
        Python小知识：
        items[-1] 是负索引，表示"倒数第一个"
        - items[-1]: 最后一个元素（栈顶）
        - items[-2]: 倒数第二个元素
        - 比items[len(items)-1]更简洁易读
        """
        if self.is_empty():
            raise IndexError("栈是空的，无法peek！空栈里没有元素可以查看 👀")
        
        # 使用负索引访问最后一个元素，不移除它
        top_element = self.items[-1]
        print(f"👁️  偷看栈顶: {top_element}")
        return top_element
    
    def size(self):
        """
        返回栈中元素的个数
        
        返回值：
        整数，表示栈中元素的数量
        
        时间复杂度：O(1) - Python列表维护长度信息
        """
        return len(self.items)
    
    def clear(self):
        """
        清空栈中的所有元素 - 就像把杯子塔全部收拾掉
        
        工作原理：
        重新创建一个空列表，原来的列表会被Python垃圾回收
        """
        self.items = []
        print("🧹 栈已清空")
    
    def __str__(self):
        """
        定义栈的字符串表示形式
        当我们print(stack)时，会调用这个方法
        """
        if self.is_empty():
            return "空栈 📭"
        return f"栈📚 {self.items} (栈顶: {self.items[-1]})"
    
    def __len__(self):
        """
        定义len(stack)的行为
        这样可以直接用len()函数获取栈的大小
        """
        return len(self.items)


class StackNode:
    """
    链式栈的节点类
    
    每个节点包含：
    - data: 存储的数据
    - next: 指向下一个节点的指针
    """
    
    def __init__(self, data):
        """
        初始化栈节点
        
        参数：
        data: 节点要存储的数据，可以是任何类型
        """
        self.data = data      # 存储数据
        self.next = None      # 指向下一个节点的指针，初始化为None
    
    def __str__(self):
        """节点的字符串表示"""
        return f"Node({self.data})"


class LinkedStack:
    """
    链式栈的实现 - 使用链表作为底层数据结构
    
    相比顺序栈的优势：
    1. 动态内存分配，不需要预设大小
    2. 不会因为容量不足而需要扩容
    3. 内存使用更灵活
    
    相比顺序栈的劣势：
    1. 每个节点需要额外的指针空间开销
    2. 内存不连续，缓存效率较低
    3. 实现稍微复杂一些
    """
    
    def __init__(self):
        """
        初始化空的链式栈
        
        属性：
        self.top: 指向栈顶节点的指针，空栈时为None
        self.count: 记录栈中元素个数，用于快速获取大小
        """
        self.top = None       # 栈顶指针，空栈时为None
        self.count = 0        # 元素计数器，避免每次都遍历链表计算大小
        print("🎪 创建了一个新的链式栈")
    
    def is_empty(self):
        """
        检查栈是否为空
        
        返回值：
        bool: True表示栈为空，False表示栈不为空
        
        实现思路：
        当栈顶指针为None时，说明栈为空
        
        时间复杂度：O(1)
        空间复杂度：O(1)
        """
        return self.top is None
    
    def push(self, data):
        """
        将元素压入栈顶 - 链式栈的插入操作
        
        参数：
        data: 要压入栈的数据
        
        算法步骤：
        1. 创建新节点，存储要插入的数据
        2. 将新节点的next指针指向当前栈顶节点
        3. 更新栈顶指针指向新节点
        4. 增加元素计数
        
        关键点：
        - 新节点总是插入在链表头部（成为新的栈顶）
        - 即使栈为空，new_node.next = None 也是正确的
        
        时间复杂度：O(1) - 只涉及常数次指针操作
        空间复杂度：O(1) - 只创建一个新节点
        """
        # 步骤1：创建新节点
        new_node = StackNode(data)
        print(f"🆕 创建新节点: {new_node}")
        
        # 步骤2：新节点指向当前栈顶
        # 这一步很关键：即使栈为空（self.top为None），这样做也是正确的
        new_node.next = self.top
        print(f"🔗 新节点指向当前栈顶")
        
        # 步骤3：更新栈顶指针
        self.top = new_node
        print(f"⬆️  更新栈顶指针")
        
        # 步骤4：更新元素计数
        self.count += 1
        
        print(f"🔵 链式栈压入: {data}")
        print(f"📊 栈大小: {self.count}")
        self._display_structure()
    
    def pop(self):
        """
        弹出栈顶元素 - 链式栈的删除操作
        
        返回值：
        栈顶元素的数据
        
        异常：
        IndexError: 当栈为空时抛出
        
        算法步骤：
        1. 检查栈是否为空
        2. 保存栈顶节点的数据（用于返回）
        3. 更新栈顶指针指向下一个节点
        4. 减少元素计数
        5. 原栈顶节点会被Python垃圾回收器自动回收
        
        关键点：
        - 删除操作实际上是移动指针，让原栈顶节点失去引用
        - Python的垃圾回收机制会自动释放不再被引用的节点
        
        时间复杂度：O(1) - 只涉及常数次指针操作
        空间复杂度：O(1) - 只使用常数额外空间
        """
        # 步骤1：检查栈是否为空
        if self.is_empty():
            raise IndexError("链式栈为空，无法执行pop操作！🫗")
        
        # 步骤2：保存要返回的数据
        data = self.top.data
        print(f"💾 保存栈顶数据: {data}")
        
        # 步骤3：更新栈顶指针（"删除"当前栈顶节点）
        old_top = self.top
        self.top = self.top.next
        print(f"🔄 栈顶指针移动到下一个节点")
        
        # 步骤4：减少元素计数
        self.count -= 1
        
        print(f"🔴 链式栈弹出: {data}")
        print(f"📊 栈大小: {self.count}")
        print(f"🗑️  节点 {old_top} 将被垃圾回收")
        self._display_structure()
        
        return data
    
    def peek(self):
        """
        查看栈顶元素但不移除 - 非破坏性查看操作
        
        返回值：
        栈顶元素的数据
        
        异常：
        IndexError: 当栈为空时抛出
        
        实现思路：
        直接返回栈顶节点的数据，不修改栈的结构
        
        时间复杂度：O(1)
        空间复杂度：O(1)
        """
        if self.is_empty():
            raise IndexError("链式栈为空，无法执行peek操作！👀")
        
        data = self.top.data
        print(f"👁️  查看栈顶: {data}")
        return data
    
    def size(self):
        """
        返回栈中元素的个数
        
        返回值：
        int: 栈中元素的数量
        
        实现说明：
        由于我们维护了count变量，可以O(1)时间返回大小
        如果不维护count，就需要O(n)时间遍历整个链表
        
        时间复杂度：O(1) - 直接返回计数器值
        空间复杂度：O(1)
        """
        return self.count
    
    def clear(self):
        """
        清空栈中所有元素
        
        实现思路：
        将栈顶指针设为None，计数器归零
        所有节点都会失去引用，被垃圾回收器回收
        
        时间复杂度：O(1) - 只需要重置两个变量
        空间复杂度：O(1)
        """
        self.top = None
        self.count = 0
        print("🧹 链式栈已清空")
    
    def _display_structure(self):
        """
        显示链式栈的内部结构 - 仅用于学习和调试
        
        这个方法展示了栈的链式结构，帮助理解指针的指向关系
        在实际应用中，栈通常不提供这种"透视"功能
        """
        if self.is_empty():
            print("📭 链式栈为空")
            return
        
        print("🔍 链式栈结构:")
        current = self.top
        position = 0
        elements = []
        
        while current:
            if position == 0:
                elements.append(f"[栈顶] {current.data}")
            else:
                elements.append(f"[{position}] {current.data}")
            current = current.next
            position += 1
        
        print(f"     {' → '.join(elements)} → None")
    
    def display(self):
        """
        显示栈的所有元素（从栈顶到栈底）
        
        注意：这个方法破坏了栈的封装性，在实际应用中通常不提供
        这里只是为了学习目的，帮助理解栈的内容
        """
        if self.is_empty():
            print("链式栈为空 🫗")
            return
        
        elements = []
        current = self.top
        while current:
            elements.append(str(current.data))
            current = current.next
        
        print(f"链式栈📚 [栈顶] {' → '.join(elements)} [栈底]")
    
    def __str__(self):
        """
        栈的字符串表示
        
        返回值：
        str: 栈的简洁字符串描述
        """
        if self.is_empty():
            return "空链式栈 📭"
        return f"链式栈📚 (栈顶: {self.top.data}, 大小: {self.count})"
    
    def __len__(self):
        """
        支持len()函数获取栈大小
        
        使用方式：len(linked_stack)
        """
        return self.count


class QueueUsingStacks:
    """
    用两个栈实现队列 - 黛芙的经典面试题
    
    核心思想：
    1. 输入栈(input_stack)：接收所有新入队的元素
    2. 输出栈(output_stack)：负责所有出队操作
    3. 通过倒转操作，将LIFO转换为FIFO
    
    巧妙之处：
    - 入队时：总是放入输入栈（简单快速）
    - 出队时：如果输出栈为空，就将输入栈全部倒入输出栈
    - 这样，最先入队的元素就变成了输出栈的栈顶
    """
    
    def __init__(self):
        """
        初始化队列
        
        input_stack: 接收新元素的栈，先进入的元素在栈底
        output_stack: 输出元素的栈，先进入的元素在栈顶
        """
        self.input_stack = Stack()    # 专门负责入队
        self.output_stack = Stack()   # 专门负责出队
        print("🎪 创建了一个用双栈实现的队列")
    
    def enqueue(self, item):
        """
        入队操作 - 新客人排队
        
        参数：
        item: 要入队的元素
        
        策略：
        新元素总是放入输入栈，这样保证了时间顺序：
        - 最先入队的元素在输入栈的底部
        - 最后入队的元素在输入栈的顶部
        
        时间复杂度：O(1) - 只是一个简单的push操作
        """
        self.input_stack.push(item)
        print(f"🟢 入队: {item} | 队列大小: {self.size()}")
    
    def dequeue(self):
        """
        出队操作 - 服务队伍中的第一个客人
        
        返回值：
        最先入队的元素（符合FIFO原则）
        
        策略：
        1. 如果输出栈不为空，直接从输出栈弹出（已经是正确顺序）
        2. 如果输出栈为空，将输入栈的所有元素倒入输出栈
        3. 倒转后，原来的栈底元素变成新的栈顶元素
        
        时间复杂度分析：
        - 最好情况：O(1) - 输出栈有元素，直接pop
        - 最坏情况：O(n) - 需要倒转所有元素
        - 平均情况：O(1) - 分摊分析，每个元素最多被移动两次
        """
        # 确保输出栈有元素可以出队
        self._ensure_output_stack_has_elements()
        
        # 从输出栈弹出元素（这就是最先入队的元素）
        item = self.output_stack.pop()
        print(f"🟡 出队: {item} | 队列大小: {self.size()}")
        return item
    
    def _ensure_output_stack_has_elements(self):
        """
        私有方法：确保输出栈有元素可以出队
        
        工作流程：
        1. 检查输出栈是否为空
        2. 如果为空，检查输入栈是否也为空
        3. 如果输入栈也为空，说明整个队列为空
        4. 否则，将输入栈的所有元素倒入输出栈
        
        为什么这样设计？
        - 分离关注点：入队和出队各自处理
        - 延迟倒转：只有在必要时才进行倒转操作
        - 批量处理：一次倒转处理多个元素，提高效率
        """
        if self.output_stack.is_empty():
            # 检查是否整个队列为空
            if self.input_stack.is_empty():
                raise IndexError("队列是空的，没有元素可以出队！🚫")
            
            # 将输入栈的所有元素倒入输出栈
            print("🔄 输出栈为空，正在从输入栈倒转元素...")
            transfer_count = 0
            while not self.input_stack.is_empty():
                # 从输入栈弹出元素，压入输出栈
                element = self.input_stack.pop()
                self.output_stack.push(element)
                transfer_count += 1
            
            print(f"✅ 倒转完成，移动了 {transfer_count} 个元素")
    
    def front(self):
        """
        查看队首元素但不移除 - 看看谁在排队的最前面
        
        返回值：
        队首元素（最先入队的元素）
        """
        self._ensure_output_stack_has_elements()
        return self.output_stack.peek()
    
    def is_empty(self):
        """
        检查队列是否为空
        
        返回值：
        True: 队列为空（两个栈都为空）
        False: 队列不为空（至少一个栈有元素）
        """
        return self.input_stack.is_empty() and self.output_stack.is_empty()
    
    def size(self):
        """
        返回队列中元素的总数
        
        返回值：
        两个栈的大小之和
        """
        return self.input_stack.size() + self.output_stack.size()
    
    def __str__(self):
        """
        队列的字符串表示
        显示输入栈和输出栈的状态
        """
        return (f"队列🎪 [输入栈: {self.input_stack.items}, "
                f"输出栈: {self.output_stack.items}] "
                f"(大小: {self.size()})")


def demonstrate_stack_operations():
    """
    演示栈的基本操作 - 安妮的杯子塔实验
    """
    print("=" * 50)
    print("🏗️  栈的基本操作演示 - 安妮的杯子塔")
    print("=" * 50)
    
    # 创建一个空栈
    cup_stack = Stack()
    print(f"初始状态: {cup_stack}")
    print(f"栈是否为空: {cup_stack.is_empty()}")
    
    print("\n--- 模拟安妮叠杯子的过程 ---")
    # 模拟安妮叠杯子
    cups = ["☕ 黛芙的马克杯", "🥤 希娅的奶茶杯", "🍵 伊莎贝尔的茶杯", "🥛 安妮的牛奶杯"]
    
    for cup in cups:
        cup_stack.push(cup)
        print(f"栈顶是: {cup_stack.peek()}")
        print()
    
    print(f"最终栈状态: {cup_stack}")
    print(f"栈大小: {cup_stack.size()}")
    
    print("\n--- 安妮想要拿黛芙的杯子 ---")
    print("需要先把上面的杯子都拿掉...")
    
    # 临时存储其他杯子
    temp_storage = []
    target_cup = "☕ 黛芙的马克杯"
    
    # 一个个拿掉上面的杯子，直到找到目标杯子
    while not cup_stack.is_empty():
        current_cup = cup_stack.pop()
        if current_cup == target_cup:
            print(f"🎯 找到目标杯子: {current_cup}")
            break
        else:
            temp_storage.append(current_cup)
        print()
    
    print("\n--- 将其他杯子按相反顺序放回去 ---")
    # 注意：要按相反顺序放回去！
    for cup in reversed(temp_storage):
        cup_stack.push(cup)
        print()
    
    print(f"恢复后的栈: {cup_stack}")
    
    print("\n--- 测试异常情况 ---")
    # 清空栈并测试异常
    cup_stack.clear()
    print(f"清空后: {cup_stack}")
    
    try:
        cup_stack.pop()
    except IndexError as e:
        print(f"捕获异常: {e}")
    
    try:
        cup_stack.peek()
    except IndexError as e:
        print(f"捕获异常: {e}")


def demonstrate_linked_stack():
    """
    演示链式栈的操作 - 希娅的链表栈实验
    """
    print("\n" + "=" * 50)
    print("🔗 链式栈操作演示 - 希娅的链表栈")
    print("=" * 50)
    
    # 创建链式栈
    linked_stack = LinkedStack()
    print(f"初始状态: {linked_stack}")
    print(f"栈是否为空: {linked_stack.is_empty()}")
    
    print("\n--- 逐步压入元素，观察链表结构 ---")
    elements = ["🍎 苹果", "🍌 香蕉", "🍊 橙子", "🥝 猕猴桃"]
    
    for element in elements:
        print(f"\n准备压入: {element}")
        linked_stack.push(element)
        print(f"当前栈顶: {linked_stack.peek()}")
        print()
    
    print(f"\n最终状态: {linked_stack}")
    linked_stack.display()
    
    print("\n--- 逐步弹出元素，观察指针变化 ---")
    while not linked_stack.is_empty():
        print(f"\n当前栈顶: {linked_stack.peek()}")
        popped = linked_stack.pop()
        print(f"弹出元素: {popped}")
        if not linked_stack.is_empty():
            print(f"新的栈顶: {linked_stack.peek()}")
        print()
    
    print(f"栈清空后: {linked_stack}")
    
    print("\n--- 测试异常情况 ---")
    try:
        linked_stack.pop()
    except IndexError as e:
        print(f"捕获异常: {e}")
    
    try:
        linked_stack.peek()
    except IndexError as e:
        print(f"捕获异常: {e}")


def compare_stack_implementations():
    """
    对比顺序栈和链式栈的性能和特点
    """
    print("\n" + "=" * 50)
    print("⚖️  顺序栈 vs 链式栈 性能对比")
    print("=" * 50)
    
    import time
    import sys
    
    def measure_time(operation, description):
        """测量操作执行时间"""
        start_time = time.time()
        operation()
        end_time = time.time()
        return (end_time - start_time) * 1000  # 转换为毫秒
    
    # 测试数据量
    n = 1000
    print(f"测试数据量: {n} 次操作")
    
    # 测试顺序栈
    def test_sequential_stack():
        stack = Stack()
        # Push操作
        for i in range(n):
            stack.push(f"item_{i}")
        # Pop操作
        for i in range(n):
            stack.pop()
    
    # 测试链式栈
    def test_linked_stack():
        stack = LinkedStack()
        # Push操作
        for i in range(n):
            stack.push(f"item_{i}")
        # Pop操作
        for i in range(n):
            stack.pop()
    
    print("\n性能测试结果:")
    
    # 关闭打印输出以准确测量时间
    import os
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stdout = os.dup(1)
    os.dup2(devnull, 1)
    
    try:
        seq_time = measure_time(test_sequential_stack, "顺序栈")
        linked_time = measure_time(test_linked_stack, "链式栈")
    finally:
        # 恢复输出
        os.dup2(old_stdout, 1)
        os.close(devnull)
        os.close(old_stdout)
    
    print(f"📊 顺序栈时间: {seq_time:.2f} 毫秒")
    print(f"🔗 链式栈时间: {linked_time:.2f} 毫秒")
    print(f"📈 性能比值: {linked_time/seq_time:.2f}x")
    
    # 内存使用分析
    print("\n内存使用分析:")
    
    # 顺序栈内存使用
    seq_stack = Stack()
    for i in range(100):
        seq_stack.push(i)
    seq_size = sys.getsizeof(seq_stack.items)
    
    # 链式栈内存使用（估算）
    linked_stack = LinkedStack()
    for i in range(100):
        linked_stack.push(i)
    
    # 估算链式栈内存：每个节点大小 + 数据大小
    node_overhead = sys.getsizeof(StackNode(0))  # 节点本身的开销
    total_linked_size = node_overhead * 100  # 100个节点的开销
    
    print(f"📦 顺序栈内存使用: {seq_size} 字节")
    print(f"🔗 链式栈内存使用(估算): {total_linked_size} 字节")
    print(f"📈 内存开销比: {total_linked_size/seq_size:.2f}x")
    
    print("\n特性总结:")
    print("顺序栈优势: 🚀 速度快、💾 内存效率高、🔧 实现简单")
    print("链式栈优势: 🔄 动态大小、🎯 无容量限制、💡 灵活性强")


def demonstrate_queue_with_stacks():
    """
    演示用两个栈实现队列 - 黛芙的经典面试题
    """
    print("\n" + "=" * 50)
    print("🎪 用两个栈实现队列 - 黛芙的挑战题")
    print("=" * 50)
    
    # 创建队列
    queue = QueueUsingStacks()
    
    print("\n--- 模拟奶茶店排队 ---")
    customers = ["👩 小红", "👨 小明", "👩 小花", "👦 小强"]
    
    # 客人依次入队
    for customer in customers:
        queue.enqueue(customer)
        print(f"队首是: {queue.front()}")
        print()
    
    print(f"排队状态: {queue}")
    
    print("\n--- 开始服务客人（先进先出）---")
    # 按排队顺序服务客人
    while not queue.is_empty():
        print(f"下一个服务: {queue.front()}")
        served_customer = queue.dequeue()
        print(f"✅ 已服务: {served_customer}")
        print(f"剩余队列: {queue}")
        print()
    
    print("🎉 所有客人都已服务完毕！")
    
    print("\n--- 测试空队列异常 ---")
    try:
        queue.dequeue()
    except IndexError as e:
        print(f"捕获异常: {e}")


def demonstrate_stack_overflow():
    """
    演示栈溢出的概念和防范方法
    """
    print("\n" + "=" * 50)
    print("💥 栈溢出演示与防范")
    print("=" * 50)
    
    import sys
    
    print(f"当前Python递归限制: {sys.getrecursionlimit()}")
    
    # 演示1：安全的递归深度测试
    print("\n--- 1. 安全的递归深度测试 ---")
    
    def safe_countdown(n, max_depth=50):
        """安全的递归倒数，限制最大深度"""
        if n <= 0:
            return "倒数结束！"
        if n > max_depth:
            return f"递归深度限制：最大允许{max_depth}，输入{n}太大！"
        
        print(f"倒数: {n}")
        return safe_countdown(n - 1, max_depth)
    
    result = safe_countdown(10)
    print(f"结果: {result}")
    
    # 尝试超过限制
    result = safe_countdown(100)
    print(f"结果: {result}")
    
    # 演示2：递归vs迭代的对比
    print("\n--- 2. 递归 vs 迭代对比 ---")
    
    def recursive_factorial(n, depth=0):
        """递归实现阶乘（带深度监控）"""
        print(f"{'  ' * depth}递归深度 {depth}: 计算 {n}!")
        if n <= 1:
            print(f"{'  ' * depth}基础情况: 返回 1")
            return 1
        result = n * recursive_factorial(n - 1, depth + 1)
        print(f"{'  ' * depth}返回 {n} * ... = {result}")
        return result
    
    def iterative_factorial(n):
        """迭代实现阶乘（避免栈溢出）"""
        print(f"迭代计算 {n}! :")
        result = 1
        for i in range(1, n + 1):
            result *= i
            print(f"  步骤 {i}: result = {result}")
        return result
    
    print("递归方式计算 5!:")
    recursive_result = recursive_factorial(5)
    print(f"最终结果: {recursive_result}")
    
    print("\n迭代方式计算 5!:")
    iterative_result = iterative_factorial(5)
    print(f"最终结果: {iterative_result}")
    
    # 演示3：尾递归优化的概念
    print("\n--- 3. 尾递归优化概念演示 ---")
    
    def traditional_factorial(n):
        """传统递归：需要保持所有中间状态"""
        if n <= 1:
            return 1
        return n * traditional_factorial(n - 1)  # 递归调用后还要做乘法
    
    def tail_recursive_factorial(n, accumulator=1):
        """尾递归：递归调用是函数的最后一个操作"""
        if n <= 1:
            return accumulator
        # 递归调用是最后一个操作，理论上可以优化为循环
        return tail_recursive_factorial(n - 1, n * accumulator)
    
    def simulated_tail_optimization(n):
        """模拟尾递归优化的效果（用循环实现）"""
        accumulator = 1
        while n > 1:
            accumulator = n * accumulator
            n = n - 1
        return accumulator
    
    print("传统递归 vs 尾递归概念:")
    print(f"传统递归 4! = {traditional_factorial(4)}")
    print(f"尾递归 4! = {tail_recursive_factorial(4)}")
    print(f"优化后循环 4! = {simulated_tail_optimization(4)}")
    
    # 演示4：记忆化减少递归深度
    print("\n--- 4. 记忆化减少递归深度 ---")
    
    def fibonacci_naive(n, depth=0):
        """朴素递归斐波那契（会导致大量重复计算）"""
        print(f"{'  ' * depth}计算 fib({n})")
        if n <= 2:
            return 1
        return fibonacci_naive(n-1, depth+1) + fibonacci_naive(n-2, depth+1)
    
    def fibonacci_memoized(n, memo={}, depth=0):
        """记忆化斐波那契（避免重复计算）"""
        print(f"{'  ' * depth}计算 fib({n})")
        if n in memo:
            print(f"{'  ' * depth}从缓存获取 fib({n}) = {memo[n]}")
            return memo[n]
        if n <= 2:
            memo[n] = 1
            return 1
        memo[n] = fibonacci_memoized(n-1, memo, depth+1) + fibonacci_memoized(n-2, memo, depth+1)
        return memo[n]
    
    print("朴素递归计算 fib(6):")
    naive_result = fibonacci_naive(6)
    print(f"结果: {naive_result}")
    
    print("\n记忆化递归计算 fib(6):")
    memo_result = fibonacci_memoized(6)
    print(f"结果: {memo_result}")
    
    # 演示5：检测和预防栈溢出的工具函数
    print("\n--- 5. 栈溢出检测工具 ---")
    
    import inspect
    
    def get_current_recursion_depth():
        """获取当前递归深度"""
        return len(inspect.stack())
    
    def safe_recursive_operation(n, operation_name="operation", max_depth=100):
        """安全的递归操作包装器"""
        current_depth = get_current_recursion_depth()
        if current_depth > max_depth:
            raise RecursionError(f"{operation_name} 递归深度 {current_depth} 超过限制 {max_depth}")
        
        print(f"执行 {operation_name}, 当前递归深度: {current_depth}")
        
        if n <= 0:
            return 0
        return n + safe_recursive_operation(n - 1, operation_name, max_depth)
    
    try:
        result = safe_recursive_operation(10, "累加计算", 50)
        print(f"安全递归结果: {result}")
    except RecursionError as e:
        print(f"捕获递归错误: {e}")
    
    print("\n--- 栈溢出防范总结 ---")
    print("1. ✅ 设置合理的递归深度限制")
    print("2. ✅ 优先考虑迭代而非深层递归")
    print("3. ✅ 使用记忆化减少重复计算")
    print("4. ✅ 正确设计递归终止条件")
    print("5. ✅ 监控递归深度，及时预警")
    print("6. ✅ 理解尾递归优化的原理")


def demonstrate_stack_applications():
    """
    演示栈的实际应用场景
    """
    print("\n" + "=" * 50)
    print("🔧 栈的实际应用演示")
    print("=" * 50)
    
    print("\n--- 1. 撤销操作 (Undo) ---")
    # 模拟文本编辑器的撤销功能
    undo_stack = Stack()
    document_content = "Hello"
    
    def perform_action(action, content):
        """执行操作并记录到撤销栈"""
        undo_stack.push(('before', content))
        return action(content)
    
    def undo_last_action():
        """撤销最后一个操作"""
        if not undo_stack.is_empty():
            action_type, previous_content = undo_stack.pop()
            return previous_content
        return None
    
    print(f"初始文档: '{document_content}'")
    
    # 执行一系列操作
    document_content = perform_action(lambda x: x + " World", document_content)
    print(f"添加' World': '{document_content}'")
    
    document_content = perform_action(lambda x: x + "!", document_content)
    print(f"添加'!': '{document_content}'")
    
    # 撤销操作
    print("\n执行撤销操作:")
    previous = undo_last_action()
    if previous:
        document_content = previous
        print(f"撤销后: '{document_content}'")
    
    previous = undo_last_action()
    if previous:
        document_content = previous
        print(f"再次撤销: '{document_content}'")
    
    print("\n--- 2. 括号匹配检查 ---")
    
    def check_parentheses(expression):
        """检查括号是否匹配"""
        stack = Stack()
        matching = {'(': ')', '[': ']', '{': '}'}
        
        for char in expression:
            if char in matching:  # 左括号
                stack.push(char)
                print(f"遇到左括号 '{char}', 压入栈")
            elif char in matching.values():  # 右括号
                if stack.is_empty():
                    print(f"❌ 遇到右括号 '{char}', 但栈为空")
                    return False
                
                left = stack.pop()
                print(f"遇到右括号 '{char}', 弹出 '{left}'")
                
                if matching[left] != char:
                    print(f"❌ 括号不匹配: '{left}' 和 '{char}'")
                    return False
        
        result = stack.is_empty()
        if result:
            print("✅ 所有括号都匹配")
        else:
            print(f"❌ 还有未匹配的左括号: {stack.items}")
        
        return result
    
    # 测试各种括号表达式
    test_expressions = [
        "((()))",      # 正确
        "([{}])",      # 正确
        "((())",       # 错误：缺少右括号
        "())",         # 错误：多余右括号
        "([)]"         # 错误：交叉匹配
    ]
    
    for expr in test_expressions:
        print(f"\n检查表达式: '{expr}'")
        check_parentheses(expr)


def performance_comparison():
    """
    性能对比：列表末尾 vs 列表开头作为栈顶
    """
    print("\n" + "=" * 50)
    print("⚡ 性能对比：为什么选择列表末尾作为栈顶")
    print("=" * 50)
    
    import time
    
    def time_operation(operation, description):
        """测量操作的执行时间"""
        start_time = time.time()
        operation()
        end_time = time.time()
        print(f"{description}: {(end_time - start_time) * 1000:.2f} 毫秒")
    
    # 测试数据量
    n = 10000
    
    print(f"测试数据量: {n} 次操作")
    
    # 方法1：使用列表末尾作为栈顶（推荐）
    def test_append_pop():
        stack = []
        # Push操作
        for i in range(n):
            stack.append(i)  # O(1)
        # Pop操作  
        for i in range(n):
            stack.pop()      # O(1)
    
    # 方法2：使用列表开头作为栈顶（不推荐）
    def test_insert_pop_front():
        stack = []
        # Push操作
        for i in range(n):
            stack.insert(0, i)  # O(n) - 需要移动所有元素
        # Pop操作
        for i in range(n):
            stack.pop(0)        # O(n) - 需要移动所有元素
    
    print("\n方法对比:")
    time_operation(test_append_pop, "✅ 末尾操作 (append/pop)")
    time_operation(test_insert_pop_front, "❌ 开头操作 (insert/pop)")
    
    print("\n结论:")
    print("• 使用列表末尾作为栈顶：每个操作O(1)，总体O(n)")
    print("• 使用列表开头作为栈顶：每个操作O(n)，总体O(n²)")
    print("• 性能差异可能达到几百倍！")


if __name__ == "__main__":
    """
    主程序 - 运行所有演示
    """
    print("🌟 欢迎来到第08章：杯子塔与后悔药的哲学")
    print("📚 让我们一起探索栈的奥秘！")
    
    # 运行所有演示
    demonstrate_stack_operations()
    demonstrate_linked_stack()
    compare_stack_implementations()
    demonstrate_queue_with_stacks()
    demonstrate_stack_overflow()
    demonstrate_stack_applications()
    performance_comparison()
    
    print("\n" + "=" * 50)
    print("🎊 栈的学习之旅结束了！")
    print("💡 记住：栈是后进先出，就像叠盘子一样")
    print("🚀 下一章我们将学习队列：先进先出的排队艺术")
    print("=" * 50) 