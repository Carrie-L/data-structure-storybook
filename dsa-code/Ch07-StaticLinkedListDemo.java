/**
 * Chapter 07: Static Linked List (Library Magic Number System) - Java Version
 * 
 * Uses 1D array + Node class implementation
 * Demonstrates "One Array, Two Logical Linked Lists" design
 */

// Static linked list node class
class StaticNode {
    Object data;    // Data field: stores actual data
    int next;       // Index pointer field: points to next node's array index
    
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

// Static linked list class
public class StaticLinkedListDemo {
    private StaticNode[] nodes;  // 1D Array: Physical storage structure
    private int head;            // Data list head pointer
    private int freeHead;        // Free list head pointer
    private int maxSize;         // Maximum capacity
    private int size;            // Current element count
    
    /**
     * Constructor: Initialize static linked list
     * @param maxSize Maximum capacity
     */
    public StaticLinkedListDemo(int maxSize) {
        this.maxSize = maxSize;
        this.nodes = new StaticNode[maxSize];  // Create 1D array
        this.head = -1;      // Data list initially empty
        this.freeHead = 0;   // Free list starts from position 0
        this.size = 0;
        
        // Initialize all nodes, build initial free list
        for (int i = 0; i < maxSize; i++) {
            nodes[i] = new StaticNode();
            nodes[i].next = i + 1;  // Each node points to next position
        }
        nodes[maxSize - 1].next = -1;  // Last node ends free list
        
        System.out.println("Library Magic Number System (Java Version) Started!");
        System.out.printf("   Total shelf positions: %d%n", maxSize);
        System.out.printf("   Data list head: %d (empty)%n", head);
        System.out.printf("   Free list head: %d%n", freeHead);
        displayStructure();
    }
    
    /**
     * Insert new element at head
     * @param data Data to insert
     * @return Whether insertion succeeded
     */
    public boolean insertAtHead(Object data) {
        System.out.printf("%nInserting at head: '%s'%n", data);
        
        // Step 1: Check if free nodes available
        if (freeHead == -1) {
            System.out.println("ERROR: Shelf is full, cannot insert new book!");
            return false;
        }
        
        // Step 2: Get free position
        int newPos = freeHead;
        System.out.printf("   Step 2: Get free position %d%n", newPos);
        
        // Step 3: Update free list head
        freeHead = nodes[newPos].next;
        System.out.printf("   Step 3: Update free head to %d%n", freeHead);
        
        // Step 4: Store data at new position
        nodes[newPos].data = data;
        System.out.printf("   Step 4: Store '%s' at position %d%n", data, newPos);
        
        // Step 5: Establish link relationship
        nodes[newPos].next = head;  // New node points to original head
        head = newPos;              // Update data list head
        size++;
        System.out.printf("   Step 5: New data list head: %d%n", head);
        
        System.out.printf("SUCCESS: Inserted! Current data list length: %d%n", size);
        return true;
    }
    
    /**
     * Delete head element
     * @return Deleted data, null if list is empty
     */
    public Object deleteAtHead() {
        System.out.println("\nDeleting head element");
        
        if (head == -1) {
            System.out.println("ERROR: List is empty, cannot delete");
            return null;
        }
        
        // Step 1: Save deletion info
        int deletedIndex = head;
        Object deletedData = nodes[head].data;
        System.out.printf("   Step 1: Deleting data '%s' at position %d%n", deletedData, deletedIndex);
        
        // Step 2: Data list skips deleted node
        head = nodes[head].next;
        System.out.printf("   Step 2: Data list head updated to %d%n", head);
        
        // Step 3: Clear deleted position data
        nodes[deletedIndex].data = null;
        System.out.printf("   Step 3: Clear data at position %d%n", deletedIndex);
        
        // Step 4: Add empty position back to free list
        nodes[deletedIndex].next = freeHead;
        freeHead = deletedIndex;
        size--;
        System.out.printf("   Step 4: Position %d added to free list, new free head: %d%n", 
                         deletedIndex, freeHead);
        
        System.out.printf("SUCCESS: Deleted! Current data list length: %d%n", size);
        return deletedData;
    }
    
    /**
     * Traverse the list
     * @return Array containing all elements
     */
    public Object[] traverse() {
        System.out.println("\nTraversing books in reading order:");
        
        Object[] result = new Object[size];
        int currentPos = head;
        int position = 0;
        
        while (currentPos != -1 && position < size) {
            Object data = nodes[currentPos].data;
            result[position] = data;
            System.out.printf("   Book %d: '%s' (at position %d)%n", position, data, currentPos);
            
            currentPos = nodes[currentPos].next;
            position++;
        }
        
        if (size == 0) {
            System.out.println("   Reading list is empty");
        }
        
        return result;
    }
    
    /**
     * Display detailed structure of static linked list
     */
    public void displayStructure() {
        System.out.println("\nStatic Linked List Internal Structure:");
        System.out.printf("   Data list head: %d%n", head);
        System.out.printf("   Free list head: %d%n", freeHead);
        System.out.printf("   Current size: %d/%d%n", size, maxSize);
        
        System.out.println("\nArray Detailed Status:");
        for (int i = 0; i < maxSize; i++) {
            StaticNode node = nodes[i];
            String dataStr = node.data != null ? String.format("'%s'", node.data) : "empty";
            String nextStr = node.next != -1 ? String.valueOf(node.next) : "end";
            
            // Determine node type
            String status;
            if (isInDataChain(i)) {
                status = "DATA";
            } else if (isInFreeChain(i)) {
                status = "FREE";
            } else {
                status = "UNKNOWN";
            }
            
            System.out.printf("   Position %d: data=%-12s next=%-3s (%s)%n", 
                             i, dataStr, nextStr, status);
        }
    }
    
    // Check if position is in data chain
    private boolean isInDataChain(int pos) {
        int current = head;
        while (current != -1) {
            if (current == pos) return true;
            current = nodes[current].next;
        }
        return false;
    }
    
    // Check if position is in free chain
    private boolean isInFreeChain(int pos) {
        int current = freeHead;
        while (current != -1) {
            if (current == pos) return true;
            current = nodes[current].next;
        }
        return false;
    }
    
    // Get list size
    public int size() {
        return size;
    }
    
    /**
     * Demo program
     */
    public static void main(String[] args) {
        System.out.println("=== Welcome to Java Static Linked List Demo! ===");
        System.out.println("Let's explore the magical world of static linked lists~\n");
        
        // Create a small static linked list
        StaticLinkedListDemo library = new StaticLinkedListDemo(8);
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("INSERTION DEMO:");
        
        // Insert some books
        String[] books = {"Algorithm", "Data Structure", "Programming Pearls", "Computer Network", "Operating System"};
        for (String book : books) {
            library.insertAtHead(book);
            System.out.println();
        }
        
        // Display current structure
        library.displayStructure();
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("TRAVERSAL DEMO:");
        Object[] readingList = library.traverse();
        System.out.print("Complete reading list: [");
        for (int i = 0; i < readingList.length; i++) {
            System.out.print(readingList[i]);
            if (i < readingList.length - 1) System.out.print(", ");
        }
        System.out.println("]");
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("DELETION DEMO:");
        
        // Delete head element
        Object deleted = library.deleteAtHead();
        System.out.printf("Deleted book: '%s'%n%n", deleted);
        
        // Display structure after deletion
        library.displayStructure();
        
        System.out.println("\nDemo completed! Library management system working properly!");
        
        System.out.println("\nJava Implementation Key Points:");
        System.out.println("   - Uses 1D array: StaticNode[] nodes");
        System.out.println("   - Each StaticNode contains data and next fields");
        System.out.println("   - Physical structure: 1 array, Logical structure: 2 linked lists");
        System.out.println("   - Type safe, no boxing/unboxing operations needed");
        
        System.out.println("\nAnswer to your question:");
        System.out.println("   JAVA STATIC LINKED LIST USES 1D ARRAY!");
        System.out.println("   - NOT a 2D array");
        System.out.println("   - Same as Python: One array, two logical linked lists");
        System.out.println("   - StaticNode[] is a 1D array of Node objects");
    }
} 