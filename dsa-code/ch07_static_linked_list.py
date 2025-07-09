"""
第07章：图书馆的魔法编号系统 - 静态链表完整实现
糖果味的完整实现 📚

这个文件包含了静态链表的完整实现，用于在固定内存空间中模拟链表操作。
静态链表就像一个智慧的图书管理员，用数组下标代替内存地址，
在固定的空间里实现灵活的数据管理。
"""

class StaticLinkedList:
    """
    静态链表类 - 图书馆的魔法编号系统
    
    就像安妮发现的图书馆管理方法一样，
    用固定的书架位置配合灵活的编号指引，
    实现高效的数据管理～
    """
    
    def __init__(self, max_size=10):
        """
        初始化静态链表
        
        参数:
            max_size: 静态链表的最大容量（书架总位置数）
        """
        self.max_size = max_size
        
        # 创建固定大小的数组，每个元素是一个字典(包含data和next)
        # 相当于准备好固定数量的书架位置
        self.nodes = [{'data': None, 'next': i+1} for i in range(max_size)]
        
        # 最后一个节点的next指向-1，表示空闲链表的结束
        self.nodes[max_size-1]['next'] = -1
        
        self.head = -1        # 数据链表头：-1表示空链表
        self.free_head = 0    # 空闲链表头：从位置0开始
        self.size = 0         # 当前存储的元素数量
        
        print(f"📚 图书馆魔法编号系统启动！")
        print(f"   书架总位置：{max_size}")
        print(f"   数据链表头：{self.head} (空)")
        print(f"   空闲链表头：{self.free_head}")
        self._display_structure()
    
    def is_empty(self):
        """检查链表是否为空"""
        return self.head == -1
    
    def is_full(self):
        """检查链表是否已满"""
        return self.free_head == -1
    
    def __len__(self):
        """返回链表长度"""
        return self.size
    
    def insert_at_head(self, data):
        """
        在链表头部插入新元素
        
        就像在阅读序列的开头添加一本新书！
        
        参数:
            data: 要插入的数据（书名）
        
        返回:
            bool: 是否插入成功
        """
        print(f"\n📥 准备在开头插入：'{data}'")
        
        # 步骤1：检查是否还有空闲节点
        if self.free_head == -1:
            print("❌ 书架已满，无法插入新书！")
            return False
        
        # 步骤2：获取空闲位置
        new_pos = self.free_head  # 记录要使用的空闲位置
        print(f"   🎯 从空闲链表获取位置：{new_pos}")
        
        # 步骤3：更新空闲链表头 
        self.free_head = self.nodes[new_pos]['next']  # 空闲头指向下一个空位
        print(f"   📋 空闲链表头更新为：{self.free_head}")
        
        # 步骤4：在新位置存储数据
        self.nodes[new_pos]['data'] = data  # 存储实际数据
        print(f"   📖 在位置{new_pos}存储数据：'{data}'")
        
        # 步骤5：建立链接关系
        self.nodes[new_pos]['next'] = self.head  # 新节点指向原头节点
        self.head = new_pos  # 更新数据链表头
        self.size += 1
        print(f"   🔗 新的数据链表头：{self.head}")
        
        print(f"✅ 成功插入！当前数据链表长度：{self.size}")
        return True
    
    def delete_at_head(self):
        """
        删除链表头部元素
        
        就像从阅读序列中移除第一本书！
        
        返回:
            删除的数据，如果链表为空则返回None
        """
        print(f"\n🗑️ 准备删除开头元素")
        
        if self.head == -1:
            print("❌ 链表为空，无法删除")
            return None
        
        # 步骤1：保存要删除的信息
        deleted_index = self.head
        deleted_data = self.nodes[self.head]['data']
        print(f"   🎯 准备删除位置{deleted_index}的数据：'{deleted_data}'")
        
        # 步骤2：数据链表跳过被删除节点
        self.head = self.nodes[self.head]['next']  # 头指针指向下一个
        print(f"   📋 数据链表头更新为：{self.head}")
        
        # 步骤3：清空删除位置的数据
        self.nodes[deleted_index]['data'] = None
        print(f"   🧹 清空位置{deleted_index}的数据")
        
        # 步骤4：将空出的位置加入空闲链表
        self.nodes[deleted_index]['next'] = self.free_head  # 指向原空闲头
        self.free_head = deleted_index  # 成为新的空闲头
        self.size -= 1
        print(f"   🔄 位置{deleted_index}加入空闲链表，新空闲头：{self.free_head}")
        
        print(f"✅ 成功删除！当前数据链表长度：{self.size}")
        return deleted_data
    
    def insert_at_index(self, index, data):
        """
        在指定位置插入元素
        
        参数:
            index: 插入位置（从0开始）
            data: 要插入的数据
        """
        if index < 0 or index > self.size:
            print(f"❌ 插入位置 {index} 超出范围 [0, {self.size}]")
            return False
        
        if index == 0:
            return self.insert_at_head(data)
        
        if self.is_full():
            print("❌ 链表已满，无法插入")
            return False
        
        print(f"\n📥 在位置 {index} 插入：'{data}'")
        
        # 找到插入位置的前一个节点
        prev_pos = self.head
        for i in range(index - 1):
            prev_pos = self.nodes[prev_pos]['next']
        
        # 获取新节点位置
        new_pos = self.free_head
        self.free_head = self.nodes[new_pos]['next']
        
        # 插入新节点
        self.nodes[new_pos]['data'] = data
        self.nodes[new_pos]['next'] = self.nodes[prev_pos]['next']
        self.nodes[prev_pos]['next'] = new_pos
        self.size += 1
        
        print(f"✅ 在位置 {index} 成功插入 '{data}'")
        return True
    
    def delete_by_value(self, data):
        """
        根据值删除元素
        
        参数:
            data: 要删除的数据值
        """
        if self.is_empty():
            print("❌ 链表为空，无法删除")
            return False
        
        print(f"\n🔍 查找并删除：'{data}'")
        
        # 如果是头节点
        if self.nodes[self.head]['data'] == data:
            self.delete_at_head()
            return True
        
        # 查找目标节点
        prev_pos = self.head
        current_pos = self.nodes[self.head]['next']
        
        while current_pos != -1:
            if self.nodes[current_pos]['data'] == data:
                # 删除找到的节点
                self.nodes[prev_pos]['next'] = self.nodes[current_pos]['next']
                
                # 回收空间
                self.nodes[current_pos]['data'] = None
                self.nodes[current_pos]['next'] = self.free_head
                self.free_head = current_pos
                self.size -= 1
                
                print(f"✅ 成功删除 '{data}'")
                return True
            
            prev_pos = current_pos
            current_pos = self.nodes[current_pos]['next']
        
        print(f"❌ 未找到 '{data}'")
        return False
    
    def search(self, data):
        """
        查找元素
        
        参数:
            data: 要查找的数据
        
        返回:
            元素在链表中的位置（从0开始），如果不存在返回-1
        """
        print(f"\n🔍 查找：'{data}'")
        
        current_pos = self.head
        index = 0
        
        while current_pos != -1:
            if self.nodes[current_pos]['data'] == data:
                print(f"✅ 在位置 {index} 找到 '{data}'")
                return index
            
            current_pos = self.nodes[current_pos]['next']
            index += 1
        
        print(f"❌ 未找到 '{data}'")
        return -1
    
    def get(self, index):
        """
        获取指定位置的元素
        
        参数:
            index: 位置索引（从0开始）
        
        返回:
            指定位置的数据，如果位置无效返回None
        """
        if index < 0 or index >= self.size:
            print(f"❌ 位置 {index} 超出范围 [0, {self.size-1}]")
            return None
        
        current_pos = self.head
        for i in range(index):
            current_pos = self.nodes[current_pos]['next']
        
        return self.nodes[current_pos]['data']
    
    def traverse(self):
        """
        遍历链表 - 按阅读顺序游览所有书籍
        
        返回:
            包含所有元素的列表
        """
        print(f"\n📖 按阅读顺序遍历书籍：")
        
        result = []
        current_pos = self.head
        position = 0
        
        while current_pos != -1:
            data = self.nodes[current_pos]['data']
            result.append(data)
            print(f"   第{position}本: '{data}' (位置{current_pos})")
            
            current_pos = self.nodes[current_pos]['next']
            position += 1
        
        if not result:
            print("   📭 阅读列表为空")
        
        return result
    
    def display_structure(self):
        """显示静态链表的详细结构"""
        self._display_structure()
    
    def _display_structure(self):
        """内部方法：显示链表结构"""
        print(f"\n🏗️ 静态链表内部结构：")
        print(f"   数据链表头：{self.head}")
        print(f"   空闲链表头：{self.free_head}")
        print(f"   当前大小：{self.size}/{self.max_size}")
        
        print(f"\n📊 数组详细状态：")
        for i in range(self.max_size):
            node = self.nodes[i]
            data_str = f"'{node['data']}'" if node['data'] is not None else "空"
            next_str = str(node['next']) if node['next'] != -1 else "结束"
            
            # 判断节点类型
            if self._is_in_data_chain(i):
                status = "📚数据"
            elif self._is_in_free_chain(i):
                status = "⭕空闲"
            else:
                status = "❓未知"
            
            print(f"   位置{i}: data={data_str:10} next={next_str:3} ({status})")
    
    def _is_in_data_chain(self, pos):
        """检查位置是否在数据链表中"""
        current = self.head
        while current != -1:
            if current == pos:
                return True
            current = self.nodes[current]['next']
        return False
    
    def _is_in_free_chain(self, pos):
        """检查位置是否在空闲链表中"""
        current = self.free_head
        while current != -1:
            if current == pos:
                return True
            current = self.nodes[current]['next']
        return False
    
    def analyze_efficiency(self):
        """分析静态链表的效率特点"""
        print(f"\n📊 静态链表效率分析：")
        print(f"   空间使用：{self.size}/{self.max_size} ({self.size/self.max_size*100:.1f}%)")
        print(f"   空间固定：✅ 不会动态扩张")
        print(f"   插入效率：O(1) - 头部插入")
        print(f"   删除效率：O(1) - 头部删除")
        print(f"   查找效率：O(n) - 需要遍历")
        print(f"   内存友好：✅ 连续存储，缓存友好")
        print(f"   空间回收：✅ 自动管理，无内存泄漏")


def demonstrate_static_linked_list():
    """演示静态链表的完整功能"""
    print("=== 📚 图书馆魔法编号系统演示 ===\n")
    
    # 创建一个小型静态链表
    library = StaticLinkedList(max_size=8)
    
    print("\n" + "="*50)
    print("📥 插入操作演示：")
    
    # 插入一些书籍
    books = ["算法导论", "数据结构", "编程珠玑", "计算机网络", "操作系统"]
    for book in books:
        library.insert_at_head(book)
        print()
    
    # 显示当前结构
    library.display_structure()
    
    print("\n" + "="*50)
    print("📖 遍历操作演示：")
    reading_list = library.traverse()
    print(f"完整阅读列表：{reading_list}")
    
    print("\n" + "="*50)
    print("🔍 查找操作演示：")
    search_books = ["数据结构", "数学分析", "编程珠玑"]
    for book in search_books:
        index = library.search(book)
        if index != -1:
            print(f"'{book}' 在阅读列表的第 {index} 位")
        print()
    
    print("\n" + "="*50)
    print("🗑️ 删除操作演示：")
    
    # 删除头部元素
    deleted = library.delete_at_head()
    print(f"删除的书籍：'{deleted}'\n")
    
    # 删除指定值
    library.delete_by_value("数据结构")
    print()
    
    # 显示删除后的结构
    library.display_structure()
    
    print("\n" + "="*50)
    print("➕ 中间插入演示：")
    library.insert_at_index(1, "深入理解计算机系统")
    print()
    
    # 最终状态
    print("\n📋 最终阅读列表：")
    final_list = library.traverse()
    
    print("\n" + "="*50)
    library.analyze_efficiency()
    
    print(f"\n🎉 演示完成！图书馆管理系统运行正常！")


def compare_with_dynamic_list():
    """对比静态链表和动态链表的特点"""
    print("\n🆚 静态链表 vs 动态链表对比：")
    print("="*60)
    
    comparison = [
        ("内存管理", "固定大小，预分配", "动态分配，按需扩展"),
        ("空间效率", "可能有未使用空间", "空间利用率高"),
        ("插入性能", "O(1) - 如有空闲位置", "O(1) - 可能需要内存分配"),
        ("删除性能", "O(1) - 空间自动回收", "O(1) - 需要手动释放"),
        ("内存碎片", "无碎片问题", "可能产生碎片"),
        ("缓存友好", "连续存储，缓存友好", "分散存储，缓存命中率低"),
        ("适用场景", "嵌入式、实时系统", "通用应用程序"),
        ("实现复杂度", "需要管理空闲链表", "相对简单"),
    ]
    
    print(f"{'特性':<12} {'静态链表':<20} {'动态链表':<20}")
    print("-" * 60)
    for feature, static, dynamic in comparison:
        print(f"{feature:<12} {static:<20} {dynamic:<20}")


if __name__ == "__main__":
    print("🌟 欢迎来到图书馆的魔法编号系统！")
    print("让我们一起探索静态链表的奇妙世界～")
    print()
    
    # 运行主要演示
    demonstrate_static_linked_list()
    
    # 运行对比分析
    compare_with_dynamic_list()
    
    print("\n🌸 感谢体验静态链表的优雅魅力！")
    print("就像安妮说的：在固定的空间里，也能创造无限的可能～ 💕") 