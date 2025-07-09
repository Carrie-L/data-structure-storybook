"""
第06章：Floyd环检测算法（龟兔赛跑算法）
糖果味的完整实现 🐢🐰

这个文件包含了Floyd环检测算法的完整实现，用于检测链表中是否存在环。
算法基于一个简单的物理原理：在圆形跑道上，跑得快的总会追上跑得慢的。
"""

class ListNode:
    """
    链表节点类
    
    在Floyd算法中，节点就像赛道上的一个个位置点
    """
    def __init__(self, val=0):
        self.val = val          # 节点的值，相当于位置的标记
        self.next = None        # 指向下一个节点的指针，相当于前进的方向

def has_cycle_floyd(head):
    """
    Floyd环检测算法：使用快慢指针检测链表是否有环
    
    算法原理：
    - 慢指针（乌龟）：每次走1步
    - 快指针（兔子）：每次走2步
    - 如果有环：兔子一定会追上乌龟（相遇）
    - 如果无环：兔子会先到达终点（遇到None）
    
    参数：
        head: 链表的头节点
    
    返回：
        bool: True表示有环，False表示无环
        
    时间复杂度：O(n) - 最多遍历链表一次
    空间复杂度：O(1) - 只使用两个指针变量
    """
    # 边界检查：空链表或只有一个节点且无环
    if not head or not head.next:
        return False
    
    # 初始化双指针
    slow = head         # 乌龟从起点开始
    fast = head         # 兔子也从起点开始
    
    # 开始龟兔赛跑
    while fast and fast.next:
        # 乌龟走1步：slow = slow.next
        slow = slow.next
        
        # 兔子走2步：fast = fast.next.next
        fast = fast.next.next
        
        # 检查是否相遇
        if slow == fast:
            return True     # 相遇了！说明有环
    
    # 循环结束说明兔子到达了终点（遇到None），无环
    return False

def has_cycle_with_details(head):
    """
    Floyd环检测算法的详细版本：不仅检测环，还提供详细信息
    
    返回：
        tuple: (has_cycle, cycle_start, cycle_length)
        - has_cycle: 是否有环
        - cycle_start: 环的起始节点（如果有环）
        - cycle_length: 环的长度（如果有环）
    """
    if not head or not head.next:
        return False, None, 0
    
    # 第一阶段：检测是否有环
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # 发现环！进入第二阶段
            break
    else:
        # 没有环
        return False, None, 0
    
    # 第二阶段：找环的起始位置
    # 数学原理：从head和相遇点同时出发，相遇处就是环的起点
    cycle_start = head
    while cycle_start != slow:
        cycle_start = cycle_start.next
        slow = slow.next
    
    # 第三阶段：计算环的长度
    cycle_length = 1
    current = cycle_start.next
    while current != cycle_start:
        current = current.next
        cycle_length += 1
    
    return True, cycle_start, cycle_length

def create_cycle_list_for_test():
    """
    创建一个有环的测试链表
    
    链表结构：1 → 2 → 3 → 4 → 5
                   ↑           ↓
                   └←←←←←←←←←←←←┘
    
    返回：head节点
    """
    # 创建节点
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    
    # 连接节点
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node2     # 创建环：5指向2
    
    return node1

def create_linear_list_for_test():
    """
    创建一个无环的测试链表
    
    链表结构：1 → 2 → 3 → 4 → 5 → None
    
    返回：head节点
    """
    # 创建节点
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    
    # 连接节点
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    # node5.next = None (默认就是None)
    
    return node1

def visualize_algorithm_process(head, max_steps=20):
    """
    可视化Floyd算法的执行过程
    
    参数：
        head: 链表头节点
        max_steps: 最大步数限制（防止无限循环）
    """
    if not head or not head.next:
        print("链表太短，无法演示算法过程")
        return
    
    slow = fast = head
    step = 0
    
    print("🐢🐰 Floyd算法执行过程：")
    print(f"步骤{step}: 乌龟在节点{slow.val}，兔子在节点{fast.val}")
    
    while fast and fast.next and step < max_steps:
        step += 1
        
        # 移动指针
        slow = slow.next
        fast = fast.next.next
        
        # 显示当前位置
        print(f"步骤{step}: 乌龟在节点{slow.val}，兔子在节点{fast.val}")
        
        # 检查是否相遇
        if slow == fast:
            print("🎉 乌龟和兔子相遇了！发现环！")
            return True
    
    if step >= max_steps:
        print("⚠️ 达到最大步数限制，算法终止")
    else:
        print("🏁 兔子到达终点，链表无环")
    
    return False

if __name__ == "__main__":
    print("=" * 50)
    print("🎠 Floyd环检测算法测试 🎠")
    print("=" * 50)
    
    # 测试1：有环链表
    print("\n📍 测试1：检测有环链表")
    cycle_list = create_cycle_list_for_test()
    result1 = has_cycle_floyd(cycle_list)
    print(f"结果：{'发现环' if result1 else '无环'}")
    
    # 详细信息
    has_cycle, start, length = has_cycle_with_details(cycle_list)
    if has_cycle:
        print(f"环起始节点值：{start.val}")
        print(f"环长度：{length}")
    
    # 可视化算法过程
    print("\n🔍 算法执行过程：")
    visualize_algorithm_process(cycle_list)
    
    print("\n" + "-" * 30)
    
    # 测试2：无环链表
    print("\n📍 测试2：检测无环链表")
    linear_list = create_linear_list_for_test()
    result2 = has_cycle_floyd(linear_list)
    print(f"结果：{'发现环' if result2 else '无环'}")
    
    # 可视化算法过程
    print("\n🔍 算法执行过程：")
    visualize_algorithm_process(linear_list)
    
    print("\n" + "=" * 50)
    print("🍭 测试完成！糖果味的算法学习之旅！")
    print("=" * 50) 