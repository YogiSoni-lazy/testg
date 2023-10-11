from src.labs.common.playbooks import Runner


def main():
    path = ""
    first = True
    for rp in Runner("").discover_roles_path():
        if first:
            path = rp
            first = False
        else:
            path = path + ":" + rp
    print(path)


if __name__ == "__main__":
    main()
