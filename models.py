from enum import Enum
from api_service import get_sellers_of_seller
import graphviz


class SellerTypes(Enum):
    PUBLISHER = 'PUBLISHER'
    INTERMEDIARY = 'INTERMEDIARY'
    BOTH = 'BOTH'
    ROOT = 'ROOT'


class Seller:
    def __init__(self, name, seller_type, parent, domain):
        self.name = name
        self.type = SellerTypes(seller_type)
        self.parent = parent
        self.domain = domain
        self.children = []


class SellersTree:
    def __init__(self, sellers):
        self.sellers_json = sellers
        self.depth = 0
        self.root_node = Seller('OpenX', "ROOT", None, 'https://openx.com')
        self.create_sellers_list()

    def create_sellers_list(self):
        for seller in self.sellers_json:
            seller = Seller(seller.get('name'), seller.get('seller_type'), self.root_node.name, seller.get('domain'))
            self.add_if_not_exist(self.root_node.children, seller)

        for sellers in self.root_node.children:
            self.create_child_sellers(sellers)

    def create_child_sellers(self, seller: Seller):
        if seller.type != SellerTypes.PUBLISHER:
            child_sellers = get_sellers_of_seller(seller.domain)
            if type(child_sellers) is not str:
                for child in child_sellers:
                    node = Seller(child.get('name'), child.get('seller_type'), seller, child.get('domain'))
                    self.add_if_not_exist(seller.children, node)
                    self.create_child_sellers(node)

    def add_if_not_exist(self, seller_children: list, new_child: Seller):
        if new_child.name not in seller_children:
            seller_children.append(new_child)


class Graph:
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Suppliers graph')

    def add_node(self, name, seller_type):
        self.dot.node(name=name, label=seller_type)

    def add_edge(self, from_node, to_node):
        self.dot.edge(from_node, to_node)

    def create_graph(self, root_seller: Seller):
        def fill_nodes(seller):
            self.add_node(seller.name, seller.type)
            for child in seller.children:
                fill_nodes(child)

        def fill_edges(seller):
            for child in seller.children:
                self.add_edge(seller.name, child.name)
                fill_edges(child)

        fill_nodes(root_seller)
        fill_edges(root_seller)

    def save_graph(self, path):
        self.dot.render(path)
