def main():
    # While developing Put your test code here
    ############################################
    from .scraper import extract_all_imports
    print(list(extract_all_imports()))
    ############################################


if __name__ == '__main__':
    main()
