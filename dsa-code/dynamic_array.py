"""
🍬 第03章：会变大的神奇盒子 - 动态数组完整实现
糖果味数据结构与算法 by 安妮的实验室

这个文件展示了动态数组的完整实现，包括扩容、缩容、各种操作
就像希娅的神奇收纳盒，能自动变大变小！
"""

class DynamicArray:
    """
    🎁 神奇的会变大变小的数组盒子
    
    这就是安妮学到的动态数组！能自动调整大小，
    不用提前知道要存多少可爱的小东西
    """
    
    def __init__(self, initial_capacity=2):
        """
        🌟 初始化动态数组
        
        参数:
            initial_capacity: 初始容量，默认为2（够放两个小玩具）
        """
        self.capacity = initial_capacity  # 当前容量（盒子总共能装多少）
        self.size = 0                     # 当前元素个数（盒子里实际有多少东西）
        self.data = [None] * self.capacity # 实际存储数据的内部数组（真正的盒子）
        
        print(f"🎁 创建了一个容量为 {self.capacity} 的神奇盒子！")
    
    def __len__(self):
        """
        📏 返回数组长度
        
        就像问安妮："你的盒子里有多少个小玩具？"
        """
        return self.size
    
    def __getitem__(self, index):
        """
        🔍 通过索引获取元素
        
        就像安妮说："我要第3个格子里的东西！"
        """
        if 0 <= index < self.size:
            return self.data[index]
        else:
            raise IndexError(f"索引 {index} 超出范围！盒子里只有 {self.size} 个东西")
    
    def __setitem__(self, index, value):
        """
        📝 通过索引设置元素
        
        就像安妮说："我要把第2个格子里的东西换成小熊！"
        """
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError(f"索引 {index} 超出范围！盒子里只有 {self.size} 个东西")
    
    def append(self, item):
        """
        ➕ 在末尾添加元素
        
        这是动态数组最重要的操作！
        如果盒子满了，会自动换一个更大的盒子
        
        参数:
            item: 要添加的可爱小东西
        """
        print(f"💭 想要添加 '{item}'...")
        
        # 检查是否需要扩容（盒子满了吗？）
        if self.size == self.capacity:
            print(f"😮 哎呀！盒子满了（{self.size}/{self.capacity}），需要换个更大的盒子！")
            self._resize_up()  # 扩容（换大盒子）
        
        # 把新东西放进盒子
        self.data[self.size] = item
        self.size += 1  # 记录盒子里又多了一个东西
        
        print(f"✅ 成功添加 '{item}'！现在有 {self.size} 个东西")
        print(f"📦 当前状态：{self.size}/{self.capacity} (使用率: {self.size/self.capacity*100:.1f}%)")
    
    def pop(self, index=None):
        """
        🗑️ 移除并返回指定位置的元素
        
        参数:
            index: 要移除的位置，默认是最后一个
        
        返回:
            被移除的元素
        """
        if self.size == 0:
            raise IndexError("空盒子里没有东西可以取出！")
        
        # 如果没指定位置，就取最后一个
        if index is None:
            index = self.size - 1
        
        if not (0 <= index < self.size):
            raise IndexError(f"索引 {index} 超出范围！")
        
        # 记住要取出的东西
        removed_item = self.data[index]
        
        # 把后面的东西都往前移一位（填补空缺）
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        
        self.size -= 1  # 盒子里的东西少了一个
        
        # 检查是否需要缩容（盒子太空了吗？）
        if self.size <= self.capacity // 4 and self.capacity > 2:
            print(f"💡 盒子太空了（{self.size}/{self.capacity}），换个小一点的盒子节省空间")
            self._resize_down()
        
        print(f"🗑️ 取出了 '{removed_item}'，现在有 {self.size} 个东西")
        return removed_item
    
    def insert(self, index, item):
        """
        📌 在指定位置插入元素
        
        就像安妮要在盒子中间插入一个新玩具，
        需要把后面的玩具都往后挪一位
        
        参数:
            index: 插入位置
            item: 要插入的元素
        """
        if not (0 <= index <= self.size):
            raise IndexError(f"插入位置 {index} 无效！")
        
        # 检查是否需要扩容
        if self.size == self.capacity:
            print(f"😮 需要扩容才能插入 '{item}'")
            self._resize_up()
        
        # 把指定位置后面的元素都往后移一位
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        
        # 在指定位置插入新元素
        self.data[index] = item
        self.size += 1
        
        print(f"📌 在位置 {index} 插入了 '{item}'")
    
    def _resize_up(self):
        """
        🏠 扩容操作 - 换个更大的盒子
        
        这是动态数组的核心魔法！
        容量翻倍，把所有东西搬到新盒子里
        """
        old_capacity = self.capacity
        self.capacity *= 2  # 容量翻倍（新盒子是旧盒子的2倍大）
        
        print(f"🔧 开始扩容：{old_capacity} → {self.capacity}")
        
        # 创建新的更大的盒子
        new_data = [None] * self.capacity
        
        # 把所有旧东西搬到新盒子里（这需要O(n)时间）
        for i in range(self.size):
            new_data[i] = self.data[i]
        
        # 扔掉旧盒子，使用新盒子
        self.data = new_data
        
        print(f"✨ 扩容完成！现在盒子能装 {self.capacity} 个东西了")
    
    def _resize_down(self):
        """
        🏠 缩容操作 - 换个小一点的盒子
        
        当盒子太空的时候（使用率 ≤ 25%），
        换个小盒子节省空间
        """
        old_capacity = self.capacity
        self.capacity //= 2  # 容量减半
        
        print(f"🔧 开始缩容：{old_capacity} → {self.capacity}")
        
        # 创建新的小盒子
        new_data = [None] * self.capacity
        
        # 把现有的东西搬到小盒子里
        for i in range(self.size):
            new_data[i] = self.data[i]
        
        # 使用新的小盒子
        self.data = new_data
        
        print(f"💫 缩容完成！现在盒子容量是 {self.capacity}")
    
    def clear(self):
        """
        🧹 清空数组
        
        把盒子里的所有东西都倒出来
        """
        self.size = 0
        print("🧹 盒子清空了！")
    
    def extend(self, iterable):
        """
        📎 批量添加元素
        
        一次性添加很多可爱的小东西
        
        参数:
            iterable: 要添加的元素集合
        """
        for item in iterable:
            self.append(item)
    
    def index(self, item):
        """
        🔍 查找元素的位置
        
        找找某个小玩具在盒子的第几个格子里
        
        参数:
            item: 要查找的元素
        
        返回:
            元素的索引位置
        """
        for i in range(self.size):
            if self.data[i] == item:
                return i
        raise ValueError(f"'{item}' 不在盒子里！")
    
    def count(self, item):
        """
        📊 统计元素出现次数
        
        数数盒子里有几个同样的小玩具
        
        参数:
            item: 要统计的元素
        
        返回:
            元素出现的次数
        """
        count = 0
        for i in range(self.size):
            if self.data[i] == item:
                count += 1
        return count
    
    def reverse(self):
        """
        🔄 反转数组
        
        把盒子里的东西倒过来排列
        """
        # 使用双指针法反转
        left, right = 0, self.size - 1
        while left < right:
            # 交换两端的元素
            self.data[left], self.data[right] = self.data[right], self.data[left]
            left += 1
            right -= 1
        print("🔄 盒子里的东西顺序颠倒了！")
    
    def __str__(self):
        """
        🎨 转换为字符串表示
        
        让安妮能看到盒子里都有什么
        """
        if self.size == 0:
            return "🎁 空盒子 []"
        
        # 只显示有东西的部分
        items = [str(self.data[i]) for i in range(self.size)]
        return f"🎁 盒子 [{', '.join(items)}] (容量: {self.capacity})"
    
    def __repr__(self):
        """
        🔍 详细表示
        """
        return f"DynamicArray(size={self.size}, capacity={self.capacity})"
    
    def get_info(self):
        """
        📋 获取数组详细信息
        
        看看盒子的详细状态
        """
        usage_rate = (self.size / self.capacity * 100) if self.capacity > 0 else 0
        
        print("=" * 40)
        print("📊 动态数组状态报告")
        print("=" * 40)
        print(f"📦 当前大小: {self.size}")
        print(f"🏠 容量: {self.capacity}")
        print(f"📈 使用率: {usage_rate:.1f}%")
        print(f"💾 内容: {self}")
        
        # 内存使用分析
        used_memory = self.size  # 实际使用的内存单位
        total_memory = self.capacity  # 总分配的内存单位
        wasted_memory = total_memory - used_memory
        
        print(f"💿 内存使用: {used_memory}/{total_memory} (浪费: {wasted_memory})")
        
        if usage_rate < 25 and self.capacity > 2:
            print("💡 提示: 使用率较低，可能适合缩容")
        elif usage_rate > 90:
            print("⚠️  提示: 使用率很高，下次添加元素可能需要扩容")
        
        print("=" * 40)


def demo_dynamic_array():
    """
    🎮 动态数组演示程序
    
    让我们看看安妮的神奇盒子是怎么工作的！
    """
    print("🌟 欢迎来到安妮的动态数组实验！")
    print("=" * 50)
    
    # 创建一个神奇的盒子
    cute_things = DynamicArray(initial_capacity=2)
    
    print("\n📦 第一部分：测试添加元素（观察扩容）")
    print("-" * 30)
    
    # 添加一些可爱的小东西
    items_to_add = ["🦄独角兽", "🌈彩虹", "⭐星星", "🌙月亮", "🌸花朵", "🦋蝴蝶", "🐚贝壳", "🎵音符"]
    
    for item in items_to_add:
        cute_things.append(item)
        print()  # 空行，让输出更清晰
    
    print("\n📊 当前状态：")
    cute_things.get_info()
    
    print("\n🔍 第二部分：测试访问和修改")
    print("-" * 30)
    
    # 测试索引访问
    print(f"📍 第3个位置的东西是: {cute_things[2]}")
    print(f"📍 最后一个东西是: {cute_things[-1]}")  # 这个会报错，因为我们没实现负索引
    
    try:
        print(f"📍 最后一个东西是: {cute_things[len(cute_things)-1]}")
    except:
        print("📍 最后一个东西是:", cute_things[len(cute_things)-1])
    
    # 修改元素
    print(f"\n🔄 把位置1的'{cute_things[1]}'换成'🎀蝴蝶结'")
    cute_things[1] = "🎀蝴蝶结"
    print(f"✅ 修改完成: {cute_things}")
    
    print("\n📌 第三部分：测试插入")
    print("-" * 30)
    
    cute_things.insert(0, "👑王冠")  # 在开头插入
    cute_things.insert(3, "💎钻石")  # 在中间插入
    print(f"📦 插入后: {cute_things}")
    
    print("\n🗑️ 第四部分：测试删除（观察缩容）")
    print("-" * 30)
    
    # 删除一些元素，观察缩容
    while len(cute_things) > 2:
        removed = cute_things.pop()
        print(f"🗑️ 删除了: {removed}")
        print(f"📦 剩余: {cute_things}")
        print()
    
    print("\n🔍 第五部分：其他操作测试")
    print("-" * 30)
    
    # 重新添加一些元素
    cute_things.extend(["🎪马戏团", "🎨画笔", "📚书本"])
    print(f"📎 批量添加后: {cute_things}")
    
    # 查找元素
    try:
        pos = cute_things.index("🎨画笔")
        print(f"🔍 '🎨画笔' 在位置 {pos}")
    except ValueError as e:
        print(f"❌ {e}")
    
    # 统计元素
    cute_things.append("📚书本")  # 再添加一个重复的
    count = cute_things.count("📚书本")
    print(f"📊 '📚书本' 出现了 {count} 次")
    
    # 反转数组
    print(f"\n🔄 反转前: {cute_things}")
    cute_things.reverse()
    print(f"🔄 反转后: {cute_things}")
    
    print("\n✨ 最终状态：")
    cute_things.get_info()
    
    print("\n🎉 实验完成！安妮的神奇盒子真厉害！")


def performance_analysis():
    """
    📈 性能分析演示
    
    展示动态数组的摊销时间复杂度
    """
    print("\n" + "=" * 50)
    print("📈 动态数组性能分析")
    print("=" * 50)
    
    import time
    
    # 测试大量插入操作的性能
    print("\n🚀 测试10000次append操作的总时间...")
    
    arr = DynamicArray(initial_capacity=1)
    
    start_time = time.time()
    resize_count = 0
    
    # 记录每次扩容
    original_resize = arr._resize_up
    def counting_resize():
        nonlocal resize_count
        resize_count += 1
        return original_resize()
    
    arr._resize_up = counting_resize
    
    # 添加10000个元素
    for i in range(10000):
        arr.append(f"item_{i}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"⏱️  总时间: {total_time:.4f} 秒")
    print(f"🔄 扩容次数: {resize_count}")
    print(f"📊 平均每次操作时间: {total_time/10000*1000:.6f} 毫秒")
    print(f"📈 最终容量: {arr.capacity}")
    print(f"📦 最终大小: {len(arr)}")
    
    # 计算理论扩容次数
    import math
    theoretical_resizes = math.floor(math.log2(10000))
    print(f"🧮 理论扩容次数: {theoretical_resizes}")
    
    print("\n💡 分析：")
    print("   - 虽然发生了多次扩容，但总体时间复杂度仍然是 O(n)")
    print("   - 平均每次插入的摊销时间复杂度是 O(1)")
    print("   - 这证明了动态数组的高效性！")


if __name__ == "__main__":
    # 运行演示
    demo_dynamic_array()
    
    # 运行性能分析
    performance_analysis()
    
    print("\n🍬 感谢阅读！这就是安妮学到的动态数组魔法！")
    print("💭 记住：虽然偶尔需要'搬家'，但平均下来还是很快的！") 