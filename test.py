attrs_acceptor = [['sponsored']]

for attr in attrs_acceptor:
    if attr in [['nofollow'], ['noindex'], ['sponsored']]:
        print(str(attr)[2:-2])
        break
