# 链地址法散列表实现 🔗
class ChainHashTable:
    def __init__(self, size=10):
        """初始化散列表"""
        self.size = size  # 桶的数量（保险柜的总数）
        # 每个位置都是一个列表（桶），用来存放碰撞的元素
        self.table = [[] for _ in range(size)]  # 创建size个空列表
        
    def hash_function(self, key):
        """简单的哈希函数：将字符串转换为数字"""
        # 将字符串的每个字符转换为数字再求和
        total = 0
        for char in str(key):  # 遍历key的每个字符
            total += ord(char)  # ord('A') = 65, ord('a') = 97
        return total % self.size  # 取模确保结果在0到size-1范围内
        
    def put(self, key, value):
        """存储键值对到散列表中"""
        index = self.hash_function(key)  # 计算应该放在哪个桶里
        bucket = self.table[index]       # 获取对应的桶（这是一个列表）
        
        # 检查key是否已经存在，如果存在就更新值
        for i, (k, v) in enumerate(bucket):  
            if k == key:
                bucket[i] = (key, value)  # 更新现有的键值对
                print(f"✏️  更新：'{key}' → '{value}' (位置{index})")
                return
                
        # 如果key不存在，就添加新的键值对到桶的末尾
        bucket.append((key, value))  # append()在列表末尾添加元素
        print(f"📥 添加：'{key}' → '{value}' (位置{index}，桶中第{len(bucket)}个)")
        
    def get(self, key):
        """根据键查找对应的值"""
        index = self.hash_function(key)  # 计算应该在哪个桶里
        bucket = self.table[index]       # 获取对应的桶
        
        # 在桶里逐个查找匹配的键
        for k, v in bucket:
            if k == key:
                print(f"✅ 找到：'{key}' → '{v}' (位置{index})")
                return v
                
        print(f"❌ 没找到：'{key}'")
        return None
        
    def display(self):
        """显示散列表的当前状态"""
        print("\\n📊 散列表状态：")
        for i, bucket in enumerate(self.table):
            if bucket:  # 如果桶不为空
                # 列表推导式：为每个键值对创建字符串表示
                items = [f"'{k}':'{v}'" for k, v in bucket]
                print(f"  位置{i}: [{' → '.join(items)}]")
            else:
                print(f"  位置{i}: [空]")

# 开放地址法散列表（线性探测）🚗
class OpenAddressHashTable:
    def __init__(self, size=10):
        """初始化散列表"""
        self.size = size
        # 用两个数组分别存储键和值
        self.keys = [None] * size    # [None, None, None, ...] None表示空位
        self.values = [None] * size  # [None, None, None, ...] 对应的值
        self.count = 0  # 记录已存储的元素数量，用于计算负载因子
        
    def hash_function(self, key):
        """哈希函数：将键转换为数组索引"""
        # sum()函数计算所有字符ASCII码的总和
        total = sum(ord(char) for char in str(key))
        return total % self.size
        
    def put(self, key, value):
        """存储键值对（线性探测法）"""
        if self.count >= self.size:  # 如果表已满，无法添加
            print("❌ 散列表已满，无法添加！")
            return
            
        index = self.hash_function(key)  # 计算初始位置
        original_index = index           # 记住起始位置，避免无限循环
        steps = 0                        # 记录探测了多少步
        
        # 线性探测：一步步寻找空位或已存在的key
        while self.keys[index] is not None:  # 如果当前位置不为空
            if self.keys[index] == key:      # 如果找到相同的key，更新值
                self.values[index] = value
                print(f"✏️  更新：'{key}' → '{value}' (位置{index})")
                return
                
            # 移动到下一个位置（线性探测的核心）
            index = (index + 1) % self.size  # %运算确保循环回到开头
            steps += 1
            
            # 安全检查：如果转了一圈都没找到空位
            if index == original_index:
                print("❌ 散列表已满（探测一圈）！")
                return
                
        # 找到空位，存储键值对
        self.keys[index] = key
        self.values[index] = value
        self.count += 1  # 增加元素计数
        
        if steps == 0:
            print(f"📥 直接存储：'{key}' → '{value}' (位置{index})")
        else:
            print(f"📥 探测存储：'{key}' → '{value}' (位置{index}，探测了{steps}步)")
            
    def get(self, key):
        """查找键对应的值（线性探测法）"""
        index = self.hash_function(key)
        original_index = index
        steps = 0
        
        # 线性探测查找
        while self.keys[index] is not None:
            if self.keys[index] == key:  # 找到了！
                if steps == 0:
                    print(f"✅ 直接找到：'{key}' → '{self.values[index]}'")
                else:
                    print(f"✅ 探测找到：'{key}' → '{self.values[index]}' (探测了{steps}步)")
                return self.values[index]
                
            # 移动到下一个位置继续找
            index = (index + 1) % self.size
            steps += 1
            
            # 如果转了一圈还没找到
            if index == original_index:
                break
                
        print(f"❌ 没找到：'{key}'")
        return None
        
    def display(self):
        """显示散列表的当前状态"""
        print("\\n📊 散列表状态：")
        for i in range(self.size):
            if self.keys[i] is not None:
                print(f"  位置{i}: '{self.keys[i]}' → '{self.values[i]}'")
            else:
                print(f"  位置{i}: [空]")
        print(f"负载因子: {self.count}/{self.size} = {self.count/self.size:.2f}")

# 二次探测法散列表 🎯
class QuadraticProbingHashTable:
    def __init__(self, size=10):
        """初始化散列表"""
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        
    def hash_function(self, key):
        """哈希函数"""
        total = sum(ord(char) for char in str(key))
        return total % self.size
        
    def put(self, key, value):
        """存储键值对（二次探测法）"""
        if self.count >= self.size:
            print("❌ 散列表已满！")
            return
            
        index = self.hash_function(key)
        original_index = index
        i = 0  # 探测次数
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.values[index] = value
                print(f"✏️  更新：'{key}' → '{value}' (位置{index})")
                return
                
            # 二次探测：步长为 i²
            i += 1
            index = (original_index + i * i) % self.size
            
            if i >= self.size:  # 避免无限循环
                print("❌ 无法找到空位！")
                return
                
        self.keys[index] = key
        self.values[index] = value
        self.count += 1
        
        if i == 0:
            print(f"📥 直接存储：'{key}' → '{value}' (位置{index})")
        else:
            print(f"📥 二次探测存储：'{key}' → '{value}' (位置{index}，探测{i}次)")
            
    def get(self, key):
        """查找键对应的值（二次探测法）"""
        index = self.hash_function(key)
        original_index = index
        i = 0
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                if i == 0:
                    print(f"✅ 直接找到：'{key}' → '{self.values[index]}'")
                else:
                    print(f"✅ 二次探测找到：'{key}' → '{self.values[index]}' (探测{i}次)")
                return self.values[index]
                
            i += 1
            index = (original_index + i * i) % self.size
            
            if i >= self.size:
                break
                
        print(f"❌ 没找到：'{key}'")
        return None
        
    def display(self):
        """显示散列表状态"""
        print("\\n📊 二次探测散列表状态：")
        for i in range(self.size):
            if self.keys[i] is not None:
                print(f"  位置{i}: '{self.keys[i]}' → '{self.values[i]}'")
            else:
                print(f"  位置{i}: [空]")

def demonstrate_collision_resolution():
    """演示三种碰撞解决方案"""
    print("=== 🔧 散列表碰撞解决方案演示 ===\\n")
    
    # 1. 链地址法演示
    print("1️⃣ 链地址法演示：")
    print("=" * 40)
    chain_table = ChainHashTable(size=5)  # 小表容易产生碰撞
    
    # 添加数据
    chain_table.put("安妮", "粉色书包")
    chain_table.put("伊莎贝尔", "公文包") 
    chain_table.put("希娅", "时尚背包")
    chain_table.put("黛芙", "电脑包")
    chain_table.put("小林", "咖啡杯")
    
    chain_table.display()
    
    # 查找测试
    print("\\n🔍 查找测试：")
    chain_table.get("安妮")
    chain_table.get("潼潼")  # 不存在的键
    
    # 2. 线性探测法演示
    print("\\n\\n2️⃣ 线性探测法演示：")
    print("=" * 40)
    linear_table = OpenAddressHashTable(size=7)
    
    # 添加相同的数据
    linear_table.put("安妮", "粉色书包")
    linear_table.put("伊莎贝尔", "公文包")
    linear_table.put("希娅", "时尚背包")
    linear_table.put("黛芙", "电脑包")
    linear_table.put("小林", "咖啡杯")
    
    linear_table.display()
    
    # 查找测试
    print("\\n🔍 查找测试：")
    linear_table.get("希娅")
    linear_table.get("潼潼")
    
    # 3. 二次探测法演示
    print("\\n\\n3️⃣ 二次探测法演示：")
    print("=" * 40)
    quad_table = QuadraticProbingHashTable(size=7)
    
    # 添加数据
    quad_table.put("安妮", "粉色书包")
    quad_table.put("伊莎贝尔", "公文包")
    quad_table.put("希娅", "时尚背包")
    quad_table.put("黛芙", "电脑包")
    
    quad_table.display()
    
    print("\\n✅ 碰撞解决方案演示完成！")
    print("💡 总结：")
    print("   • 链地址法：简单但需要额外空间")
    print("   • 线性探测：节省空间但可能聚集")
    print("   • 二次探测：减少聚集但实现复杂")

if __name__ == "__main__":
    demonstrate_collision_resolution() 