from App import App, sys

if __name__ == '__main__':
    bd = App("data_base.db")
    connection = bd.connection
    cur = bd.cursor
    bd.commandHandler(int(sys.argv[1]))
