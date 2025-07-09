"""
🍬 第04章：糖葫芦的秘密 - 单向链表完整实现
糖果味数据结构与算法 by 安妮的实验室

这个文件展示了单向链表的完整实现，包括插入、删除、查找等所有操作
每个节点就像糖葫芦上的果子，通过指针(竹签)串联起来
"""

class ListNode:
    """
    链表中的单个节点类
    
    每个节点包含两个部分：
    1. data: 存储的数据
    2. next: 指向下一个节点的指针
    """
    
    def __init__(self, data):
        """
        初始化一个新节点
        
        参数:
            data: 要存储在节点中的数据
        """
        self.data = data    # 节点存储的实际数据
        self.next = None    # 指向下一个节点的指针，初始化为None（空指针）
        
        print(f"🍓 创建了一个新节点：{data}")

class SinglyLinkedList:
    """
    单向链表的完整实现
    
    单向链表是一种线性数据结构，节点通过指针连接
    只能从头节点开始，按顺序访问每个节点
    """
    
    def __init__(self):
        """
        初始化一个空的单向链表
        """
        self.head = None    # 头指针，指向链表的第一个节点，空链表时为None
        self.size = 0       # 链表中节点的数量，用于快速获取长度
        
        print("🎯 创建了一个空的单向链表！")
    
    def is_empty(self):
        """
        检查链表是否为空
        
        返回:
            bool: True表示链表为空，False表示链表有节点
        """
        return self.head is None  # 如果头指针为None，则链表为空
    
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
        new_node = ListNode(data)  # 创建新节点
        new_node.next = self.head  # 新节点的next指针指向原来的头节点
        self.head = new_node       # 头指针指向新节点（新节点成为第一个节点）
        self.size += 1             # 节点数量加1
        
        print(f"🚀 在头部插入了 {data}，现在有 {self.size} 个节点")
    
    def append(self, data):
        """
        在链表尾部插入新节点（尾插法）
        
        时间复杂度：O(n) - 线性时间，因为需要遍历到最后一个节点
        
        参数:
            data: 要插入的数据
        """
        new_node = ListNode(data)  # 创建新节点
        
        if self.is_empty():  # 如果链表为空
            # 空链表时，新节点既是第一个节点也是最后一个节点
            self.head = new_node
        else:
            # 链表不为空时，需要找到最后一个节点
            current = self.head  # 从头节点开始遍历
            
            # 遍历到最后一个节点（next为None的节点）
            # 注意：使用current.next作为循环条件，而不是current
            # 这样循环结束时，current指向最后一个真实节点
            while current.next:
                current = current.next  # 移动到下一个节点
            
            # 现在current指向最后一个节点，将新节点连接到末尾
            current.next = new_node
        
        self.size += 1
        print(f"🎯 在尾部插入了 {data}，现在有 {self.size} 个节点")
    
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
            print(f"❌ 索引 {index} 超出范围！链表长度为 {self.size}")
            return False
        
        if index == 0:  # 在头部插入
            self.prepend(data)
            return True
        
        if index == self.size:  # 在尾部插入
            self.append(data)
            return True
        
        # 在中间位置插入
        new_node = ListNode(data)
        
        # 找到插入位置的前一个节点（第index-1个节点）
        current = self.head
        for i in range(index - 1):  # 遍历index-1次
            current = current.next
        
        # 执行插入操作：先连后断的原则
        new_node.next = current.next  # 新节点指向下一个节点
        current.next = new_node       # 前一个节点指向新节点
        
        self.size += 1
        print(f"🎪 在位置 {index} 插入了 {data}，现在有 {self.size} 个节点")
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
            print("❌ 链表为空，无法删除")
            return False
        
        # 特殊情况：删除头节点
        if self.head.data == data:
            self.head = self.head.next  # 头指针指向第二个节点
            self.size -= 1
            print(f"🗑️ 删除了头节点 {data}，现在有 {self.size} 个节点")
            return True
        
        # 查找要删除的节点，需要记录前驱节点
        prev = self.head           # 前驱节点（要删除节点的前一个节点）
        current = self.head.next   # 当前检查的节点
        
        while current:  # 遍历链表
            if current.data == data:  # 找到目标节点
                # 删除操作：让前驱节点跳过当前节点
                prev.next = current.next
                self.size -= 1
                print(f"🗑️ 删除了节点 {data}，现在有 {self.size} 个节点")
                return True
            
            # 移动到下一个节点
            prev = current
            current = current.next
        
        print(f"❌ 未找到节点 {data}")
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
            print(f"❌ 索引 {index} 超出范围！链表长度为 {self.size}")
            return None
        
        # 特殊情况：删除头节点
        if index == 0:
            deleted_data = self.head.data
            self.head = self.head.next
            self.size -= 1
            print(f"📍 删除了位置 {index} 的节点 {deleted_data}")
            return deleted_data
        
        # 删除中间或尾部节点：找到前驱节点
        prev = self.head
        for i in range(index - 1):  # 遍历到第index-1个节点
            prev = prev.next
        
        # 执行删除操作
        to_delete = prev.next           # 要删除的节点
        deleted_data = to_delete.data   # 保存要删除的数据
        prev.next = to_delete.next      # 前驱节点跳过要删除的节点
        
        self.size -= 1
        print(f"📍 删除了位置 {index} 的节点 {deleted_data}")
        return deleted_data
    
    def find(self, data):
        """
        查找指定数据的节点位置
        
        时间复杂度：O(n) - 线性时间，最坏情况需要遍历整个链表
        
        参数:
            data: 要查找的数据
            
        返回:
            int: 节点位置（从0开始），未找到返回-1
        """
        current = self.head  # 从头节点开始
        index = 0            # 当前检查的位置
        
        while current:  # 遍历链表
            if current.data == data:  # 找到目标数据
                print(f"🔍 找到了 {data}，位置为 {index}")
                return index
            current = current.next  # 移动到下一个节点
            index += 1              # 位置递增
        
        print(f"❌ 未找到 {data}")
        return -1
    
    def get(self, index):
        """
        获取指定位置的节点数据
        
        时间复杂度：O(n) - 线性时间，需要遍历到指定位置
        
        参数:
            index: 节点位置（从0开始的索引）
            
        返回:
            节点的数据，位置无效返回None
        """
        # 检查索引是否有效
        if index < 0 or index >= self.size:
            print(f"❌ 索引 {index} 超出范围！链表长度为 {self.size}")
            return None
        
        current = self.head
        for i in range(index):  # 遍历index次到达目标位置
            current = current.next
        
        print(f"📦 位置 {index} 的数据是：{current.data}")
        return current.data
    
    def reverse(self):
        """
        反转链表（就地反转）
        
        时间复杂度：O(n) - 线性时间，需要遍历一次链表
        空间复杂度：O(1) - 常数空间，只使用几个指针变量
        
        这是链表的经典操作，需要改变所有节点的next指针方向
        """
        if self.is_empty() or self.size == 1:
            print("🔄 链表太短，无需反转")
            return
        
        # 三个指针：prev(前一个)、current(当前)、next(下一个)
        prev = None          # 前一个节点，初始为None
        current = self.head  # 当前处理的节点
        
        while current:
            next_node = current.next  # 先保存下一个节点的引用
            current.next = prev       # 当前节点指向前一个节点（反转指针）
            prev = current            # 前一个节点向前移动
            current = next_node       # 当前节点向前移动
        
        self.head = prev  # 更新头指针，指向原来的最后一个节点
        print("🔄 链表反转完成！")
    
    def display(self):
        """
        显示整个链表的内容
        
        时间复杂度：O(n) - 线性时间，需要遍历所有节点
        """
        if self.is_empty():
            print("🎨 链表为空：head -> NULL")
            return
        
        print("🎨 链表内容：", end="")
        current = self.head
        elements = []  # 收集所有元素
        
        while current:
            elements.append(str(current.data))
            current = current.next
        
        # 打印链表结构：元素1 -> 元素2 -> ... -> NULL
        print(" -> ".join(elements) + " -> NULL")
        print(f"   总共 {self.size} 个节点")
    
    def clear(self):
        """
        清空链表，删除所有节点
        
        时间复杂度：O(1) - 常数时间，只需要重置头指针和大小
        """
        self.head = None  # 头指针置空，所有节点变成垃圾回收对象
        self.size = 0     # 大小重置为0
        print("🧹 链表已清空！")


def demonstrate_linked_list():
    """
    单向链表的完整演示程序
    
    展示链表的各种操作，帮助理解链表的工作原理
    """
    print("\n" + "="*50)
    print("🍭 欢迎来到安妮的单向链表实验室！")
    print("="*50)
    
    # 创建空链表
    fruits = SinglyLinkedList()
    
    print("\n📋 第一部分：尾部插入操作")
    print("-" * 30)
    
    # 在末尾添加节点 - O(n)时间复杂度
    fruits.append("🍎苹果")
    fruits.append("🍇葡萄")
    fruits.append("🍓草莓")
    fruits.display()
    
    print("\n📋 第二部分：头部插入操作")
    print("-" * 30)
    
    # 在开头添加节点 - O(1)时间复杂度
    fruits.prepend("🍊橘子")
    fruits.display()
    
    print("\n📋 第三部分：指定位置插入")
    print("-" * 30)
    
    # 在指定位置插入 - O(n)时间复杂度
    fruits.insert(2, "🍒樱桃")
    fruits.display()
    
    print("\n📋 第四部分：查找操作")
    print("-" * 30)
    
    # 查找操作 - O(n)时间复杂度
    fruits.find("🍓草莓")        # 存在的元素
    fruits.find("🥝猕猴桃")      # 不存在的元素
    
    # 按位置获取元素 - O(n)时间复杂度
    fruits.get(0)  # 第一个节点
    fruits.get(2)  # 第三个节点
    
    print("\n📋 第五部分：删除操作")
    print("-" * 30)
    
    # 按值删除 - O(n)时间复杂度
    fruits.delete_by_value("🍇葡萄")
    fruits.display()
    
    # 按位置删除 - O(n)时间复杂度
    fruits.delete_by_index(1)
    fruits.display()
    
    print("\n📋 第六部分：链表反转")
    print("-" * 30)
    
    print("反转前：")
    fruits.display()
    
    fruits.reverse()  # O(n)时间复杂度
    
    print("反转后：")
    fruits.display()
    
    print("\n📋 第七部分：链表状态检查")
    print("-" * 30)
    
    print(f"🔍 链表是否为空：{fruits.is_empty()}")
    print(f"📏 链表长度：{len(fruits)}")
    
    print("\n📋 第八部分：清空链表")
    print("-" * 30)
    
    fruits.clear()
    fruits.display()
    print(f"🔍 清空后是否为空：{fruits.is_empty()}")
    
    print("\n🎉 单向链表实验完成！")
    print("💡 关键要点：")
    print("   - 头部插入：O(1) - 快速")
    print("   - 尾部插入：O(n) - 需要遍历")
    print("   - 随机访问：O(n) - 不支持直接访问")
    print("   - 插入删除：灵活，但需要找到位置")
    print("   - 内存占用：每个节点需要额外指针空间")


# 运行演示程序
if __name__ == "__main__":
    demonstrate_linked_list() 