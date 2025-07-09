from collections import deque

class TreeNode:
    """二叉树节点类"""
    def __init__(self, data):
        self.data = data          # 数据域：存储节点的值
        self.left = None          # 左指针：指向左子树
        self.right = None         # 右指针：指向右子树

def create_simple_family_tree():
    """构建演示用的简单家族树
    
    创建一个简单的三代家族树：
            爷爷
            /    \
        爸爸    叔叔  
        /  \      \
    儿子   女儿    侄子
    """
    grandpa = TreeNode("爷爷")     # 根节点
    dad = TreeNode("爸爸")         # 左子树根
    uncle = TreeNode("叔叔")       # 右子树根
    son = TreeNode("儿子")         # 左子树的左叶子
    daughter = TreeNode("女儿")    # 左子树的右叶子
    nephew = TreeNode("侄子")      # 右子树的右叶子
    
    # 建立关系
    grandpa.left = dad
    grandpa.right = uncle
    dad.left = son
    dad.right = daughter
    uncle.right = nephew
    
    return grandpa

def preorder_traversal(node, visit_path=None):
    """前序遍历：根 → 左 → 右（家长优先访问法）
    
    参数:
        node: 当前要访问的节点
        visit_path: 访问路径记录列表
    
    返回:
        访问顺序的列表
    """
    if visit_path is None:
        visit_path = []
        print("\n🏃‍♀️ 开始前序遍历（家长优先访问法）：")
        print("规则：到达每个家庭时，先见家长，再见左边孩子，最后见右边孩子")
        print("-" * 50)
    
    if node is not None:
        # 步骤1：访问当前节点（根）
        visit_path.append(node.data)
        print(f"👋 拜访了：{node.data}")
        
        # 步骤2：递归访问左子树
        if node.left is not None:
            print(f"↙️ 从 {node.data} 转向左孩子 {node.left.data}")
        preorder_traversal(node.left, visit_path)
        
        # 步骤3：递归访问右子树  
        if node.right is not None:
            print(f"↘️ 从 {node.data} 转向右孩子 {node.right.data}")
        preorder_traversal(node.right, visit_path)
    
    return visit_path

def inorder_traversal(node, visit_path=None):
    """中序遍历：左 → 根 → 右（年龄顺序访问法）
    
    参数:
        node: 当前要访问的节点
        visit_path: 访问路径记录列表
    
    返回:
        访问顺序的列表
    """
    if visit_path is None:
        visit_path = []
        print("\n🎯 开始中序遍历（年龄顺序访问法）：")
        print("规则：到达每个家庭时，先见小孩子，再见家长，最后见大孩子")
        print("-" * 50)
    
    if node is not None:
        # 步骤1：递归访问左子树
        if node.left is not None:
            print(f"↙️ 准备访问 {node.data} 的左孩子 {node.left.data}")
        inorder_traversal(node.left, visit_path)
        
        # 步骤2：访问当前节点（根）
        visit_path.append(node.data)
        print(f"👋 拜访了：{node.data}")
        
        # 步骤3：递归访问右子树
        if node.right is not None:
            print(f"↘️ 准备访问 {node.data} 的右孩子 {node.right.data}")
        inorder_traversal(node.right, visit_path)
    
    return visit_path

def postorder_traversal(node, visit_path=None):
    """后序遍历：左 → 右 → 根（晚辈优先访问法）
    
    参数:
        node: 当前要访问的节点
        visit_path: 访问路径记录列表
    
    返回:
        访问顺序的列表
    """
    if visit_path is None:
        visit_path = []
        print("\n🧒 开始后序遍历（晚辈优先访问法）：")
        print("规则：到达每个家庭时，先见完所有孩子，最后才见家长")
        print("-" * 50)
    
    if node is not None:
        # 步骤1：递归访问左子树
        if node.left is not None:
            print(f"↙️ 准备访问 {node.data} 的左孩子 {node.left.data}")
        postorder_traversal(node.left, visit_path)
        
        # 步骤2：递归访问右子树  
        if node.right is not None:
            print(f"↘️ 准备访问 {node.data} 的右孩子 {node.right.data}")
        postorder_traversal(node.right, visit_path)
        
        # 步骤3：访问当前节点（根）
        visit_path.append(node.data)
        print(f"👋 最后拜访：{node.data}")
    
    return visit_path

def level_order_traversal(root):
    """层序遍历：按辈分层级访问（按辈分访问法）
    
    使用队列实现广度优先搜索
    
    参数:
        root: 树的根节点
    
    返回:
        访问顺序的列表
    """
    if root is None:
        return []
    
    print("\n🏠 开始层序遍历（按辈分访问法）：")
    print("规则：一代一代地拜访，同代的从左到右")
    print("-" * 50)
    
    visit_path = []              # 访问路径记录
    queue = deque([root])        # 初始化队列，放入根节点
    level = 0                    # 层级计数器
    
    while queue:                 # 当队列不为空时继续
        level_size = len(queue)  # 当前层的节点数量
        print(f"\n第 {level} 层（{level_size} 个成员）：")
        
        # 处理当前层的所有节点
        for i in range(level_size):
            current_node = queue.popleft()  # 取出队列第一个节点
            visit_path.append(current_node.data)
            print(f"  👋 拜访了：{current_node.data}")
            
            # 将当前节点的子节点加入队列（先左后右）
            if current_node.left:
                queue.append(current_node.left)
                print(f"    ↙️ {current_node.data} 的左孩子 {current_node.left.data} 进入下一层队列")
            
            if current_node.right:
                queue.append(current_node.right)
                print(f"    ↘️ {current_node.data} 的右孩子 {current_node.right.data} 进入下一层队列")
        
        level += 1
    
    return visit_path

def simple_preorder(node):
    """简化版前序遍历（无打印输出）"""
    if node is None:
        return []
    return [node.data] + simple_preorder(node.left) + simple_preorder(node.right)

def simple_inorder(node):
    """简化版中序遍历（无打印输出）"""
    if node is None:
        return []
    return simple_inorder(node.left) + [node.data] + simple_inorder(node.right)

def simple_postorder(node):
    """简化版后序遍历（无打印输出）"""
    if node is None:
        return []
    return simple_postorder(node.left) + simple_postorder(node.right) + [node.data]

def simple_levelorder(root):
    """简化版层序遍历（无打印输出）"""
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.data)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

def compare_all_traversals(root):
    """对比四种遍历方式的结果"""
    print("\n🎭 四种遍历方式大对比：")
    print("=" * 60)
    
    # 获取四种遍历结果
    preorder = simple_preorder(root)
    inorder = simple_inorder(root)
    postorder = simple_postorder(root)
    levelorder = simple_levelorder(root)
    
    # 打印对比结果
    print(f"🏃‍♀️ 前序遍历（根→左→右）：{' → '.join(preorder)}")
    print(f"   特点：家长优先，适合复制树结构")
    print()
    print(f"🎯 中序遍历（左→根→右）：{' → '.join(inorder)}")
    print(f"   特点：二叉搜索树会得到有序结果")
    print()
    print(f"🧒 后序遍历（左→右→根）：{' → '.join(postorder)}")
    print(f"   特点：晚辈优先，适合删除树结构")
    print()
    print(f"🏠 层序遍历（按层级）：  {' → '.join(levelorder)}")
    print(f"   特点：按辈分访问，适合广度优先搜索")

def demonstrate_tree_traversals():
    """演示所有遍历方法的完整功能"""
    print("=== 🌳 二叉树遍历方法演示 ===")
    
    # 创建演示树
    demo_root = create_simple_family_tree()
    print("🏠 演示家族树构建完成！")
    print("     家族结构：")
    print("       爷爷")
    print("      /    \\")
    print("   爸爸    叔叔")
    print("   /  \\      \\")
    print("儿子  女儿   侄子")
    
    # 演示前序遍历
    preorder_result = preorder_traversal(demo_root)
    print(f"\n✅ 前序遍历完成！")
    print(f"📋 访问顺序：{' → '.join(preorder_result)}")
    
    # 演示中序遍历
    inorder_result = inorder_traversal(demo_root)
    print(f"\n✅ 中序遍历完成！")
    print(f"📋 访问顺序：{' → '.join(inorder_result)}")
    
    # 演示后序遍历
    postorder_result = postorder_traversal(demo_root)
    print(f"\n✅ 后序遍历完成！")
    print(f"📋 访问顺序：{' → '.join(postorder_result)}")
    
    # 演示层序遍历
    levelorder_result = level_order_traversal(demo_root)
    print(f"\n✅ 层序遍历完成！")
    print(f"📋 访问顺序：{' → '.join(levelorder_result)}")
    
    # 对比所有遍历方式
    compare_all_traversals(demo_root)

if __name__ == "__main__":
    demonstrate_tree_traversals() 