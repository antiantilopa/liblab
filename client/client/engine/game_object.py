from typing import TypeVar

DEBUG = True

class Component:
    game_object: "GameObject"

    def set_game_object(self, game_object: "GameObject"):
        self.game_object = game_object

    def iteration(self):
        pass

    def draw(self):
        pass

    def __str__(self):
        return f""

T = TypeVar("T", bound=Component)

class GameObject:
    tags: list[str]
    components: list[Component]
    childs: list["GameObject"]
    parent: "GameObject"
    active: bool

    objs: list["GameObject"] = []
    root: "GameObject"
    group_tag_dict: dict[str, list["GameObject"]] = {}

    def __init__(self, tags: list[str] = []) -> None:
        self.tags = tags
        self.components = []
        self.childs = []
        self.parent = None
        self.active = True
        self.root = None
        GameObject.objs.append(self)
        if not tags in GameObject.group_tag_dict.keys():
            GameObject.group_tag_dict[tags] = []
        GameObject.group_tag_dict[tags].append(self)

    @staticmethod
    def get_group_by_tag(tag: str) -> list["GameObject"]:
        if not tag in GameObject.group_tag_dict.keys():
            raise KeyError(f"There is no GameObject with \"{tag}\" tag")
        return GameObject.group_tag_dict[tag]

    def add_component(self, component: Component):
        self.components.append(component)
        component.set_game_object(self)
        
    def add_child(self, child: "GameObject"):
        self.childs.append(child)
        child.parent = self

    def get_component(self, component_type: type[T]) -> T:
        for component in self.components:
            if isinstance(component, component_type):
                return component
        raise KeyError(f"{self} has no component \"{component_type}\"")

    def contains_component(self, component_type: type[T]) -> T:
        for component in self.components:
            if isinstance(component, component_type):
                return True
        return False

    def get_childs(self, tag: str) -> list["GameObject"]:
        result = []
        for child in self.childs:
            if child.tag == tag:
                result.append(child)
        return result

    def iteration(self):
        for component in self.components:
            component.iteration()

    def draw(self):
        for component in self.components:
            component.draw()

    def update(self):
        for component in self.components:
            component.iteration()
            component.draw()

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False

    def destroy(self):
        for child in self.childs:
            child.destroy()
        GameObject.objs.remove(self)
        GameObject.tag_dict[self.tag].remove(self)
        if self.parent is None:
            GameObject.roots.remove(self)
        else:
            self.parent.childs.remove(self)

    @staticmethod
    def show_geneology_tree(g_obj: "GameObject|None" = None, depth: int = 1):
        if g_obj is None:
            g_obj = GameObject.root
        print("| " * (depth - 1) + "|-", g_obj)
        for child in g_obj.childs:
            GameObject.show_geneology_tree(child, depth + 1)

    def __str__(self):
        return f"GameObject \"{self.tags}\""
