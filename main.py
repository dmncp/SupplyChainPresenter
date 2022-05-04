from api_service import get_sellers_list
from models import SellersTree, Graph


if __name__ == "__main__":
    seller_tree = SellersTree(get_sellers_list())
    print(seller_tree)
    graph = Graph()
    graph.create_graph(seller_tree.root_node)
    graph.save_graph('./graph_outputs/graph')
