/**
 * 第07章：图书馆的魔法编号系统 - Java版静态链表
 * 
 * 使用一维数组 + Node类的实现方式
 * 体现了"一个数组，两个逻辑链表"的设计思想
 */

// 静态链表节点类
class StaticNode {
    Object data;    // 数据域：存储实际数据
    int next;       // 下标指针域：指向下一个节点的数组下标
    
    public StaticNode() {
        this.data = null;
        this.next = -1;
    }
    
    public StaticNode(Object data, int next) {
        this.data = data;
        this.next = next;
    }
    
    @Override
    public String toString() {
        return String.format("Node{data=%s, next=%d}", data, next);
    }
}

// 静态链表类
public class StaticLinkedList {
    private StaticNode[] nodes;  // 📚 一维数组：物理存储结构
    private int head;            // 📖 数据链表头指针
    private int freeHead;        // ⭕ 空闲链表头指针
    private int maxSize;         // 最大容量
    private int size;            // 当前元素数量
    
    /**
     * 构造函数：初始化静态链表
     * @param maxSize 最大容量
     */
    public StaticLinkedList(int maxSize) {
        this.maxSize = maxSize;
        this.nodes = new StaticNode[maxSize];  // 🎯 创建一维数组
        this.head = -1;      // 数据链表初始为空
        this.freeHead = 0;   // 空闲链表从位置0开始
        this.size = 0;
        
        // 初始化所有节点，构建初始空闲链表
        for (int i = 0; i < maxSize; i++) {
            nodes[i] = new StaticNode();
            nodes[i].next = i + 1;  // 每个节点指向下一个位置
        }
        nodes[maxSize - 1].next = -1;  // 最后一个节点结束空闲链表
        
        System.out.println("📚 Java版图书馆魔法编号系统启动！");
        System.out.printf("   书架总位置：%d%n", maxSize);
        System.out.printf("   数据链表头：%d (空)%n", head);
        System.out.printf("   空闲链表头：%d%n", freeHead);
        displayStructure();
    }
    
    /**
     * 在链表头部插入新元素
     * @param data 要插入的数据
     * @return 是否插入成功
     */
    public boolean insertAtHead(Object data) {
        System.out.printf("%n📥 准备在开头插入：'%s'%n", data);
        
        // 步骤1：检查是否还有空闲节点
        if (freeHead == -1) {
            System.out.println("❌ 书架已满，无法插入新书！");
            return false;
        }
        
        // 步骤2：获取空闲位置
        int newPos = freeHead;
        System.out.printf("   🎯 从空闲链表获取位置：%d%n", newPos);
        
        // 步骤3：更新空闲链表头
        freeHead = nodes[newPos].next;
        System.out.printf("   📋 空闲链表头更新为：%d%n", freeHead);
        
        // 步骤4：在新位置存储数据
        nodes[newPos].data = data;
        System.out.printf("   📖 在位置%d存储数据：'%s'%n", newPos, data);
        
        // 步骤5：建立链接关系
        nodes[newPos].next = head;  // 新节点指向原头节点
        head = newPos;              // 更新数据链表头
        size++;
        System.out.printf("   🔗 新的数据链表头：%d%n", head);
        
        System.out.printf("✅ 成功插入！当前数据链表长度：%d%n", size);
        return true;
    }
    
    /**
     * 删除链表头部元素
     * @return 删除的数据，如果链表为空则返回null
     */
    public Object deleteAtHead() {
        System.out.println("\n🗑️ 准备删除开头元素");
        
        if (head == -1) {
            System.out.println("❌ 链表为空，无法删除");
            return null;
        }
        
        // 步骤1：保存要删除的信息
        int deletedIndex = head;
        Object deletedData = nodes[head].data;
        System.out.printf("   🎯 准备删除位置%d的数据：'%s'%n", deletedIndex, deletedData);
        
        // 步骤2：数据链表跳过被删除节点
        head = nodes[head].next;
        System.out.printf("   📋 数据链表头更新为：%d%n", head);
        
        // 步骤3：清空删除位置的数据
        nodes[deletedIndex].data = null;
        System.out.printf("   🧹 清空位置%d的数据%n", deletedIndex);
        
        // 步骤4：将空出的位置加入空闲链表
        nodes[deletedIndex].next = freeHead;
        freeHead = deletedIndex;
        size--;
        System.out.printf("   🔄 位置%d加入空闲链表，新空闲头：%d%n", deletedIndex, freeHead);
        
        System.out.printf("✅ 成功删除！当前数据链表长度：%d%n", size);
        return deletedData;
    }
    
    /**
     * 查找元素
     * @param data 要查找的数据
     * @return 元素在链表中的位置（从0开始），如果不存在返回-1
     */
    public int search(Object data) {
        System.out.printf("%n🔍 查找：'%s'%n", data);
        
        int currentPos = head;
        int index = 0;
        
        while (currentPos != -1) {
            if (nodes[currentPos].data != null && nodes[currentPos].data.equals(data)) {
                System.out.printf("✅ 在位置 %d 找到 '%s'%n", index, data);
                return index;
            }
            
            currentPos = nodes[currentPos].next;
            index++;
        }
        
        System.out.printf("❌ 未找到 '%s'%n", data);
        return -1;
    }
    
    /**
     * 遍历链表
     * @return 包含所有元素的数组
     */
    public Object[] traverse() {
        System.out.println("\n📖 按阅读顺序遍历书籍：");
        
        Object[] result = new Object[size];
        int currentPos = head;
        int position = 0;
        
        while (currentPos != -1 && position < size) {
            Object data = nodes[currentPos].data;
            result[position] = data;
            System.out.printf("   第%d本: '%s' (位置%d)%n", position, data, currentPos);
            
            currentPos = nodes[currentPos].next;
            position++;
        }
        
        if (size == 0) {
            System.out.println("   📭 阅读列表为空");
        }
        
        return result;
    }
    
    /**
     * 显示静态链表的详细结构
     */
    public void displayStructure() {
        System.out.println("\n🏗️ 静态链表内部结构：");
        System.out.printf("   数据链表头：%d%n", head);
        System.out.printf("   空闲链表头：%d%n", freeHead);
        System.out.printf("   当前大小：%d/%d%n", size, maxSize);
        
        System.out.println("\n📊 数组详细状态：");
        for (int i = 0; i < maxSize; i++) {
            StaticNode node = nodes[i];
            String dataStr = node.data != null ? String.format("'%s'", node.data) : "空";
            String nextStr = node.next != -1 ? String.valueOf(node.next) : "结束";
            
            // 判断节点类型
            String status;
            if (isInDataChain(i)) {
                status = "📚数据";
            } else if (isInFreeChain(i)) {
                status = "⭕空闲";
            } else {
                status = "❓未知";
            }
            
            System.out.printf("   位置%d: data=%-10s next=%-3s (%s)%n", i, dataStr, nextStr, status);
        }
    }
    
    // 检查位置是否在数据链表中
    private boolean isInDataChain(int pos) {
        int current = head;
        while (current != -1) {
            if (current == pos) return true;
            current = nodes[current].next;
        }
        return false;
    }
    
    // 检查位置是否在空闲链表中
    private boolean isInFreeChain(int pos) {
        int current = freeHead;
        while (current != -1) {
            if (current == pos) return true;
            current = nodes[current].next;
        }
        return false;
    }
    
    // 获取链表大小
    public int size() {
        return size;
    }
    
    // 检查是否为空
    public boolean isEmpty() {
        return head == -1;
    }
    
    // 检查是否已满
    public boolean isFull() {
        return freeHead == -1;
    }
    
    /**
     * 演示程序
     */
    public static void main(String[] args) {
        System.out.println("🌟 欢迎来到Java版图书馆的魔法编号系统！");
        System.out.println("让我们一起探索静态链表的奇妙世界～\n");
        
        // 创建一个小型静态链表
        StaticLinkedList library = new StaticLinkedList(8);
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("📥 插入操作演示：");
        
        // 插入一些书籍
        String[] books = {"算法导论", "数据结构", "编程珠玑", "计算机网络", "操作系统"};
        for (String book : books) {
            library.insertAtHead(book);
            System.out.println();
        }
        
        // 显示当前结构
        library.displayStructure();
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("📖 遍历操作演示：");
        Object[] readingList = library.traverse();
        System.out.print("完整阅读列表：[");
        for (int i = 0; i < readingList.length; i++) {
            System.out.print(readingList[i]);
            if (i < readingList.length - 1) System.out.print(", ");
        }
        System.out.println("]");
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("🔍 查找操作演示：");
        String[] searchBooks = {"数据结构", "数学分析", "编程珠玑"};
        for (String book : searchBooks) {
            int index = library.search(book);
            if (index != -1) {
                System.out.printf("'%s' 在阅读列表的第 %d 位%n", book, index);
            }
            System.out.println();
        }
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("🗑️ 删除操作演示：");
        
        // 删除头部元素
        Object deleted = library.deleteAtHead();
        System.out.printf("删除的书籍：'%s'%n%n", deleted);
        
        // 显示删除后的结构
        library.displayStructure();
        
        System.out.println("\n🎉 Java版演示完成！图书馆管理系统运行正常！");
        
        System.out.println("\n💡 Java实现要点：");
        System.out.println("   • 使用一维数组 StaticNode[] nodes");
        System.out.println("   • 每个StaticNode包含data和next字段");
        System.out.println("   • 物理结构：1个数组，逻辑结构：2个链表");
        System.out.println("   • 类型安全，无需装箱/拆箱操作");
    }
} 