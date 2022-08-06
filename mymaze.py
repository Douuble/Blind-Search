import sys

class Node():                 #节点定义，包括状态、双亲节点和行为
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():        #frontier表存储未扩展的节点
    def __init__(self):       #初始化
        self.frontier = []

    def add(self, node):      #新增
        self.frontier.append(node)

    def contains_state(self, state):      #可执行状态筛选
        return any(node.state == state for node in self.frontier)

    def empty(self):           #判空
        return len(self.frontier) == 0

    def remove(self):          #移除
        if self.empty():
            raise Exception("empty frontier")
        else:
            #please add your code here to get a node from the frontier, according to FIBO
            #请在下面添加你的代码，从frontier表中按照后进先出的顺序移除一个结点，并将移除的结点给node
            node = self.frontier[-1]
            #after remove a node ,your frontier should adaptive accordingly
            #在移除了一个结点后，你的frontier表应该相应的更新
            self.frontier =self.frontier[:-1]            #返回[1,-1)的元素序列
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            #请添加你的代码，按照先进先出的顺序移除结点
            node = self.frontier[0]
            #请更新frontier表，使得frontier表为移除了一个结点剩下的结点组成
            self.frontier =self.frontier[1:]
            return node

class Maze():         #文件读取

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open('maze1.txt') as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines() #splitlines( )默认为将\r\n转化为， 如果（TRUE）则输出
        self.height = len(contents)
        self.width = max(len(line) for line in contents)   #len（）返回个数

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:                                     #异常处理程序 不报错而是打印输出错误，是异常类BaseException的衍生
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):            #enumerate( )列举索引和值的索引序列
            for j, col in enumerate(row):
                if col:
                    print("■", end="" )
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        
        #please add the frontier of stackfroniter or queuefrontier
        #请声明栈结构或者队列的frontier实例
        #frontier =StackFrontier()
        frontier =QueueFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier,please finish the sentence
            node =frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save("maze1 BFS.png")


#if len(sys.argv) != 2:
#    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[0])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
