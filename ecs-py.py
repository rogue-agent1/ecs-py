#!/usr/bin/env python3
"""Entity Component System (ECS) architecture."""
import sys
from collections import defaultdict

class World:
    def __init__(self):self._next=0;self._components=defaultdict(dict);self._systems=[]
    def create_entity(self):self._next+=1;return self._next
    def add_component(self,entity,comp_type,data):self._components[comp_type][entity]=data
    def get_component(self,entity,comp_type):return self._components[comp_type].get(entity)
    def has_component(self,entity,comp_type):return entity in self._components[comp_type]
    def remove_component(self,entity,comp_type):self._components[comp_type].pop(entity,None)
    def remove_entity(self,entity):
        for comp in self._components.values():comp.pop(entity,None)
    def query(self,*comp_types):
        if not comp_types:return[]
        entities=set(self._components[comp_types[0]].keys())
        for ct in comp_types[1:]:entities&=set(self._components[ct].keys())
        return[(e,tuple(self._components[ct][e] for ct in comp_types)) for e in entities]
    def add_system(self,fn):self._systems.append(fn)
    def update(self):
        for sys_fn in self._systems:sys_fn(self)

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        w=World()
        e1=w.create_entity();e2=w.create_entity();e3=w.create_entity()
        w.add_component(e1,"pos",{"x":0,"y":0})
        w.add_component(e1,"vel",{"dx":1,"dy":2})
        w.add_component(e2,"pos",{"x":5,"y":5})
        w.add_component(e3,"pos",{"x":10,"y":10})
        w.add_component(e3,"vel",{"dx":-1,"dy":0})
        # Query entities with both pos and vel
        movers=w.query("pos","vel")
        assert len(movers)==2
        # Movement system
        def move_system(world):
            for e,(pos,vel) in world.query("pos","vel"):
                pos["x"]+=vel["dx"];pos["y"]+=vel["dy"]
        w.add_system(move_system);w.update()
        assert w.get_component(e1,"pos")=={"x":1,"y":2}
        assert w.get_component(e2,"pos")=={"x":5,"y":5}  # no vel, unchanged
        # Remove
        w.remove_entity(e3)
        assert len(w.query("pos","vel"))==1
        print("All tests passed!")
    else:
        w=World();e=w.create_entity()
        w.add_component(e,"pos",{"x":0,"y":0})
        w.add_component(e,"name","Player")
        print(f"Entity {e}: {w.get_component(e,'name')} at {w.get_component(e,'pos')}")
if __name__=="__main__":main()
