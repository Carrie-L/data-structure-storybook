class SensorMonitor:
    """传感器状态监控系统 - 使用位集高效存储传感器状态"""
    
    def __init__(self, sensor_count):
        """初始化传感器监控系统
        
        Args:
            sensor_count: 传感器总数
        """
        self.sensor_count = sensor_count
        # 计算需要多少个字节来存储所有传感器状态
        # 例如：512个传感器需要 (512 + 7) // 8 = 64字节
        self.byte_count = (sensor_count + 7) // 8  # 向上取整除法
        # 初始化位数组，所有传感器默认为OFF(0)
        # bytearray创建一个可修改的字节数组
        self.bit_array = bytearray(self.byte_count)
        print(f"📡 传感器监控系统启动！")
        print(f"传感器数量: {sensor_count}")
        print(f"存储空间: {self.byte_count} 字节 (相比传统方式节省 {self._calculate_savings():.1%})")
        
    def _calculate_savings(self):
        """计算相比传统字符串存储的空间节省比例"""
        traditional_size = self.sensor_count * 7  # 假设平均每个状态7字符
        bit_size = self.byte_count
        return 1 - (bit_size / traditional_size)
        
    def set_sensor(self, sensor_id, status):
        """设置指定传感器的状态
        
        Args:
            sensor_id: 传感器编号 (从0开始)
            status: True表示工作，False表示休息
        """
        if not (0 <= sensor_id < self.sensor_count):
            print(f"❌ 传感器编号 {sensor_id} 超出范围！")
            return
            
        # 关键计算：确定这个传感器在哪个字节的哪一位
        byte_index = sensor_id // 8      # 在第几个字节？(整数除法)
        bit_position = sensor_id % 8     # 在字节内的第几位？(取余数)
        
        if status:
            # 设置为1：使用"或运算"和"位掩码"
            # (1 << bit_position) 创建只有目标位为1的掩码
            # 例如：位置3 → (1 << 3) = 00001000
            self.bit_array[byte_index] |= (1 << bit_position)
            print(f"💡 传感器 {sensor_id} 开始工作")
        else:
            # 设置为0：使用"与运算"和"反向位掩码"  
            # ~(1 << bit_position) 创建只有目标位为0的掩码
            # 例如：位置3 → ~(1 << 3) = 11110111
            self.bit_array[byte_index] &= ~(1 << bit_position)
            print(f"⚫ 传感器 {sensor_id} 停止工作")
            
    def get_sensor(self, sensor_id):
        """获取指定传感器的状态
        
        Args:
            sensor_id: 传感器编号 (从0开始)
            
        Returns:
            bool: True表示工作，False表示休息
        """
        if not (0 <= sensor_id < self.sensor_count):
            print(f"❌ 传感器编号 {sensor_id} 超出范围！")
            return False
            
        # 计算字节位置和位位置
        byte_index = sensor_id // 8      # 位于第几个字节
        bit_position = sensor_id % 8     # 位于字节内的第几位
        
        # 使用"与运算"和"位掩码"检查特定位
        # (1 << bit_position) 创建检查掩码
        # 如果目标位是1，与运算结果非0；如果目标位是0，与运算结果为0
        result = self.bit_array[byte_index] & (1 << bit_position)
        return result != 0  # 非0表示该位为1(工作)，0表示该位为0(休息)
        
    def get_working_count(self):
        """获取正在工作的传感器数量"""
        count = 0
        # 遍历每个字节
        for byte_value in self.bit_array:
            # 计算每个字节中1的数量
            while byte_value:
                count += byte_value & 1  # 检查最低位是否为1
                byte_value >>= 1         # 右移1位，继续检查下一位
        return count
        
    def get_status_summary(self):
        """获取所有传感器状态的摘要信息"""
        working_count = self.get_working_count()
        idle_count = self.sensor_count - working_count
        working_percentage = (working_count / self.sensor_count) * 100
        
        return {
            'total': self.sensor_count,
            'working': working_count,
            'idle': idle_count,
            'working_percentage': working_percentage
        }
        
    def display_status(self, show_details=False):
        """显示传感器状态
        
        Args:
            show_details: 是否显示每个传感器的详细状态
        """
        summary = self.get_status_summary()
        print(f"\n📊 传感器状态摘要：")
        print(f"总数: {summary['total']}")
        print(f"工作中: {summary['working']} ({summary['working_percentage']:.1f}%)")
        print(f"休息中: {summary['idle']} ({100-summary['working_percentage']:.1f}%)")
        
        if show_details:
            print(f"\n📋 详细状态（前32个传感器）：")
            for i in range(min(32, self.sensor_count)):
                status = "💡" if self.get_sensor(i) else "⚫"
                print(f"传感器{i:2d}: {status}", end="  ")
                if (i + 1) % 8 == 0:  # 每8个换行
                    print()
            print()

class BitSetOperations:
    """位集的高级操作示例"""
    
    @staticmethod
    def bitwise_demo():
        """演示基本位运算操作"""
        print("🔧 位运算操作演示：")
        print("=" * 50)
        
        # 示例数据
        a = 0b11001010  # 二进制：11001010，十进制：202
        b = 0b10101100  # 二进制：10101100，十进制：172
        
        print(f"a = {a:08b} (十进制: {a})")
        print(f"b = {b:08b} (十进制: {b})")
        print("-" * 30)
        
        # 与运算 (AND)
        and_result = a & b
        print(f"a & b = {and_result:08b} (十进制: {and_result}) - 两个都是1才是1")
        
        # 或运算 (OR)
        or_result = a | b
        print(f"a | b = {or_result:08b} (十进制: {or_result}) - 任一个是1就是1")
        
        # 异或运算 (XOR)
        xor_result = a ^ b
        print(f"a ^ b = {xor_result:08b} (十进制: {xor_result}) - 不同时为1")
        
        # 非运算 (NOT) - 只对8位进行操作
        not_a = (~a) & 0xFF  # 限制在8位内
        print(f"~a    = {not_a:08b} (十进制: {not_a}) - 所有位取反")
        
    @staticmethod
    def set_operations_demo():
        """演示位集的集合操作"""
        print("\n🎭 位集集合操作演示：")
        print("=" * 50)
        
        # 创建两个传感器组
        group_a = SensorMonitor(16)  # 16个传感器
        group_b = SensorMonitor(16)  # 16个传感器
        
        # 设置group_a的一些传感器工作
        working_sensors_a = [0, 2, 4, 6, 8, 10]
        for sensor_id in working_sensors_a:
            group_a.set_sensor(sensor_id, True)
            
        # 设置group_b的一些传感器工作  
        working_sensors_b = [1, 2, 3, 6, 7, 11]
        for sensor_id in working_sensors_b:
            group_b.set_sensor(sensor_id, True)
            
        print(f"\n组A工作中的传感器: {working_sensors_a}")
        print(f"组B工作中的传感器: {working_sensors_b}")
        
        # 并集：任一组中工作的传感器
        union_result = BitSetOperations.union(group_a, group_b)
        print(f"并集 (A ∪ B): {union_result}")
        
        # 交集：两组都工作的传感器
        intersection_result = BitSetOperations.intersection(group_a, group_b)
        print(f"交集 (A ∩ B): {intersection_result}")
        
        # 差集：只在A组工作的传感器
        difference_result = BitSetOperations.difference(group_a, group_b)
        print(f"差集 (A - B): {difference_result}")
        
        # 对称差集：只在一个组中工作的传感器
        symmetric_diff_result = BitSetOperations.symmetric_difference(group_a, group_b)
        print(f"对称差集 (A △ B): {symmetric_diff_result}")
        
    @staticmethod
    def union(set_a, set_b):
        """计算两个位集的并集"""
        result = []
        for i in range(min(set_a.sensor_count, set_b.sensor_count)):
            if set_a.get_sensor(i) or set_b.get_sensor(i):
                result.append(i)
        return result
        
    @staticmethod
    def intersection(set_a, set_b):
        """计算两个位集的交集"""
        result = []
        for i in range(min(set_a.sensor_count, set_b.sensor_count)):
            if set_a.get_sensor(i) and set_b.get_sensor(i):
                result.append(i)
        return result
        
    @staticmethod
    def difference(set_a, set_b):
        """计算两个位集的差集 (A - B)"""
        result = []
        for i in range(min(set_a.sensor_count, set_b.sensor_count)):
            if set_a.get_sensor(i) and not set_b.get_sensor(i):
                result.append(i)
        return result
        
    @staticmethod
    def symmetric_difference(set_a, set_b):
        """计算两个位集的对称差集"""
        result = []
        for i in range(min(set_a.sensor_count, set_b.sensor_count)):
            if set_a.get_sensor(i) != set_b.get_sensor(i):  # 异或逻辑
                result.append(i)
        return result

def demonstrate_bitset_usage():
    """演示位集的完整使用流程"""
    print("=== 🔬 位集(Bitset)操作演示 ===\n")
    
    # 1. 基础位运算演示
    BitSetOperations.bitwise_demo()
    
    # 2. 创建传感器监控系统
    print("\n📡 创建传感器监控系统：")
    monitor = SensorMonitor(32)  # 32个传感器的小型系统
    
    # 3. 设置一些传感器状态
    print("\n🔧 设置传感器状态：")
    working_sensors = [0, 3, 5, 8, 13, 21, 29, 31]
    for sensor_id in working_sensors:
        monitor.set_sensor(sensor_id, True)
        
    # 4. 查询传感器状态
    print(f"\n🔍 查询传感器状态：")
    for sensor_id in [0, 1, 3, 7]:
        status = monitor.get_sensor(sensor_id)
        emoji = "💡" if status else "⚫"
        print(f"传感器 {sensor_id}: {emoji} ({'工作中' if status else '休息中'})")
        
    # 5. 显示系统状态摘要
    monitor.display_status(show_details=True)
    
    # 6. 高级集合操作演示
    BitSetOperations.set_operations_demo()
    
    print("\n✅ 位集操作演示完成！")
    print("💡 位集在实际应用中可以：")
    print("   • 高效存储大量布尔状态")
    print("   • 快速进行集合运算") 
    print("   • 大幅节省内存空间")
    print("   • 提升数据处理性能")

if __name__ == "__main__":
    demonstrate_bitset_usage() 