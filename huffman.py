import collections
import random


class Node:
    def __init__(self, item, left=None, right=None):
        self.item = item
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.item}"


class Huffman(object):
    def __init__(self, li: list):
        self.__li = li
        self.root: Node | None = self.__createHuffman()
        self.__huffmanCode: dict[str:str] | None = None

    def __createHuffman(self) -> Node | None:
        nodelist = [Node(i) for i in self.__li]
        while len(nodelist) > 1:
            nodelist.sort(key=lambda x: (x.item[1], x.item[0]) if x.item[0] else (x.item[1], ))
            # print([n.item for n in nodelist])
            left, right = nodelist[0:2]
            parent = Node((None, left.item[1] + right.item[1]), left, right)
            del nodelist[0:2]
            nodelist.append(parent)
        return nodelist[0] if nodelist else None

    def preOrder(self, node):
        if not node:
            return
        print(node, end=", ")
        self.preOrder(node.left)
        self.preOrder(node.right)

    def inOrder(self, node):
        if not node:
            return
        self.inOrder(node.left)
        print(node, end=", ")
        self.inOrder(node.right)

    def postOrder(self, node):
        if not node:
            return
        self.postOrder(node.left)
        self.postOrder(node.right)
        print(node, end=", ")

    def getHuffmanCode(self):
        if not self.__huffmanCode:
            self.__huffmanCode = {}
            self.__getCode(self.root, "")
        return self.__huffmanCode

    def __getCode(self, node, code):
        if not node:
            return

        if not node.item[0]:
            self.__huffmanCode[node.item[0]] = code
        self.__getCode(node.left, code+"0")
        self.__getCode(node.right, code+"1")


def getCountMap(s: str) -> dict[str, int]:
    d = {}
    for c in s:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    return d


if __name__ == '__main__':
    sentence = "can you can a can as a canner can can a can."

    new_sentence = sentence
    for i in set(new_sentence):
        new_sentence = new_sentence.replace(i, f"{ord(i):08b}")
    print(new_sentence)

    print(len(new_sentence))

    # 统计每个字符的出现次数
    d: dict[str: int] = getCountMap(sentence)

    # 创建霍夫曼树
    # l = [random.randint(0, 100) for _ in range(10)]
    l = list(d.items())
    # print(sorted(l))
    h = Huffman(l)

    # 获取霍夫曼编码表
    huffmanCode = h.getHuffmanCode()

    print(huffmanCode)

    # 使用霍夫曼编码表进行编码
    new_sentence = sentence
    for ch, code in huffmanCode.items():
        new_sentence = new_sentence.replace(ch, code)

    print(new_sentence)
    print(len(new_sentence))

    # 解码
    huffman_discode = {v: k for k, v in huffmanCode.items()}
    min_code_len = min({len(i) for i in huffman_discode.keys()})
    max_code_len = max({len(i) for i in huffman_discode.keys()})

    print(max_code_len, min_code_len)

    renew_sentence = ""
    i = 0
    while i < len(new_sentence):
        for j in range(min_code_len, max_code_len + 1):
            code = "".join(new_sentence[i:i + j])
            if code in huffman_discode:
                renew_sentence += huffman_discode[code]
                i += j
                break

    print(renew_sentence)

    #
    # print("前序遍历")
    # h.preOrder(h.root)
    # print("\n中序遍历")
    # h.inOrder(h.root)
    # print("\n后序遍历")
    # h.postOrder(h.root)
