class StaticNode {
    Object data;
    int next;
    
    StaticNode() { this.data = null; this.next = -1; }
}

public class SimpleDemo {
    private StaticNode[] nodes;  // KEY POINT: This is a 1D array!
    
    public SimpleDemo(int size) {
        this.nodes = new StaticNode[size];  // 1D array creation
        
        // Initialize each position
        for (int i = 0; i < size; i++) {
            nodes[i] = new StaticNode();
        }
    }
    
    public static void main(String[] args) {
        System.out.println("==== ANSWER TO YOUR QUESTION ====");
        System.out.println();
        
        System.out.println("Question: Does Java static linked list use 1D or 2D array?");
        System.out.println("Answer: JAVA USES 1D ARRAY!");
        System.out.println();
        
        System.out.println("Evidence:");
        SimpleDemo demo = new SimpleDemo(5);
        
        System.out.println("1. Declaration: StaticNode[] nodes");
        System.out.println("   - This is a 1D array of StaticNode objects");
        System.out.println("   - NOT a 2D array");
        System.out.println();
        
        System.out.println("2. Array structure comparison:");
        System.out.println("   Python: self.nodes = [{'data': None, 'next': i+1}...]");
        System.out.println("   Java:   StaticNode[] nodes = new StaticNode[maxSize]");
        System.out.println("   Both are 1D arrays!");
        System.out.println();
        
        System.out.println("3. Access pattern:");
        System.out.println("   Python: self.nodes[index]['data']");
        System.out.println("   Java:   nodes[index].data");
        System.out.println("   Both access: position[index] -> object -> field");
        System.out.println();
        
        System.out.println("4. Memory layout:");
        System.out.println("   [Node0] [Node1] [Node2] [Node3] [Node4] ...");
        System.out.println("   ^       ^       ^       ^       ^");
        System.out.println("   |       |       |       |       |");
        System.out.println("   0       1       2       3       4  <- 1D indices");
        System.out.println();
        
        System.out.println("CONCLUSION:");
        System.out.println("- Java static linked list uses 1D array");
        System.out.println("- Same principle as Python: One array, two logical lists");
        System.out.println("- Physical structure: 1 array");
        System.out.println("- Logical structure: 2 linked lists (data + free)");
    }
} 