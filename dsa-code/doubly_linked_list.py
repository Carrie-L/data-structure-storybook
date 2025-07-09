"""
🍬 第05章：双向小火车的魔法 - 双向链表完整实现
糖果味数据结构与算法 by 安妮的实验室

这个文件展示了双向链表的完整实现，包括双向插入、删除、遍历等所有操作
每个节点就像火车车厢，通过前后两个连接器(指针)连接起来
"""

class DoublyListNode:
    """
    双向链表中的单个节点类
    
    每个节点包含三个部分：
    1. data: 存储的数据
    2. next: 指向下一个节点的指针（前连接器）
    3. prev: 指向前一个节点的指针（后连接器）
    """
    
    def __init__(self, data):
        """
        初始化一个新的双向节点
        
        参数:
            data: 要存储在节点中的数据
        """
        self.data = data    # 节点存储的实际数据
        self.next = None    # 指向下一个节点的指针，初始化为None（空指针）
        self.prev = None    # 指向前一个节点的指针，初始化为None（空指针）
        
        print(f"🚃 创建了一个新车厢：{data}")

class DoublyLinkedList:
    """
    双向链表的完整实现
    
    双向链表是一种线性数据结构，节点通过双向指针连接
    可以从任意节点向前或向后遍历整个链表
    """
    
    def __init__(self):
        """
        初始化一个空的双向链表
        """
        self.head = None    # 头指针，指向链表的第一个节点（火车头）
        self.tail = None    # 尾指针，指向链表的最后一个节点（火车尾）
        self.size = 0       # 链表中节点的数量，用于快速获取长度
        
        print("🚆 创建了一个空的双向小火车！")
    
    def is_empty(self):
        """
        检查链表是否为空
        
        返回:
            bool: True表示链表为空，False表示链表有节点
        """
        return self.head is None and self.tail is None
    
    def __len__(self):
        """
        获取链表的长度（节点数量）
        
        返回:
            int: 链表中节点的数量
        """
        return self.size
    
    def prepend(self, data):
        """
        在链表头部插入新节点（头插法）
        
        时间复杂度：O(1) - 常数时间，因为直接操作头指针
        
        参数:
            data: 要插入的数据
        """
        new_node = DoublyListNode(data)  # 创建新车厢
        
        if self.is_empty():  # 如果火车是空的（没有任何车厢）
            # 为什么同时设置head和tail指向同一个节点？
            # 因为空火车加入第一节车厢时，这节车厢既是火车头也是火车尾
            self.head = self.tail = new_node
        else:
            # 火车不为空时，在头部添加新车厢
            new_node.next = self.head       # 新车厢的前连接器连接原火车头
            self.head.prev = new_node       # 原火车头的后连接器连接新车厢
            self.head = new_node            # 更新火车头指针到新车厢
        
        self.size += 1
        print(f"🚀 在火车头部添加了 {data}，现在有 {self.size} 节车厢")
    
    def append(self, data):
        """
        在链表尾部插入新节点（尾插法）
        
        时间复杂度：O(1) - 常数时间，因为有tail指针直接访问最后节点
        
        参数:
            data: 要插入的数据
        """
        new_node = DoublyListNode(data)  # 创建新车厢
        
        if self.is_empty():  # 如果火车是空的
            # 同样的原理：第一节车厢既是火车头也是火车尾
            self.head = self.tail = new_node
        else:
            # 火车不为空时，在尾部添加新车厢
            self.tail.next = new_node       # 原火车尾的前连接器连接新车厢
            new_node.prev = self.tail       # 新车厢的后连接器连接原火车尾
            self.tail = new_node            # 更新火车尾指针到新车厢
        
        self.size += 1
        print(f"🎯 在火车尾部添加了 {data}，现在有 {self.size} 节车厢")
    
    def insert(self, index, data):
        """
        在指定位置插入新节点
        
        时间复杂度：O(n) - 线性时间，需要遍历到指定位置
        
        参数:
            index: 插入位置（从0开始的索引）
            data: 要插入的数据
            
        返回:
            bool: 插入成功返回True，位置无效返回False
        """
        # 检查索引是否有效
        if index < 0 or index > self.size:
            print(f"❌ 索引 {index} 超出范围！火车长度为 {self.size}")
            return False
        
        if index == 0:  # 在头部插入
            self.prepend(data)
            return True
        
        if index == self.size:  # 在尾部插入
            self.append(data)
            return True
        
        # 在中间位置插入
        new_node = DoublyListNode(data)
        
        # 优化：选择从头部或尾部开始遍历，取较短的路径
        if index <= self.size // 2:
            # 从头部开始遍历（前半部分）
            current = self.head
            for i in range(index):  # 遍历index次到达目标位置
                current = current.next
        else:
            # 从尾部开始遍历（后半部分）
            current = self.tail
            for i in range(self.size - 1, index, -1):  # 从尾部往前遍历
                current = current.prev
        
        # 执行插入操作：在current位置之前插入新节点
        prev_node = current.prev        # 保存当前节点的前驱
        
        # 建立新节点的连接
        new_node.next = current         # 新节点指向当前节点
        new_node.prev = prev_node       # 新节点指向前驱节点
        
        # 更新相邻节点的连接
        prev_node.next = new_node       # 前驱节点指向新节点
        current.prev = new_node         # 当前节点指向新节点
        
        self.size += 1
        print(f"🎪 在位置 {index} 插入了 {data}，现在有 {self.size} 节车厢")
        return True
    
    def delete_by_value(self, data):
        """
        删除第一个匹配指定值的节点
        
        时间复杂度：O(n) - 线性时间，需要遍历查找目标节点
        
        参数:
            data: 要删除的节点数据
            
        返回:
            bool: 删除成功返回True，未找到返回False
        """
        if self.is_empty():
            print("❌ 火车是空的，无法删除")
            return False
        
        # 查找要删除的节点
        current = self.head
        while current:
            if current.data == data:  # 找到目标节点
                self._delete_node(current)  # 调用私有方法删除节点
                print(f"🗑️ 删除了车厢 {data}，现在有 {self.size} 节车厢")
                return True
            current = current.next
        
        print(f"❌ 未找到车厢 {data}")
        return False
    
    def delete_by_index(self, index):
        """
        删除指定位置的节点
        
        时间复杂度：O(n) - 线性时间，需要遍历到指定位置
        
        参数:
            index: 要删除的节点位置（从0开始的索引）
            
        返回:
            删除的节点数据，如果删除失败返回None
        """
        # 检查索引是否有效
        if index < 0 or index >= self.size:
            print(f"❌ 索引 {index} 超出范围！火车长度为 {self.size}")
            return None
        
        # 优化：选择从头部或尾部开始遍历，取较短的路径
        if index <= self.size // 2:
            # 从头部开始遍历
            current = self.head
            for i in range(index):
                current = current.next
        else:
            # 从尾部开始遍历
            current = self.tail
            for i in range(self.size - 1, index, -1):
                current = current.prev
        
        deleted_data = current.data     # 保存要删除的数据
        self._delete_node(current)      # 调用私有方法删除节点
        
        print(f"📍 删除了位置 {index} 的车厢 {deleted_data}")
        return deleted_data
    
    def _delete_node(self, node):
        """
        删除指定节点的私有方法（已知节点删除 - O(1)时间）
        
        这是双向链表的核心优势：已知节点可以在O(1)时间内删除
        
        参数:
            node: 要删除的节点对象
        """
        # if not node: 检查节点是否存在（是否为None或空值）
        if not node:
            return
        
        # 处理前驱节点的连接
        if node.prev:
            # 如果有前驱节点，让前驱节点的next指向当前节点的后继
            node.prev.next = node.next
        else:
            # 如果没有前驱节点，说明删除的是头节点
            # 更新头指针指向当前节点的后继
            self.head = node.next
        
        # 处理后继节点的连接
        if node.next:
            # 如果有后继节点，让后继节点的prev指向当前节点的前驱
            node.next.prev = node.prev
        else:
            # 如果没有后继节点，说明删除的是尾节点
            # 更新尾指针指向当前节点的前驱
            self.tail = node.prev
        
        self.size -= 1
        
        # 清理被删除节点的指针（可选，有助于垃圾回收）
        node.prev = None
        node.next = None
    
    def find(self, data):
        """
        从头部开始查找指定数据的节点位置
        
        时间复杂度：O(n) - 线性时间，最坏情况需要遍历整个链表
        
        参数:
            data: 要查找的数据
            
        返回:
            int: 节点位置（从0开始），未找到返回-1
        """
        current = self.head
        index = 0
        
        while current:
            if current.data == data:
                print(f"🔍 找到了 {data}，位置为 {index}")
                return index
            current = current.next
            index += 1
        
        print(f"❌ 未找到 {data}")
        return -1
    
    def find_from_tail(self, data):
        """
        从尾部开始查找指定数据的节点位置（双向链表独有）
        
        时间复杂度：O(n) - 线性时间，但如果数据在后半部分会更快
        
        参数:
            data: 要查找的数据
            
        返回:
            int: 节点位置（从0开始），未找到返回-1
        """
        current = self.tail
        index = self.size - 1
        
        while current:
            if current.data == data:
                print(f"🔍 从尾部找到了 {data}，位置为 {index}")
                return index
            current = current.prev
            index -= 1
        
        print(f"❌ 从尾部未找到 {data}")
        return -1
    
    def get(self, index):
        """
        获取指定位置的节点数据（优化版本）
        
        时间复杂度：O(n) - 线性时间，但选择最短路径遍历
        
        参数:
            index: 节点位置（从0开始的索引）
            
        返回:
            节点的数据，位置无效返回None
        """
        if index < 0 or index >= self.size:
            print(f"❌ 索引 {index} 超出范围！火车长度为 {self.size}")
            return None
        
        # 优化：选择从头部或尾部开始遍历，取较短的路径
        if index <= self.size // 2:
            # 从头部开始遍历（效率更高）
            current = self.head
            for i in range(index):
                current = current.next
        else:
            # 从尾部开始遍历（效率更高）
            current = self.tail
            for i in range(self.size - 1, index, -1):
                current = current.prev
        
        print(f"📦 位置 {index} 的车厢载有：{current.data}")
        return current.data
    
    def traverse_forward(self):
        """
        正向遍历链表（从头到尾）
        
        时间复杂度：O(n) - 线性时间，需要访问每个节点
        """
        if self.is_empty():
            print("🔄 火车是空的，无法遍历")
            return
        
        print("🔄 正向遍历火车：", end="")
        current = self.head
        elements = []
        
        # 为什么用 while current 而不是 while current.next？
        # 因为我们要遍历所有节点包括最后一个，当current为None时停止
        while current:
            elements.append(str(current.data))
            current = current.next  # 通过next指针向前移动
        
        print(" -> ".join(elements) + " -> NULL")
    
    def traverse_backward(self):
        """
        反向遍历链表（从尾到头）- 双向链表独有功能
        
        时间复杂度：O(n) - 线性时间，需要访问每个节点
        """
        if self.is_empty():
            print("🔄 火车是空的，无法遍历")
            return
        
        print("🔄 反向遍历火车：", end="")
        current = self.tail
        elements = []
        
        # 同样用 while current，从尾部开始通过prev指针向后移动
        while current:
            elements.append(str(current.data))
            current = current.prev  # 通过prev指针向后移动
        
        print(" -> ".join(elements) + " -> NULL")
    
    def reverse(self):
        """
        反转整个双向链表（就地反转）
        
        时间复杂度：O(n) - 线性时间，需要遍历一次链表
        空间复杂度：O(1) - 常数空间，只需要几个临时变量
        
        双向链表的反转比单向链表更简单，因为每个节点都知道前驱和后继
        """
        if self.is_empty() or self.size == 1:
            print("🔄 火车太短，无需反转")
            return
        
        current = self.head
        
        # 遍历每个节点，交换每个节点的prev和next指针
        while current:
            # 交换当前节点的prev和next指针
            current.prev, current.next = current.next, current.prev
            current = current.prev  # 注意：因为已经交换，所以向prev移动实际是向原来的next方向
        
        # 交换头尾指针
        self.head, self.tail = self.tail, self.head
        
        print("🔄 火车反转完成！")
    
    def display(self):
        """
        显示整个链表的内容和结构
        
        时间复杂度：O(n) - 线性时间，需要遍历所有节点
        """
        if self.is_empty():
            print("🎨 火车为空：head -> NULL <- tail")
            return
        
        print("🎨 双向火车结构：")
        print(f"   头指针(head) -> {self.head.data}")
        print(f"   尾指针(tail) -> {self.tail.data}")
        print("   正向链接：", end="")
        
        # 显示正向链接
        current = self.head
        forward_elements = []
        while current:
            forward_elements.append(str(current.data))
            current = current.next
        print(" <-> ".join(forward_elements))
        
        print(f"   总共 {self.size} 节车厢")
    
    def clear(self):
        """
        清空链表，删除所有节点
        
        时间复杂度：O(1) - 常数时间，只需要重置指针和大小
        """
        # 清理所有节点的指针连接（可选，有助于垃圾回收）
        current = self.head
        while current:
            next_node = current.next
            current.prev = None
            current.next = None
            current = next_node
        
        self.head = None
        self.tail = None
        self.size = 0
        print("🧹 双向火车已清空！")


def demonstrate_doubly_linked_list():
    """
    双向链表的完整演示程序
    
    展示双向链表的各种操作，特别是其相对于单向链表的优势
    """
    print("\n" + "="*50)
    print("🚆 欢迎来到安妮的双向小火车实验室！")
    print("="*50)
    
    # 创建空的双向链表
    train = DoublyLinkedList()
    
    print("\n📋 第一部分：基本插入操作")
    print("-" * 30)
    
    # 演示双向链表的快速插入操作
    train.append("🚂机车")        # 尾部插入 O(1)
    train.append("🚃客车")        # 尾部插入 O(1)
    train.prepend("🚄高铁")       # 头部插入 O(1)
    train.append("🚅动车")        # 尾部插入 O(1)
    train.display()
    
    print("\n📋 第二部分：双向遍历演示")
    print("-" * 30)
    
    # 展示双向遍历的独特能力
    train.traverse_forward()      # 正向遍历：高铁 -> 机车 -> 客车 -> 动车
    train.traverse_backward()     # 反向遍历：动车 -> 客车 -> 机车 -> 高铁
    
    print("\n📋 第三部分：优化的查找操作")
    print("-" * 30)
    
    # 演示双向查找的优势
    train.find("🚃客车")           # 从头开始查找
    train.find_from_tail("🚃客车") # 从尾开始查找（可能更快）
    
    # 演示优化的随机访问
    train.get(0)  # 从头部访问
    train.get(3)  # 从尾部访问（更快）
    
    print("\n📋 第四部分：高效的插入操作")
    print("-" * 30)
    
    # 在中间位置插入
    train.insert(2, "🚋地铁")      # 在位置2插入
    train.display()
    
    print("\n📋 第五部分：删除操作演示")
    print("-" * 30)
    
    # 演示各种删除操作
    train.delete_by_value("🚄高铁")  # 按值删除
    train.display()
    
    train.delete_by_index(1)          # 按位置删除
    train.display()
    
    print("\n📋 第六部分：链表反转")
    print("-" * 30)
    
    print("反转前：")
    train.traverse_forward()
    
    train.reverse()  # 反转整个链表
    
    print("反转后：")
    train.traverse_forward()
    
    print("\n📋 第七部分：性能对比总结")
    print("-" * 30)
    
    print("🚆 双向链表 vs 单向链表性能对比：")
    print("   • 头部插入：O(1) vs O(1) - 相同")
    print("   • 尾部插入：O(1) vs O(n) - 双向链表更快")
    print("   • 已知节点删除：O(1) vs O(n) - 双向链表更快")
    print("   • 反向遍历：O(n) vs 不支持 - 双向链表独有")
    print("   • 内存开销：更多 vs 更少 - 单向链表更省内存")
    
    print("\n📋 第八部分：清空链表")
    print("-" * 30)
    
    print(f"🔍 链表是否为空：{train.is_empty()}")
    print(f"📏 链表长度：{len(train)}")
    
    train.clear()
    train.display()
    print(f"🔍 清空后是否为空：{train.is_empty()}")
    
    print("\n🎉 双向链表实验完成！")
    print("💡 关键优势：")
    print("   - 尾部操作：O(1) - 超快")
    print("   - 双向遍历：正向反向都支持")
    print("   - 已知节点删除：O(1) - 革命性优势")
    print("   - 算法优化：很多高级算法的基础")
    print("💡 适用场景：")
    print("   - LRU缓存、浏览器历史、音乐播放器")
    print("   - 需要频繁双向访问的数据结构")


# 运行演示程序
if __name__ == "__main__":
    demonstrate_doubly_linked_list() 