#Code for MCAS

import random

f_cost = 0
f_min = 100000000
flag = 0
final_config = 0

class f_cons(object):
    def __init__(self):
        self.table = {}
    def push(self, key, val):
        self.table[key] = val
        
class g_cons(object):
    def __init__(self):
        self.table = {}
    def push(self, key, val):
        self.table[key] = val
    
class link(object):
    def __init__(self, A1, A2, F, G):
        self.count = 0
        self.a1 = A1
        self.a2 = A2
        self.f = F
        self.g = G
        
class Agent(object):
    def __init__(self):
        self.number = -1
        self.g_thresh = 10000000000
        self.val = random.choice([0, 1])
        self.upper = []
        self.lower = []
        self.links = []
    def add_child(self, ag, f, g):
        self.lower.append(ag)
        ag.links.append(link(self, ag, f, g))
        ag.upper.append(self)
    def set_gthresh(self, val):
        self.g_thresh = val
    def set_num(self, val):
        self.number = val

def get_numbers(root):
    n = 0
    agents = []
    agents.append(root)
    while len(agents) != 0:
        if agents[0].number == -1:
            agents[0].set_num(n)
            n += 1
            for i in agents[0].lower:
                agents.append(i)
        del agents[0]

def find_fcost(cur_agent, bit_string, parent):
    global f_cost, f_min, flag
    my_val = get_val(bit_string, cur_agent.number)
    if f_cost > f_min:
        flag = 1
        return
    index = 0
    if len(cur_agent.upper) > 0:
        for i in xrange(len(cur_agent.links)):
            if cur_agent.links[i].a1.number == parent.number:
                index = i
                break

    if len(cur_agent.upper) > 0:
        f_cost += cur_agent.links[index].f.table[(get_val(bit_string, parent.number), my_val)]
    if f_cost > f_min:
        flag = 1
        return
    g_cost = 0
    for i in cur_agent.upper:
        for j in xrange(len(cur_agent.links)):
            if cur_agent.links[j].a1.number == i.number:
                g_cost += cur_agent.links[j].g.table[(get_val(bit_string, i.number), my_val)]
                break

    for i in cur_agent.lower:
        for j in xrange(len(i.links)):
            if i.links[j].a1.number == cur_agent.number:
                g_cost += i.links[j].g.table[(my_val, get_val(bit_string, i.number))]
                break

    if g_cost > cur_agent.g_thresh:
        flag = 1
        f_cost = 100000000
        return
    
    for i in cur_agent.lower:
        if len(cur_agent.upper) > 0:
            cur_agent.links[index].count += 1
        new_index = 0
        for j in xrange(len(i.links)):
            if i.links[j].a1.number == cur_agent.number:
                new_index = j
                break

        if len(cur_agent.upper) > 0 and i.links[new_index].count < cur_agent.links[index].count:
            find_fcost(i, bit_string, cur_agent)
            if f_cost > f_min:
                flag = 1
                return
        if len(cur_agent.upper) == 0:
            find_fcost(i, bit_string, cur_agent)
            if f_cost > f_min:
                flag = 1
                return
    
        
def get_final_f(agents):
    global f_cost, f_min, flag, final_config
    n = len(agents)
    for i in xrange((1 << n)):
        f_cost = 0
        flag = 0
        find_fcost(agents[0], i, -1)
        if f_min > f_cost:
            f_min = f_cost
            final_config = i
    print "Final Cost: " + str(f_min)
    print "Final Config: "
    for i in agents:
        print "Agent " + str(i.number) + ": " + str(get_val(final_config, i.number))
    
def get_val(bit_string, pos):
    if bit_string & (1 << pos):
        return 1
    return 0

def init():
    n = 4
    my_agents = []
    for i in xrange(n):
        my_agents.append(Agent())
    f = f_cons()
    f.push( (0, 0), 2 )
    f.push( (0, 1), 5 )
    f.push( (1, 0), 7 )
    f.push( (1, 1), 0 )

    g = g_cons()
    g.push( (0, 0), 6 )
    g.push( (0, 1), 4 )
    g.push( (1, 0), 1 )
    g.push( (1, 1), 7 )

    my_agents[0].add_child(my_agents[1], f, g)

    f = f_cons()
    f.push( (0, 0), 1 )
    f.push( (0, 1), 8 )
    f.push( (1, 0), 8 )
    f.push( (1, 1), 7 )

    g = g_cons()
    g.push( (0, 0), 9 )
    g.push( (0, 1), 1 )
    g.push( (1, 0), 7 )
    g.push( (1, 1), 4 )
    
    my_agents[0].add_child(my_agents[2], f, g)

    f = f_cons()
    f.push( (0, 0), 5 )
    f.push( (0, 1), 2 )
    f.push( (1, 0), 2 )
    f.push( (1, 1), 0 )

    g = g_cons()
    g.push( (0, 0), 1 )
    g.push( (0, 1), 2 )
    g.push( (1, 0), 5 )
    g.push( (1, 1), 7 )
    
    my_agents[2].add_child(my_agents[3], f, g)

    f = f_cons()
    f.push( (0, 0), 7 )
    f.push( (0, 1), 4 )
    f.push( (1, 0), 2 )
    f.push( (1, 1), 5 )

    g = g_cons()
    g.push( (0, 0), 9 )
    g.push( (0, 1), 9 )
    g.push( (1, 0), 3 )
    g.push( (1, 1), 3 )
    
    my_agents[0].add_child(my_agents[3], f, g)
    my_agents[2].set_gthresh(9)
    get_numbers(my_agents[0])
    
    test = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i in xrange(4):
        for j in my_agents[i].links:
            print "Link between " + str(j.a1.number) + " " + str(j.a2.number)
            for k in test:
                print str(k) + ": " + str(j.f.table[k]) + ": " + str(j.g.table[k])

    get_final_f(my_agents)
    
init()
