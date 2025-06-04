for path in data_paths:
    data = read(path)
    
    result = process(data)

    save(result)