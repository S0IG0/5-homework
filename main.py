import os
from sys import argv
from GitClasses.Sha1Hash import Sha1Hash
from GitClasses.Commit import Commit
from zlib import decompress
from string import printable
import graphviz


def create_graph(data: dict[str, list[Commit]]) -> None:
    dot = graphviz.Graph(node_attr={'shape': 'box'}, graph_attr={'layout': 'dot'})
    for commit in data['commits']:
        node = str(commit.sha1_hash)
        dot.node(node, commit.commit)
        [dot.edge(node, str(item), node[:8]) for item in commit.parents]
    dot.render(r'graph\graph.gv', view=True)


def deserialization_commit(data: list[bytes], sha1_hash: Sha1Hash) -> Commit:
    data = list(map(lambda x: x.decode('UTF-8'), data))

    tree, = [' '.join(item.split(' ')[1:]) for item in data if 'tree' in item]
    author, = [' '.join(item.split(' ')[1:]) for item in data if 'author' in item]
    committer, = [' '.join(item.split(' ')[1:]) for item in data if 'committer' in item]
    commit = ' '.join(
        [item for item in data if item.split(' ')[0] not in ('author', 'committer', 'parent', 'commit', 'tree')]
    ).replace('\r', '')

    return Commit(
        parents=[Sha1Hash(item.split(' ')[-1]) for item in data if 'parent' in item],
        sha1_hash=sha1_hash,
        tree=Sha1Hash(tree),
        author=author,
        committer=committer,
        commit=''.join(
            filter(lambda x: str(x).lower() in printable[:-2] + ' абвгдеёжзийклмнопрстуфхцчшщъыьэюя', commit)
        ),
    )


def deserialization(path) -> dict[str, Commit]:
    item = dict()
    with open(path, 'rb') as file:
        data = decompress(file.read()).replace(b'\x00', b'\n').split(b"\n")
        while b'' in data:
            data.remove(b'')

    if b'commit' in data[0]:
        item['commit'] = deserialization_commit(data, Sha1Hash(''.join(path.split('\\')[-2:])))

    return item


def main(path) -> None:
    items = {
        'commits': [],
    }
    for item in os.listdir(path):
        absolute_path_dir = os.path.join(path, item)
        for file in os.listdir(absolute_path_dir):
            temp = deserialization(os.path.join(absolute_path_dir, file))
            if 'commit' in temp.keys():
                items['commits'].append(temp['commit'])

    create_graph(items)


if __name__ == '__main__':
    main(
        argv[1:] if len(argv[1:]) != 0 else 'D:\Project\С++\TestGit\.git\objects',
    )
