# -*- coding: utf-8 -*-
"""
静态KD树
@author:    Allen Oris
"""
import copy
import queue

vis = 0


def sqr(x):
    return x * x


class Node:
    def __init__(self, axes=None, num=0):
        self.x = copy.deepcopy(axes)
        self.num = num

    def axes_in(self, axes):
        if self.x:
            self.x.clear()
        self.x = copy.deepcopy(axes)


class DAN:
    def __init__(self, dis=0.0, num=0):
        """记录距离，与点下标"""
        self.dis = dis
        self.num = num

    def __cmp__(self, other):
        return -1 if self.dis > other.dis else 1 if self.dis < other.dis else 0

    def __lt__(self, other):
        return self.dis > other.dis


class KDTree:
    def __init__(self, nodes=None):
        """传入向量矩阵即可"""
        self.N = len(nodes)  # 静态点数
        self.node = [Node(nod, j) for j, nod in enumerate(nodes)]
        self.K = self.tree_dimension()
        self.sz = [0 for i in range(self.N << 2)]  # size数组
        self.p = self.open_array()
        self.idx = 0
        self.q_sz = 0
        self.que = queue.PriorityQueue()
        self.target = Node()
        self.build_kd(1, 0, self.N - 1, 0)
        #
        # for nod in self.node:
        #     print(nod.x,end='  ')

    def build_kd(self, i, l, r, dep):
        """构建kd树，传入树下标(初始为1)，左端点(0)，右端点(N-1)，深度(0)"""
        if l > r:
            return  # 树底结束
        mid = (l + r) >> 1
        # print("mid", l, r, mid) #
        lc = i << 1
        rc = i << 1 | 1
        idx = dep % self.K  # 该层维度
        self.sz[i] = r - l
        self.sz[lc] = self.sz[rc] = -1
        # nth_element(node + l, node + mid, node + r + 1) pyhton没有nth_element需要自己写，会比直接sort快，留坑
        self.sort_node(l, r + 1, idx)
        self.p[i] = self.node[mid]
        self.build_kd(lc, l, mid - 1, dep + 1)
        self.build_kd(rc, mid + 1, r, dep + 1)

    def query_kd(self, m, a):
        """查询最邻近的m个点",m:查询个数，a:查询向量，结果返回一个向量列表"""
        if len(a) != self.K:
            raise RuntimeError("相似度传入维数错误")
        self.que_clear()
        self.target.axes_in(a)
        self.query(1, m, 0)
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        ans = []
        for nod in reversed(res):
            ans.append(self.p[nod.num])
        return ans

    def query(self, i, m, dep):
        if self.sz[i] == -1:
            return
        global vis
        vis+=1
        tmp = DAN(0, i)
        lc, rc, idx, flag = i << 1, i << 1 | 1, dep % self.K, False
        for j, xj in enumerate(self.target.x):
            tmp.dis += sqr(xj - self.p[i].x[j])
        if self.target.x[idx] >= self.p[i].x[idx]:
            lc, rc = rc, lc
        self.query(lc, m, dep + 1)
        if self.q_sz < m:
            self.que.put(tmp)
            flag = True
            self.q_sz += 1
        else:
            backup = self.que.get()
            if tmp.dis < backup.dis:
                self.que.put(tmp)
                backup = self.que.get()
                self.que.put(backup)
            else:
                self.que.put(backup)
            if sqr(self.target.x[idx] - self.p[i].x[idx]) < backup.dis:
                flag = True
        if flag:
            self.query(rc, m, dep + 1)

    def tree_dimension(self):
        if len(self.node) == 0:
            return 0
        k = len(self.node[0].x)
        for nod in self.node:
            if len(nod.x) != k:
                raise RuntimeError("维度失衡!")
        return k

    def open_array(self):
        arr = []
        for i in range(self.N << 2):
            arr.append(Node())
            arr[i].x = [0 for i in range(self.K)]
        return arr

    def sort_node(self, l, r, idx):
        tmp = []
        for i in range(l, r):
            tmp.append(self.node[i])
        # print("sort")
        # for nod in tmp:
        #     print(nod.x,end=' ')
        # print()
        # print(idx)
        tmp.sort(key=lambda x: x.x[idx], reverse=False)
        # for nod in tmp:
        #     print(nod.x,end=' ')
        # print()
        j = 0
        for i in range(l, r):
            self.node[i] = tmp[j]
            j += 1

    def que_clear(self):
        while not self.que.empty():
            self.que.get()
        self.q_sz = 0


lines = []
line_pos = -1
test = open("test.ans", "r")
test = test.readlines()
test_pos = -1


def input():
    global line_pos
    line_pos += 1
    return lines[line_pos]


def solve(T):
    n = int(input())
    a = [[0, 0] for i in range(n)]
    for i in range(n):
        a[i] = list(map(int, input().strip().split()))
    print("n=", n)
    kdt = KDTree(a)
    # print("build success")
    mvis = 0
    for i, nod in enumerate(a):
        global vis
        vis = 0
        res = kdt.query_kd(2, nod)
        mvis = max(mvis, vis)
        ans = 0
        if n <= 1:
            print(0)
            continue
        for j in range(2):
            ans += sqr(nod[j] - res[1].x[j])
        global test_pos
        test_pos += 1
        if ans != int(test[test_pos]):
            print(i, ans, test[test_pos])
    print("vis", mvis)


if __name__ == '__main__':
    """测试HDU2966,静态KD树模板题"""
    with open("test.in", "r") as f:
        lines = f.readlines()
    T = int(input())
    for i in range(1, T + 1):
        # if (i > 4): continue
        print("case" + str(i))
        solve(i)
        print()
    print("pass")
