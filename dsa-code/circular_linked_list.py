"""
🍬 第06章：永不停歇的旋转木马 - 循环链表完整实现
糖果味数据结构与算法 by 安妮的实验室

这个文件展示了循环链表的完整实现，包括：
- 单向循环链表的基本操作
- 约瑟夫环问题的解决方案
- 环检测算法（快慢指针）
- 实际应用场景的代码示例

循环链表就像旋转木马，每匹木马都知道下一匹是谁，
最后一匹木马指向第一匹，形成永不停歇的循环
"""

class CircularNode:
    """
    循环链表中的单个节点类
    
    每个节点包含两个部分：
    1. data: 存储的数据（就像木马的编号）
    2. next: 指向下一个节点的指针
    """
    
    def __init__(self, data):
        """
        初始化一个新的循环链表节点
        
        参数:
            data: 要存储在节点中的数据
        """
        self.data = data    # 节点存储的实际数据
        self.next = None    # 指向下一个节点的指针，初始化为None
        
        print(f"🎠 创建了一匹新木马：{data}")

class CircularLinkedList:
    """
    单向循环链表的完整实现
    
    循环链表是一种特殊的链表，最后一个节点指向第一个节点
    形成闭环，没有NULL结尾，可以无限循环遍历
    """
    
    def __init__(self):
        """
        初始化一个空的循环链表
        """
        self.head = None    # 头指针，指向链表的任意一个节点（通常是"第一个"）
        self.size = 0       # 链表中节点的数量，用于循环控制
        
        print("🎪 建造了一个空的旋转木马平台！")
    
    def is_empty(self):
        """
        检查循环链表是否为空
        
        返回:
            bool: 如果链表为空返回True，否则返回False
        """
        return self.head is None
    
    def __len__(self):
        """
        获取链表长度（支持len()函数）
        
        返回:
            int: 链表中节点的数量
        """
        return self.size
    
    def append(self, data):
        """
        在循环链表尾部添加新节点
        
        参数:
            data: 要添加的数据
            
        时间复杂度: O(n) - 需要遍历找到最后一个节点
        空间复杂度: O(1) - 只需要常数额外空间
        """
        new_node = CircularNode(data)
        
        if self.is_empty():
            # 如果是第一个节点，它指向自己形成最小的循环
            # 这是循环链表的关键：即使只有一个节点，也要形成环
            new_node.next = new_node
            self.head = new_node
        else:
            # 找到最后一个节点（它的next指向head）
            current = self.head
            while current.next != self.head:  # 遍历直到找到指向head的节点
                current = current.next
            
            # 建立新的循环连接：
            # 1. 新节点指向原来的头节点（保持循环）
            new_node.next = self.head
            # 2. 原来的最后一个节点指向新节点
            current.next = new_node
        
        self.size += 1
        print(f"🎠 添加了木马 {data}，旋转木马现在有 {self.size} 匹木马")
    
    def prepend(self, data):
        """
        在循环链表头部添加新节点
        
        参数:
            data: 要添加的数据
            
        时间复杂度: O(n) - 需要找到最后一个节点来维护循环
        空间复杂度: O(1)
        """
        new_node = CircularNode(data)
        
        if self.is_empty():
            # 空链表的情况，和append相同
            new_node.next = new_node
            self.head = new_node
        else:
            # 找到最后一个节点（它的next指向head）
            current = self.head
            while current.next != self.head:
                current = current.next
            
            # 建立连接：
            # 1. 新节点指向原来的头节点
            new_node.next = self.head
            # 2. 最后一个节点指向新节点（维护循环）
            current.next = new_node
            # 3. 更新头指针到新节点
            self.head = new_node
        
        self.size += 1
        print(f"🚀 在旋转木马头部添加了 {data}，现在有 {self.size} 匹木马")
    
    def insert(self, index, data):
        """
        在指定位置插入新节点
        
        参数:
            index: 插入位置（0-based索引）
            data: 要插入的数据
            
        时间复杂度: O(n) - 需要遍历到指定位置
        空间复杂度: O(1)
        """
        # 边界检查
        if index < 0 or index > self.size:
            raise IndexError(f"插入位置 {index} 超出范围 [0, {self.size}]")
        
        # 特殊情况处理
        if index == 0:
            self.prepend(data)
            return
        if index == self.size:
            self.append(data)
            return
        
        # 一般情况：在中间位置插入
        new_node = CircularNode(data)
        current = self.head
        
        # 移动到插入位置的前一个节点
        for _ in range(index - 1):
            current = current.next
        
        # 插入新节点：
        # 1. 新节点指向当前节点的下一个节点
        new_node.next = current.next
        # 2. 当前节点指向新节点
        current.next = new_node
        
        self.size += 1
        print(f"🎠 在位置 {index} 插入了木马 {data}")
    
    def delete_by_value(self, data):
        """
        删除第一个匹配指定值的节点
        
        参数:
            data: 要删除的数据值
            
        返回:
            bool: 删除成功返回True，未找到返回False
            
        时间复杂度: O(n) - 最坏情况遍历整个链表
        空间复杂度: O(1)
        """
        if self.is_empty():
            print(f"❌ 旋转木马是空的，无法删除 {data}")
            return False
        
        # 特殊情况：只有一个节点
        if self.size == 1:
            if self.head.data == data:
                print(f"🗑️ 删除了唯一的木马 {data}，旋转木马现在是空的")
                self.head = None
                self.size = 0
                return True
            else:
                print(f"❌ 没有找到木马 {data}")
                return False
        
        # 特殊情况：要删除头节点
        if self.head.data == data:
            # 找到最后一个节点
            current = self.head
            while current.next != self.head:
                current = current.next
            
            # 让最后一个节点指向新的头节点
            current.next = self.head.next
            # 更新头指针
            self.head = self.head.next
            self.size -= 1
            print(f"🗑️ 删除了头部木马 {data}，剩余 {self.size} 匹木马")
            return True
        
        # 一般情况：删除非头节点
        prev = self.head
        current = self.head.next
        
        # 遍历寻找目标节点
        while current != self.head:  # 注意：在循环链表中，终止条件是回到头节点
            if current.data == data:
                # 找到目标，执行删除
                prev.next = current.next
                self.size -= 1
                print(f"🗑️ 删除了木马 {data}，剩余 {self.size} 匹木马")
                return True
            prev = current
            current = current.next
        
        print(f"❌ 没有找到木马 {data}")
        return False
    
    def delete_by_index(self, index):
        """
        删除指定位置的节点
        
        参数:
            index: 要删除的位置（0-based索引）
            
        返回:
            删除的节点数据，如果索引无效返回None
            
        时间复杂度: O(n) - 需要遍历到指定位置
        空间复杂度: O(1)
        """
        # 边界检查
        if index < 0 or index >= self.size:
            print(f"❌ 删除位置 {index} 超出范围 [0, {self.size-1}]")
            return None
        
        if self.is_empty():
            print("❌ 旋转木马是空的，无法删除")
            return None
        
        # 特殊情况：只有一个节点
        if self.size == 1:
            data = self.head.data
            self.head = None
            self.size = 0
            print(f"🗑️ 删除了位置 {index} 的木马 {data}，旋转木马现在是空的")
            return data
        
        # 特殊情况：删除头节点
        if index == 0:
            # 找到最后一个节点
            current = self.head
            while current.next != self.head:
                current = current.next
            
            data = self.head.data
            # 让最后一个节点指向新的头节点
            current.next = self.head.next
            # 更新头指针
            self.head = self.head.next
            self.size -= 1
            print(f"🗑️ 删除了位置 {index} 的木马 {data}，剩余 {self.size} 匹木马")
            return data
        
        # 一般情况：删除非头节点
        current = self.head
        # 移动到要删除位置的前一个节点
        for _ in range(index - 1):
            current = current.next
        
        # 保存要删除的数据
        data = current.next.data
        # 跳过要删除的节点
        current.next = current.next.next
        self.size -= 1
        print(f"🗑️ 删除了位置 {index} 的木马 {data}，剩余 {self.size} 匹木马")
        return data
    
    def find(self, data):
        """
        查找指定数据在链表中的位置
        
        参数:
            data: 要查找的数据
            
        返回:
            int: 数据的索引位置，未找到返回-1
            
        时间复杂度: O(n) - 最坏情况遍历整个链表
        空间复杂度: O(1)
        """
        if self.is_empty():
            return -1
        
        current = self.head
        index = 0
        
        # 遍历一圈寻找目标
        for _ in range(self.size):
            if current.data == data:
                print(f"🔍 找到木马 {data}，位置是第 {index} 个")
                return index
            current = current.next
            index += 1
        
        print(f"❌ 没有找到木马 {data}")
        return -1
    
    def get(self, index):
        """
        获取指定位置的节点数据
        
        参数:
            index: 要获取的位置（0-based索引）
            
        返回:
            指定位置的数据，索引无效返回None
            
        时间复杂度: O(n) - 需要遍历到指定位置
        空间复杂度: O(1)
        """
        if index < 0 or index >= self.size:
            print(f"❌ 访问位置 {index} 超出范围 [0, {self.size-1}]")
            return None
        
        current = self.head
        # 移动到指定位置
        for _ in range(index):
            current = current.next
        
        return current.data
    
    def traverse(self, rounds=1):
        """
        遍历循环链表指定圈数
        
        参数:
            rounds: 要转动的圈数，默认1圈
            
        时间复杂度: O(n * rounds) - 每圈遍历n个节点
        空间复杂度: O(1)
        """
        if self.is_empty():
            print("🎪 旋转木马是空的，没有木马可以转动")
            return
        
        print(f"🎠 旋转木马开始转动 {rounds} 圈：")
        current = self.head
        
        for round_num in range(rounds):
            print(f"第 {round_num + 1} 圈：", end="")
            
            # 转动一整圈
            for _ in range(self.size):
                print(f" {current.data}", end="")
                current = current.next
            print()  # 换行
    
    def traverse_once(self):
        """
        安全地遍历一圈（用于调试和显示）
        
        时间复杂度: O(n)
        空间复杂度: O(1)
        """
        if self.is_empty():
            print("空链表")
            return
        
        current = self.head
        print(f"{current.data}", end="")
        current = current.next
        
        # 使用"回到起点"法安全遍历
        while current != self.head:
            print(f" → {current.data}", end="")
            current = current.next
        print(" → (回到起点)")
    
    def clear(self):
        """
        清空整个循环链表
        
        时间复杂度: O(1) - 只需要重置头指针和大小
        空间复杂度: O(1)
        """
        self.head = None
        self.size = 0
        print("🧹 清空了旋转木马，所有木马都已移除")
    
    def display(self):
        """
        显示循环链表的当前状态
        """
        print(f"🎪 旋转木马状态：{self.size} 匹木马")
        if not self.is_empty():
            print("🎠 木马排列：", end="")
            self.traverse_once()


def josephus_problem(n, k):
    """
    约瑟夫环问题：n个人围成圆圈，每隔k个人淘汰一个
    
    这是循环链表最经典的应用，通过模拟淘汰过程找到最后的幸存者
    
    参数:
        n: 总人数
        k: 间隔数（数到第k个人淘汰）
    
    返回:
        最后幸存者的原始位置
        
    时间复杂度: O(n²) - 每次删除需要O(n)时间找前驱，共删除n-1次
    空间复杂度: O(n) - 存储n个节点
    """
    print(f"\n🎪 约瑟夫环问题：{n}个人，每隔{k}个人淘汰一个")
    
    # 创建循环链表，代表n个人围成圆圈
    circle = CircularLinkedList()
    for i in range(1, n + 1):
        circle.append(f"人{i}")
    
    print("🎠 初始圆圈：", end="")
    current = circle.head
    for _ in range(n):
        print(f" {current.data}", end="")
        current = current.next
    print()
    
    # 模拟淘汰过程
    current = circle.head
    while circle.size > 1:
        # 数k-1个人（因为当前人算第1个）
        for _ in range(k - 1):
            current = current.next
        
        # 记录要淘汰的人
        eliminated = current.data
        
        # 找到被淘汰者的前驱（需要绕一圈）
        prev = current
        while prev.next != current:
            prev = prev.next
        
        # 执行淘汰：让前驱跳过当前节点
        prev.next = current.next
        
        # 如果淘汰的是head，更新head
        if current == circle.head:
            circle.head = current.next
        
        # 移动到下一个人继续
        current = current.next
        circle.size -= 1
        
        print(f"❌ 淘汰了 {eliminated}，剩余 {circle.size} 人")
    
    # 最后的幸存者
    survivor = circle.head.data
    print(f"🏆 最后的幸存者是：{survivor}")
    return survivor


def has_cycle(head):
    """
    检测链表是否有环（Floyd判圈算法 - 快慢指针法）
    
    这个算法用于检测普通链表是否意外形成了环
    
    参数:
        head: 链表的头节点
    
    返回:
        bool: 如果有环返回True，否则返回False
        
    时间复杂度: O(n) - 最多遍历链表两次
    空间复杂度: O(1) - 只需要两个指针变量
    
    算法原理：
    - 快指针每次走2步，慢指针每次走1步
    - 如果链表有环，快指针最终会追上慢指针
    - 如果链表无环，快指针会先到达末尾（NULL）
    """
    if not head or not head.next:
        return False
    
    slow = head      # 慢指针（乌龟），每次走一步
    fast = head      # 快指针（兔子），每次走两步
    
    print("🐢🐰 开始龟兔赛跑检测环...")
    step = 0
    
    while fast and fast.next:
        slow = slow.next        # 慢指针走1步
        fast = fast.next.next   # 快指针走2步
        step += 1
        
        if slow == fast:        # 相遇说明有环
            print(f"🎯 第{step}步：快慢指针相遇，检测到环！")
            return True
    
    print(f"🏁 快指针到达末尾，链表无环")
    return False


def find_cycle_start(head):
    """
    找到环的起始位置（Floyd算法的扩展）
    
    参数:
        head: 链表的头节点
    
    返回:
        环的起始节点，如果无环返回None
        
    时间复杂度: O(n)
    空间复杂度: O(1)
    
    算法原理：
    1. 使用快慢指针找到相遇点
    2. 将一个指针重置到头节点
    3. 两个指针同时每次走一步，相遇点即为环的起始位置
    """
    if not head or not head.next:
        return None
    
    # 第一阶段：检测是否有环
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # 无环
    
    # 第二阶段：找到环的起始位置
    slow = head  # 重置慢指针到头节点
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow  # 环的起始位置


def demonstrate_circular_linked_list():
    """
    演示循环链表的各种操作
    """
    print("=" * 50)
    print("🎪 循环链表（旋转木马）功能演示")
    print("=" * 50)
    
    # 创建循环链表
    print("\n📝 1. 创建旋转木马并添加木马")
    carousel = CircularLinkedList()
    
    carousel.append("白马")
    carousel.append("黑马")
    carousel.append("斑马")
    carousel.prepend("红马")
    carousel.display()
    
    # 遍历演示
    print("\n🎠 2. 旋转木马转动演示")
    carousel.traverse(2)  # 转2圈
    
    # 查找操作
    print("\n🔍 3. 查找木马")
    carousel.find("斑马")
    carousel.find("金马")  # 不存在的马
    
    # 插入操作
    print("\n➕ 4. 在指定位置插入木马")
    carousel.insert(2, "紫马")
    carousel.display()
    
    # 删除操作
    print("\n🗑️ 5. 删除木马")
    carousel.delete_by_value("黑马")
    carousel.delete_by_index(0)  # 删除头节点
    carousel.display()
    
    # 约瑟夫环问题演示
    print("\n🎯 6. 约瑟夫环问题演示")
    josephus_problem(7, 3)
    
    # 环检测演示
    print("\n🔍 7. 环检测算法演示")
    # 创建一个有环的链表进行测试
    test_node1 = CircularNode("A")
    test_node2 = CircularNode("B") 
    test_node3 = CircularNode("C")
    
    # 构造环：A -> B -> C -> B (B和C形成环)
    test_node1.next = test_node2
    test_node2.next = test_node3
    test_node3.next = test_node2  # 形成环
    
    print("测试有环链表：A -> B -> C -> B")
    has_cycle(test_node1)
    
    # 构造无环链表
    test_node3.next = None  # 断开环
    print("测试无环链表：A -> B -> C -> NULL")
    has_cycle(test_node1)
    
    print("\n✅ 循环链表演示完成！")


# 实际应用示例：简单的轮播系统
class SimpleCarousel:
    """
    简单的轮播系统 - 循环链表的实际应用
    
    模拟网页轮播图、音乐播放列表等循环播放的场景
    """
    
    def __init__(self):
        self.items = CircularLinkedList()
        self.current = None
    
    def add_item(self, item):
        """添加轮播项目"""
        self.items.append(item)
        if self.current is None:
            self.current = self.items.head
    
    def next_item(self):
        """切换到下一个项目"""
        if self.current:
            self.current = self.current.next
            return self.current.data
        return None
    
    def current_item(self):
        """获取当前项目"""
        return self.current.data if self.current else None
    
    def auto_play(self, count):
        """自动播放指定次数"""
        print(f"🎵 开始自动轮播 {count} 次：")
        for i in range(count):
            current = self.current_item()
            print(f"播放第 {i+1} 次：{current}")
            self.next_item()


def demonstrate_carousel_application():
    """
    演示轮播系统的实际应用
    """
    print("\n" + "=" * 50)
    print("🎵 轮播系统应用演示")
    print("=" * 50)
    
    # 创建音乐播放列表
    playlist = SimpleCarousel()
    playlist.add_item("🎵 《夜的钢琴曲》")
    playlist.add_item("🎵 《Canon in D》")
    playlist.add_item("🎵 《月光奏鸣曲》")
    playlist.add_item("🎵 《致爱丽丝》")
    
    # 自动播放
    playlist.auto_play(8)  # 播放8次，会循环播放列表
    
    print("\n✅ 轮播系统演示完成！")


if __name__ == "__main__":
    # 运行所有演示
    demonstrate_circular_linked_list()
    demonstrate_carousel_application() 