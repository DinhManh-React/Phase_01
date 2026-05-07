def chunking_with_overlap(token, chunk_size, overlap):
    words = token.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

token =input("token: ")
chunk_size = int(input("chunk_size: "))
overlap = int(input( "overlap: "))
chunks = chunking_with_overlap(token, chunk_size, overlap)
print(chunks)