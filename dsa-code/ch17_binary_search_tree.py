class TreeNode:
    """二叉搜索树节点类 - 像花园里的每朵花都有自己的位置"""
    def __init__(self, val):
        self.val = val          # 节点存储的值，就像花的编号
        self.left = None        # 左子节点指针，指向更小的花
        self.right = None       # 右子节点指针，指向更大的花

class BinarySearchTree:
    """二叉搜索树类 - 一个有序的秘密花园"""
    
    def __init__(self):
        self.root = None        # 根节点，花园的入口
        self.size = 0           # 树中节点的数量
    
    def insert(self, val):
        """插入新节点 - 为花园种植新花"""
        if self.root is None:
            self.root = TreeNode(val)    # 如果花园为空，这朵花就是第一朵
            self.size += 1
            print(f"🌱 {val} 成为了花园的第一朵花（根节点）")
        else:
            if self._insert_recursive(self.root, val):
                self.size += 1
    
    def _insert_recursive(self, node, val):
        """递归插入辅助函数 - 寻找花的合适位置"""
        if val < node.val:                          # 新花比当前花小，向左种植
            if node.left is None:
                node.left = TreeNode(val)           # 左边没有花，直接种植
                print(f"🌿 {val} 种在了 {node.val} 的左侧（小花区域）")
                return True
            else:
                return self._insert_recursive(node.left, val)  # 递归向左寻找位置
        elif val > node.val:                        # 新花比当前花大，向右种植
            if node.right is None:
                node.right = TreeNode(val)          # 右边没有花，直接种植
                print(f"🌿 {val} 种在了 {node.val} 的右侧（大花区域）")
                return True
            else:
                return self._insert_recursive(node.right, val)  # 递归向右寻找位置
        else:
            print(f"⚠️ {val} 这朵花已经存在了，不重复种植")   # 花园里不种重复的花
            return False
    
    def search(self, val):
        """查找节点 - 在花园里寻找特定的花"""
        print(f"🔍 开始在花园里寻找编号为 {val} 的花...")
        path = []  # 记录查找路径
        result = self._search_recursive(self.root, val, path)
        if result:
            print(f"✨ 查找路径：{' → '.join(map(str, path))} (共 {len(path)} 步)")
        return result
    
    def _search_recursive(self, node, val, path):
        """递归查找辅助函数 - 遵循花园的有序规律"""
        if node is None:
            print(f"❌ 花园里没有编号为 {val} 的花")
            return False
        
        path.append(node.val)  # 记录访问的节点
        print(f"👀 当前检查：编号 {node.val} 的花")
        
        if val == node.val:
            print(f"🌸 找到了！编号 {val} 的花就在这里")
            return True
        elif val < node.val:
            print(f"⬅️ {val} < {node.val}，向小花区域(左边)寻找")
            return self._search_recursive(node.left, val, path)
        else:
            print(f"➡️ {val} > {node.val}，向大花区域(右边)寻找")
            return self._search_recursive(node.right, val, path)
    
    def delete(self, val):
        """删除节点 - 从花园中移除某朵花"""
        print(f"🗑️ 准备从花园中移除编号为 {val} 的花...")
        self.root, deleted = self._delete_recursive(self.root, val)
        if deleted:
            self.size -= 1
            print(f"✅ 成功移除了编号为 {val} 的花")
        else:
            print(f"❌ 花园里没有编号为 {val} 的花")
        return deleted
    
    def _delete_recursive(self, node, val):
        """递归删除辅助函数 - 处理三种删除情况"""
        if node is None:
            return None, False
        
        if val < node.val:
            node.left, deleted = self._delete_recursive(node.left, val)
            return node, deleted
        elif val > node.val:
            node.right, deleted = self._delete_recursive(node.right, val)
            return node, deleted
        else:
            # 找到要删除的节点，开始处理三种情况
            print(f"🎯 找到要删除的花：{val}")
            
            # 情况1：叶子节点（没有子花）
            if node.left is None and node.right is None:
                print(f"  这是一朵孤单的花（叶子节点），直接移除")
                return None, True
            
            # 情况2：只有一个子节点
            elif node.left is None:
                print(f"  这朵花只有右边的小伙伴，让小伙伴接替它的位置")
                return node.right, True
            elif node.right is None:
                print(f"  这朵花只有左边的小伙伴，让小伙伴接替它的位置")
                return node.left, True
            
            # 情况3：有两个子节点（最复杂的情况）
            else:
                print(f"  这朵花有左右两边的小伙伴，需要找个合适的接班人...")
                # 找到右子树中最小的节点（中序后继）
                successor = self._find_min(node.right)
                print(f"  找到接班人：编号 {successor.val} 的花")
                
                # 用后继节点的值替换当前节点
                node.val = successor.val
                print(f"  接班人 {successor.val} 接替了位置")
                
                # 删除后继节点（它最多只有右子树）
                node.right, _ = self._delete_recursive(node.right, successor.val)
                return node, True
    
    def _find_min(self, node):
        """找到子树中的最小节点 - 找到最小的花"""
        while node.left is not None:
            node = node.left
        return node
    
    def _find_max(self, node):
        """找到子树中的最大节点 - 找到最大的花"""
        while node.right is not None:
            node = node.right
        return node
    
    def inorder_traversal(self):
        """中序遍历 - 按编号从小到大游览花园"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """中序遍历递归辅助函数"""
        if node is not None:
            self._inorder_recursive(node.left, result)   # 先看左边的小花
            result.append(node.val)                      # 记录当前花的编号
            self._inorder_recursive(node.right, result)  # 再看右边的大花
    
    def get_height(self):
        """获取树的高度 - 花园有多少层"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """递归计算高度"""
        if node is None:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return max(left_height, right_height) + 1
    
    def analyze_efficiency(self):
        """分析查找效率 - 为什么BST这么快？"""
        height = self.get_height()
        print(f"\n📊 花园效率分析：")
        print(f"🌳 花园总共有 {self.size} 朵花")
        print(f"📏 花园高度：{height} 层")
        print(f"⚡ 最坏查找步数：{height} 步")
        print(f"🎯 平均查找步数：约 {height//2} 步")
        
        # 对比线性查找
        linear_avg = self.size // 2
        print(f"\n🆚 效率对比：")
        print(f"📝 线性查找平均需要：{linear_avg} 步")
        print(f"🌳 BST查找最多需要：{height} 步")
        if self.size > 0:
            improvement = linear_avg / height if height > 0 else 1
            print(f"🚀 BST比线性查找快：{improvement:.1f} 倍")
        
        # 理论分析
        import math
        theoretical_height = math.ceil(math.log2(self.size + 1)) if self.size > 0 else 0
        print(f"\n🧮 理论分析：")
        print(f"📐 理想高度(完全平衡)：{theoretical_height}")
        print(f"📊 当前高度：{height}")
        balance_ratio = theoretical_height / height if height > 0 else 1
        print(f"⚖️ 平衡度：{balance_ratio:.2f} (越接近1越平衡)")
    
    def visualize_tree(self):
        """可视化展示树结构"""
        if self.root is None:
            print("🌱 花园还是空的")
            return
        
        print(f"\n🌳 花园结构图：")
        self._print_tree(self.root, "", True)
    
    def _print_tree(self, node, prefix, is_last):
        """递归打印树结构"""
        if node is not None:
            print(prefix + ("└── " if is_last else "├── ") + str(node.val))
            
            children = []
            if node.left is not None:
                children.append((node.left, False))
            if node.right is not None:
                children.append((node.right, True))
            
            for i, (child, is_child_last) in enumerate(children):
                child_prefix = prefix + ("    " if is_last else "│   ")
                self._print_tree(child, child_prefix, is_child_last and i == len(children) - 1)

def demonstrate_bst_operations():
    """演示BST的完整功能"""
    print("=== 🌸 二叉搜索树花园演示 ===\n")
    
    # 创建花园
    garden = BinarySearchTree()
    
    # 插入花朵（模拟书籍编号）
    print("🌱 开始种植花园：")
    flowers = [50, 30, 70, 20, 40, 60, 80, 25, 35]
    for flower in flowers:
        garden.insert(flower)
    
    # 可视化花园结构
    garden.visualize_tree()
    
    # 查找操作演示
    print("\n" + "="*50)
    print("🔍 查找演示：")
    search_targets = [25, 60, 90]
    for target in search_targets:
        garden.search(target)
        print()
    
    # 删除操作演示
    print("="*50)
    print("🗑️ 删除操作演示：")
    
    # 删除叶子节点
    print("\n1. 删除叶子节点（25）：")
    garden.delete(25)
    
    # 删除只有一个子节点的节点
    print("\n2. 删除只有一个子节点的节点（20）：")
    garden.delete(20)
    
    # 删除有两个子节点的节点
    print("\n3. 删除有两个子节点的节点（30）：")
    garden.delete(30)
    
    print("\n删除后的花园结构：")
    garden.visualize_tree()
    
    # 中序遍历
    print("\n" + "="*50)
    print("🚶‍♀️ 按编号顺序游览花园（中序遍历）：")
    sorted_flowers = garden.inorder_traversal()
    print(f"游览顺序：{sorted_flowers}")
    print("✨ 神奇！自动按从小到大的顺序排列")
    
    # 效率分析
    print("\n" + "="*50)
    garden.analyze_efficiency()
    
    print(f"\n🎉 演示完成！花园里现在有 {garden.size} 朵美丽的花")

if __name__ == "__main__":
    demonstrate_bst_operations() 