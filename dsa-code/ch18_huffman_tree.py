"""
第18章：编码世界的温柔秘密 - 哈夫曼树完整实现
作者：数据之心小说组
主题：哈夫曼编码(Huffman Coding)与哈夫曼树(Huffman Tree)

本文件包含：
1. 哈夫曼树节点类的完整实现
2. 字符频率统计功能
3. 哈夫曼树构建算法
4. 编码表生成
5. 文本编码与解码
6. 压缩效果分析
7. 实际应用示例
"""

import heapq  # 优先队列，用于构建哈夫曼树
from collections import Counter, defaultdict  # 计数器和默认字典
import pickle  # 用于序列化哈夫曼树
import os     # 用于文件操作


class HuffmanNode:
    """
    哈夫曼树节点类
    
    就像伊莎贝尔温柔地构建家族树一样，
    哈夫曼树的每个节点都承载着重要的信息～
    """
    
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char    # 字符（叶子节点才有字符，内部节点为None）
        self.freq = freq    # 频率（权重）
        self.left = left    # 左子树
        self.right = right  # 右子树
    
    def __lt__(self, other):
        """
        定义节点比较方法，让优先队列能够正确排序
        频率小的节点优先级更高（小顶堆）
        """
        return self.freq < other.freq
    
    def __gt__(self, other):
        """定义大于比较"""
        return self.freq > other.freq
    
    def __eq__(self, other):
        """定义相等比较"""
        if other is None:
            return False
        if not isinstance(other, HuffmanNode):
            return False
        return self.freq == other.freq
    
    def is_leaf(self):
        """判断是否为叶子节点"""
        return self.char is not None
    
    def __repr__(self):
        """节点的字符串表示，方便调试"""
        if self.is_leaf():
            return f"HuffmanNode('{self.char}', {self.freq})"
        else:
            return f"HuffmanNode(None, {self.freq})"


class HuffmanCoder:
    """
    哈夫曼编码器类
    
    就像黛芙优雅地处理复杂算法一样，
    这个类温柔而高效地处理文本压缩～
    """
    
    def __init__(self):
        self.root = None           # 哈夫曼树的根节点
        self.codes = {}           # 字符到编码的映射表
        self.reverse_codes = {}   # 编码到字符的映射表（用于解码）
    
    def _count_frequency(self, text):
        """
        统计文本中每个字符的出现频率
        
        就像安妮仔细数着书架上每种书的数量，
        我们需要知道每个字符出现了多少次～
        
        Args:
            text (str): 输入文本
            
        Returns:
            dict: 字符频率字典 {字符: 频率}
        """
        if not text:  # 如果文本为空，直接返回空字典
            return {}
        
        # 使用Counter来统计频率，这是Python的计数器类
        # Counter会自动遍历文本中的每个字符并统计出现次数
        frequency = Counter(text)
        
        print(f"📊 字符频率统计完成！")
        print(f"   发现 {len(frequency)} 种不同字符")
        print(f"   文本总长度：{len(text)} 个字符")
        
        # 显示频率最高的几个字符
        most_common = frequency.most_common(5)
        print(f"   出现频率最高的字符：")
        for char, freq in most_common:
            # 处理特殊字符的显示
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            print(f"     {display_char}: {freq}次 ({freq/len(text)*100:.1f}%)")
        
        return frequency
    
    def _build_huffman_tree(self, frequency):
        """
        构建哈夫曼树
        
        就像希娅耐心地搭建积木塔一样，
        我们从最小的频率开始，逐步构建完整的哈夫曼树～
        
        Args:
            frequency (dict): 字符频率字典
            
        Returns:
            HuffmanNode: 哈夫曼树的根节点
        """
        if not frequency:
            return None
        
        # 如果只有一个字符，创建一个简单的树
        if len(frequency) == 1:
            char, freq = list(frequency.items())[0]
            root = HuffmanNode(freq=freq)
            root.left = HuffmanNode(char=char, freq=freq)
            print(f"🌱 只有一个字符 '{char}'，创建简单树结构")
            return root
        
        # 创建优先队列（小顶堆）
        heap = []
        
        # 为每个字符创建叶子节点并放入堆中
        for char, freq in frequency.items():  # 遍历字符频率字典
            node = HuffmanNode(char=char, freq=freq)  # 创建叶子节点
            heapq.heappush(heap, node)  # 将节点放入优先队列（小顶堆）
        
        print(f"🌳 开始构建哈夫曼树...")
        print(f"   初始节点数：{len(heap)}")
        
        step = 1
        # 不断合并频率最小的两个节点，直到只剩一个根节点
        while len(heap) > 1:  # 当堆中还有多个节点时继续合并
            # 取出频率最小的两个节点
            left = heapq.heappop(heap)   # heappop()取出堆顶最小元素，作为左子树
            right = heapq.heappop(heap)  # 再取出下一个最小元素，作为右子树
            
            # 创建新的内部节点（不对应任何字符，只是中间节点）
            merged_freq = left.freq + right.freq  # 新节点频率=两个子节点频率之和
            merged_node = HuffmanNode(char=None, freq=merged_freq, left=left, right=right)
            
            # 将新节点放回堆中，它会根据频率自动排序
            heapq.heappush(heap, merged_node)
            
            print(f"   步骤 {step}: 合并频率 {left.freq} + {right.freq} = {merged_freq}")
            step += 1
        
        root = heap[0]  # 最后剩下的就是根节点
        print(f"✨ 哈夫曼树构建完成！根节点频率：{root.freq}")
        return root
    
    def _generate_codes(self, root):
        """
        从哈夫曼树生成编码表
        
        就像伊莎贝尔温柔地为每个家族成员标记路径，
        我们为每个字符分配唯一的二进制编码～
        
        Args:
            root (HuffmanNode): 哈夫曼树的根节点
        """
        if not root:
            return
        
        self.codes = {}
        self.reverse_codes = {}
        
        def dfs(node, code):
            """深度优先搜索生成编码"""
            if node.is_leaf():  # 判断是否为叶子节点（有字符的节点）
                # 叶子节点：保存字符的编码
                self.codes[node.char] = code if code else "0"  # 如果只有一个字符，编码为"0"
                self.reverse_codes[code if code else "0"] = node.char  # 建立反向映射用于解码
            else:
                # 内部节点：继续向下搜索
                if node.left:  # 如果有左子树
                    dfs(node.left, code + "0")   # 向左走，编码添加"0"
                if node.right:  # 如果有右子树
                    dfs(node.right, code + "1")  # 向右走，编码添加"1"
        
        dfs(root, "")
        
        print(f"📝 编码表生成完成！")
        print(f"   共生成 {len(self.codes)} 个字符的编码")
        
        # 显示编码表（按编码长度排序）
        sorted_codes = sorted(self.codes.items(), key=lambda x: len(x[1]))
        print(f"   编码表（按长度排序）：")
        for char, code in sorted_codes[:10]:  # 只显示前10个
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            print(f"     {display_char}: {code}")
        if len(sorted_codes) > 10:
            print(f"     ... 还有 {len(sorted_codes) - 10} 个字符")
    
    def fit(self, text):
        """
        训练哈夫曼编码器
        
        就像安妮认真学习新知识一样，
        编码器需要先学习文本的特征，才能高效压缩～
        
        Args:
            text (str): 训练文本
        """
        print(f"🎓 开始训练哈夫曼编码器...")
        
        # 第一步：统计字符频率
        frequency = self._count_frequency(text)
        if not frequency:
            print("⚠️  输入文本为空，无法训练编码器")
            return
        
        # 第二步：构建哈夫曼树
        self.root = self._build_huffman_tree(frequency)
        
        # 第三步：生成编码表
        self._generate_codes(self.root)
        
        print(f"🎉 哈夫曼编码器训练完成！")
    
    def encode(self, text):
        """
        编码文本
        
        就像黛芙将复杂的想法转化为简洁的代码，
        我们将文本转换为紧凑的二进制编码～
        
        Args:
            text (str): 待编码的文本
            
        Returns:
            str: 编码后的二进制字符串
        """
        if not self.codes:
            raise ValueError("编码器尚未训练！请先调用 fit() 方法")
        
        if not text:
            return ""
        
        # 将每个字符转换为对应的编码
        encoded_bits = []  # 存储所有字符的编码
        for char in text:  # 遍历原文本的每个字符
            if char in self.codes:  # 如果该字符在编码表中
                encoded_bits.append(self.codes[char])  # 添加对应的二进制编码
            else:
                # 处理训练时未见过的字符（实际应用中需要更好的处理）
                print(f"⚠️  警告：字符 '{char}' 不在编码表中，跳过")
        
        encoded_text = "".join(encoded_bits)  # 将所有编码连接成一个长字符串
        
        # 计算压缩效果
        original_bits = len(text) * 8  # 假设原文每字符8位（ASCII）
        compressed_bits = len(encoded_text)
        compression_ratio = (1 - compressed_bits / original_bits) * 100 if original_bits > 0 else 0
        
        print(f"📦 编码完成！")
        print(f"   原始长度：{len(text)} 字符 ({original_bits} 位)")
        print(f"   编码长度：{compressed_bits} 位")
        print(f"   压缩率：{compression_ratio:.1f}%")
        
        return encoded_text
    
    def decode(self, encoded_text):
        """
        解码二进制文本
        
        就像希娅耐心地解读密码一样，
        我们将二进制编码还原为原始文本～
        
        Args:
            encoded_text (str): 编码后的二进制字符串
            
        Returns:
            str: 解码后的原始文本
        """
        if not self.root:
            raise ValueError("编码器尚未训练！请先调用 fit() 方法")
        
        if not encoded_text:
            return ""
        
        decoded_chars = []  # 存储解码后的字符
        current_node = self.root  # 从根节点开始
        
        # 遍历每个二进制位
        for bit in encoded_text:  # 逐个处理编码字符串中的每一位
            if bit == '0':  # 如果是'0'，向左走
                current_node = current_node.left
            elif bit == '1':  # 如果是'1'，向右走
                current_node = current_node.right
            else:
                raise ValueError(f"无效的二进制位：{bit}")  # 非0非1的字符是错误的
            
            # 到达叶子节点，找到一个字符
            if current_node.is_leaf():  # 如果到达叶子节点
                decoded_chars.append(current_node.char)  # 记录找到的字符
                current_node = self.root  # 重新从根节点开始下一个字符的解码
        
        # 检查是否正确结束在根节点
        if current_node != self.root:
            print("⚠️  警告：编码不完整，可能存在截断")
        
        decoded_text = "".join(decoded_chars)
        print(f"📖 解码完成！恢复了 {len(decoded_text)} 个字符")
        
        return decoded_text
    
    def get_code_table(self):
        """
        获取编码表
        
        Returns:
            dict: 字符到编码的映射表
        """
        return self.codes.copy()
    
    def save_model(self, filename):
        """
        保存训练好的模型
        
        就像伊莎贝尔细心地保存研究成果，
        我们将编码器保存起来以便重复使用～
        
        Args:
            filename (str): 保存文件名
        """
        model_data = {
            'root': self.root,
            'codes': self.codes,
            'reverse_codes': self.reverse_codes
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 模型已保存到：{filename}")
    
    def load_model(self, filename):
        """
        加载训练好的模型
        
        Args:
            filename (str): 模型文件名
        """
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.root = model_data['root']
        self.codes = model_data['codes']
        self.reverse_codes = model_data['reverse_codes']
        
        print(f"📂 模型已从 {filename} 加载完成")


class FileCompressor:
    """
    文件压缩器类
    
    就像希娅用巧妙的方法解决实际问题，
    这个类专门处理文件的压缩和解压缩～
    """
    
    def __init__(self):
        self.coder = HuffmanCoder()
    
    def compress_file(self, input_file, output_file):
        """
        压缩文件
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
        """
        print(f"🗜️  开始压缩文件：{input_file}")
        
        # 读取原始文件
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(input_file, 'r', encoding='latin1') as f:
                text = f.read()
        
        if not text:
            print("⚠️  文件为空，无法压缩")
            return
        
        # 训练编码器并压缩
        self.coder.fit(text)
        compressed_data = self.coder.encode(text)
        
        # 保存压缩文件（包含哈夫曼树和压缩数据）
        with open(output_file, 'wb') as f:
            # 保存哈夫曼树和压缩数据
            compress_info = {
                'huffman_tree': self.coder.root,
                'compressed_data': compressed_data,
                'original_length': len(text)
            }
            pickle.dump(compress_info, f)
        
        # 计算压缩效果
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"✨ 文件压缩完成！")
        print(f"   原始大小：{original_size:,} 字节")
        print(f"   压缩大小：{compressed_size:,} 字节")
        print(f"   压缩率：{compression_ratio:.1f}%")
    
    def decompress_file(self, input_file, output_file):
        """
        解压缩文件
        
        Args:
            input_file (str): 压缩文件路径
            output_file (str): 输出文件路径
        """
        print(f"📦 开始解压缩文件：{input_file}")
        
        # 读取压缩文件
        with open(input_file, 'rb') as f:
            compress_info = pickle.load(f)
        
        # 恢复哈夫曼编码器
        self.coder.root = compress_info['huffman_tree']
        self.coder._generate_codes(self.coder.root)
        
        # 解压缩数据
        decompressed_text = self.coder.decode(compress_info['compressed_data'])
        
        # 保存解压缩文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decompressed_text)
        
        print(f"✨ 文件解压缩完成！")
        print(f"   恢复长度：{len(decompressed_text)} 字符")


def demonstrate_huffman_coding():
    """
    演示哈夫曼编码的完整过程
    
    就像安妮兴奋地展示新学到的知识，
    让我们看看哈夫曼编码是如何工作的～
    """
    print("🎯 哈夫曼编码演示开始！")
    print("="*50)
    
    # 示例文本
    sample_texts = [
        "AAAAABBC",  # 简单示例
        "Hello, World! This is a test of Huffman coding.",  # 英文文本
        "这是一个中文测试文本，用来演示哈夫曼编码的效果。",  # 中文文本
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 示例 {i}：")
        print(f"原始文本：{text}")
        
        # 创建编码器
        coder = HuffmanCoder()
        
        # 训练并编码
        coder.fit(text)
        encoded = coder.encode(text)
        
        # 解码验证
        decoded = coder.decode(encoded)
        
        # 验证正确性
        is_correct = text == decoded
        print(f"✅ 解码验证：{'通过' if is_correct else '失败'}")
        
        if not is_correct:
            print(f"   原文：{text}")
            print(f"   解码：{decoded}")
        
        print("-" * 30)


def analyze_compression_efficiency():
    """
    分析不同类型文本的压缩效率
    
    就像黛芙深入分析算法性能，
    让我们看看哈夫曼编码在不同场景下的表现～
    """
    print("\n🔍 压缩效率分析")
    print("="*50)
    
    test_cases = [
        ("均匀分布", "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 10),
        ("高度重复", "AAAAAAAAAA" + "B" * 2 + "C"),
        ("自然语言", "The quick brown fox jumps over the lazy dog. " * 5),
        ("程序代码", "for i in range(10):\n    print(f'Hello {i}')\n" * 3),
    ]
    
    for name, text in test_cases:
        print(f"\n📊 测试案例：{name}")
        print(f"文本长度：{len(text)} 字符")
        
        coder = HuffmanCoder()
        coder.fit(text)
        encoded = coder.encode(text)
        
        # 计算统计信息
        original_bits = len(text) * 8
        compressed_bits = len(encoded)
        compression_ratio = (1 - compressed_bits / original_bits) * 100
        
        print(f"压缩前：{original_bits} 位")
        print(f"压缩后：{compressed_bits} 位")
        print(f"压缩率：{compression_ratio:.1f}%")
        
        # 分析编码长度分布
        code_lengths = [len(code) for code in coder.codes.values()]
        avg_length = sum(code_lengths) / len(code_lengths)
        print(f"平均编码长度：{avg_length:.2f} 位")
        print(f"编码长度范围：{min(code_lengths)} - {max(code_lengths)} 位")


if __name__ == "__main__":
    print("🌟 欢迎来到编码世界的温柔秘密！")
    print("让我们一起探索哈夫曼编码的神奇魅力～")
    print()
    
    # 运行演示
    demonstrate_huffman_coding()
    
    # 分析压缩效率
    analyze_compression_efficiency()
    
    print("\n🎉 演示完成！")
    print("感谢体验哈夫曼编码的优雅世界～")
    print("就像伊莎贝尔说的：最温柔的关怀，就是给最需要的人最多的爱 💕") 