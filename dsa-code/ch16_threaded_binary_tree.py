class ThreadedTreeNode:
    """线索二叉树节点
    
    相比普通节点，增加了：
    - ltag: 左指针类型标志 (0=孩子, 1=前驱线索)
    - rtag: 右指针类型标志 (0=孩子, 1=后继线索)
    """
    def __init__(self, data):
        self.data = data          # 数据域：存储节点的值
        self.left = None          # 左指针域：可能指向左孩子或前驱节点
        self.right = None         # 右指针域：可能指向右孩子或后继节点
        self.ltag = 0             # 左标志位：0=指向孩子，1=指向前驱线索
        self.rtag = 0             # 右标志位：0=指向孩子，1=指向后继线索
    
    def __str__(self):
        """节点的字符串表示，清楚显示指针类型和指向"""
        left_desc = "左孩子" if self.ltag == 0 else "前驱线索"
        right_desc = "右孩子" if self.rtag == 0 else "后继线索"
        left_target = self.left.data if self.left else "空"
        right_target = self.right.data if self.right else "空"
        return f"节点{self.data}[{left_desc}:{left_target}, {right_desc}:{right_target}]"

class ThreadedBinaryTree:
    """线索二叉树类"""
    
    def __init__(self):
        self.root = None          # 根节点指针
        
    def create_from_array(self, arr):
        """从数组创建普通二叉树，然后可以进行线索化
        
        Args:
            arr: 层序遍历的数组表示，None表示空节点
        """
        if not arr:               # 如果数组为空，返回None
            return None
            
        # 第一步：为每个非空值创建ThreadedTreeNode节点
        nodes = [ThreadedTreeNode(val) if val is not None else None for val in arr]
        
        # 第二步：建立父子关系（按照完全二叉树的索引规律）
        for i in range(len(nodes)):
            if nodes[i] is not None:      # 当前节点存在
                left_idx = 2 * i + 1      # 左孩子的索引
                right_idx = 2 * i + 2     # 右孩子的索引
                
                # 连接左孩子
                if left_idx < len(nodes) and nodes[left_idx] is not None:
                    nodes[i].left = nodes[left_idx]
                    nodes[i].ltag = 0     # 标记为指向孩子
                    
                # 连接右孩子
                if right_idx < len(nodes) and nodes[right_idx] is not None:
                    nodes[i].right = nodes[right_idx]
                    nodes[i].rtag = 0     # 标记为指向孩子
        
        self.root = nodes[0] if nodes else None  # 设置根节点
        return self.root
    
    def inorder_threading(self):
        """对二叉树进行中序线索化
        
        这是线索化的核心算法，通过中序遍历建立前驱后继关系
        """
        if self.root is None:     # 空树无需线索化
            return
            
        print("🧵 开始中序线索化过程：")
        print("-" * 50)
        
        # 用于追踪前驱节点的变量
        self.prev_node = None
        
        # 递归进行线索化
        self._inorder_threading_recursive(self.root)
        
        print("✅ 线索化完成！")
    
    def _inorder_threading_recursive(self, node):
        """递归进行中序线索化的核心逻辑
        
        按照中序遍历的顺序：左子树 → 根节点 → 右子树
        """
        if node is None:          # 递归终止条件
            return
            
        # 第一步：线索化左子树
        self._inorder_threading_recursive(node.left)
        
        # 第二步：处理当前节点的线索
        # 处理左线索（前驱关系）
        if node.left is None:     # 如果左指针域为空
            node.left = self.prev_node    # 指向前驱节点
            node.ltag = 1         # 标记为线索
            if self.prev_node:
                print(f"   🔗 {node.data} 的前驱线索指向 {self.prev_node.data}")
        
        # 处理右线索（后继关系）- 需要在遍历过程中设置
        if self.prev_node and self.prev_node.right is None:  # 前一个节点的右指针为空
            self.prev_node.right = node    # 前一个节点的后继是当前节点
            self.prev_node.rtag = 1        # 标记为线索
            print(f"   🔗 {self.prev_node.data} 的后继线索指向 {node.data}")
        
        # 第三步：更新前驱节点为当前节点
        self.prev_node = node
        
        # 第四步：线索化右子树
        self._inorder_threading_recursive(node.right)
    
    def inorder_traversal_threaded(self):
        """使用线索进行中序遍历（无需递归栈！）
        
        这是线索二叉树的核心优势：无栈遍历
        """
        if self.root is None:
            return []
            
        print("\n🚶‍♀️ 使用线索进行中序遍历（无递归）：")
        print("-" * 50)
        
        result = []               # 存储遍历结果
        current = self._find_leftmost(self.root)  # 从最左节点开始
        
        while current:            # 遍历直到没有下一个节点
            # 访问当前节点
            result.append(current.data)
            print(f"👋 访问节点：{current.data}")
            
            # 寻找后继节点
            if current.rtag == 1: # 右指针是线索
                # 直接跟随线索到达后继节点
                current = current.right
                if current:
                    print(f"   ↗️ 通过后继线索到达：{current.data}")
            else:                 # 右指针是孩子
                # 进入右子树，找到最左节点
                if current.right:
                    current = self._find_leftmost(current.right)
                    if current:
                        print(f"   ↘️ 进入右子树，到达最左节点：{current.data}")
                else:
                    current = None    # 遍历结束
        
        return result
    
    def _find_leftmost(self, node):
        """找到以node为根的子树中最左边的节点
        
        这是线索遍历的辅助方法
        """
        if node is None:
            return None
            
        # 一直向左走，直到没有左孩子（注意：线索不算孩子）
        while node.ltag == 0 and node.left:
            node = node.left
            
        return node
    
    def find_predecessor(self, target_data):
        """查找指定节点的前驱（O(1)时间复杂度！）
        
        Args:
            target_data: 目标节点的数据值
            
        Returns:
            前驱节点的数据值，如果没有前驱则返回None
        """
        node = self._find_node(target_data)      # 先找到目标节点
        if node is None:
            return None
            
        if node.ltag == 1:        # 有前驱线索
            return node.left.data if node.left else None
        else:                     # 没有前驱线索，说明有左子树
            # 前驱是左子树的最右节点
            if node.left:
                pred = node.left
                while pred.rtag == 0 and pred.right:  # 一直向右走
                    pred = pred.right
                return pred.data
            return None
    
    def find_successor(self, target_data):
        """查找指定节点的后继（O(1)时间复杂度！）
        
        Args:
            target_data: 目标节点的数据值
            
        Returns:
            后继节点的数据值，如果没有后继则返回None
        """
        node = self._find_node(target_data)      # 先找到目标节点
        if node is None:
            return None
            
        if node.rtag == 1:        # 有后继线索
            return node.right.data if node.right else None
        else:                     # 没有后继线索，说明有右子树
            # 后继是右子树的最左节点
            if node.right:
                return self._find_leftmost(node.right).data
            return None
    
    def _find_node(self, target_data):
        """查找指定数据的节点（辅助方法）
        
        Args:
            target_data: 要查找的数据值
            
        Returns:
            找到的节点，如果不存在则返回None
        """
        def search(node):
            if node is None:
                return None
            if node.data == target_data:  # 找到目标节点
                return node
                
            # 在左子树中查找（只在真正的孩子中查找）
            if node.ltag == 0:    # 有左孩子
                result = search(node.left)
                if result:
                    return result
                    
            # 在右子树中查找（只在真正的孩子中查找）
            if node.rtag == 0:    # 有右孩子
                return search(node.right)
                
            return None
        
        return search(self.root)
    
    def display_tree_structure(self):
        """显示线索二叉树的详细结构"""
        print("\n🌳 线索二叉树结构详情：")
        print("=" * 60)
        self._display_node_details(self.root, 0)
    
    def _display_node_details(self, node, depth):
        """递归显示节点详情"""
        if node is None:
            return
            
        indent = "  " * depth     # 缩进表示层次
        print(f"{indent}{node}")
        
        # 递归显示子节点（只显示真正的孩子，不显示线索）
        if node.ltag == 0 and node.left:
            self._display_node_details(node.left, depth + 1)
        if node.rtag == 0 and node.right:
            self._display_node_details(node.right, depth + 1)

def analyze_null_pointers(root):
    """统计二叉树中的空指针数量"""
    if root is None:
        return 0, 0  # (总指针数, 空指针数)
    
    total_pointers = 0
    null_pointers = 0
    
    def count_pointers(node):
        nonlocal total_pointers, null_pointers
        if node is None:
            return
            
        # 每个节点有两个指针域
        total_pointers += 2
        
        # 统计空指针
        if node.left is None:
            null_pointers += 1
        if node.right is None:
            null_pointers += 1
            
        # 递归统计子树
        count_pointers(node.left)
        count_pointers(node.right)
    
    count_pointers(root)
    return total_pointers, null_pointers

def main():
    """演示线索二叉树的完整功能"""
    print("=== 🧵 线索二叉树演示 ===")

    # 创建示例二叉树：    A
    #                  /   \
    #                 B     C  
    #                /     / \
    #               D     E   F

    tree_data = ['A', 'B', 'C', 'D', None, 'E', 'F']  # 层序数组表示
    threaded_tree = ThreadedBinaryTree()              # 创建线索二叉树对象
    threaded_tree.create_from_array(tree_data)        # 从数组创建树结构

    print("原始二叉树结构：")
    print("        A")
    print("       / \\")
    print("      B   C")
    print("     /   / \\")
    print("    D   E   F")

    # 进行线索化
    threaded_tree.inorder_threading()

    # 显示线索化后的结构
    threaded_tree.display_tree_structure()

    # 使用线索进行遍历
    traversal_result = threaded_tree.inorder_traversal_threaded()
    print(f"\n📋 中序遍历结果：{' → '.join(traversal_result)}")

    # 演示前驱后继查找的强大功能
    print(f"\n🔍 前驱后继查找演示：")
    for node_data in ['D', 'B', 'A', 'E', 'C', 'F']:
        pred = threaded_tree.find_predecessor(node_data)    # O(1)查找前驱
        succ = threaded_tree.find_successor(node_data)      # O(1)查找后继
        print(f"节点 {node_data}: 前驱={pred if pred else '无'}, 后继={succ if succ else '无'}")

if __name__ == "__main__":
    main() 