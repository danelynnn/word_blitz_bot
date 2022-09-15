def order(c):
    return ord(c) - ord('a')

class TrieNode:
    def __init__(self, word):
        self.word = word
        self.children = [None]*26
        self.isWord = False
    
    def __repr__(self):
        return f'Trie node representing {self.word}'

class Trie:
    def __init__(self):
        self.root = TrieNode('')
    
    def insert(self, word):
        cursor = self.root

        for c in word:
            if not cursor.children[order(c)]:
                cursor.children[order(c)] = TrieNode(cursor.word + c)
            cursor = cursor.children[order(c)]
        
        cursor.isWord = True

def graph_traversal(grid, x, y, trie_node, current_path, words_list):
    c = grid[x][y]
    if not trie_node or (x, y) in current_path:
        return
    
    new_node = trie_node.children[order(c)]
    new_path = [*current_path, (x, y)]
    if new_node and new_node.isWord:
        words_list[new_node.word] = new_path

    if x > 0:
        if y > 0:
            graph_traversal(grid, x - 1, y - 1, new_node, new_path, words_list)
        graph_traversal(grid, x - 1, y, new_node, new_path, words_list)
        if y < len(grid)-1:
            graph_traversal(grid, x - 1, y + 1, new_node, new_path, words_list)
    if x < len(grid)-1:
        if y > 0:
            graph_traversal(grid, x + 1, y - 1, new_node, new_path, words_list)
        graph_traversal(grid, x + 1, y, new_node, new_path, words_list)
        if y < len(grid)-1:
            graph_traversal(grid, x + 1, y + 1, new_node, new_path, words_list)
    if y > 0:
        graph_traversal(grid, x, y - 1, new_node, new_path, words_list)
    if y < len(grid)-1:
        graph_traversal(grid, x, y + 1, new_node, new_path, words_list)
    
    return

def find_solutions(grid):
    root = trie.root
    current_path = []
    words_list = {}

    for i in range(len(grid)):
        for j in range(len(grid)):
            graph_traversal(grid, i, j, root, current_path, words_list)
    
    return words_list

trie = Trie()
f = open('words_alpha.txt', 'r')

while word := f.readline()[:-1]:
    if 2 <= len(word) <= 16:
        trie.insert(word)

if __name__ == '__main__':
    path = 'money'
    cursor = trie.root
    # for c in path:
    #     if cursor.children[order(c)]:
    #         cursor = cursor.children[order(c)]
    #         print(f'found {c}: {cursor.children}')
    #         if cursor.isWord:
    #             print(f'valid word: {cursor}')
    #     else:
    #         print('blocked')
    #         break

    words_list = []
    graph_traversal([['a', 'b'], ['c', 'd']], 1, 0, cursor, words_list, [])
    print(words_list)
